---
id: std-0002
title: "Versiones y recursos experimentales"
status: in-review
revision: 3
created: 2026-09-29
updated: 2026-10-17
---

# Versiones y recursos experimentales

## Capas de versión

Identificar código por commit; usar SemVer cuando exista una interfaz publicada, inicialmente
`0.x`. Documentos, casos, datasets y evaluadores conservan ID y revisión o hash.

| Capa | Convención | Ejemplo |
|---|---|---|
| Protocolo | `<case-id>-<study-slug>-vN`; incrementar ante cambios materiales | `case-0003-prompt-search-v3` |
| Ejecución | `YYYYMMDDTHHMMSSZ-<8-lowercase-hex>`, UTC | `20261017T011558Z-f5eca942` |
| Prompt | `p` y al menos tres dígitos, dentro de una ejecución | `p000`, `p001`, `p002` |

Publicar registros en `results/<run-id>/` dentro del caso. Salida local sin depurar puede
permanecer en `runs/`, ignorado por Git; documentar procedencia y tratamiento al publicarla.
Los prompts quedan en `prompts/`, con padre, hash y evaluación. En el piloto actual, `p000`
es la semilla y `p001` el baseline generado; los siguientes IDs no implican mejora aceptada.
Otros artefactos definen su identidad en el protocolo, sin adoptar un prefijo de prompts.

Un protocolo pequeño cabe en la guía del caso. Usar `exp-NNNN` si necesita documento propio;
no confundirlo con un run ID. Cada ejecución o reintento recibe un ID nuevo, conserva costo
y fallos y referencia intentos previos. No modificar registros históricos.

## Manifiesto mínimo

Commit y cambios locales; protocolo y caso; configuración resuelta; modelo, proveedor y
parámetros; dataset, particiones y checksums; evaluador; semillas; imagen y hardware cuando
correspondan; presupuesto, inicio, fin y motivo de parada. Una semilla no garantiza
reproducibilidad exacta con un proveedor remoto.

## Recursos

Prefijo `th`; proyectos Compose como `th-case0001-dev-01` o `th-case0001-eval-01`.
Servicios por función: `agent`, `evaluator`, `request-api`, `postgres`. Evitar `container_name`
fijo y aislar puertos y almacenamiento. Etiquetas: `project`, `case-id`, `experiment-id`,
`run-id`, `environment`, `owner`, `expires-at`. Adaptar nombres a restricciones del proveedor.
Un push no autoriza recursos de nube ni llamadas a modelos.

Referencias: [SemVer](https://semver.org/), [Compose](https://docs.docker.com/compose/how-tos/project-name/),
[Azure](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming).
