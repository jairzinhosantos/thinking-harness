---
id: doc-0003
title: Estrategia de agentes para desarrollar el proyecto
status: draft
revision: 1
created: 2026-09-29
updated: 2026-09-29
---

# Estrategia de agentes para desarrollar el proyecto

## Estado
Propuesta para un piloto posterior. Ningún agente persistente, scheduler ni bucle de
auto-modificación del proyecto está habilitado.

## Separación
Una cosa es usar agentes para construir thinking-harness; otra es evaluar científicamente
un método de mejora del harness. El primero es una herramienta de ingeniería.
No modifica datasets de prueba, criterios de aceptación ni resultados para obtener aprobación.

| Rol | Entrada | Entrega | Límite |
|---|---|---|---|
| coordinator | Objetivo e issue | Plan, asignación y resumen | No amplía alcance silenciosamente |
| research-reviewer | Paper y ficha | Evidencia, objeciones y citas | No marca lecturas humanas como completas |
| builder | Issue y criterios | Diff pequeño y explicación | No aprueba su propio cambio |
| qa | Diff y criterios originales | Verificaciones y fallos reproducibles | No debilita criterios para hacer pasar el cambio |
| experiment-runner | Protocolo fijado | Manifiesto, métricas y logs | Presupuesto y parada explícitos |
| documentation-reviewer | Evidencia aceptada | Documentación coherente | No convierte expectativas en resultados |

## Piloto incremental
1. Contratos de rol y plantilla de handoff.
2. Una tarea determinista, sin llamadas a modelos externos adicionales: builder produce el cambio.
3. QA revisa criterios originales y diseña una prueba de fallo plausible.
4. Coordinador integra evidencia; investigador resuelve discrepancias materiales.
5. Medir rework, tiempo, costo y defectos frente al flujo de referencia.
6. Solo entonces evaluar paralelismo y herramientas de orquestación.

## Handoff mínimo
Issue, objetivo, alcance, entradas, archivos permitidos, criterios, presupuesto,
commit de referencia, resultado esperado y condiciones para escalar una duda.
Una tarea tiene un dueño de escritura. El trabajo paralelo usa ramas o checkouts separados.
Registrar contribuciones y resolver conflictos antes de integrar.

## Aceptación del piloto
El cambio satisface criterios originales; QA entrega evidencia independiente; el historial
permite reconstruirlo; el costo está registrado; ninguna afirmación de calidad se basa solo
en autoaprobación. Un desacuerdo termina en revisión, no en un bucle ilimitado.

Diagrama editable: [development workflow](../../diagrams/source/agentic-development-workflow.drawio).
