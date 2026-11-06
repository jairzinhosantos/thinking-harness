# Casos de investigación

Cada carpeta reúne la especificación, estudios relacionados y evidencia del caso.
Ninguno define todavía la contribución final de la tesis.

| Caso | Entradas de lectura | Estado |
|---|---|---|
| [case-0001: corrección de código](case-0001-code-repair-harness/README.md) | [Escenarios y EDA](case-0001-code-repair-harness/scenarios.md); [participación del harness](case-0001-code-repair-harness/harness-participation.md) | Propuesta, sin ejecución; la extensión mantiene un alcance separado |
| [case-0003: negociación sintética](case-0003-debt-negotiation/README.md) | [Test 1: adaptación](case-0003-debt-negotiation/harness-smoke-test.ipynb); [Test 2: modelos locales](case-0003-debt-negotiation/local-model-test.ipynb); [Test 3: inferencia](case-0003-debt-negotiation/inference-tuning.ipynb); [Test 4: B1/B2](case-0003-debt-negotiation/paired-search.ipynb); [Test 5: JSON](case-0003-debt-negotiation/structured-output.ipynb) | Pruebas exploratorias ejecutadas; alcance y límites en cada notebook |

El plan de escenarios de corrección propone 36 ejecuciones de viabilidad; no son resultados.
Los notebooks de negociación consultan evidencia guardada sin llamadas a modelos. El piloto
original permanece en la carpeta como antecedente; su PDF es una copia de lectura.

El caso de workflow de servicios y su estudio se retiraron. Los IDs case-0002 y doc-0006
siguen reservados en la [decisión de limpieza](../../docs/decisions/dec-0006-active-research-cleanup.md).
