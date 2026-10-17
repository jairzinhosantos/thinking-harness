---
id: doc-0004
title: "Progreso y revisión humana"
status: draft
revision: 2
created: 2026-09-29
updated: 2026-10-17
---

# Progreso y revisión humana

## Decisión pendiente

La disponibilidad horaria es referencial. Se propone medir avance observable, sin cuotas
ni compromisos automáticos de calendario.

| Opción | Unidad | Ventaja | Límite |
|---|---|---|---|
| A. Evidencia semanal | Pregunta resuelta y decisión registrada | Se adapta a incertidumbre | Requiere acordar evidencia suficiente |
| B. Hitos | Literatura, alcance, protocolo, piloto y plan de tesis | Muestra madurez general | Puede ocultar progreso parcial |
| C. Flujo aceptado | Entregas, tiempo de ciclo y correcciones | Útil al implementar | Las tareas no tienen igual dificultad |

Propuesta todavía no adoptada: A en la revisión semanal, B para el mapa general y C cuando
exista suficiente implementación. Un resultado negativo puede reducir incertidumbre;
commits, líneas de código y papers descargados no miden éxito científico.

## Revisión semanal propuesta

- Pregunta prioritaria y evidencia esperada.
- Evidencia obtenida, enlace y limitaciones.
- Decisión: continuar, ajustar, descartar o pedir revisión.
- Incertidumbre restante y siguiente tarea con criterio de cierre y presupuesto.

## Trabajo entre revisiones

Definir objetivo, entradas, alcance, archivos permitidos, presupuesto y parada antes de delegar.
Leer, probar localmente y preparar cambios dentro de lo autorizado no exige pedir aprobación
por cada paso. Cambios de alcance, costo, exposición o criterios científicos necesitan decisión.
No asumir que un agente continúa trabajando al terminar una sesión.

El agente prepara evidencia y llega a Review. Las dos aceptaciones humanas de integración
se rigen por [std-0003](../standards/std-0003-branching-and-releases.md); no seleccionan por sí
solas una métrica de progreso. Al alcanzar un límite, conservar evidencia y solicitar revisión.

El primer piloto de builder y QA se describe en la
[estrategia de desarrollo](doc-0003-agentic-development-strategy.md). No se ejecuta por documentarlo.
