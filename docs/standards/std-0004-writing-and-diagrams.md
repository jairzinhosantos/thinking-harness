---
id: std-0004
title: "Escritura y diagramas"
status: in-review
revision: 5
created: 2026-09-30
updated: 2026-10-17
---

# Escritura y diagramas

## Idioma y tono

La documentación principal se escribe en **español**. Nombres de archivos y carpetas,
identificadores, claves y valores controlados, código, comentarios de código y docstrings
permanecen en **inglés**. Los decks se redactan en inglés. Commits usan descripciones breves
en inglés; issues y PRs pueden explicar el trabajo en español.

Conservar títulos bibliográficos, citas atribuidas y licencias originales. No traducir ni
reescribir prompts, configuraciones, trazas o resultados históricos como parte de una limpieza
editorial: modificar una entrada experimental requiere una revisión de protocolo independiente.

Usar frases concretas y voz del proyecto: «Se compararán dos mejoradores con el mismo
presupuesto». Evitar narrar preferencias personales, conversaciones o actividad del asistente.
Sin emojis, guiones largos, afirmaciones promocionales ni repeticiones. Atribuir resultados
externos y distinguir interpretación, inspección estática y reproducción.

## Una fuente por tema

- `README.md`: entrada principal en español; contexto, mecanismo y enlaces necesarios.
- Una review explica el paper. Priorizar ecuaciones originales, un flujo y fragmentos de código
  vinculados a la fuente. Ejercicios básicos y explicaciones extensas se trabajan por chat.
- La guía de cada caso conserva su interpretación; `results/` conserva la evidencia original.
  El plan y el README raíz enlazan el detalle sin repetir todas sus tablas.
- El [estándar de ramas](std-0003-branching-and-releases.md) define la integración;
  otros documentos lo enlazan. El Project conserva el estado de tareas.
- Eliminar duplicados y registrar reemplazos según [std-0001](std-0001-naming-and-lifecycle.md).
  No crear archivos para cada conversación ni archivar borradores obsoletos.

## Traducciones selectivas

Crear `README.en.md` o `<name>.en.md` únicamente para una audiencia que lo necesite.
La traducción comparte identidad y estados con el original: `translation_of`, `language: en`,
`source`, `source_revision`, `title`, `status`, `created` y `updated`. No lleva otro `id`.
Enlazar ambos idiomas y revisar la traducción cuando cambie la fuente. Si deja de ser útil,
eliminarla; no mantener versiones divergentes como equivalentes.

Un resumen en inglés debe identificarse como resumen, no como traducción completa.
Los decks en inglés son una presentación derivada, con referencias a sus fuentes y commit;
no requieren duplicar la documentación. Esta política sustituye el bilingüismo obligatorio
mediante [dec-0008](../decisions/dec-0008-spanish-primary-documentation.md).

## Diagramas

Preferir **Mermaid** para flujos, secuencias y dependencias legibles. Usar etiquetas breves
en el idioma del documento, una dirección clara y pocos nodos. Definir símbolos antes de
las ecuaciones. Evitar macros matemáticas que GitHub no renderice; usar `\mathrm{...}`
para nombres de operaciones cuando corresponda.

Usar **Draw.io** cuando importe la colocación manual. Guardar XML editable y SVG generado
junto al documento. No editar el SVG por separado; registrar hashes después de exportar y
revisar visualmente. No mantener dos representaciones independientes del mismo diagrama.
Los notebooks usan fuentes `.mmd` y adjuntos con hashes de fuente e imagen.

Archify se evalúa con una prueba local; todavía no sustituye Mermaid ni agrega una dependencia al CI.

## Validación

```sh
python3 scripts/check_repository.py
npm ci
npm run check:diagrams
```

El CI verifica estructura, enlaces, catálogo y sintaxis de diagramas. No garantiza precisión
científica, equivalencia de traducciones ni calidad visual; esas revisiones siguen siendo necesarias.
Los diagramas Draw.io se registran con `python3 scripts/check_diagrams.py --record-drawio`
solo después de exportar. La regeneración de adjuntos usa `python3 scripts/render_notebook_diagrams.py`.

Referencia: [diagramas en GitHub](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).
