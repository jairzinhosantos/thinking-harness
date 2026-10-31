# Matriz de consistencia y siguiente sprint

**Tema:** Mejora recursiva de harnesses agénticos con modelos de pesos abiertos.

**[Matriz de consistencia en PDF: una página](https://github.com/jairzinhosantos/thinking-harness/blob/develop/docs/academic/consistency-matrix.pdf)** · [Test 1 ejecutado](https://github.com/jairzinhosantos/thinking-harness/blob/develop/research/cases/case-0003-debt-negotiation/harness-smoke-test.ipynb)

Se busca que el sistema construya y mejore su configuración, y comprobar qué aporta cambiar también sus instrucciones de mejora.

## Problema y comparación

Construir agentes exige probar instrucciones, roles y formas de coordinación hasta alcanzar una calidad aceptable. Se busca que el propio sistema haga esos ajustes con intervención humana acotada y comprobar si también conviene que cambie su forma de proponer mejoras.

**Pregunta:** ¿puede un sistema de IA construir y mejorar sus prompts y workflows hasta alcanzar una calidad definida, con intervención humana acotada? ¿Adaptar sus instrucciones de mejora aporta una ventaja frente a mantenerlas fijas?

- **B0:** configuración inicial, sin búsqueda; sirve para el diagnóstico.
- **B1:** cambia el harness con instrucciones de mejora fijas.
- **B2:** cambia el harness y también puede adaptar sus instrucciones de mejora.

B1 y B2 son automáticos. Se mantienen modelo, pesos, inferencia, motor, evaluación, datos y tope de recursos. El caso inicial es una negociación de deuda simulada, con uno a tres agentes y sin datos de clientes ni despliegue productivo.

## Variables

| Rol | Símbolo | Definición |
|---|---|---|
| Independiente principal | $Z\in\{0,1\}$ | Régimen de mejora: **0 = B1**, fijo; **1 = B2**, adaptable. Es una condición experimental binaria, no una puntuación. |
| Dependiente | $q$ | **Calidad:** proporción de ejecuciones correctas que cumplen todas las restricciones críticas. |
| Dependiente | $v$ | **Incumplimientos:** proporción de ejecuciones con alguna infracción crítica. |
| Dependiente | $T_{\mathrm{meta}}$ | **Tiempo hasta la meta:** tiempo acumulado hasta alcanzar el criterio en validación. Si no se alcanza, se registra el fallo y el tiempo consumido. |
| Dependiente | $\mathbf r_{\mathrm{uso}}$ | **Recursos:** tokens, llamadas y gasto monetario medible, registrados por separado. Incluye la adaptación y evaluación. |
| Dependientes | $N_h$, $M_h$ | **Intervención humana:** número de intervenciones durante el ciclo y minutos humanos por etapa, respectivamente. |

El acento en $\widehat q$ y $\widehat v$ indica que son estimaciones obtenidas de las ejecuciones. No son complementos: una decisión puede ser incorrecta sin violar una regla. La variación entre búsquedas también se informa.

## Matriz de consistencia

El problema y la pregunta anteriores se aplican a las tres filas. Hay **dos objetivos específicos**; diagnosticar fallos y delimitar el espacio editable son actividades del método.

| Nivel | Objetivo: qué se busca lograr | Hipótesis | Variables | Indicadores y criterio propuesto |
|---|---|---|---|---|
| **General** | Lograr que un sistema de IA construya y mejore su configuración agéntica, mediante cambios en roles, system prompts y workflows, hasta alcanzar una calidad definida con intervención humana acotada, usando modelos de pesos abiertos en escenarios simulados de cobranzas. | **HG:** el sistema puede obtener una configuración que alcance la calidad y el cumplimiento requeridos sin ediciones humanas durante el ciclo de mejora, manteniendo fijos los pesos del modelo y la evaluación. | **VI:** régimen $Z$.<br>**VD:** $q$, $v$, $N_h$.<br>**Complementarias:** $T_{\mathrm{meta}}$, $\mathbf r_{\mathrm{uso}}$, $M_h$. | • **Calidad final:** $\widehat q_{\mathrm{test}}\ge0.80$, al menos 80% de éxito válido.<br>• **Cumplimiento:** $\widehat v_{\mathrm{test}}=0$, ninguna infracción crítica observada.<br>• **Autonomía:** $N_h=0$, sin edición humana dentro del ciclo.<br>Comparte el criterio de OE1; la ventaja de adaptar se contrasta en OE2. |
| **OE1** | Obtener un sistema que construya, pruebe y mejore su configuración hasta alcanzar la calidad requerida, sin edición humana durante el ciclo, y que pueda actualizar y reutilizar sus instrucciones de mejora. | **HE1:** el sistema alcanza la calidad y el cumplimiento requeridos sin intervención durante el ciclo; en B2, utiliza al menos una actualización de sus instrucciones para proponer una versión posterior. | **Condición:** $Z=1$ para verificar adaptación.<br>**VD:** $q$, $v$, $N_h$.<br>**Comprobación técnica:** $N_{\mathrm{uso}}$, $V_{\mathrm{prot}}$, $\rho_{\mathrm{traza}}$. | • **Resultado:** $\widehat q_{\mathrm{test}}\ge0.80$ y $\widehat v_{\mathrm{test}}=0$.<br>• **Autonomía:** $N_h=0$.<br>• **Adaptación utilizada:** $N_{\mathrm{uso}}\ge1$.<br>• **Controles intactos:** $V_{\mathrm{prot}}=0$.<br>• **Trazabilidad completa:** $\rho_{\mathrm{traza}}=1$.<br>Informar qué proporción de búsquedas cumple estos criterios y con qué incertidumbre. |
| **OE2** | Lograr que adaptar las instrucciones de mejora aumente el éxito válido frente a mantenerlas fijas, sin aumentar los incumplimientos, con el mismo modelo y tope de recursos. | **HE2:** B2 supera a B1 en éxito válido en escenarios reservados para la prueba final, sin aumentar la tasa de infracciones críticas y contabilizando el costo de adaptar las instrucciones. | **VI:** $Z=0$ frente a $Z=1$.<br>**VD principales:** $q$, $v$.<br>**Contrastes:** $\Delta_q$, $\Delta_v$.<br>**Complementarias:** $T_{\mathrm{meta}}$, $\mathbf r_{\mathrm{uso}}$, $M_h$. | • **Ventaja observada:** $\widehat\Delta_q\ge0.05$, al menos 5 puntos porcentuales más de éxito válido.<br>• **Ventaja respaldada:** $L_{95}(\Delta_q)>0$, el intervalo de la diferencia de calidad queda por encima de cero.<br>• **Sin aumento de infracciones:** $U_{95}(\Delta_v)\le0$, el intervalo descarta un aumento según el criterio propuesto.<br>• **Comparación equivalente:** mismo tope de recursos y condiciones emparejadas. |

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

- No se entrenarán pesos ni se calculará la importancia de columnas de un clasificador.
- Sí se estimará el aporte de cada grupo de componentes, en el caso y las condiciones que se prueben.
- Por ejemplo, si la calidad pasa de 0,80 a 0,65 al fijar los prompts, la diferencia observada es de 15 puntos. Es un ejemplo; todavía no se ha medido.
- Los prompts y el workflow pueden depender entre sí. Esas diferencias no se sumarán como porcentajes de una importancia total.

**Para el siguiente sprint:**

- Definir los campos YAML que podrán cambiar y los que quedarán fijos.
- Preparar los escenarios y el criterio de evaluación.
- Fijar las tres condiciones, el modelo, las repeticiones y el presupuesto.

El Test 1 comprueba el bucle sobre prompts; todavía no compara componentes. El [diseño de las ablaciones](https://github.com/jairzinhosantos/thinking-harness/blob/develop/docs/academic/doc-0008-component-analysis.md) desarrolla esta parte.

[Matriz en PDF](https://github.com/jairzinhosantos/thinking-harness/blob/develop/docs/academic/consistency-matrix.pdf) · [Caso y ejecuciones](https://github.com/jairzinhosantos/thinking-harness/blob/develop/research/cases/case-0003-debt-negotiation/README.md)
