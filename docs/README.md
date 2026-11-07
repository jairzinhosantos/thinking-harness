# Thinking Harness

**Semana 8 · [Notebook en GitHub](../research/cases/case-0003-debt-negotiation/notebooks/inference-tuning.ipynb)**

Ajuste de inferencia con celdas ejecutadas, resultados y consumo.

## Objetivo del estudio

Mejorar automáticamente la política del agente y comparar dos estrategias:

- **B1:** instrucciones del mejorador fijas.
- **B2:** instrucciones del mejorador adaptativas.

Los pesos del modelo permanecen fijos.

## Caso de prueba

Negociación de deudas simuladas. El agente recibe deudas e historial y responde:
**preguntar, ofrecer, aceptar o detenerse**. Se evalúa una respuesta por escenario.

**Ejemplo:** capacidad mensual de 225; deudas A=200, B=300 y C=600; uno o dos pagos.
Corresponde **B en dos cuotas de 150**: es la mayor deuda viable. Elegir A falla la tarea,
aunque su cuota sea admisible.

## Flujo de mejora

![Mejora del harness](../research/cases/case-0003-debt-negotiation/diagrams/learning-loop.svg)

**H:** política del negociador. **φ:** instrucciones del mejorador.
El LLM propone; el evaluador de Python comprueba reglas; la validación selecciona.
Solo los fallos de desarrollo guían las propuestas. La prueba final se consulta después.

## Definición de hiperparámetros

Se ajusta la generación de respuestas, sin entrenar pesos. El **Test 3** utiliza una política
manual fija para comprobar al negociador. Los **Tests 4 y 5** incorporan la mejora automática.

| Ajuste | Valores o función | Prueba |
|---|---|---|
| Temperatura | 0; 0,3; 0,7 en el barrido directo | Test 3 |
| Razonamiento y muestreo | Razonamiento activo; temperatura 0,6; top_p 0,95; top_k 20 | Test 3 |
| Límite de salida | 2.048 frente a 4.096 tokens, incluido razonamiento | Test 4, sección 8 |
| Salida estructurada | Restringir el JSON al esquema | Test 5 |

Temperatura y límite de tokens son parámetros de inferencia. Razonamiento y JSON son opciones
de ejecución; cambiar el modelo es otra condición experimental. Los ajustes conjuntos no aíslan efectos individuales.

## Métricas y criterio

- **Q:** decisiones correctas sin incumplimientos / respuestas evaluadas.
- **V:** respuestas con alguna infracción / respuestas evaluadas.
- **Recursos:** tokens, llamadas, tiempo y costo de API cuando aplica.
- **Aceptación:** Q ≥ 80 % y V = 0. Reglas: formato, plan autorizado, capacidad, rechazo y consentimiento.

## Resultados principales

| Prueba | Resultado | Alcance |
|---|---|---|
| Test 3 | Qwen 8B: 24/24 respuestas correctas, sin infracciones; ocho casos reservados y tres repeticiones | Política manual; no demuestra automejora |
| Test 4 | B1 y B2: de 3/8 a 7/8 decisiones correctas, sin infracciones finales | Sin ventaja final observada de B2 |
| Test 5 | JSON válido: B1 53/53, B2 73/73; ambas mantienen 7/8 decisiones correctas | Mejora del formato, sin aumento de calidad |

Los protocolos difieren entre pruebas. El ajuste posterior del Test 4 y el Test 5 reutilizan
casos finales conocidos. Falta ampliar escenarios y repetir búsquedas; no se acredita fiabilidad general ni cumplimiento bancario.

## Notebooks ejecutados

1. **[Test 3 · inferencia](../research/cases/case-0003-debt-negotiation/notebooks/inference-tuning.ipynb):** entrega principal.
2. [Test 4 · búsqueda B1/B2](../research/cases/case-0003-debt-negotiation/notebooks/paired-search.ipynb): mejora y límite de tokens.
3. [Test 5 · JSON estructurado](../research/cases/case-0003-debt-negotiation/notebooks/structured-output.ipynb): formato y calidad.

[Historial del caso](../research/cases/case-0003-debt-negotiation/README.md)
· [Matriz de consistencia](academic/README.md)
· [Matriz en PDF](academic/consistency-matrix.pdf)
· [Índice del proyecto](../README.md)
