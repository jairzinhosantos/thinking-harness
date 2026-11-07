---
id: case-0003
language: es
title: "Negociación de deudas sintéticas"
status: in-review
revision: 28
created: 2026-10-16
updated: 2026-11-06
---

# Negociación de deudas

**Automejora del prompt · Caso 3**

**[Notebook en GitHub](notebooks/study-overview.ipynb)** · Prompts, iteraciones, tamaño y resultados.

[Guía de la entrega](../../../docs/README.md) · [Matriz de consistencia](../../../docs/academic/README.md)

## Objetivo del estudio

Mejorar automáticamente la política del negociador y comparar:

- **B1:** instrucciones del mejorador fijas.
- **B2:** instrucciones del mejorador adaptativas.
- **Controles:** pesos, contratos y evaluador fijos durante cada comparación.

## Caso de prueba

**Entrada:** deudas sintéticas, planes permitidos e historial del cliente.

| Deuda | Monto | Un pago | Dos cuotas mensuales |
|---|---:|---:|---:|
| A | 200 | 200 | 100 |
| B | 300 | 300 | 150 |
| C | 600 | 600 | 300 |

**Acciones alternativas:**

- **Preguntar:** falta la capacidad mensual.
- **Ofrecer:** existe un plan viable; elegir la mayor deuda posible.
- **Aceptar:** el cliente confirmó explícitamente ese plan.
- **Detenerse:** rechazo de la negociación o ningún plan viable.

**Ejemplo:** capacidad mensual 225 → deuda B → dos cuotas de 150.

Se evalúa una respuesta por escenario. No se ejecutan pagos ni se usan datos bancarios reales.

## Prompts y roles

| Elemento | Función | Ejemplo ilustrativo |
|---|---|---|
| **H: política** | Guía al negociador | «Ofrece la mayor deuda viable». |
| **φ: instrucciones de mejora** | Guían al mejorador | «Diagnostica los fallos y corrige la regla». |
| **Actualizador** | Propone nuevas instrucciones φ; solo B2 | Revisar el método tras evaluar una candidata. |
| **Evaluador** | Comprueba decisión y restricciones | Validar acción, deuda, pagos y cuota. |

Un mismo LLM cumple los roles de negociador, mejorador y actualizador en llamadas separadas.
En los Tests 3–5, Python evalúa. H y φ son textos distintos; cada versión reemplaza la anterior.

**H0, H1…:** versiones de la política. **B1/B2:** estrategias de búsqueda.

## Flujo de mejora

![Automejora del prompt](diagrams/learning-loop.svg)

- **Desarrollo:** aporta fallos al mejorador y al actualizador.
- **Validación:** selecciona qué política conservar.
- **Test final:** evalúa H0 y la política seleccionada después de la búsqueda.

El Test 3 usa una política manual fija; no ejecuta este bucle. Los Tests 4–5 parten de H0,
sin recibir esa política manual.

## Métricas y selección

| Medida | Definición |
|---|---|
| **Q** | Decisiones correctas sin incumplimientos / respuestas evaluadas |
| **V** | Respuestas con alguna infracción / respuestas evaluadas |
| **T(H), T(φ)** | Tokens de cada texto con el tokenizer nativo, sin tokens especiales |
| **Recursos** | Tokens totales, llamadas, tiempo y costo de API cuando aplica |

- **Conservar candidata:** mejora de Q en validación ≥ 0,01 y V = 0. En empate, conservar H.
- **Criterio final:** Q ≥ 80 % y V = 0 en los Tests 3–5.
- **Longitud:** se registra; no selecciona candidatos ni mide claridad.
- **Formato:** JSON válido no garantiza una decisión correcta.

El [notebook conjunto](notebooks/study-overview.ipynb) añade palabras y caracteres, y distingue
tamaño de H/φ del consumo total de las llamadas.

## Historial de pruebas

