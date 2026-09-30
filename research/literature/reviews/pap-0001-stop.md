---
id: pap-0001
title: STOP: primera lectura
status: draft
revision: 1
created: 2026-09-29
updated: 2026-09-29
---

# STOP: primera lectura

## Fuentes y estado
[Paper v3](https://arxiv.org/abs/2310.02304v3), COLM 2024.
[Repositorio](https://github.com/microsoft/stop).
Lectura parcial: resumen, introducción, sección 3 y algoritmo 1.
Código: inspección parcial de run_improver.py y eval_improver.py; no ejecutado.
Discusión con investigador: pendiente.

## Mecanismo documentado
STOP utiliza un programa mejorador que recibe una utilidad u, una solución s y un
modelo L. Produce una solución candidata s'. La meta-utilidad evalúa qué tan bien
ese mejorador resuelve un conjunto de tareas. Luego el propio mejorador se aplica
a su código usando esa meta-utilidad. El modelo permanece fijo; los autores distinguen
este alcance de una RSI completa. Fuente: sección 3 y algoritmo 1.

~~~text
s' = I(u, s, L)
meta(I) = promedio sobre (u,s) en D de u(I(u,s,L))
I[t+1] = I[t](meta, I[t], L)
~~~

I: programa mejorador; D: tareas usadas para estimarlo. La mejora es un objetivo,
no una garantía por iteración. El algoritmo no demuestra optimalidad general.
Resultados y apéndices siguen pendientes de lectura crítica.

## Preguntas propias para la próxima sesión
- ¿Cómo distinguiremos mejorar una solución de mejorar el constructor?
- ¿Qué tarea pequeña permitiría medir ambas cosas?
- ¿Cuánto costaría producir el mejorador antes de reutilizarlo?
- ¿Qué evaluación deberá quedar fuera del alcance del código propuesto?
- ¿Qué baseline aislaría el efecto de modificar el mejorador?
- ¿Qué afirma exactamente cada experimento y qué no podemos generalizar?

## Guion de sesión
Explicar el problema; dibujar ambos niveles; trabajar un ejemplo numérico propio;
seguir una llamada en código; registrar dudas; decidir la siguiente lectura.
No se ha ejecutado código de terceros ni se reportan resultados propios.

## Recorrido inicial del código
Commit verificado: 0d6780c54306b2486dd36e9c4ae9b49aceb27ea4.
- [run_improver.py](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/run_improver.py):
  inspección de inicialización y recuperación del mejorador.
- [eval_improver.py](https://github.com/microsoft/stop/blob/0d6780c54306b2486dd36e9c4ae9b49aceb27ea4/eval_improver.py):
  localizar el recorrido de evaluación antes de preparar una reproducción.
- Pendiente: dependencias, utilidades de tareas, aislamiento, costos y correspondencia
  completa entre versión publicada y repositorio.
