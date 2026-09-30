# Thinking Harness

Investigación aplicada sobre construcción, adaptación y mejora de harnesses agénticos.
El contenido está en español; los nombres de archivos, identificadores y código están en inglés.

**Estado:** preparación de investigación. El caso de tesis, algoritmo y framework siguen abiertos.
Este repositorio todavía no implementa un método de mejora ni reporta resultados experimentales propios.

## Empezar

1. [Plan de arranque](docs/doc-0002-initial-plan.md).
2. [Modelo operativo](docs/operating-model.md).
3. [Catálogo de papers](research/literature/catalog.csv).
4. [Primera lectura: STOP](research/literature/reviews/pap-0001-stop.md).
5. [Estrategia de agentes para construir el proyecto](docs/designs/doc-0003-agentic-development-strategy.md).
6. [Opciones de seguimiento e HITL](docs/designs/doc-0004-progress-and-hitl.md).
7. [Repositorio y tablero](docs/project-links.md).

La tesis seleccionará un caso y una pregunta concretos. El laboratorio público puede estudiar otros casos.
Una extensión institucional privada será opcional y consumirá versiones identificadas de este núcleo.

## Navegación

| Carpeta | Propósito |
|---|---|
| docs | Reglas, decisiones, diseño y seguimiento |
| research | Literatura, síntesis y propuestas |
| src, tests, configs | Implementación, pruebas y configuración |
| benchmarks, environments | Casos, evaluadores y servicios de referencia |
| experiments | Protocolos, manifiestos y análisis |
| data | Catálogo y ejemplos publicables |
| manuscripts, templates | Contenido académico y formato institucional |
| diagrams | Fuentes Draw.io y exportaciones |
| assets, scripts, deliverables | Recursos, herramientas y entregas |
| _archive | Material retirado con valor documental |

## Verificación local

Requiere Python 3.11 o superior, sin dependencias de terceros para estos controles.

~~~sh
python3 scripts/check_repository.py
python3 -m unittest discover -s tests/unit -v
~~~

La CI valida estructura documental, enlaces locales, catálogos y pruebas del verificador.
No ejecuta modelos ni consume servicios de nube.

## Alcance público

Solo se incorporan contenidos originales o cuya publicación sea apropiada.
Los documentos recibidos, datos institucionales, credenciales y conversaciones de trabajo
permanecen fuera de este repositorio. Las lecturas distinguen afirmaciones de autores,
interpretaciones y resultados comprobados.

## Licencia

MIT para el material original de este repositorio. Las referencias enlazadas mantienen sus propias licencias.
