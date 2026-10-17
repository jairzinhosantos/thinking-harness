---
id: std-0001
title: "Nombres y ciclo de vida documental"
status: in-review
revision: 10
created: 2026-09-29
updated: 2026-10-17
---

# Nombres y ciclo de vida documental

## Identidad

Nombres en inglés, ASCII y `kebab-case`; Python usa `snake_case`. Conservar convenciones como
`README.md`, `AGENTS.md`, `LICENSE`, `CITATION.cff` y `Dockerfile`.
Los documentos controlados usan IDs estables: `std`, `dec`, `prd`, `pap`, `case`, `exp` y `doc`,
cada uno con secuencia propia. Consultar catálogos y decisiones de retiro antes de asignar un ID.
No reutilizar, renumerar ni completar huecos. Los documentos generales usan `<type>-NNNN-description.md`.

## Una carpeta por unidad de investigación

```text
research/cases/case-NNNN-description/
  README.md
  scenarios.md                 # Only when a separate study is needed
  prompt-search.ipynb          # Only when implemented
  utils/                      # Case-local Python support
  results/                    # Immutable recorded runs
research/literature/reviews/pap-NNNN-description/
  README.md
```

El README principal está en español y lleva el ID de la carpeta. Los estudios de apoyo
conservan su ID en metadatos aunque usen un nombre descriptivo. Compartir carpeta no convierte
una extensión en parte del caso aceptado. Entradas, configuración y diagramas permanecen
junto al caso; herramientas comunes en `scripts/`. No crear carpetas vacías por anticipación.

Una traducción selectiva usa `.en.md` sin ID propio. Sus metadatos y condiciones se definen
en [std-0004](std-0004-writing-and-diagrams.md#traducciones-selectivas).
Los notebooks principales no necesitan sufijo de idioma. Los PDFs derivados tampoco.

## Revisiones y conservación

Metadatos: `id`, `title`, `status`, `revision`, `created`, `updated`; `language: es` cuando
se declare idioma. Estados: `draft`, `in-review`, `accepted`, `superseded`, `withdrawn`.
Incrementar `revision` ante cambios sustanciales; Git conserva el detalle de cada edición.
Las entregas formales usan revisiones `r001`, `r002`, etc.

Eliminar duplicados y borradores sustituidos, sin `_archive`. Registrar reemplazo y retiro
de IDs en `docs/decisions/`. Conservar decisiones que explican restricciones actuales.
Evidencia histórica, incluso negativa, mantiene bytes, nombres, commits y hashes originales.
No renombrar ejecuciones o candidatos para adaptarlos a una nueva convención.

Originales de papers y anotaciones permanecen fuera de Git en la biblioteca local.
Entregas formales y manifiestos irán a `deliverables/` cuando existan. Material privado nunca
entra al repositorio público. Véase [evolución](../project-evolution.md).

## Catálogo

```sh
python3 scripts/check_repository.py --write-catalog
```

El catálogo lista documentos actuales. Las decisiones conservan los IDs retirados.
Las convenciones de protocolos y ejecuciones están en [std-0002](std-0002-experiment-versioning.md).
Esta revisión sustituye excepciones por caso e idioma según [dec-0008](../decisions/dec-0008-spanish-primary-documentation.md).
