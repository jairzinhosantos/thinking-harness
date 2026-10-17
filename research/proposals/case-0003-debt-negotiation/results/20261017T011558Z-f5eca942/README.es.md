# Primera ejecución real de búsqueda de prompts

[English](README.md) | Español | [Caso](../../README.es.md) | [Modelamiento](../../modeling.es.md) | [Notebook](../../prompt-search.es.ipynb)

Se ejecutó una notebook en inglés con OpenAI el 16 de octubre de 2026 (America/Lima).
El ID de ejecución usa UTC. Ambas notebooks publicadas muestran esa misma evidencia sin nuevas llamadas.

## Resultado observado

Ningún candidato reemplazó al baseline generado una vez. La reserva de tokens detuvo la búsqueda
antes de completar la segunda ronda o llegar a la prueba final. Un puntaje de validación mayor
no cumplió la condición de cero incumplimientos. No se demuestra mejora final ni generalización.

| Versión | Etapa | Éxitos en validación | Respuestas con incumplimientos | Decisión |
|---|---|---:|---:|---|
| p000 | Semilla genérica | Sin evaluar | Sin evaluar | Semilla didáctica |
| p001 | Baseline generado una vez | 9/12 (75,0%) | 1 | Versión conservada |
| p002 | Ronda 1, candidato 1 | 9/12 (75,0%) | 2 | No admisible |
| p003 | Ronda 1, candidato 2 | 8/12 (66,7%) | 2 | No admisible |
| p004 | Ronda 2, candidato 1 | 10/12 (83,3%) | 1 | No admisible |

El baseline ofreció B en un pago en vez de C en dos pagos, que era la mayor deuda viable,
en las dos repeticiones de un caso de validación. En otra respuesta ofreció una cuota de 100
con capacidad declarada de 70. Estas comprobaciones separan el objetivo de una redacción fluida.
El optimizador recibió errores de desarrollo, no estas trazas de validación.

## Presupuesto y límites

- Modelo: `gpt-5.4-mini-2026-03-17`, para los tres roles.
- 148 llamadas a la API; 83 815 tokens de entrada y salida reportados por el proveedor.
- Costo estimado: USD 0,10261125, con los precios registrados sin descuento de caché.
- Límites: USD 1 y 100 000 tokens para optimizador, negociador, juez y comparación final.
- Reserva de la siguiente solicitud: 24 329 tokens; consumo más reserva habría sido 108 144.
  Esa solicitud no se envió. El límite efectivo fue de tokens, no de dólares.
- Prueba final: no alcanzada. La ejecución está incompleta, sin consumo incierto del proveedor.

Es un piloto sintético pequeño con un juez sin calibrar. Dos repeticiones no establecen
significancia estadística. Los hashes vinculan código y prompts al commit de origen.
Este experimento no entrena un modelo ni constituye auto-mejora recursiva.

## Evidencia

- [Reporte](report.json): evaluaciones, respuestas, justificaciones, parámetros y selección.
- Versiones YAML: [p000](prompts/p000.yaml), [p001](prompts/p001.yaml), [p002](prompts/p002.yaml), [p003](prompts/p003.yaml), [p004](prompts/p004.yaml).
- [Registro de consumo](usage.jsonl): reservas y uso reportado, sin cuerpos de solicitudes ni IDs.
- [Procedencia](provenance.json): hashes, activación explícita y diagnóstico del presupuesto.

Las solicitudes completas y la credencial local permanecen fuera de Git. No se hizo otra
prueba real para español. Antes de otro experimento, revisar los errores, la calibración del
juez y un presupuesto que reserve espacio para la prueba final. Se conserva esta búsqueda
sin mejora aceptada como evidencia.
