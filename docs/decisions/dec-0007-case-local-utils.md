---
id: dec-0007
title: "Utilidades Python dentro del caso"
status: in-review
revision: 3
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
