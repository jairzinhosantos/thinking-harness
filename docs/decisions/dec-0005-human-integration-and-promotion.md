---
id: dec-0005
title: "Integración y promoción con revisión humana"
status: accepted
revision: 2
created: 2026-10-02
updated: 2026-10-17
---

# Integración y promoción con revisión humana

Decisión del 2026-10-02. La aceptación de tareas y la promoción formal son puertas separadas:

1. PR de tarea, checks, revisión humana y squash merge a `develop` por el responsable humano.
2. Decisión de preparar baseline, PR de promoción, checks, aceptación explícita y merge commit a `main`.

La revisión de baseline cada una o dos semanas es referencial; no dispara promociones.
La sincronización posterior de `main` a `develop` también pasa por PR y revisión humana.
El agente prepara y llega a Review. Checks correctos no constituyen aceptación.

La corrección aclaró un diagrama que parecía unir checks directamente a `develop` y mostrar
revisión humana solo antes de `main`. El [estándar de ramas](../standards/std-0003-branching-and-releases.md)
concentra el flujo vigente. Atiende la parte de integración del
[issue 11](https://github.com/jairzinhosantos/thinking-harness/issues/11), sin elegir métrica de progreso,
caso, presupuesto ni programaciones.
