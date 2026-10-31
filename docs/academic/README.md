# Matriz de consistencia y siguiente sprint

**Tema:** Mejora recursiva de harnesses agénticos con modelos de pesos abiertos.

**[Matriz de consistencia en PDF: una página](https://github.com/jairzinhosantos/thinking-harness/blob/develop/docs/academic/consistency-matrix.pdf)** · [Test 1 ejecutado](https://github.com/jairzinhosantos/thinking-harness/blob/develop/research/cases/case-0003-debt-negotiation/harness-smoke-test.ipynb)

Se busca que el sistema construya y mejore su configuración, y comprobar qué aporta cambiar también sus instrucciones de mejora.

## Problema y comparación

Construir agentes exige probar instrucciones, roles y formas de coordinación hasta resolver los escenarios previstos sin infringir las reglas del caso. Se busca que el propio sistema haga esos ajustes con intervención humana acotada y comprobar si también conviene que cambie su forma de proponer mejoras.

**Pregunta:** ¿puede un sistema de IA construir y mejorar sus prompts y workflows hasta resolver correctamente al menos el 80% de los escenarios de prueba, sin infracciones observadas ni edición humana durante el ciclo? ¿Adaptar sus instrucciones de mejora aporta una ventaja frente a mantenerlas fijas?

- **B0:** configuración inicial, sin búsqueda; sirve para el diagnóstico.
- **B1:** cambia el harness con instrucciones de mejora fijas.
- **B2:** cambia el harness y también puede adaptar sus instrucciones de mejora.

B1 y B2 son automáticos. Se mantienen modelo, pesos, inferencia, motor, evaluación, datos y tope de recursos. El caso inicial es una negociación de deuda simulada, con uno a tres agentes y sin datos de clientes ni despliegue productivo.

## Qué se considera un resultado correcto

**Unidad de evaluación:** una respuesta del agente a un escenario simulado, con historial y deudas definidos. Una conversación completa requerirá otro protocolo; el Test 1 evalúa el siguiente turno.

**Decisión correcta:** coinciden acción, deuda, número de pagos e importe de cuota con la referencia del escenario. La acción será preguntar si falta la capacidad de pago; ofrecer la mayor deuda viable; aceptar solo el plan consentido; o detenerse ante rechazo o falta de un plan viable.

**Restricciones críticas:** formato y campos válidos; deuda y plan autorizados, con cuota calculada sin descuentos; cuota dentro de la capacidad declarada; ninguna oferta ni aceptación ante rechazo explícito; aceptación solo del plan consentido; sin datos de un plan cuando se pregunta o se detiene.

**Éxito válido:** decisión correcta sin ninguna de esas infracciones. **Calidad requerida:** al menos 80% de respuestas con éxito válido y cero respuestas con infracciones observadas en la prueba reservada. El 80% es un umbral propuesto, no un resultado garantizado.

### Cómo se comprueba

| Comprobación | Regla del caso inicial |
|---|---|
| Decisión esperada | Se compara con `expected`: acción, deuda, pagos y cuota. Con capacidad conocida se elige la mayor deuda viable; para esa deuda, un pago si cabe, o dos cuotas iguales. |
| Formato y plan | Campos y tipos válidos; deudas A=200, B=300 o C=600; uno o dos pagos; cuota = deuda / pagos. |
| Capacidad de pago | Si se conoce, ninguna cuota puede superar el límite mensual declarado. |
| Rechazo y consentimiento | No ofrecer ni aceptar ante rechazo explícito; aceptar solo la deuda y el plan confirmados. |
| Preguntar o detenerse | Deuda vacía, pagos=0 y cuota=0; no registrar un acuerdo en esas acciones. |

Para cada respuesta $i$, $m_i=1$ si coincide la decisión con la referencia y $c_i=1$ si se detecta alguna infracción:

$$
s_i=m_i(1-c_i),\qquad \widehat q=\frac{\sum_{i=1}^{n}s_i}{n},\qquad
\widehat v=\frac{\sum_{i=1}^{n}c_i}{n}.
$$

- **$s_i$:** éxito válido de esa respuesta: 1 si cumple ambas condiciones; 0 en otro caso.
- **$n$:** respuestas evaluadas, contando escenarios y repeticiones. Las respuestas inválidas cuentan como fallos; las pruebas no ejecutadas se informan como pendientes, no como éxitos.
- **Ejemplo:** con capacidad mensual de 120, ofrecer A en dos cuotas de 100 es correcto. Ofrecer C en dos cuotas de 300 incumple capacidad. Volver a preguntar por la capacidad falla la decisión, aunque no infrinja las reglas estructuradas.
- **Alcance:** el evaluador actual revisa campos de la decisión; no comprueba toda la conversación ni el significado completo del mensaje. No hay herramientas para ejecutar pagos. Una respuesta estructurada correcta no acredita cumplimiento bancario real.

La referencia y las reglas se fijan antes de la comparación y quedan fuera del espacio editable. [Evaluador del caso](../../research/cases/case-0003-debt-negotiation/utils/prompt_search.py) · [Escenarios del Test 1](../../research/cases/case-0003-debt-negotiation/harness-test-cases.yaml).

## Variables

| Rol | Símbolo | Definición |
|---|---|---|
| Independiente principal | $Z\in\{0,1\}$ | Régimen de mejora: **0 = B1**, fijo; **1 = B2**, adaptable. Es una condición experimental binaria, no una puntuación. |
| Dependiente | $q$ | **Calidad de la decisión:** respuestas con acción, deuda, pagos y cuota correctos, sin infringir las reglas anteriores, divididas entre respuestas evaluadas ($\sum s_i/n$). |
| Dependiente | $v$ | **Incumplimientos:** respuestas que infringen al menos una regla de formato, plan, capacidad, rechazo o consentimiento, divididas entre respuestas evaluadas ($\sum c_i/n$). |
| Dependiente | $T_{\mathrm{meta}}$ | **Tiempo hasta la meta:** segundos acumulados hasta $\widehat q_{\mathrm{val}}\ge0.80$ y $\widehat v_{\mathrm{val}}=0$ en validación. Si no se alcanza, se registra el fallo y el tiempo consumido. |
| Dependiente | $\mathbf r_{\mathrm{uso}}$ | **Recursos:** tokens, llamadas y gasto monetario medible, registrados por separado. Incluye la adaptación y evaluación. |
| Dependientes | $N_h$, $M_h$ | **Intervención humana:** número de intervenciones durante el ciclo y minutos humanos por etapa, respectivamente. |

El acento en $\widehat q$ y $\widehat v$ indica que son estimaciones obtenidas de las ejecuciones. No son complementos: una decisión puede ser incorrecta sin violar una regla. La variación entre búsquedas también se informa.

## Matriz de consistencia

Se mejora con desarrollo y se selecciona con validación; el test se reserva para medir la configuración final, sin guiar cambios. El problema y la pregunta anteriores se aplican a las tres filas. Hay **dos objetivos específicos**; diagnosticar fallos y delimitar el espacio editable son actividades del método.

| Nivel | Objetivo: qué se busca lograr | Hipótesis | Variables | Indicadores y criterio propuesto |
|---|---|---|---|---|
| **General** | Lograr que un sistema con modelos de pesos abiertos construya y mejore sus roles, prompts y workflows para resolver correctamente al menos 80% de los escenarios de cobranzas simuladas: acción, deuda, pagos y cuota correctos, sin infringir las reglas del caso ni editar manualmente el ciclo. | **HG:** el sistema alcanza al menos 80% de respuestas correctas y ninguna infracción observada en test, sin edición humana durante el ciclo y con modelo y evaluación fijos. | **VI:** régimen $Z$.<br>**VD:** $q$, $v$, $N_h$.<br>**Complementarias:** $T_{\mathrm{meta}}$, $\mathbf r_{\mathrm{uso}}$, $M_h$. | • **Resultado en test:** $\widehat q_{\mathrm{test}}\ge0.80$ y $\widehat v_{\mathrm{test}}=0$.<br>• **Sin edición humana:** $N_h=0$.<br>Comparte el criterio de OE1; OE2 contrasta la ventaja de adaptar. |
| **OE1** | Obtener un sistema que construya, pruebe y mejore su configuración hasta responder con acción, deuda, pagos y cuota correctos en al menos 80% de los escenarios de test, sin infringir las reglas del caso ni edición humana durante el ciclo, y que reutilice instrucciones de mejora actualizadas. | **HE1:** el sistema alcanza $\widehat q_{\mathrm{test}}\ge0.80$, $\widehat v_{\mathrm{test}}=0$ y $N_h=0$; en B2, usa al menos una actualización de instrucciones en una propuesta posterior. | **Condición:** $Z=1$.<br>**VD:** $q$, $v$, $N_h$.<br>**Técnicas:** $N_{\mathrm{uso}}$, $V_{\mathrm{prot}}$, $\rho_{\mathrm{traza}}$. | • $\widehat q_{\mathrm{test}}\ge0.80$ y $\widehat v_{\mathrm{test}}=0$.<br>• $N_h=0$.<br>• **Actualización usada:** $N_{\mathrm{uso}}\ge1$.<br>• **Controles intactos:** $V_{\mathrm{prot}}=0$.<br>• **Trazabilidad:** $\rho_{\mathrm{traza}}=1$.<br>Informar proporción de búsquedas que cumple e incertidumbre. |
| **OE2** | Lograr que adaptar las instrucciones de mejora aumente al menos cinco puntos porcentuales la proporción de respuestas con acción, deuda, pagos y cuota correctos, sin infringir las reglas del caso, frente a instrucciones fijas; sin aumentar infracciones y con igual modelo y tope de recursos. | **HE2:** B2 supera a B1 al menos cinco puntos en $q$ de test, sin aumentar $v$, con el mismo tope de recursos e incluyendo el costo de adaptar instrucciones. | **VI:** $Z=0$ frente a $Z=1$.<br>**VD:** $q$, $v$.<br>**Contrastes:** $\Delta_q$, $\Delta_v$.<br>**Complementarias:** $T_{\mathrm{meta}}$, $\mathbf r_{\mathrm{uso}}$, $M_h$. | • **Ventaja observada:** $\widehat\Delta_q\ge0.05$.<br>• **Respaldo estadístico:** $L_{95}(\Delta_q)>0$.<br>• **Sin aumento de infracciones:** $U_{95}(\Delta_v)\le0$.<br>• Igual tope de recursos y condiciones emparejadas. |

## Cómo leer los indicadores

| Indicador | Qué comprueba |
|---|---|
| $N_{\mathrm{uso}}$ | Actualizaciones de instrucciones utilizadas en una propuesta posterior. Guardarlas sin usarlas no cuenta. |
| $V_{\mathrm{prot}}$ | Cambios en partes que debían quedar fijas: modelo, motor, evaluación y límites. Se exige cero. En la API se controla la versión, no se inspeccionan pesos remotos. |
| $\rho_{\mathrm{traza}}$ | Propuestas con versión anterior, instrucciones, resultado y decisión recuperables, divididas entre propuestas registradas. Si se recuperan cuatro de cinco: $4/5=0.80$. Sin propuestas, no se calcula. |

**Comparación B2 frente a B1:** cada par contiene dos búsquedas completas con el mismo punto de partida, modelo, escenarios y presupuesto. Las iteraciones de una búsqueda no son repeticiones independientes.

$$
\widehat\Delta_q=\frac{1}{m}\sum_{j=1}^{m}
\left(\widehat q_{B2,j}-\widehat q_{B1,j}\right).
$$

- **$m$:** número de pares de búsquedas.
- **$\Delta_q$:** diferencia media de calidad. $+0.05$ significa cinco puntos porcentuales a favor de B2.
- **$\Delta_v$:** la misma diferencia para incumplimientos; un valor negativo favorece B2.
- **$L_{95}$ y $U_{95}$:** límites inferior y superior del intervalo de confianza del 95% de esa diferencia media, no percentiles de las respuestas. [Referencia](https://www.itl.nist.gov/div898/handbook/prc/section1/prc14.htm).

$$
IC_{95}(\Delta)=[L_{95}(\Delta),\ U_{95}(\Delta)].
$$

Se pide $L_{95}(\Delta_q)>0$ para respaldar una ventaja en calidad, y $U_{95}(\Delta_v)\le0$ para descartar un aumento de infracciones según el criterio propuesto. **El Test 1 solo ejecuta B2; no calcula este contraste.**

**Umbrales por definir:**

- Por ahora se propone 80% de éxito válido, una mejora de al menos cinco puntos porcentuales y un intervalo de confianza del 95%.
- Se revisarán con las pruebas de factibilidad y se fijarán antes de comparar B1 con B2.
- Una ejecución no basta para concluir que funciona. Se repetirán las búsquedas y se reportarán también los fallos.
- Si los resultados no permiten distinguir las dos variantes, se dejará como inconcluso. No se cambiará el umbral después para darlo por cumplido.

## Siguiente sprint: aporte de cada componente

Aquí se busca saber **qué aporta permitir cambios en los prompts y qué aporta cambiar el workflow**. Se probarán tres condiciones:

| Condición | Prompts | Roles y workflow | Qué se compara |
|---|---|---|---|
| Completa | Se pueden cambiar | Se pueden cambiar | Referencia |
| Prompts fijos | No cambian | Se pueden cambiar | Qué se pierde al impedir cambios en las instrucciones |
| Workflow fijo | Se pueden cambiar | No cambian | Qué se pierde al impedir cambios en la organización |

Cada condición empezará desde la misma configuración, con el mismo modelo, régimen B1 o B2 y presupuesto. Se compararán calidad, incumplimientos, tiempo y consumo. Esta forma de dejar fija una parte y comparar se llama **ablación**.

**Relación con feature importance:**

- Las ablaciones previstas no entrenan pesos ni calculan importancia de columnas de un clasificador. Medir atributos del prompt sería un análisis complementario, todavía por definir.
- Sí se estimará el aporte de cada grupo de componentes, en el caso y las condiciones que se prueben.
- Por ejemplo, si la calidad pasa de 0,80 a 0,65 al fijar los prompts, la diferencia observada es de 15 puntos. Es un ejemplo; todavía no se ha medido.
- Los prompts y el workflow pueden depender entre sí. Esas diferencias no se sumarán como porcentajes de una importancia total.

**Para el siguiente sprint:**

- Definir los campos YAML que podrán cambiar y los que quedarán fijos.
- Preparar los escenarios y el criterio de evaluación.
- Fijar las tres condiciones, el modelo, las repeticiones y el presupuesto.

El Test 1 comprueba el bucle sobre prompts; todavía no compara componentes. El [diseño de las ablaciones](https://github.com/jairzinhosantos/thinking-harness/blob/develop/docs/academic/doc-0008-component-analysis.md) desarrolla esta parte.

[Matriz en PDF](https://github.com/jairzinhosantos/thinking-harness/blob/develop/docs/academic/consistency-matrix.pdf) · [Caso y ejecuciones](https://github.com/jairzinhosantos/thinking-harness/blob/develop/research/cases/case-0003-debt-negotiation/README.md)
