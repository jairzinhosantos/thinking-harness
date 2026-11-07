# Thinking Harness

**Automejora del prompt · Semana 8**

**[Notebook en GitHub](../research/cases/case-0003-debt-negotiation/notebooks/study-overview.ipynb)** · Caso, prompts, ajustes y resultados en una sola lectura.

## Objetivo del estudio

Mejorar automáticamente las instrucciones que usa un agente para negociar una deuda.
Ese texto se llama **política H**: por ejemplo, «ofrece la mayor deuda cuya cuota pueda pagar el cliente».

El sistema realiza tres llamadas distintas al mismo modelo:

| Rol | Trabajo |
|---|---|
| **Negociador** | Usa H para decidir qué responder al cliente. |
| **Mejorador** | Propone otra H a partir de los fallos observados. Sigue unas instrucciones llamadas **φ**. |
| **Actualizador** | Reescribe φ para cambiar cómo trabaja el mejorador en el siguiente intento. |

Se comparan dos estrategias de búsqueda:

| Estrategia | Política H | Instrucciones φ |
|---|---|---|
| **B1: mejora fija** | Puede cambiar entre intentos | Se mantienen iguales durante toda la búsqueda |
| **B2: mejora adaptativa** | Puede cambiar entre intentos | El actualizador puede reemplazarlas entre intentos |

**H0, H1… son versiones del texto; B1 y B2 son estrategias.** Cambiar un texto no garantiza mejor desempeño.

**Restricción experimental:** no se entrenan los pesos del modelo. Se editan textos;
el modelo, las reglas de evaluación y el presupuesto se mantienen iguales al comparar B1 con B2.

## Caso de prueba

**Entrada del negociador:**

- **Tabla de deudas:** montos ficticios y planes permitidos, indicados abajo.
- **Historial de conversación:** mensajes previos del cliente y del asistente. Puede incluir capacidad de pago, ofertas, rechazo o aceptación; no es un historial de pagos.

El agente elige una acción: **preguntar** por la capacidad (`ask`), **ofrecer** un plan (`offer`),
**confirmar** un plan aceptado (`accept`) o **detenerse** (`stop`).

| Dato del ejemplo | Valor |
|---|---|
| Mensaje ilustrativo del cliente | «Puedo destinar 225 al mes para pagar». |
| Capacidad de pago mensual | **225 unidades ficticias** disponibles para la deuda; no es el ingreso mensual |
| Planes permitidos | Un pago o dos cuotas mensuales iguales |

| Deuda | Monto total / un pago | Cuota con dos pagos | Evaluación |
|---|---:|---:|---|
| A | 200 | 100 | Viable, pero de menor monto |
| B | 300 | 150 | **Mayor deuda viable: ofrecer dos cuotas** |
| C | 600 | 300 | La cuota supera la capacidad de pago |

**JSON esperado del negociador** en los Tests 3–5:

```json
{
  "action": "offer",
  "debt": "B",
  "payments": 2,
  "installment": 150
}
```

| Campo | Significado |
|---|---|
| `action` | Acción; `offer` significa ofrecer, no confirmar un acuerdo |
| `debt` | Deuda elegida; `B` identifica el monto de 300 |
| `payments` | Número de pagos; aquí, dos |
| `installment` | Monto de cada cuota mensual; aquí, 150 |

Para `ask` y `stop`: `debt=null`, `payments=0`, `installment=0`.
Python redacta el mensaje a partir de esos campos, sin corregir la decisión.
La respuesta esperada pertenece al evaluador: **el negociador no la recibe**.

## Prompts y roles

- **System prompt:** instrucciones para una llamada. Combina un contrato fijo (límites y formato) con el texto editable H o φ, según el rol.
- **Entrada `user`:** datos para esa llamada. En el negociador son deudas y conversación; en el mejorador son objetivo, H y fallos de desarrollo.
- **Salida:** decisión JSON del negociador, nueva H del mejorador o nueva φ del actualizador.

**Ejemplos ilustrativos:** H: «Ofrece la mayor deuda viable». φ: «Revisa primero los fallos de capacidad y corrige esa regla».
φ guía al mejorador; **no se añade al prompt del negociador**. Una versión aceptada reemplaza a la anterior.

![Entradas y salidas del modelo](../research/cases/case-0003-debt-negotiation/diagrams/model-inputs.svg)

## Flujo de mejora

![Mejora del harness](../research/cases/case-0003-debt-negotiation/diagrams/learning-loop.svg)

Python evalúa y selecciona. Los fallos de desarrollo guían las propuestas;
la validación decide qué H conservar; el test final se consulta después.

## Pruebas ejecutadas

| Prueba | Qué se comprueba | Evidencia |
|---|---|---|
| Piloto | Búsqueda inicial con mejorador fijo | [Registro](../research/cases/case-0003-debt-negotiation/notebooks/prompt-search.ipynb) |
| Test 1 | Actualizar φ y reutilizarla | [Adaptación](../research/cases/case-0003-debt-negotiation/notebooks/harness-smoke-test.ipynb) |
| Test 2 | Capacidad de Qwen 4B y 8B | [Modelos locales](../research/cases/case-0003-debt-negotiation/notebooks/local-model-test.ipynb) |
| Test 3 | Ajustar inferencia con H manual fija | [Inferencia](../research/cases/case-0003-debt-negotiation/notebooks/inference-tuning.ipynb) |
| Test 4 | Buscar H con B1/B2; ampliar tokens | [Automejora](../research/cases/case-0003-debt-negotiation/notebooks/paired-search.ipynb) |
| Test 5 | Restringir la generación de JSON | [Formato](../research/cases/case-0003-debt-negotiation/notebooks/structured-output.ipynb) |

