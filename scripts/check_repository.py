#!/usr/bin/env python3
"""Validate controlled documents, local references and literature metadata."""
import argparse
import csv
from datetime import date
import io
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET

STATUSES = {'draft', 'in-review', 'accepted', 'superseded', 'withdrawn'}
ID = re.compile(r'(std|dec|prd|pap|case|exp|doc)-\d{4}')
IGNORED = {'.git', '.venv', '__pycache__', '_scratch', '_local', 'runs', 'node_modules'}
FIELDS = ['id', 'title', 'status', 'revision', 'created', 'updated', 'path']


def source_files(root):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and not any(part in IGNORED for part in p.relative_to(root).parts))


def controlled_documents(root):
    rows, errors, seen = [], [], set()
    for path in source_files(root):
        if path.suffix != '.md':
            continue
        content = path.read_text(encoding='utf-8')
        if not content.startswith('---\n'):
            continue
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            errors.append(f'{path.relative_to(root)}: unterminated front matter')
            continue
        meta = {}
        for line in parts[1].splitlines():
            key, separator, value = line.partition(':')
            if separator:
                meta[key.strip()] = value.strip().strip('"')
        if 'id' not in meta:
            continue  # GitHub issue templates have unrelated front matter.
        relative = path.relative_to(root).as_posix()
        identifier = meta['id']
        if not ID.fullmatch(identifier):
            errors.append(f'{relative}: invalid document id')
        if identifier in seen:
            errors.append(f'{relative}: duplicate id {identifier}')
        seen.add(identifier)
        if not path.name.startswith(identifier + '-'):
            errors.append(f'{relative}: filename must start with its id')
        for field in FIELDS[:-1]:
            if not meta.get(field):
                errors.append(f'{relative}: missing {field}')
        if meta.get('status') not in STATUSES:
            errors.append(f'{relative}: invalid status')
        if not meta.get('revision', '').isdigit() or int(meta.get('revision', '0') or 0) < 1:
            errors.append(f'{relative}: revision must be a positive integer')
        dates = {}
        for key in ('created', 'updated'):
            try:
                dates[key] = date.fromisoformat(meta.get(key, ''))
            except ValueError:
                errors.append(f'{relative}: invalid {key} date')
        if len(dates) == 2 and dates['updated'] < dates['created']:
            errors.append(f'{relative}: updated date precedes creation')
        rows.append({**{field: meta.get(field, '') for field in FIELDS[:-1]}, 'path': relative})
    return sorted(rows, key=lambda row: row['id']), errors


def prose_only(content):
    lines, fence = [], None
    for line in content.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return re.sub(r'`+[^`]*`+', '', '\n'.join(lines))


def local_links(root):
    errors = []
    for path in source_files(root):
        if path.suffix != '.md':
            continue
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', prose_only(path.read_text(encoding='utf-8'))):
            target = target.strip().split(' "', 1)[0].strip('<>')
            parsed = urlparse(target)
            if parsed.scheme or target.startswith('#') or not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f'{path.relative_to(root)}: broken or external local link {target}')
    return errors


def literature_checks(root):
    path = root / 'research/literature/catalog.csv'
    if not path.exists():
        return ['Missing research/literature/catalog.csv']
    errors, seen = [], set()
    allowed = {
        'bibliography_status': {'pending', 'verified'},
        'reading_status': {'not-started', 'initial-review', 'partial', 'complete'},
        'code_status': {'not-inspected', 'partial-inspection', 'inspected', 'not-applicable'},
        'execution_status': {'not-run', 'smoke-tested', 'partial-reproduction', 'reproduced'},
        'discussion_status': {'pending', 'discussed'},
        'origin': {'seed', 'expansion'},
    }
    with path.open(newline='', encoding='utf-8') as handle:
        for row in csv.DictReader(handle):
            identifier = row.get('id', '')
            if not re.fullmatch(r'pap-\d{4}', identifier) or identifier in seen:
                errors.append(f'Literature: invalid or duplicate id {identifier}')
            seen.add(identifier)
            for key, values in allowed.items():
                if row.get(key) not in values:
                    errors.append(f'{identifier}: invalid {key}')
            for key in ('paper_url', 'code_url'):
                value = row.get(key, '')
                parsed = urlparse(value)
                if (key == 'paper_url' or value) and (parsed.scheme != 'https' or not parsed.netloc):
                    errors.append(f'{identifier}: invalid {key}')
    return errors


