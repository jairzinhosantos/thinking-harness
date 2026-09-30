---
id: std-0002
title: Versionamiento y recursos
status: accepted
revision: 1
created: 2026-09-29
updated: 2026-09-29
---

# Versionamiento y recursos

## Capas
Código: commit. Software publicado: SemVer cuando exista interfaz definida; desarrollo inicial 0.x.
Documentos: revisiones rNNN. Protocolo, caso, dataset y evaluador: ID y revisión o hash.
Run: exp-NNNN-YYYYMMDDtHHMMSSz-<unique-suffix>, en UTC.
Candidato: cand-NNNN dentro de un run; registrar parent_id y modificación.
Cada reintento tiene nueva identidad y enlace al intento previo. Registrar costo y fallos.

## Manifiesto mínimo
Registrar commit (y cambios locales si los hubiera), protocolo, caso, configuración resuelta,
modelo/proveedor/parámetros, dataset/particiones/checksums, evaluador, semillas,
imagen por digest, hardware, presupuesto, inicio/fin y motivo de terminación.
Una semilla no garantiza reproducibilidad exacta de un proveedor remoto.
No sobrescribir evidencias de una ejecución emitida.

## Recursos
Prefijo: th. Compose project: th-case0001-dev-01 o th-case0001-eval-01.
Servicios funcionales: agent, evaluator, request-api, postgres.
Evitar container_name fijo. Aislar puertos y almacenamiento entre ejecuciones.
Etiquetas: project, case-id, experiment-id, run-id, environment, owner, expires-at.
Los recursos de nube adaptan el patrón a sus restricciones; las versiones viven en manifiestos.
Nada de nube o modelos se ejecuta automáticamente al hacer push.

## Referencias
- [SemVer](https://semver.org/)
- [Compose project names](https://docs.docker.com/compose/how-tos/project-name/)
- [Azure naming](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
