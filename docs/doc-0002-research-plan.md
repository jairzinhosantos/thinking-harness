---
id: doc-0002
title: "Plan de investigación"
status: in-review
revision: 11
created: 2026-09-29
updated: 2026-10-31
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
| Adaptación mínima | [Test 1](../research/cases/case-0003-debt-negotiation/harness-smoke-test.ipynb): cinco propuestas en español y cuatro actualizaciones reutilizadas; propuesta 2 conservada, validación 2/2 y test 2/2 con reglas estructuradas; sin comparación B1/B2 |
| Modelos locales | [Test 2](../research/cases/case-0003-debt-negotiation/local-model-test.ipynb): Qwen3 4B completó tres propuestas sin mejora; Qwen2.5 1,5B y Gemma 2B se detuvieron por errores de salida. Longitud registrada con el tokenizer; sin llamadas a API |
| Contraste local mínimo | Qwen3 4B, protocolo v4 con contexto de desarrollo completo: tres propuestas fijas y tres adaptativas, ninguna aceptada. B2 consumió más tokens; B1 repitió propuestas. Escenarios reutilizados, sin conclusión de superioridad |
| Tesis | Plan centrado en configuración declarativa para cobranzas simuladas; contraste de mejora fija y adaptativa propuesto, todavía sin validar |

Las fuentes detalladas están en el [mapa de literatura](../research/synthesis/research-options.md)
y el [índice de casos](../research/cases/README.md). No reinterpretar resultados v2 como evidencia v3.

## Próximo sprint académico

Se prepara el [entrega académica: matriz y siguiente sprint](academic/README.md)
para negociación sintética: representación YAML, controles y ablaciones de prompts y organización.
La entrega define cómo medir. Las pruebas muestran el mecanismo y sus fallos, pero todavía
no demuestran importancia de componentes ni ventaja comparativa. Antes de ampliar el contraste,
se revisará la coherencia de las decisiones y la repetición de propuestas.
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