def diagram_checks(root):
    errors = []
    for path in source_files(root):
        if path.suffix != '.drawio':
            continue
        try:
            doc = ET.parse(path)
            if doc.getroot().tag != 'mxfile' or not doc.findall('.//mxGraphModel'):
                errors.append(f'{path.name}: expected editable, uncompressed Draw.io XML')
            for model in doc.findall('.//mxGraphModel'):
                cells = model.findall('.//mxCell')
                ids = [cell.get('id') for cell in cells]
                if None in ids or len(ids) != len(set(ids)):
                    errors.append(f'{path.name}: missing or duplicate cell id')
                for cell in cells:
                    for key in ('source', 'target', 'parent'):
                        if cell.get(key) and cell.get(key) not in ids:
                            errors.append(f'{path.name}: unresolved {key}')
        except ET.ParseError as exc:
            errors.append(f'{path.name}: invalid XML: {exc}')
    return errors


# Focused regression patterns, not a general authorship or language classifier.
EXTERNAL_NARRATION = re.compile(
    r"\b(?:the (?:researcher|user|project owner)(?:['’]s)?\s+"
    r"(?:prefers?|wants?|requests?|requested|asks?|asked|approved|agreed|provided|"
    r"can guide|will choose|states?|receives?|decides?|resolves?|pace|approval)\b"
    r"|provided by the (?:researcher|user|project owner)\b"
    r"|as (?:you|the researcher|the user) requested\b)",
    re.IGNORECASE,
)


def editorial_checks(root):
    errors = []
    for path in source_files(root):
        segments = []
        if path.suffix == '.md':
            prose = prose_only(path.read_text(encoding='utf-8'))
            # Attributed block quotations retain the source's wording.
            segments = ['\n'.join(line for line in prose.splitlines()
                                   if not line.lstrip().startswith('>'))]
        elif path.suffix == '.drawio':
            try:
                segments = [re.sub(r'<[^>]+>', ' ', cell.get('value', ''))
                            for cell in ET.parse(path).findall('.//mxCell')]
            except ET.ParseError:
                continue  # diagram_checks reports malformed XML.
        elif path.suffix == '.csv':
            with path.open(encoding='utf-8', newline='') as handle:
                for row in csv.DictReader(handle):
                    # Preserve exact bibliographic titles; documentation titles are checked in Markdown.
                    segments.extend(value for key, value in row.items()
                                    if isinstance(value, str) and key not in {'title', 'short_name', 'query'})
        for segment in segments:
            match = EXTERNAL_NARRATION.search(segment)
            if match:
                phrase = ' '.join(match.group(0).split())
                errors.append(f'{path.relative_to(root)}: external narration "{phrase}"; '
                              'state the project objective, decision, or rule directly')
    return errors


def render_catalog(rows):
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--write-catalog', action='store_true')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    rows, errors = controlled_documents(root)
    errors.extend(local_links(root))
    errors.extend(editorial_checks(root))
    errors.extend(literature_checks(root))
    errors.extend(diagram_checks(root))
    from check_diagrams import preview_checks
    errors.extend(preview_checks(root))
    catalog = root / 'docs/catalog.csv'
    expected = render_catalog(rows)
    if args.write_catalog and not errors:
        catalog.write_text(expected, encoding='utf-8')
    elif not catalog.exists() or catalog.read_text(encoding='utf-8') != expected:
        errors.append('docs/catalog.csv is stale; run with --write-catalog')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Repository checks passed: {len(rows)} controlled documents.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
