---
translation_of: case-0003
language: es
source: README.md
source_revision: 5
title: "Synthetic debt negotiation harness"
status: in-review
created: 2026-10-16
updated: 2026-10-16
---

# Harness de negociación de deudas sintéticas

[English](README.md) | Español

## Caso

Un prestamista ficticio ofrece planes para tres deudas del año anterior. El asistente busca
un acuerdo explícito para la mayor deuda viable, respetando la capacidad de pago y la decisión
del cliente. Un rechazo o un plan inviable pueden terminar correctamente sin acuerdo.

| Deuda | Monto | Un pago | Dos pagos mensuales |
|---|---:|---:|---:|
| A | 200 | 200 | 100 cada uno |
| B | 300 | 300 | 150 cada uno |
| C | 600 | 600 | 300 cada uno |

Los montos y conversaciones son sintéticos. Se negocia como máximo una deuda, la capacidad
mensual es constante y no hay descuentos, intereses ni pagos reales. Un acuerdo representa
un compromiso, no una cobranza efectiva. No se usan datos ni implementaciones institucionales.

## Alcance inicial

El prototipo mejora **un prompt de política en YAML**, con LLM, optimizador y evaluador fijos.
Genera la siguiente respuesta a partir de un historial proporcionado. Todavía no ejecuta una
conversación completa, implementa herramientas de pago, reescribe código ni cambia su optimizador.

**Pregunta:** ¿la búsqueda iterativa de prompts mejora las decisiones del siguiente turno frente
a un prompt generado una sola vez, con el mismo objetivo, modelo y protocolo de evaluación?
Es un candidato activo junto con [reparación de código](../case-0001-code-repair-harness.es.md).
El [caso de servicios](../case-0002-service-workflow-harness.es.md) permanece sustituido.
El método final de tesis sigue abierto.

```mermaid
flowchart LR
    A[Caso: negociación permitida] --> B[Definiciones y modelo de evaluación]
    B --> C[Entradas y política en YAML]
    C --> D[Notebook: búsqueda acotada de candidatos]
    D --> E[Prompts versionados y decisiones medidas]
    E --> F[Revisión humana]
```

## Lectura y ejecución

1. Revisar las [definiciones y el modelamiento](modeling.es.md): entradas, características
   derivadas, evaluador, regla de selección y límites.
2. Abrir la [notebook en español](prompt-search.es.ipynb) o la [notebook en inglés](prompt-search.ipynb).
   Ambas usan los mismos YAML, implementación y evidencia de ejecución.
3. Seguir la [preparación local](modeling.es.md#preparación-local). Por defecto se muestra la [primera ejecución real](results/20261017T011558Z-f5eca942/README.es.md)
   sin llamadas a la API. Una nueva ejecución con costo requiere activación explícita.

El [objetivo](objective.md), [golden set](golden-set.yaml), [prompt inicial](prompt.yaml) y
la [configuración](config.yaml) están en esta carpeta. El [runtime](prompt_search.py) conserva
cada política propuesta en YAML, incluidas las descartadas. La notebook muestra cada versión,
sus cambios, evaluación, selección, motivo de parada y comparación final cuando estén disponibles.

Una extensión con herramientas podría extraer motivos de rechazo, seleccionar planes autorizados
y registrar aceptación. Requeriría un protocolo propio. La mejora automática del prompt con
un optimizador fijo no constituye auto-mejora recursiva.

La revisión 5 incorpora la primera ejecución medida: ningún candidato aceptado, parada por tokens y prueba final no alcanzada. Ambas notebooks muestran la misma evidencia.