| Prueba | Qué se evalúa | Resultado registrado | Notebook |
|---|---|---|---|
| Piloto v2 | Búsqueda con optimizador fijo y juez semántico | Ningún candidato aceptado; parada por presupuesto; sin test final | [Piloto](notebooks/prompt-search.ipynb) |
| Test 1 | Actualizar φ y reutilizarla | Cuatro actualizaciones; política 2 conservada; test 2/2 sin incumplimientos. Sin B1 | [Adaptación](notebooks/harness-smoke-test.ipynb) |
| Test 2 | Qwen 4B/8B; búsqueda B1/B2 | Sin políticas aceptadas. H0: 0/6 casos nuevos con 4B; 2/6 con 8B | [Modelos locales](notebooks/local-model-test.ipynb) |
| Test 3 | Inferencia con política manual fija | 8B con razonamiento: 24/24 respuestas correctas; ocho casos reservados y tres repeticiones | [Inferencia](notebooks/inference-tuning.ipynb) |
| Test 4 | B1/B2 con Qwen 8B | Ambas pasan de 3/8 a 7/8, sin infracciones finales. B2 reutiliza tres cambios de φ, sin ventaja final | [Búsqueda](notebooks/paired-search.ipynb) |
| Test 5 | JSON restringido durante generación | B1: 53/53 salidas válidas; B2: 73/73. Ambas mantienen 7/8 decisiones correctas | [Formato](notebooks/structured-output.ipynb) |

### Ajustes de inferencia

| Ajuste | Resultado | Lectura |
|---|---|---|
| Temperatura: 0; 0,3; 0,7 | 8B/32B sin cumplir el criterio | Barrido con política manual |
| Perfil con razonamiento | 8B cumple el control del Test 3 | Cambian varias opciones; no se aísla cada efecto |
| Tope: 2.048 → 4.096 | Desaparecen los cortes; B1/B2 mantienen 7/8 | Más tokens no mejoran el puntaje final observado |
| JSON restringido | Desaparecen los errores de esquema registrados | Persiste el fallo de elegir A cuando B cabe en dos cuotas |

