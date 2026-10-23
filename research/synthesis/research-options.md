# Alternativas de investigación

Hipótesis de trabajo, no conclusiones de novedad. Seleccionar por relevancia, costo,
evaluabilidad y posibilidad de reproducir el caso.

| Alternativa | Pregunta | Comparación necesaria |
|---|---|---|
| Mejorador fijo | Qué aporta el feedback | Baseline y costo por candidato |
| Mejora recursiva | Qué aporta modificar al mejorador | Ablación frente a mejorador fijo con presupuesto comparable |
| Evolución | Qué aporta una población o archivo | Búsqueda local como referencia |
| Planificación | Qué aporta planificar operaciones de construcción | Modelo de acciones y costo de búsqueda |
| RL | Qué aprende una política de construcción | Costo de entrenamiento y generalización |

Los [casos activos](../cases/README.md) exploran código y negociación sintética. Un juego sigue
siendo una alternativa, sin caso activo. No afirmar que mejorar harnesses es un vacío sin estudiar
los antecedentes cercanos.

## Mapa de literatura

Pregunta orientadora: ¿qué aporta mejorar al mejorador frente a un procedimiento fijo,
con presupuesto comparable y tareas no vistas?

La ampliación de 2026-10-11 añadió diez trabajos a los trece previos. El
[catálogo](../literature/catalog.csv) conserva fuentes y estados; el
[protocolo](../literature/search-protocol.md#clasificación-y-originales-locales) define la clasificación.
La tabla es una interpretación preliminar de resúmenes, pasajes seleccionados y repositorios
vinculados, no una review completa ni aplicabilidad demostrada.

| Paper y versión | Prioridad | Cercanía | Función y distinción |
|---|---|---|---|
| pap-0020 [Meta-Harness v1](https://arxiv.org/abs/2603.28052v1) | P0 | Directa | Baseline: búsqueda sobre código de harness con puntuaciones y trazas. Instrucciones fijas pueden usar feedback cambiante |
| pap-0021 [MetaSkill-Evolve v1](https://arxiv.org/abs/2607.05297v1) | P0 | Directa | Mejorador adaptativo: skills y meta-skills evolucionan a distinta velocidad con modelo fijo; cambian archivos de skills |
| pap-0017 [Mixture of Self-Improving Branches v1](https://arxiv.org/abs/2609.37834v1) | P0 | Directa | Cambian instrucciones de propuesta y subconjuntos de desarrollo, no código del optimizador |
| pap-0019 [RRSI v3](https://arxiv.org/abs/2609.24972v3) | P0 | Directa | Búsqueda regularizada: restricciones de propuesta y selección para estudiar generalización y costo |
| pap-0015 [SO-RSI v2](https://arxiv.org/abs/2610.05701v2) | P0 | Directa | Diagnosticar fallos recurrentes antes de editar workflows; segundo orden no implica código optimizador que se reescribe |
| pap-0018 [Harness Evolution as Learning v1](https://arxiv.org/abs/2609.36892v1) | P1 | Directa | Teoría de aproximación, generalización y límites; verificar transferencia de supuestos a reparación de código |
| pap-0022 [RHI v1](https://arxiv.org/abs/2607.15524v1) | P1 | Directa | Revisar una especificación de bucle agéntico mediante feedback por pares; separar prompt y código optimizador |
| pap-0023 [HELIX v1](https://arxiv.org/abs/2608.13951v1) | P1 | Complementaria | Representación del harness y extracción de datos; el experimento reportado de reparación cubre una ronda, no coevolución repetida demostrada |
| pap-0014 [MASS v1](https://arxiv.org/abs/2610.12176v1) | P2 | Complementaria | Alterna evolución de workflow y fine-tuning; cambiar el modelo requiere otra comparación y cómputo |
| pap-0016 [Reasoning Data Synthesis v1](https://arxiv.org/abs/2610.03548v1) | P2 | Complementaria | Evoluciona skills y workflows de síntesis con pesos y verificación fijos; producir tareas no equivale a resolver una suite fija |

Nuevo en el catálogo no significa publicado recientemente: Meta-Harness es de marzo;
MetaSkill-Evolve y RHI, de julio; HELIX, de agosto. No se afirma venue revisado para este lote.

## Ampliación de 2026-10-22

Se incorporan doce trabajos a los 23 previos. Las fechas son el primer envío a arXiv;
las versiones identifican el texto seleccionado. La clasificación procede de metadatos
y resúmenes, no de lectura completa. Los siete primeros son posteriores al corte de
2026-10-11; los cinco restantes son incorporaciones recuperadas de fechas anteriores.

| Paper y versión | Primer envío | Prioridad | Función y límite preliminar |
|---|---|---|---|
| pap-0024 [HarnessPro v2](https://arxiv.org/abs/2610.26770v2) | 2026-10-19 | P0 | Evoluciona harnesses con pruebas generadas por LLM y selecciona variantes según rendimiento y costo. Mejorar el harness no establece que el mejorador se modifique; falta auditar el costo total de búsqueda y la independencia de evaluación. |
| pap-0025 [RSIFlow v1](https://arxiv.org/abs/2610.21791v1) | 2026-10-15 | P0 | Diagnostica fallos y selecciona workflows por componente; destila resultados en skills y principios del metaagente. Candidato para estudiar evolución del mejorador; falta aislar su contribución con presupuesto comparable. |
| pap-0026 [Harness-Delta Attribution v1](https://arxiv.org/abs/2610.22466v1) | 2026-10-15 | P0 | Descompone ganancias en sobreajuste detectado, cómputo adicional y residuo. El residuo es una cota superior de posible mejora generalizable, no prueba de transferencia; depende de los controles de neutralización y cómputo. |
| pap-0027 [UCoE v1](https://arxiv.org/abs/2610.17609v1) | 2026-10-13 | P1 | Coevoluciona un verificador ejecutable y el estado del harness con pesos fijos, usando contrastes de respuestas para seleccionar verificadores. Posible referencia para tareas abiertas; la evaluación final debe distinguirse del verificador evolutivo. |
| pap-0028 [HERO v2](https://arxiv.org/abs/2610.19184v2) | 2026-10-13 | P1 | Aprende prompts reutilizables con feedback de ejecución y refina programas por instancia en inferencia. Comparador para generación de código; separar optimización offline, refinamiento por tarea y modificación del mejorador. |
| pap-0029 [Self-Evolving Agent Harness v1](https://arxiv.org/abs/2610.18813v1) | 2026-10-13 | P1 | Distingue estado interpretado y componentes ejecutables, mecanismos de propuesta y admisión. Presenta cotas condicionadas a supuestos y validación independiente; no garantiza mejora general para cualquier harness. |
| pap-0030 [SpecRSI v1](https://arxiv.org/abs/2610.16491v1) | 2026-10-12 | P1 | Propone sucesores antes de terminar verificaciones, exige verificación antes de adopción y aprende el mejorador de búsquedas completas. Falta revisar qué parámetros cambia GVO y su costo antes de usarlo en una comparación con modelo fijo. |
| pap-0031 [Two Perspectives on RSI v1](https://arxiv.org/abs/2610.14625v1) | 2026-10-10 | P1 | Organiza métodos en nueve dimensiones y conecta RSI con mecanismos de aprendizaje y evolución. Referencia para formular comparaciones; no constituye un baseline experimental ni evidencia de eficacia de una nueva combinación. |
| pap-0032 [HMED v1](https://arxiv.org/abs/2610.07979v1) | 2026-10-06 | P0 | Reejecuta meta-skills originales y revisadas desde el mismo estado restaurado y conserva sus consecuencias como meta-experiencia. Permite estudiar atribución al mejorador; falta comprobar controles de ruido y contabilizar el costo de reejecución. |
| pap-0033 [MESH-Harness v1](https://arxiv.org/abs/2610.05300v1) | 2026-10-04 | P1 | Recombina módulos mediante LinUCB y búsqueda por coordenadas, con ediciones guiadas por trazas y pesos fijos. Comparador de búsqueda modular; no establece modificación recursiva del algoritmo de búsqueda. |
| pap-0034 [ActiveSaddler v1](https://arxiv.org/abs/2610.00906v1) | 2026-10-01 | P1 | Adapta escenarios mediante patrones de fallo y un bandit no estacionario, equilibrando optimización y descubrimiento. Permite separar selección adaptativa de feedback y reglas de edición; cambiar currículo no implica reescribir el mejorador. |
| pap-0035 [Meta-Skill AI4AI v2](https://arxiv.org/abs/2609.38143v2) | 2026-09-29 | P1 | Un Builder aprende principios de construcción del feedback de un Target con ambos modelos fijos; congela el banco antes de construir harnesses para tareas no vistas. No equivale a mejora recursiva continua en evaluación; revisar costo de construcción. |

RSIFlow y HMED son candidatos prioritarios para estudiar cambios del mejorador;
Harness-Delta Attribution aporta controles de evaluación y HarnessPro, comparación de costo
y rendimiento. Estas prioridades no sustituyen las lecturas en curso ni seleccionan un método.
Los doce registros mantienen lectura pendiente, código sin inspeccionar y ejecución no realizada.
No se descargaron sus PDFs ni se verificaron sus repositorios o publicación revisada por pares.

## Orden y extracción

Continuar STOP y Self-Harness. Luego: Meta-Harness, MetaSkill-Evolve, Mixture, RRSI y SO-RSI.
La prioridad es ajustable; la teoría de generalización puede adelantarse al formalizar supuestos.

Por paper, identificar:

1. Objeto editable y componentes fijos: solución, harness, instrucciones, datos o pesos.
2. Quién propone la siguiente versión y si vuelve a ejecutar el procedimiento actualizado.
3. Ablaciones con mismo modelo, punto de partida, particiones y presupuesto.
4. Generalización fuera de búsqueda; costo de búsqueda separado del costo de uso.

La sección 4.5 de Mixture separa adaptación de propuestas y poda del conjunto de desarrollo.
Reporta que adaptar solo propuestas no supera la referencia de búsqueda independiente.
Es un motivo para estudiar la ablación, no una conclusión universal sobre nuestro caso.

## Límites de verificación del lote de 2026-10-11

Se verificaron páginas de [MASS](https://github.com/SakanaAI/mass),
[Harness Evolution as Learning](https://github.com/ZyGan1999/self-evolving-harness-as-learning),
[RRSI](https://github.com/google-research/rrsi),
[Meta-Harness](https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact) y
[HELIX](https://github.com/HKUDS/HELIX); falta inspección y ejecución.
Meta-Harness enlaza un artefacto optimizado de Terminal-Bench, no un sistema de búsqueda
completo verificado. MASS documenta diferencias entre paquete y experimentos publicados.

Los otros cinco enlaces de código siguen sin verificar. Los diez PDFs están en la biblioteca
local. Este screening no completa lectura, discusión ni reproducción; los trece registros
iniciales todavía tienen comprobaciones bibliográficas y cobertura BibTeX pendientes.
