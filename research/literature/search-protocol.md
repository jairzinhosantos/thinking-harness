# Protocolo de búsqueda

Mapear métodos de construcción y mejora de harnesses para seleccionar comparadores.
Corte inicial: 2026-09-29. La ampliación de 2026-10-11 verificó diez candidatos aprobados;
no fue una búsqueda exhaustiva ni recuperó resultados de la tarea programada inaccesible.
Actualizar la búsqueda al revisar alcance y antes de la evaluación final.

## Fuentes y consultas

Priorizar papers y proceedings oficiales, arXiv, OpenReview, ACL Anthology, PMLR y repositorios
vinculados por autores. Los buscadores sirven para descubrir fuentes. Distinguir publicación
revisada, preprint y proyecto técnico.

- `"recursive self-improvement" AND (agent OR harness OR scaffolding)`
- `"agentic workflow" AND (optimization OR search OR planning)`
- `"harness" AND ("self-improving" OR adaptive OR evolution)`
- `"reinforcement learning" AND (agent OR workflow OR tool-use)`
- Referencias y trabajos que citan los estudios centrales.

Incluir mecanismos explícitos, cercanos a la pregunta y evaluables. Registrar versión,
código, objeto modificable, controles, método, evaluación, presupuesto, límites y decisión
de inclusión. Deduplicar versiones. No inferir publicación o código disponible de una conversación.

## Estados independientes

| Campo | Valores |
|---|---|
| Bibliografía | `pending`, `verified` |
| Lectura | `not-started`, `initial-review`, `partial`, `complete` |
| Código | `not-inspected`, `partial-inspection`, `inspected`, `not-applicable` |
| Ejecución | `not-run`, `smoke-tested`, `partial-reproduction`, `reproduced` |
| Discusión | `pending`, `discussed` |

Una inspección inicial no acredita lectura completa ni reproducción.

## Clasificación y originales locales

| Campo del catálogo | Significado |
|---|---|
| `theme` | Tema principal: evolución, metaoptimización, generalización, coevolución o síntesis de datos |
| `proximity` | `direct`, `complementary` o `contextual`, según relación con diseño y evaluación del harness |
| `reference_role` | Uso previsto como baseline, candidato o referencia de evaluación |
| `priority` | P0: siguiente comparación; P1: apoyo; P2: extensiones. No mide calidad |
| `classification_basis` | `preliminary-source-screening`: resumen, pasajes seleccionados y repositorios enlazados |
| `classification_notes` | Motivo y principal incertidumbre |
| `pdf_filename` | Nombre del PDF original local, no adjunto de GitHub |

Los campos de clasificación se incorporaron en pap-0014 a pap-0023. Vacíos anteriores
indican clasificación pendiente, no menor relevancia. Prioridades y estados no cambian al
traducir. Véase [mapa de literatura](../synthesis/research-options.md#mapa-de-literatura).

Originales fuera de Git en `paper-library/originals/`, con nombre
`<pap-id>-<short-slug>-v<arxiv-version>.pdf`. Anotaciones en `paper-library/annotated/`.
No sobrescribir originales ni reemplazar versiones silenciosamente. Una copia importada
en Goodnotes no se considera sincronizada con el archivo local.

Antes de registrar una descarga, verificar título, versión arXiv, apertura y portada.
Un `code_url` vacío significa no verificado aquí; un repositorio disponible no demuestra reproducción.

## Registro

Conservar consulta, fuente, fecha, candidatos retenidos y alcance en `search-log.csv`.
Los registros históricos mantienen su idioma original. Los conteos no cubren todos los
resultados del buscador. El screening sistemático sigue pendiente.
[PRISMA-ScR](https://www.prisma-statement.org/scoping) y
[PRISMA-S](https://www.prisma-statement.org/prisma-search) son guías de reporte, no certificaciones.
