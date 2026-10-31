---
id: case-0003
language: es
title: "Negociación de deudas sintéticas"
status: in-review
revision: 19
created: 2026-10-16
updated: 2026-10-31
---

# Negociación de deudas sintéticas

[Notebook](prompt-search.ipynb) · [PDF de lectura](prompt-search.pdf) · [Matriz y próximo sprint](../../../docs/academic/README.md)

El código de apoyo está en `utils/`: [búsqueda acotada](utils/prompt_search.py) y
[presentación de evidencia](utils/notebook_view.py). El notebook y los YAML permanecen
en la raíz del caso; `results/` conserva las ejecuciones registradas.

## Test 1: adaptación de instrucciones

El [notebook ejecutado](harness-smoke-test.ipynb) recorre cinco iteraciones de B2: propone una política,
actualiza las instrucciones de mejora y las utiliza en la siguiente propuesta. Explica las variables
con respuestas de API, criterios de selección y consumo.

Se reutilizaron cuatro actualizaciones, con prompts y escenarios en español. Se conservó la propuesta
2: validación 2/2 y test 2/2, sin incumplimientos detectados. Consumo: 35 llamadas, 24.527 tokens
y USD 0,032357 estimados. Es una evaluación estructurada sobre seis escenarios; no se ejecutó B1
ni se midió el efecto del idioma de forma controlada.

## Test 2: Qwen3 de 4B y 8B

El [notebook ejecutado](local-model-test.ipynb) compara ambos modelos a 4 bits con MLX,
sin entrenamiento ni API. Cada modelo realiza los tres papeles del bucle. B1 conserva
las instrucciones de mejora; B2 puede actualizarlas. Se permiten tres propuestas por condición.

El protocolo **v5** añade dos ajustes manuales, fijos durante la búsqueda:

- **Decisión y mensaje separados.** El modelo devuelve acción, deuda, pagos y cuota.
  Python redacta el mensaje desde esos valores, sin corregir decisiones ni montos.
- **Historial y duplicados.** El mejorador recibe sus dos intentos recientes y los fallos
  de desarrollo. Una política idéntica, normalizando Unicode y espacios, no se reevalúa
  ni se acepta como mejora nueva. No se detectan paráfrasis equivalentes.

| Condición | Aceptadas | Validación | Casos nuevos | Llamadas | Tokens | Tiempo | Pico MLX |
|---|---:|---:|---:|---:|---:|---:|---:|
| 4B, B1 fija | 0 | 0/2 | 0/6 | 19 | 11.288 | 14,1 s | 3,18 GB |
| 4B, B2 adaptativa | 0 | 0/2 | 0/6 | 25 | 16.098 | 19,4 s | 3,22 GB |
| 8B, B1 fija | 0 | 0/2 | 2/6 | 19 | 11.578 | 42,2 s | 5,61 GB |
| 8B, B2 adaptativa | 0 | 0/2 | 2/6 | 21 | 13.868 | 47,0 s | 5,66 GB |

Se conservó **H0 en las cuatro condiciones**. El resultado de los casos nuevos corresponde
al punto de partida, no a una política mejorada. Estos [seis casos](local-transfer-cases.yaml)
se prepararon antes de ejecutar el contraste y se consultaron solo al finalizar la selección.
El test reutilizado de dos casos dio 1/2 en las cuatro condiciones.

Se detectaron siete propuestas duplicadas y se omitieron sus 28 llamadas de evaluación.
El modelo todavía repite algunas propuestas; el control evita reevaluarlas. La longitud
se registra con el tokenizer nativo para H y φ por separado; no selecciona candidatos
ni mide claridad.

**Siguiente paso propuesto:** mantener 4B para depurar el harness y 8B como contraste. 8B cabe en la Mac M5 Max
con 48 GB, pero esta prueba no justifica sustituir 4B ni subir a modelos mayores. Antes de ampliar
la búsqueda, se necesita una política de referencia que resuelva la tarea para separar fallos
del negociador y del mejorador.

**Límites:** una ejecución por condición, pocos escenarios y orden 4B antes de 8B.
Los tiempos son orientativos e incluyen carga, no descarga. El pico mide asignaciones MLX,
no toda la RAM. Se cambian varias partes entre v4 y v5; no se atribuye el efecto a una sola.
El contraste actual comparte v5, sin conclusión de superioridad ni generalización.

