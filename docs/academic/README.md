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

### Adaptación, controles y trazabilidad

- **$N_{\mathrm{uso}}$: actualizaciones utilizadas.** Cuenta cuántas veces se reescriben las instrucciones de mejora y después se usan para proponer otra versión. Guardar instrucciones nuevas sin utilizarlas no cuenta. No demuestra por sí solo que hayan mejorado el resultado.
- **$V_{\mathrm{prot}}$: cambios detectados en elementos protegidos.** Son partes que deben permanecer fijas para atribuir el resultado a los cambios del harness. Por ejemplo, modificar el evaluador para aceptar una respuesta antes incorrecta invalidaría la comparación. Se exige cero cambios detectados dentro del alcance auditado.
- **$\rho_{\mathrm{traza}}$: proporción de cambios que se pueden reconstruir.** Para cada propuesta se debe poder recuperar la versión de origen, las instrucciones usadas, la nueva versión, su evaluación y la decisión de conservarla o rechazarla. Esto permite explicar **qué cambió y por qué**; no implica que volver a llamar al LLM produzca exactamente el mismo texto.

| Elemento protegido | Qué significa | Cómo se controla |
|---|---|---|
| Modelo y pesos | El modelo utilizado y sus parámetros aprendidos durante el entrenamiento | Mantener el mismo modelo y versión; no entrenar ni cambiar pesos durante la comparación. Con una API se verifica el identificador y la configuración, no se inspeccionan los pesos del proveedor. |
| Motor | Código que llama al modelo, ejecuta el bucle y selecciona candidatos | Comparar la versión o hash del código antes y después. Un hash identifica el contenido de un archivo. |
| Evaluación | Reglas, respuestas esperadas y criterio de aceptación | Conservar el evaluador, los escenarios reservados y sus referencias. No reducir el umbral después de observar el resultado. |
| Presupuesto y flujo | Límites de llamadas, tokens, costo y orden de ejecución | Fijarlos antes de comenzar y registrarlos con la ejecución. |

**Ejemplo de trazabilidad:** se propuso cambiar «preguntar siempre por la capacidad» por «preguntar solo si se desconoce». El registro debe mostrar el prompt anterior, la petición y respuesta del mejorador, el prompt nuevo, sus puntuaciones y si se conservó. Si de cinco cambios registrados se pueden reconstruir cuatro, $\rho_{\mathrm{traza}}=4/5=0.80$. Si no hubo cambios, el indicador queda **no calculable**, no se asigna uno y no se acredita la adaptación de OE1.

El Test 1 usa un control acotado: hashes de los archivos de motor, cliente/evaluador y escenarios, más las peticiones registradas. No certifica la infraestructura ni los pesos remotos. Las propuestas rechazadas también se conservan para poder revisar sus fallos.

### Diferencia entre B2 y B1

Una **búsqueda** es una ejecución completa del proceso de mejora; una **iteración** es uno de sus pasos. Se comparan varias búsquedas completas, no se tratan los pasos de una misma búsqueda como experimentos independientes.

Cada par $j$ contiene una búsqueda B1 y otra B2 con el mismo punto de partida, modelo, escenarios y límite de recursos; se empareja la aleatoriedad cuando el proveedor lo permite. Sobre $m$ pares:

$$
d_{q,j}=\widehat q_{B2,j}-\widehat q_{B1,j},\qquad
\widehat\Delta_q=\frac{1}{m}\sum_{j=1}^{m}d_{q,j}.
$$

- **$\widehat\Delta_q$:** diferencia media de calidad. Si un par pasa de 0,70 en B1 a 0,78 en B2, aporta $+0,08$: ocho puntos porcentuales.
- **$\widehat\Delta_v$:** se calcula igual con la tasa de incumplimientos. Un valor negativo favorece B2; uno positivo significa más infracciones.

### Qué significan $L_{95}$ y $U_{95}$

El intervalo de confianza cuantifica la incertidumbre al estimar la **diferencia media**, a partir de varias búsquedas emparejadas:

$$
IC_{95}(\Delta)=[L_{95}(\Delta),\ U_{95}(\Delta)].
$$

- **$L_{95}$:** extremo inferior del intervalo.
- **$U_{95}$:** extremo superior del mismo intervalo.
- **95%:** nivel de confianza del procedimiento. Bajo sus supuestos, al repetir el estudio muchas veces, aproximadamente 95 de cada 100 intervalos construidos así contendrían la diferencia media verdadera. No es el percentil 95 de las respuestas ni la proporción de casos correctos. [Referencia: NIST](https://www.itl.nist.gov/div898/handbook/prc/section1/prc14.htm).

**Ejemplos ilustrativos, no resultados:**

| Intervalo | Lectura |
|---|---|
| Calidad: $[0.02,\ 0.12]$ | El límite inferior es positivo: respalda una ventaja media de B2. Además debe comprobarse el criterio separado de al menos cinco puntos observados. |
| Calidad: $[-0.02,\ 0.12]$ | Incluye cero: la evidencia todavía no permite concluir una ventaja. |
| Incumplimientos: $[-0.04,\ 0.01]$ | El límite superior permite un aumento de un punto: no cumple el criterio de no aumento. |

El método para calcular estos intervalos, el número de pares y los supuestos se fijarán antes del contraste. El Test 1 solo ejecuta B2; **no calcula diferencias B2 frente a B1 ni intervalos de confianza**. Sus cinco iteraciones no equivalen a cinco pares de búsquedas.

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
