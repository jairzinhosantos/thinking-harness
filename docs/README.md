# Thinking Harness · entrega semana 8

**[Notebook en GitHub: ajuste de hiperparámetros](../research/cases/case-0003-debt-negotiation/notebooks/inference-tuning.ipynb)**

Celdas ejecutadas, configuraciones probadas, resultados y consumo. Se puede leer directamente;
esta página explica el caso y cómo se conecta el ajuste de inferencia con la automejora.

## Qué buscamos

Se estudia si un sistema puede mejorar las instrucciones que utiliza para resolver una tarea,
y si también conviene que cambie sus instrucciones para proponer esas mejoras. El modelo
mantiene sus pesos: se ajusta su ejecución y se modifica una parte del harness, el andamiaje
que organiza su comportamiento.

**Caso actual:** negociación de deudas simuladas. El agente recibe deudas e historial y decide
si pregunta, ofrece un plan, acepta un acuerdo o se detiene. Se evalúa una respuesta por escenario.

Por ejemplo, con capacidad mensual de 225 y deudas A=200, B=300 y C=600, se permiten uno o dos
pagos. Corresponde ofrecer **B en dos cuotas de 150**: C no cabe y A es una deuda menor.
Ofrecer A sería un error de elección, aunque su cuota no supere la capacidad.

## Cómo funciona la mejora

![Flujo de propuesta, ejecución, evaluación y selección; actualización adicional de instrucciones en B2](../research/cases/case-0003-debt-negotiation/diagrams/learning-loop.svg)

- **Negociador:** usa la política H para responder al escenario.
- **Mejorador:** propone otra política H usando sus instrucciones φ y los fallos de desarrollo.
- **Evaluador:** código con reglas fijas; comprueba la decisión y los incumplimientos.
- **B1:** cambia H y conserva φ. **B2:** también puede actualizar φ para el siguiente intento.

La validación selecciona la política; sus respuestas no se entregan al mejorador. La prueba final
se consulta después de fijar la selección. La figura corresponde a los Tests 4 y 5.

## Qué significa ajustar hiperparámetros aquí

Primero comprobamos si el negociador puede resolver el caso con una política manual fija.
Así separamos la capacidad del modelo de la capacidad del mejorador. **Ese es el Test 3,
el notebook principal de esta entrega.** Después retomamos la búsqueda automática de políticas.

| Ajuste | Qué cambia | Dónde se registra |
|---|---|---|
| Temperatura | Variación del muestreo: 0; 0,3; 0,7 en el barrido directo | Test 3 |
| Modo de razonamiento y muestreo | Activación del razonamiento con temperatura 0,6, top_p 0,95 y top_k 20 | Test 3 |
| Máximo de tokens de salida | 2.048 frente a 4.096, incluyendo razonamiento y respuesta | Test 4, sección 8 |
| Generación estructurada | Restringir los tokens al esquema JSON después del razonamiento | Test 5 |

No se entrenan pesos. Temperatura y límite de tokens son parámetros de inferencia;
el modo de razonamiento y la salida estructurada son opciones de ejecución. Cambiar de modelo
es otra condición experimental. Cuando cambian varias opciones juntas, no atribuimos el resultado
a una sola.

## Qué medimos y qué obtuvimos

- **Q, calidad:** decisiones correctas y sin incumplimientos, divididas entre respuestas evaluadas.
- **V, incumplimientos:** respuestas que infringen alguna regla, divididas entre respuestas evaluadas.
- **Recursos:** tokens, llamadas y tiempo. En API también se registra el costo estimado.
- **Criterio del piloto:** Q ≥ 80 % y V = 0. Se comprueba formato, plan autorizado, capacidad,
  rechazo y consentimiento. No acredita cumplimiento bancario real.

| Prueba | Resultado observado | Qué permite concluir |
|---|---|---|
| **Test 3: inferencia** | Qwen 8B con razonamiento y política manual: 24/24 respuestas correctas en ocho casos reservados, tres repeticiones; sin incumplimientos | Esa configuración resolvió el control. No demuestra automejora |
| **Test 4: búsqueda B1/B2** | Ambas pasan de 3/8 con H0 a 7/8 con la política seleccionada; sin incumplimientos finales | Se obtuvo una política mejor en esta prueba, sin ventaja final de B2 |
| **Test 5: JSON restringido** | B1: 53/53 respuestas válidas; B2: 73/73. Ambas mantienen 7/8 decisiones finales correctas | El formato deja de fallar en estas ejecuciones; persiste un error de decisión |

Los protocolos y las particiones cambian entre pruebas: esta tabla resume el recorrido, no es
una clasificación comparable de modelos. Los ajustes posteriores del Test 4 y el Test 5 reutilizan
casos finales ya conocidos. Falta ampliar escenarios y repetir búsquedas para estudiar estabilidad.

## Abrir la evidencia

1. **[Notebook en GitHub · Test 3](../research/cases/case-0003-debt-negotiation/notebooks/inference-tuning.ipynb):** ajuste de inferencia, controles fallidos y confirmación.
2. [Test 4 · mejora fija y adaptativa](../research/cases/case-0003-debt-negotiation/notebooks/paired-search.ipynb): búsqueda de políticas y ajuste de tokens.
3. [Test 5 · salida estructurada](../research/cases/case-0003-debt-negotiation/notebooks/structured-output.ipynb): formato frente a calidad.

[Detalle del caso e historial completo](../research/cases/case-0003-debt-negotiation/README.md)
· [Matriz de consistencia](academic/README.md)
· [Matriz en PDF](academic/consistency-matrix.pdf)
· [Índice del proyecto](../README.md)

La entrega se mantiene en `develop`. Cada caso conserva sus pruebas y registros originales;
esta entrada presenta la entrega actual y puede apuntar a otros casos conforme avance el estudio.