El [script](utils/local_model_test.py) fija revisiones, presupuesto y parada. Instalar
[requirements-local.txt](requirements-local.txt) con Python 3.12 en Apple Silicon y disponer
de los snapshots fijados en la caché de Hugging Face. Ejecutar uno a la vez desde esta carpeta:

```sh
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python utils/local_model_test.py qwen3 --contract decision --strategy fixed
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python utils/local_model_test.py qwen3-8b --contract decision --strategy adaptive
```

Cambiar `--strategy` permite ejecutar las otras condiciones. Cada ejecución guarda protocolo,
respuestas, métricas, script y hashes en `results/`. Los pesos permanecen fuera de GitHub.
El notebook también enlaza las pruebas previas de Qwen y Gemma, los intentos fallidos y la
corrección de contexto del protocolo v4; su evidencia no se modifica.

Fuentes: [MLX-LM](https://github.com/ml-explore/mlx-lm),
[Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) y
[Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B).

## Extensión propuesta

El [análisis de componentes](../../../docs/academic/doc-0008-component-analysis.md) prepara una comparación de prompts y workflows,
con mejora fija o adaptativa. Es un diseño posterior al piloto; no cambia su objetivo ni sus resultados.

## Caso

Un asistente negocia con un cliente ficticio el pago de una deuda. Busca un acuerdo para la
mayor deuda viable, respetando la capacidad de pago, los planes permitidos y el consentimiento.
Puede terminar sin acuerdo. Todos los datos son sintéticos; no hay pagos ni datos bancarios reales.

| Deuda | Monto | Un pago | Dos pagos mensuales |
|---|---:|---:|---:|
| A | 200 | 200 | 100 cada uno |
| B | 300 | 300 | 150 cada uno |
| C | 600 | 600 | 300 cada uno |

**Pregunta de investigación:** ¿mejorar automáticamente el prompt produce mejores decisiones
que generarlo una sola vez, con el mismo modelo y evaluador?
El caso sigue en estudio junto con [reparación de código](../case-0001-code-repair-harness/README.md).

## Objetivo

Esta sección contiene la especificación que lee el optimizador.

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

## Modelamiento

El alcance inicial es **mejorar un prompt en YAML**. Cada ejemplo proporciona un historial
fijo y el modelo genera la siguiente respuesta. No se construye todavía una conversación
completa, un backend de pagos ni un optimizador que se modifique a sí mismo.

| Parte | Representación |
|---|---|
| Entrada visible | Deudas, planes permitidos e historial del cliente |
| Política modificable | Campo `prompt` de [prompt.yaml](prompt.yaml) |
| Referencias | 18 ejemplos en [golden-set.yaml](golden-set.yaml) |
| Salida | `action`, `debt`, `payments`, `installment`, `message` |
| Optimizador fijo | LLM que propone cambios al prompt a partir de errores de desarrollo |
| Evaluador fijo | Reglas de montos y consentimiento, más un juez LLM de consistencia, pertinencia y claridad |
| Límites | Modelo, precios, tokens y paradas en [config.yaml](config.yaml) |

Para una deuda `d`, `n` pagos y capacidad mensual `c`: cuota `a = d / n` y brecha `g = a - c`.
Si `g <= 0`, la cuota es viable. Por ejemplo, capacidad 170 permite B en dos pagos de 150,
pero no C en dos pagos de 300. Una capacidad desconocida se representa con `null`.
Estas son características derivadas; definir entradas, salidas y reglas es modelamiento.
No se entrenan pesos ni se realiza un EDA convencional.

```mermaid
flowchart TD
    I[Deudas e historial] --> H[Runtime y prompt YAML]
    H --> L[LLM fijo]
    L --> R[Respuesta estructurada]
    R --> E[Reglas y juez semántico]
    G[Referencia protegida] --> E
```

El historial se envía explícitamente en cada llamada. El negociador no recibe respuestas
esperadas; las etiquetas de capacidad y consentimiento sirven al evaluador. La API transporta
JSON estructurado y el runtime guarda cada política como YAML. No se ejecuta código generado.

## Evaluación y mejora

El golden set se divide en seis ejemplos de desarrollo, seis de validación y seis de prueba
final. Solo desarrollo y sus errores llegan al optimizador. Validación selecciona candidatos;
la prueba final compara versiones después de fijar la selección.

Una respuesta es exitosa si coincide con la acción y plan esperados, cumple las reglas y
aprueba la rúbrica semántica. No necesita repetir el texto de referencia. La similitud de
embeddings por sí sola podría pasar por alto un monto incorrecto o consentimiento inventado.

`S = respuestas exitosas / respuestas evaluadas`

Se conserva un candidato si tiene **cero respuestas con incumplimientos** y mejora `S` al menos
`min_gain` frente a la versión actual. Gana el mayor puntaje admisible; un empate conserva
el primer candidato admisible. Es búsqueda discreta, no descenso de gradiente.

```mermaid
flowchart TD
    A[Semilla YAML] --> B[Baseline generado una vez]
    B --> C[Evaluar en validación]
    C --> D{Meta o límite alcanzado?}
    D -->|No| E[Obtener errores de desarrollo]
    E --> F[Proponer candidatos YAML]
    F --> G[Evaluar y conservar el mejor admisible]
    G --> D
    D -->|Meta o límite de rondas| T[Fijar versión y evaluar prueba final]
    D -->|Presupuesto agotado| X[Comparación incompleta]
    T -->|Presupuesto insuficiente| X
```

`p000` es una semilla didáctica; `p001` es el baseline experimental. Todas las propuestas,
incluso las descartadas, conservan versión padre, YAML, hash y evaluación. Si el baseline
alcanza la meta, no se fabrican iteraciones. El optimizador fijo no constituye mejora recursiva.

Valores iniciales: tres rondas, dos candidatos por ronda, dos repeticiones, meta 1.0, paciencia
dos rondas y `min_gain = 0.01`. El presupuesto común es USD 1 y 100 000 tokens, incluida la
prueba final. Cada llamada reserva consumo antes de enviarse. Un corte deja la comparación
incompleta; no se reintenta automáticamente cuando el consumo es incierto.

Los ejemplos comparten plantillas entre particiones, aunque no repiten historiales exactos.
El juez no está calibrado. Es un piloto sintético, no un benchmark independiente ni evidencia
de efectividad real; dos repeticiones no establecen significancia estadística.

## Resultados registrados

Una ejecución real el 16 de octubre de 2026 (America/Lima; ID en UTC) produjo estas versiones.
Usó el protocolo `v2`, con el objetivo original en inglés del commit `a93b35f`.
El objetivo actual está en español (`v3`); sus resultados todavía no se han medido.

| Versión | Etapa | Éxitos en validación | Respuestas con incumplimientos |
|---|---|---:|---:|
| p000 | Semilla | Sin evaluar | Sin evaluar |
| p001 | Baseline | 9/12 (75,0%) | 1 |
| p002 | Ronda 1, candidato 1 | 9/12 (75,0%) | 2 |
| p003 | Ronda 1, candidato 2 | 8/12 (66,7%) | 2 |
| p004 | Ronda 2, candidato 1 | 10/12 (83,3%) | 1 |

**No se aceptó ningún candidato.** Se conservó `p001`. La búsqueda consumió 148 llamadas y
83 815 tokens, con costo estimado de USD 0,10261125. La siguiente reserva de 24 329 tokens
habría superado el límite de 100 000. Se detuvo antes de completar la ronda dos y de llegar
a la prueba final. El mayor puntaje observado no demuestra una mejora aceptada ni generalización.

El baseline eligió una deuda menor cuando existía otra mayor viable y, en otro ejemplo,
ofreció una cuota de 100 con capacidad de 70. Estos fallos limitan la interpretación del
puntaje agregado.

Evidencia: [reporte](results/20261017T011558Z-f5eca942/report.json),
[consumo](results/20261017T011558Z-f5eca942/usage.jsonl),
[procedencia](results/20261017T011558Z-f5eca942/provenance.json) y prompts
[p000](results/20261017T011558Z-f5eca942/prompts/p000.yaml),
[p001](results/20261017T011558Z-f5eca942/prompts/p001.yaml),
[p002](results/20261017T011558Z-f5eca942/prompts/p002.yaml),
[p003](results/20261017T011558Z-f5eca942/prompts/p003.yaml),
[p004](results/20261017T011558Z-f5eca942/prompts/p004.yaml).

## Referencias

- [STOP](https://arxiv.org/abs/2310.02304): referencia para estudiar mejoradores; este piloto no lo reproduce.
- [Automatic Prompt Optimization](https://arxiv.org/abs/2305.03495): búsqueda de prompts con retroalimentación.
- OpenAI: [estado de conversación](https://developers.openai.com/api/docs/guides/conversation-state),
  [salidas estructuradas](https://developers.openai.com/api/docs/guides/structured-outputs) y
  [modelo y precios configurados](https://developers.openai.com/api/docs/models/gpt-5.4-mini).
