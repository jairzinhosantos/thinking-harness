---
id: std-0001
title: Nomenclatura y ciclo de vida
status: accepted
revision: 1
created: 2026-09-29
updated: 2026-09-29
---

# Nomenclatura y ciclo de vida

## Nombres e identidad
Inglés, ASCII y minúsculas con kebab-case para archivos documentales y carpetas.
Python usa snake_case. Se conservan nombres convencionales: README.md, AGENTS.md,
LICENSE, CITATION.cff, Dockerfile y archivos de herramientas.
Documentos controlados: <type>-<four-digit-sequence>-<description>.md.
Tipos: std, dec, prd, pap, case, exp y doc. Las secuencias son independientes por tipo
y repositorio; no se reutilizan ni renumeran. Los huecos son válidos.
Antes de asignar un ID revisar docs/catalog.csv y research/literature/catalog.csv.

## Revisiones
Ruta estable durante edición; Git registra cambios.
Una revisión formal aumenta revision y produce una entrega r001, r002, etc.
Estados: draft, in-review, accepted, superseded, withdrawn.
La revisión no cambia al corregir cada errata, sino al emitir una nueva versión controlada.
Los documentos sustituidos enlazan su reemplazo. Las decisiones anteriores siguen localizables.
Las notas de reuniones utilizan YYYY-MM-DD-description.md.

## Conservación
Historial Git para ediciones anteriores; deliverables para entregas emitidas e inmutables.
_archive conserva documentos retirados con motivo, fecha y reemplazo en index.csv.
Las decisiones sustituidas permanecen en docs/decisions con estado superseded.
Los prototipos descartados pueden retirarse tras registrar evidencia y un commit recuperable.
Los temporales reproducibles se pueden eliminar; la evidencia negativa se conserva.
Los datos y logs grandes se almacenan fuera de Git, con manifiesto y checksum.
No archivar material privado dentro de este repositorio público.

## Catálogo
La cabecera YAML simple contiene id, title, status, revision, created y updated.
scripts/check_repository.py --write-catalog genera docs/catalog.csv.
No usar estructuras YAML anidadas en estos seis campos del catálogo.
