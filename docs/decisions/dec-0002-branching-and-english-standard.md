---
id: dec-0002
title: "Ramas e idioma: decisión inicial"
status: accepted
revision: 2
created: 2026-09-30
updated: 2026-10-17
---

# Ramas e idioma: decisión inicial

Decisión adoptada el 2026-09-30, [issue 12](https://github.com/jairzinhosantos/thinking-harness/issues/12).

**Ramas, vigente:** `develop` integra iteraciones mediante PRs; `main` conserva baselines
formales y sigue como entrada pública predeterminada. La promoción requiere aceptación humana.
La implementación inicial partió de `main`, conservó bootstrap y usó `docs/12-english-documentation`.

**Idioma, sustituido:** inicialmente se eligió inglés para todo el contenido del proyecto.
[dec-0004](dec-0004-bilingual-paper-reviews.md) añadió traducciones de reviews en 2026-10-01.
[dec-0008](dec-0008-spanish-primary-documentation.md) sustituye ambas políticas de idioma:
español principal y traducciones selectivas; código y nombres en inglés.

Se mantiene prosa concreta, Mermaid por defecto y Draw.io para colocación precisa.
El [estándar de ramas](../standards/std-0003-branching-and-releases.md) y el
[estándar editorial](../standards/std-0004-writing-and-diagrams.md) contienen las reglas actuales.
Esta decisión no selecciona método, caso, métrica de progreso ni runtime agéntico.
