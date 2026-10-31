# Matriz de consistencia y siguiente sprint

**Tema:** Mejora recursiva de harnesses agénticos con modelos de pesos abiertos.

Esta página reúne la matriz y el diseño de importancia de componentes. El [plan de tesis completo](thesis-plan.pdf) queda como lectura opcional. Se presenta un diseño experimental; todavía no se atribuyen resultados a la mejora recursiva.

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
| **General** | Lograr que un sistema de IA construya y mejore su configuración agéntica, mediante cambios en roles, system prompts y workflows, hasta alcanzar una calidad definida con intervención humana acotada, usando modelos de pesos abiertos en escenarios simulados de cobranzas. | **HG:** el sistema puede obtener una configuración que alcance la calidad y el cumplimiento requeridos sin ediciones humanas durante el ciclo de mejora, manteniendo fijos los pesos del modelo y la evaluación. | **VI:** régimen $Z$.<br>**VD:** $q$, $v$, $N_h$.<br>**Complementarias:** $T_{\mathrm{meta}}$, $\mathbf r_{\mathrm{uso}}$, $M_h$. | Calidad final $\widehat q_{\mathrm{test}}\ge0.80$.<br>Infracciones observadas $\widehat v_{\mathrm{test}}=0$.<br>Intervenciones en el ciclo $N_h=0$.<br>Comparte el criterio de calidad y autonomía de OE1; no supone la ventaja de HE2. |
| **OE1** | Obtener un sistema que construya, pruebe y mejore su configuración hasta alcanzar la calidad requerida, sin edición humana durante el ciclo, y que pueda actualizar y reutilizar sus instrucciones de mejora. | **HE1:** el sistema alcanza la calidad y el cumplimiento requeridos sin intervención durante el ciclo; en B2, utiliza al menos una actualización de sus instrucciones para proponer una versión posterior. | **Condición:** $Z=1$ para verificar adaptación.<br>**VD:** $q$, $v$, $N_h$.<br>**Comprobación técnica:** $N_{\mathrm{uso}}$, $V_{\mathrm{prot}}$, $\rho_{\mathrm{traza}}$. | $\widehat q_{\mathrm{test}}\ge0.80$; $\widehat v_{\mathrm{test}}=0$; $N_h=0$.<br>$N_{\mathrm{uso}}\ge1$; $V_{\mathrm{prot}}=0$; $\rho_{\mathrm{traza}}=1$.<br>Reportar la fracción de búsquedas que cumple y su incertidumbre. |
| **OE2** | Lograr que adaptar las instrucciones de mejora aumente el éxito válido frente a mantenerlas fijas, sin aumentar los incumplimientos, con el mismo modelo y tope de recursos. | **HE2:** B2 supera a B1 en éxito válido en escenarios reservados para la prueba final, sin aumentar la tasa de infracciones críticas y contabilizando el costo de adaptar las instrucciones. | **VI:** $Z=0$ frente a $Z=1$.<br>**VD principales:** $q$, $v$.<br>**Contrastes:** $\Delta_q$, $\Delta_v$.<br>**Complementarias:** $T_{\mathrm{meta}}$, $\mathbf r_{\mathrm{uso}}$, $M_h$. | $\widehat\Delta_q\ge0.05$: al menos 5 puntos porcentuales.<br>$L_{95}(\Delta_q)>0$.<br>$U_{95}(\Delta_v)\le0$.<br>Mismo tope total de recursos; condiciones emparejadas. |

**Cómo leer los indicadores:**

- $N_{\mathrm{uso}}$: actualizaciones de instrucciones utilizadas en una propuesta posterior.
- $V_{\mathrm{prot}}$: ediciones de elementos protegidos, como pesos, motor o evaluación.
- $\rho_{\mathrm{traza}}$: cambios reconstruibles / cambios registrados. Sin cambios registrados no se calcula y OE1 no se cumple.
- $\Delta_q$ y $\Delta_v$: diferencias medias de B2 menos B1 entre búsquedas emparejadas; $L_{95}$ y $U_{95}$ son los límites del intervalo de confianza del 95%.

**Los umbrales son provisionales.** El 80%, los 5 puntos y el nivel de confianza deben justificarse en factibilidad y fijarse antes de la comparación. Un éxito aislado no acredita fiabilidad general; cero infracciones observadas no demuestra riesgo nulo. No alcanzar un objetivo se reportará como tal. Si falta precisión, el contraste será inconcluso; no se ajustará el umbral para declarar éxito.

## Siguiente sprint: importancia de componentes

En este estudio, la importancia se examina mediante **ablaciones**: repetir la búsqueda dejando fija una parte del harness y comparar el resultado. No se entrenan pesos ni se calcula importancia de columnas de un clasificador.

| Condición | Prompts | Roles y workflow | Propósito |
|---|---|---|---|
| Espacio completo | Editables | Editables | Referencia |
| Prompts congelados | Fijos | Editables | Medir qué aporta permitir cambios en instrucciones |
| Organización congelada | Editables | Fijos | Medir qué aporta permitir cambios en roles y coordinación |

En estas tres condiciones se mantiene el mismo $Z$, punto inicial, modelo, datos y presupuesto. El espacio editable es un segundo factor experimental, distinto del contraste principal B2 frente a B1. Los efectos pueden interactuar; no se sumarán como porcentajes de importancia.

**Entrega prevista:**

- Esquema YAML y campos protegidos definidos.
- Matriz de escenarios y criterios de evaluación, con cobertura del alcance acordado.
- Protocolo de las tres condiciones, particiones separadas y reserva para prueba final.
- Modelo, número de búsquedas, presupuesto y condición de parada fijados antes de ejecutar.

**Cierre del sprint:** diseño preparado y revisado. Las ejecuciones y sus resultados corresponden a una etapa posterior. El [detalle del análisis](doc-0008-component-analysis.md) incluye el flujo, la estimación del aporte y las referencias.

[Plan de tesis completo (PDF)](thesis-plan.pdf) · [Caso y evidencia previa](../../research/cases/case-0003-debt-negotiation/README.md)