La lectura principal reúne los Tests 3–5. Las otras notebooks conservan cada prueba; no es necesario abrirlas para seguir el estudio.

El Test 3 separa capacidad del negociador y calidad del mejorador. Los Tests 4–5 utilizan
la inferencia elegida, pero parten de H0; no reciben la política manual.

## Definición de hiperparámetros

Se ajusta **cómo el modelo genera respuestas**, sin entrenarlo. Un token es una unidad de texto del modelo; no equivale siempre a una palabra.

| Parámetro | Significado | Valores y fundamento |
|---|---|---|
| Temperatura | Regula la diversidad al elegir el siguiente token | **0:** elegir siempre el más probable; **0,3:** explorar poca variación; **0,7:** referencia sin razonamiento; **0,6:** referencia con razonamiento |
| `top_k` | Limita la selección a los k tokens más probables | **20**, valor de referencia de Qwen; no se hizo un barrido de k |
| `top_p` | Filtra candidatos por probabilidad acumulada | **0,8** sin razonamiento; **0,95** con razonamiento, valores de referencia de Qwen |
| `max_tokens` | Tope de salida por llamada, incluido razonamiento | **512** en el barrido directo; **2.048** con razonamiento; **4.096** para comprobar si los cortes explicaban los fallos |

Los perfiles 0,7/0,8/20 y 0,6/0,95/20 coinciden con las [recomendaciones de Qwen3](https://huggingface.co/Qwen/Qwen3-8B#best-practices).
Los valores 0 y 0,3 amplían la exploración hacia menor variación; no son valores óptimos demostrados.
Los topes de salida son límites locales de estas pruebas, no la recomendación de longitud de Qwen.

**Aplicación real:** el código pasa temperatura, `top_p` y `top_k` al muestreador de MLX.
Con temperatura cero elige el máximo y omite los otros filtros. Con temperatura positiva,
aplica los filtros y muestrea con esa temperatura. `top_p=0,8` no significa 80 % de aciertos.

El perfil con razonamiento cambia varias opciones juntas. Permite comparar perfiles,
pero no atribuir el resultado únicamente a temperatura, `top_p` o razonamiento.

## Métricas y criterio

Sea **N** el número de respuestas evaluadas:

$$Q=\frac{\text{respuestas correctas sin infracciones}}{N},\qquad
V=\frac{\text{respuestas con al menos una infracción}}{N}.$$

- **Correcta:** acción, deuda, pagos y cuota coinciden con la respuesta esperada del escenario.
- **Infracción:** salida inválida, plan no permitido, cuota mal calculada o superior a la capacidad, oferta tras rechazo explícito, o aceptación sin consentimiento.
- **Q ≥ 80 %:** al menos 8 de cada 10 respuestas cumplen ambos requisitos. Con ocho respuestas se necesitan siete aciertos; con 24, al menos 20.
- **V = 0:** ninguna respuesta evaluada infringe las reglas. Se exige cero porque una cuota impagable o una aceptación inventada invalida la decisión.

**Ejemplo:** ofrecer A cuando B también cabe es una elección incorrecta, aunque no infrinja las restricciones. Reduce Q, pero puede mantener V en cero.
El 80 % es una meta provisional del piloto, no un umbral validado para producción. V = 0 describe la muestra observada.

- **T(H), T(φ):** tokens de cada texto con el tokenizer del modelo, sin tokens especiales.
- **Palabras y caracteres:** conteos complementarios.
- **Consumo:** tokens de todas las entradas y salidas, llamadas, tiempo y costo de API.

La longitud se registró, pero no selecciona políticas ni mide claridad. T(H) y T(φ) excluyen contrato, esquema e historial.

## Escenarios y repeticiones

Un **escenario** contiene una conversación simulada y su decisión esperada.

| Grupo del Test 3 | Uso |
|---|---|
| **12 conocidos** | Casos ya disponibles para diagnóstico: capacidad de pago, planes, rechazo y consentimiento. Se usan para comparar perfiles, no para entrenar pesos. |
| **8 reservados** | Conversaciones distintas, fijadas antes del barrido y excluidas de la selección del perfil. Sirven para comprobarlo después. |
| **3 repeticiones** | Se responde tres veces a cada conversación reservada con el mismo perfil y distintas semillas: **8 × 3 = 24 respuestas**, no 24 casos diferentes. |

La semilla inicializa el muestreo aleatorio; permite repetir la configuración.
Se usaron 11, 22 y 33 como identificadores de repetición, no como valores optimizados.
Estos ocho casos se reutilizaron después en diagnósticos: dejaron de ser una prueba nueva para los ajustes posteriores.

## Resultados principales

| Prueba | Resultado | Alcance |
|---|---|---|
| Test 3 | Qwen 8B: 24/24 respuestas correctas, sin infracciones | H manual; ocho casos reservados, tres repeticiones |
| Test 4 | B1 y B2: de 3/8 a 7/8 decisiones correctas | Sin ventaja final observada de B2 |
| Test 5 | JSON válido: B1 53/53 y B2 73/73; ambas mantienen 7/8 | Mejora del formato, no de las decisiones |

El ajuste posterior del Test 4 y el Test 5 reutilizan casos finales conocidos. Falta ampliar
escenarios y repetir búsquedas para estudiar generalización.

[Historial del caso](../research/cases/case-0003-debt-negotiation/README.md)
· [Matriz de consistencia](academic/README.md)
· [Matriz en PDF](academic/consistency-matrix.pdf)
· [Índice del proyecto](../README.md)
