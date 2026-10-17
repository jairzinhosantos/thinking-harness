---
id: dec-0008
title: "Español principal y notas de investigación"
status: in-review
revision: 1
created: 2026-10-17
updated: 2026-10-17
---

# Español principal y notas de investigación

## Decisión

Documentación principal en español. Nombres, identificadores, código y comentarios de código
en inglés; decks en inglés. Traducciones selectivas según audiencia, sin duplicar cada archivo.
La integración de esta migración se revisa en el [issue 43](https://github.com/jairzinhosantos/thinking-harness/issues/43).

| Cambio | Resultado |
|---|---|
| Reviews y casos bilingües | Un `README.md` principal en español; opcional `.en.md` cuando se necesite |
| Notebook de negociación | Una versión en español y su PDF derivado |
| Charter doc-0001 | Integrado en [doc-0002](../doc-0002-research-plan.md); ID retirado |
| Review STOP | Mecanismo, ecuaciones y código original; ejercicios básicos extensos permanecen en Git |
| Flujo de desarrollo con agentes | Un Mermaid en doc-0003 sustituye Draw.io y su exportación duplicada |
| Reglas de integración | Fuente principal en std-0003; otros documentos enlazan |

**ID reservado:** doc-0001 no se reutiliza. Su última versión previa a la consolidación
está en `413fe096dd37f2a1ca7bebba36b7d086d02b66f1`.
Se sustituye la parte de idioma de dec-0002 y la política bilingüe de dec-0004;
las decisiones históricas se conservan con esa aclaración.

## Límites

No cambia el objetivo experimental, prompts, configuración, evaluador ni resultados registrados.
El cambio de ruta de la guía solo actualiza dónde se lee el mismo objetivo y los hashes de
fuentes para futuras ejecuciones. No convierte el piloto v2 en evidencia del objetivo v3.

Los PDFs originales y anotaciones permanecen locales. Se conservan títulos bibliográficos,
citas, registros de búsqueda y evidencia histórica en su idioma original. El catálogo conserva
claves y estados controlados para mantener trazabilidad.

Archify se prueba localmente; todavía no forma parte de la estructura ni del CI. La ubicación
de los decks se decidirá antes de crearlos. No se publica contenido institucional.
