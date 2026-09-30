---
id: doc-0004
title: Opciones de seguimiento y revisión humana
status: draft
revision: 1
created: 2026-09-29
updated: 2026-09-29
---

# Opciones de seguimiento y revisión humana

## Decisión pendiente
El investigador puede orientar el trabajo por conversación, dejar ejecutar tareas acotadas
y revisar al volver. La disponibilidad es una referencia, no una métrica de progreso.
Este documento propone opciones; no fija cuotas, calendario ni agentes en ejecución.

| Opción | Unidad de avance | Ventaja | Límite |
|---|---|---|---|
| A. Evidencia y decisión semanal | Pregunta resuelta con ficha, prueba o comparación y decisión registrada | Adecuada para incertidumbre científica | Requiere acordar qué evidencia basta |
| B. Hitos con criterios de salida | Literature, scope, protocol, pilot y thesis plan | Visión clara de madurez | Puede ocultar avances pequeños dentro de un hito |
| C. Flujo de trabajo aceptado | Entregas aceptadas, tiempo de ciclo y correcciones | Útil al construir software | No todas las tareas tienen dificultad equivalente |

Propuesta: A como revisión semanal, B como mapa general y C cuando haya suficiente
implementación para interpretar sus señales. El investigador elegirá antes de convertirlo
en un estándar. Un resultado negativo documentado cuenta como avance si reduce incertidumbre.
No usar número de commits, líneas de código ni papers descargados como éxito científico.

## Reporte semanal propuesto
- Pregunta prioritaria y evidencia esperada.
- Evidencia obtenida, enlace y limitaciones.
- Decisión: continuar, ajustar, descartar o solicitar revisión.
- Incertidumbre que sigue abierta.
- Siguiente tarea con criterio de cierre y costo máximo acordado.

## Human-in-the-loop (HITL)
1. El investigador expresa el objetivo por voz o texto.
2. El coordinador lo convierte en una tarea verificable: alcance, entradas, criterios,
   permisos y presupuesto. Solo pide aclaración cuando falta una decisión necesaria.
3. Un builder o research-reviewer prepara cambios o evidencia dentro de ese alcance.
4. QA verifica de forma separada, deja resultados y devuelve defectos concretos.
5. El investigador recibe un paquete breve: propuesta, diff o ficha, pruebas, límites
   y decisión que necesita tomar. Puede aceptar, ajustar o descartar.
6. Se integra lo aceptado y se registra lo aprendido para la siguiente tarea.

Las instrucciones previamente autorizadas siguen vigentes. No pedir aprobación por cada
paso rutinario; escalar cambios de alcance, presupuesto, exposición de información o
conclusiones científicas que todavía no hayan sido acordados. Las credenciales de cada
agente deben corresponder a su tarea y entorno.

## Trabajo mientras el investigador está ausente
Preparar lecturas, ejecutar pruebas locales autorizadas y producir cambios en una rama
son candidatos a delegación acotada. La ejecución necesita un proceso activo y un contrato
de tarea; no se asume que el asistente sigue trabajando después de terminar una sesión.
Definir límites de intentos, costo, duración y recursos antes de activar un piloto.
Al agotarlos o detectar una dependencia sin resolver, conservar evidencia y pasar a Review.
No desplegar, publicar datos, cambiar criterios científicos ni habilitar gasto fuera del
alcance previamente autorizado. Evitar bucles de corrección sin límite.

## Primer piloto propuesto
Una tarea técnica pequeña con criterios objetivos. Comparar flujo asistido con builder + QA:
aceptación, fallos encontrados, correcciones necesarias, costo y carga de revisión humana.
Un piloto no basta para atribuir mejoras causales ni para concluir resultados de tesis.
La estrategia completa está en [agentic development](doc-0003-agentic-development-strategy.md).
