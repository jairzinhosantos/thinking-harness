---
id: dec-0007
title: "Utilidades Python dentro del caso"
status: in-review
revision: 4
created: 2026-10-16
updated: 2026-11-06
---

# Utilidades Python dentro del caso

Usar `utils/` dentro de cada caso implementado para módulos Python de apoyo. Mantener
README, entradas y configuración en la raíz. Los notebooks ejecutados se agrupan en
`notebooks/` cuando hay varias pruebas. No crear estructura vacía.

En case-0003 se trasladaron `prompt_search.py` y `notebook_view.py`: búsqueda acotada y
presentación de evidencia, respectivamente. No cambió el protocolo ni sus responsabilidades.
Es una carpeta local, no una biblioteca compartida.

Carga del notebook, pruebas y hashes futuros siguen las rutas nuevas; resultados históricos
conservan bytes, rutas y hashes originales. La copia PDF puede actualizar enlaces sin cambiar
la evidencia presentada.

Comprobaciones comunes en `scripts/`, pruebas en `tests/`. Los checkouts originales de papers
mantienen su estructura. Extraer código compartido cuando exista reutilización real según
[evolución del proyecto](../project-evolution.md).

En case-0003, los seis notebooks pasan de la raíz a `notebooks/`. Se actualizan navegación,
rutas de lectura y figuras; se conservan salidas y contadores de ejecución. Los registros de
`results/` no cambian. La entrega se abre desde `docs/README.md`, con enlace directo al notebook;
el README del caso conserva el índice completo. No se crea una copia de síntesis.

Los hashes históricos de notebooks del Test 5 corresponden al commit anterior a esta
reorganización. Cada notebook registra además el hash de sus salidas conservadas.

## Simplificación del caso

Se retiran los ejecutores `prompt_search.py`, `harness_smoke_test.py`, `local_model_test.py`
y `api_reference_test.py`. Sus versiones permanecen en Git y en las fuentes históricas de
`results/`; las ejecuciones guardadas no se modifican.

- `paired_search.py`: único bucle de propuestas, selección y adaptación B1/B2.
- `task.py`: contratos, evaluación y selección compartidos.
- `models.py`: transporte local o API; no decide qué política conservar.
- `inference_tuning.py`: control con política fija, sin bucle de automejora.
- `study_view.py`: lectura principal. `notebook_view.py`: presentación de pilotos anteriores.
- `structured_output.py`: extensión opcional del formato, usada solo cuando se solicita.

Las nuevas ejecuciones fijan fuentes en un commit y registran hashes, configuración y entorno.
Si las fuentes difieren del commit, la ejecución real se detiene antes de cargar el modelo.
No se copian scripts a cada resultado nuevo. Las notebooks históricas quedan en modo lectura;
las variaciones se presentan en `study-overview.ipynb`, sin crear una notebook por ajuste.
