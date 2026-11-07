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
