---
id: dec-0007
title: "Utilidades Python dentro del caso"
status: in-review
revision: 2
created: 2026-10-16
updated: 2026-10-17
---

# Utilidades Python dentro del caso

Usar `utils/` dentro de cada caso implementado para módulos Python de apoyo. Mantener
README, notebooks, entradas y configuración en la raíz del caso. No crear estructura vacía.

En case-0003 se trasladaron `prompt_search.py` y `notebook_view.py`: búsqueda acotada y
presentación de evidencia, respectivamente. No cambió el protocolo ni sus responsabilidades.
Es una carpeta local, no una biblioteca compartida.

Carga del notebook, pruebas y hashes futuros siguen las rutas nuevas; resultados históricos
conservan bytes, rutas y hashes originales. La copia PDF puede actualizar enlaces sin cambiar
la evidencia presentada.

Comprobaciones comunes en `scripts/`, pruebas en `tests/`. Los checkouts originales de papers
mantienen su estructura. Extraer código compartido cuando exista reutilización real según
[evolución del proyecto](../project-evolution.md).
