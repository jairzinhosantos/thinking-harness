---
id: doc-0002
title: "Plan de investigación"
status: in-review
revision: 5
created: 2026-09-29
updated: 2026-10-30
---

# Plan de investigación

## Motivación y pregunta

Construir soluciones agénticas exige ajustar instrucciones, herramientas, flujos, memoria
y evaluación. Se estudia cómo automatizar parte de esa construcción y medir calidad,
costo e intervención humana.

**Pregunta provisional:** bajo un presupuesto acotado, ¿qué aporta mejorar al propio
mejorador frente a un procedimiento fijo, en una familia específica de tareas?

El caso, método y contribución final siguen abiertos. Se consideran búsqueda fija, mejora
recursiva, evolución, planificación y RL. El punto de partida utiliza modelos fijos;
entrenar un controlador o modelo requiere justificación y presupuesto. El feedback por sí solo no implica RL.

## Evidencia disponible

| Frente | Estado |
|---|---|
| Literatura | 35 papers catalogados; STOP y Self-Harness con lectura parcial y sin reproducción |
| Corrección de código | Caso y escenarios propuestos; participación del harness en su mejora como extensión separada, sin ejecutar |
| Negociación sintética | Piloto v2 con optimizador fijo, detenido por presupuesto, sin candidato aceptado ni comparación final; objetivo v3 sin medir |
| Tesis | Caso y comparación principal por seleccionar; colaboración institucional opcional |

Las fuentes detalladas están en el [mapa de literatura](../research/synthesis/research-options.md)
y el [índice de casos](../research/cases/README.md). No reinterpretar resultados v2 como evidencia v3.

## Próximo sprint académico

Se prepara el [análisis de variables y componentes](../research/cases/case-0003-debt-negotiation/component-analysis.md)
para negociación sintética: representación YAML, controles y ablaciones de prompts y organización.
La entrega define cómo medir; todavía no ejecuta búsquedas recursivas ni demuestra importancia.
No modifica los protocolos ni los resultados del piloto.

## Próximas decisiones

| Paso | Evidencia para revisar | Decisión |
|---|---|---|
| Leer STOP y Self-Harness | Mecanismo, ecuaciones y recorrido del código original | Qué cambia, qué queda fijo y qué constituye recursión |
| Diagnosticar el piloto | Cobertura, violaciones, consumo y condición de parada | Si negociación merece otra prueba |
| Acotar una comparación | Baseline, particiones, métricas, aceptación y presupuesto total, incluida evaluación final | Qué caso ejecutar |
| Ejecutar con autorización | Registro nuevo, resultados y limitaciones | Conservar, ajustar o descartar el método |
| Preparar el plan de tesis | Pregunta, variables, evaluación y alcance | Ajuste a [requisitos académicos](academic/requirements.csv) |

Son dependencias, no compromisos automáticos de ejecución. Medidas candidatas: calidad,
tiempo hasta aceptación, intervención humana, costo total, generalización y estabilidad.
Definirlas operacionalmente antes de una comparación confirmatoria.

## Método y gestión

Se propone adaptar [DSRM](https://doi.org/10.2753/MIS0742-1222240302) para construcción,
[FEDS](https://doi.org/10.1057/ejis.2014.36) para evaluación y prácticas de PRINCE2 y
[Kanban](https://kanbanguides.org/the-kanban-guide/) para gestión. Es una combinación del proyecto.

Mantener una lectura profunda y una tarea técnica en curso. El
[modelo operativo](operating-model.md) define el flujo; el [Project](project-links.md),
el estado de tareas. La [métrica de progreso](designs/doc-0004-progress-and-hitl.md)
sigue pendiente. El [piloto multiagente](designs/doc-0003-agentic-development-strategy.md)
requiere una decisión posterior.

Esta revisión integra la motivación de doc-0001, retirado sin reutilizar su ID.