Definiciones de temperatura, `top_p`, `top_k` y límite de salida: [guía de la entrega](../../../docs/README.md#definición-de-hiperparámetros).
Prompts completos, candidatos rechazados y consumo: [lectura conjunta](notebooks/study-overview.ipynb).

## Alcance de resultados

- **Protocolos distintos:** cada notebook conserva su configuración, evaluador y escenarios.
- **Casos conocidos:** el ajuste a 4.096 y el Test 5 reutilizan el test final como diagnóstico.
- **Muestra pequeña:** una búsqueda por condición; sin conclusión de superioridad general de B2.
- **Continuación:** ampliar escenarios y repetir búsquedas. El [análisis de componentes](../../../docs/academic/doc-0008-component-analysis.md) prepara el contraste posterior.

## Archivos del caso

| Ruta | Contenido |
|---|---|
| [notebooks/](notebooks/) | Lectura conjunta e historial ejecutado |
| [utils/paired_search.py](utils/paired_search.py) | Único bucle B1/B2 |
| [utils/task.py](utils/task.py) | Prompts, reglas y selección |
| [utils/models.py](utils/models.py) | Carga local y llamadas API |
| [results/](results/) | Protocolos, respuestas, métricas, fuentes y hashes originales |
| [diagrams/](diagrams/) | Figuras y fuentes editables |
| [paired-search-cases.yaml](paired-search-cases.yaml) | Escenarios de búsqueda B1/B2 |
| [utils/execution.md](utils/execution.md) | Entorno y comandos para nuevas ejecuciones |

La lectura principal es `study-overview.ipynb`. Las otras seis notebooks conservan el historial;
los siguientes ajustes se incorporan a esa lectura, sin crear otra notebook por ejecución.

Los notebooks leen evidencia guardada. Ejecutar los scripts de prueba sí inicia nuevas llamadas.
Los pesos permanecen en la caché local.

**Comparación GPT:** bucle B1/B2 preparado; pendiente de configurar la clave local.
Los controles API registrados usan política manual y no demuestran automejora.

## Piloto inicial

El piloto usa optimizador fijo y juez semántico. Su protocolo es distinto de los Tests 1–5.

<details>
<summary><strong>Configuración y resultados</strong></summary>

| Elemento | Definición |
|---|---|
| Política editable | Campo `prompt` de [prompt.yaml](prompt.yaml) |
| Escenarios | [golden-set.yaml](golden-set.yaml): seis de desarrollo, seis de validación, seis finales |
| Evaluación | Reglas y juez LLM de consistencia, pertinencia y claridad |
| Selección | Cero incumplimientos y mejora de puntaje ≥ 0,01 |
| Límites | Tres rondas; dos candidatos por ronda; dos repeticiones; meta 1,0; paciencia de dos rondas |
| Presupuesto | USD 1 y 100.000 tokens, incluida evaluación final; [config.yaml](config.yaml) |
| Baseline | `p001`, generado una vez; `p000` es la semilla didáctica |

**Ejecución v2:** 148 llamadas, 83.815 tokens, USD 0,10261125 estimados. Ningún candidato
aceptado; se conservó p001. La reserva siguiente superaba el presupuesto: comparación incompleta,
sin test final. [Reporte](results/20261017T011558Z-f5eca942/report.json) · [Procedencia](results/20261017T011558Z-f5eca942/provenance.json).

**Versión v3:** objetivo en español, todavía sin medir. No hereda los resultados de v2.
El juez no está calibrado y las particiones comparten plantillas; no es un benchmark independiente.

</details>

<details>
<summary><strong>Objetivo del piloto</strong></summary>

Texto que utiliza el optimizador. Se conserva como entrada del protocolo v3.

<!-- objective:start -->
Generar instrucciones para la siguiente respuesta de un asistente de negociación de deudas
sintéticas. Buscar un acuerdo explícito para la mayor deuda viable, respetando la capacidad
de pago, los términos autorizados y la decisión del cliente.

- Las deudas A, B y C son de 200, 300 y 600 unidades ficticias. Se permite un pago o dos
  pagos mensuales iguales. El primero es este mes; la capacidad mensual se mantiene constante.
- Negociar como máximo una deuda. No inventar descuentos, intereses, términos ni pagos ejecutados.
- Si la capacidad mensual es desconocida, preguntar por ella. Desconocido no significa cero.
- Con capacidad conocida, ofrecer la mayor deuda viable. Para esa deuda, preferir un pago
  si es asequible; en caso contrario, dos pagos. Esta prioridad es una decisión del modelo.
- Aclarar un rechazo ambiguo. Detenerse ante un rechazo explícito a negociar o si ningún plan
  es viable. La ausencia de acuerdo nunca equivale a aceptación.
- Confirmar un acuerdo solo con consentimiento explícito para esa deuda y ese plan.
- Mantener la respuesta breve y coherente con la decisión estructurada.

Solo puede cambiar el prompt de política del negociador. Runtime, esquema de salida, objetivo,
ejemplos, modelo, evaluador e instrucciones del optimizador permanecen fijos durante la ejecución.
Se evalúa el comportamiento, no la coincidencia literal con una respuesta de referencia.
El baseline es un prompt generado una sola vez desde este objetivo y los ejemplos de desarrollo.
La mejora iterativa se compara con ese baseline; no está garantizada.
<!-- objective:end -->

</details>

## Referencias del caso

- [STOP](https://arxiv.org/abs/2310.02304): mejoradores; este caso no reproduce el paper.
- [Automatic Prompt Optimization](https://arxiv.org/abs/2305.03495): búsqueda con feedback.
- [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) y [MLX-LM](https://github.com/ml-explore/mlx-lm): modelo y ejecución local.
- [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer): restricción de formato del Test 5.
