# Ejecución del caso

La notebook principal lee resultados guardados. Estos comandos generan nuevas respuestas.

## Entorno y fuentes

- Python 3.12 y [dependencias](../requirements-local.txt) para MLX.
- Pesos locales en la revisión fijada en [models.py](models.py).
- Fuentes guardadas en Git antes de ejecutar; se registran commit y hashes.
- Terminal en la carpeta del caso. API: completar `OPENAI_API_KEY` en el `.env` local.
  [Plantilla](../.env.example). El archivo `.env` está excluido de Git; nunca se muestra en el notebook.

## Búsqueda B1/B2

Un único [bucle](paired_search.py); cambia la condición, no el programa.

```sh
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python utils/paired_search.py --strategy fixed --model qwen3-8b --output-tokens 4096
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python utils/paired_search.py --strategy adaptive --model qwen3-8b --output-tokens 4096
```

- `fixed`: B1; φ permanece fija.
- `adaptive`: B2; φ puede cambiar después de cada propuesta.
- `--decoding json_schema`: restricción del JSON local; por defecto, solo instrucciones.
- Cinco intentos. Hasta 90 llamadas, 180.000 tokens y 30 minutos por condición.
- Desarrollo aporta feedback; validación selecciona; test se consulta después.

## Comparación con GPT

Mismo bucle y escenarios. Cambian proveedor, tokenizer y generación estructurada nativa.
No hay control de semilla API ni comparación aislada del número de parámetros.

```sh
python utils/paired_search.py --strategy fixed --model gpt-4o-mini-2024-07-18 --allow-live
python utils/paired_search.py --strategy adaptive --model gpt-4o-mini-2024-07-18 --allow-live
```

Tope estimado: USD 0,50 por condición; USD 1 por el par. Sin reintentos automáticos.
Tarifas: USD 0,15/M de entrada y 0,60/M de salida. Se registran tokens reales y costo
estimado; el límite es una reserva de la aplicación, no un límite de facturación del proveedor.
[Ficha del modelo](https://developers.openai.com/api/docs/models/gpt-4o-mini).

## Control de inferencia

[Control con política manual](inference_tuning.py), sin mejorador ni actualizador:

```sh
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python utils/inference_tuning.py --model qwen3-8b --thinking
```

Sin `--thinking`: barrido de temperatura. `--confirmation-of results/RUN_NAME` evalúa
un ajuste que cumplió el criterio y mantiene las mismas fuentes y casos.
Los protocolos anteriores a la reorganización se consultan como historial; para repetirlos
se utiliza su commit original. No se presentan como nuevas ejecuciones del código actual.

## Archivos de salida

- `protocol.json`: condiciones, escenarios, versiones y hashes de fuentes.
- `calls.jsonl`: entradas, salidas, errores y consumo.
- `report.json`: propuestas, selección y métricas.
- `manifest.json`: hashes de los archivos de evidencia.

Las carpetas históricas también incluyen copias de scripts. Se conservan sin cambios.

## Demo local

Abre [la demo](../demo/index.html) para recorrer los dos primeros intentos registrados del Test 4. La escritura en esta vista previa tiene un ritmo ilustrativo.

### Presentación en vivo

1. En la terminal, desde la carpeta `demo/`, usa el entorno Python del caso con MLX y el modelo Qwen3 8B a 4 bits en caché.
2. Ejecuta `python server.py` y abre la dirección local que imprime.
3. Coloca el navegador y la terminal lado a lado. La primera conexión inicia la carga del modelo. La terminal muestra las llamadas y el navegador recibe los eventos y los fragmentos de la respuesta pública de Qwen.

La sesión ejecuta un intento adaptativo. Evalúa H0, propone H1 y aplica el mismo evaluador del caso a cuatro conversaciones de desarrollo y cuatro de validación. Se acepta la candidata si gana al menos un punto porcentual en validación y V es cero. Al completar una propuesta válida se revisa φ. El resultado pertenece a esta demostración de un intento.

### Reproducir una sesión

La terminal imprime la ruta de `events.jsonl`. Para conservar la sesión, copia ese archivo fuera de la carpeta temporal. Reprodúcelo con `python server.py --replay /ruta/events.jsonl`. El navegador mostrará «Grabación». La reproducción respeta los tiempos capturados y admite `--speed 2`.

Ctrl+C cierra el servidor. Usa `--port 8766` para elegir otro puerto.
