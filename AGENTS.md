# Acuerdos de trabajo

- Documentación principal en español; nombres de archivos, identificadores, código,
  comentarios de código y docstrings en inglés. Los decks se redactan en inglés.
  Aplicar [std-0004](docs/standards/std-0004-writing-and-diagrams.md): traducciones
  selectivas, voz del proyecto, fuentes explícitas y prosa concreta.
- Leer el [plan](docs/doc-0002-research-plan.md) y el issue antes de cambiar el alcance.
- Un `README.md` por caso o paper. Mantener recursos y `utils/` dentro del caso;
  herramientas compartidas en `scripts/`. Crear carpetas cuando exista contenido.
- Eliminar borradores reemplazados y duplicados. Registrar reemplazos e IDs retirados
  en `docs/decisions/`; no reutilizar IDs ni modificar evidencia histórica de ejecuciones.
- Mantener títulos bibliográficos, citas, protocolos, prompts y resultados registrados
  en su forma original. Traducir documentación no autoriza cambiar el experimento.
- No incorporar PDFs de papers, material institucional, credenciales ni datos privados.
  Los originales y anotaciones permanecen en la biblioteca local.
- Usar ramas de tarea desde `develop` y PR hacia `develop`, según
  [std-0003](docs/standards/std-0003-branching-and-releases.md). Un responsable de escritura por rama.
- El agente llega como máximo a Review. Solo Jairzinho acepta y fusiona PRs, cierra issues
  como completadas, mueve tarjetas a Done y asigna Completed date. No habilitar auto-merge
  ni automatizaciones de cierre. CI correcto o un merge anterior no aceptan trabajo nuevo.
  La regla también se aplica al trabajo delegado. No escribir directamente en ramas permanentes.
- Preferir Mermaid para diagramas simples; Draw.io cuando sea necesario controlar el diseño.
  Mantener fuentes editables y verificar las representaciones que se publiquen.
- Distinguir afirmaciones de autores, interpretación, inspección estática y reproducción.
  Preparar una review no acredita lectura personal completa ni reproducción de resultados.
- Todo experimento necesita protocolo, presupuesto, condición de parada y ruta de evidencia.
  La asistencia de agentes al desarrollo es distinta del método científico evaluado.
- Ejecutar `python3 scripts/check_repository.py`, pruebas pertinentes y
  `npm run check:diagrams` antes de presentar el PR. Usar enlaces relativos.
- El diseño multiagente sigue siendo un piloto futuro. Estos acuerdos no autorizan
  delegación, agentes persistentes, programaciones, mensajes, gasto en modelos ni despliegues.
