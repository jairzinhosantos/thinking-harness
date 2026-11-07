# Ejecución del control

El notebook lee resultados guardados. Ejecutar sus celdas no inicia una búsqueda nueva.
Estos comandos sí ejecutan modelos y generan otra carpeta en `results/`.

## Entorno local

- Python 3.12 y [dependencias](../requirements-local.txt).
- Pesos Qwen en caché, en la revisión fijada por el protocolo.
- Terminal situada en la carpeta del caso.
- `HF_HUB_OFFLINE=1` y `TRANSFORMERS_OFFLINE=1`: impiden descargas durante la prueba.
- `--thinking`: activa razonamiento; omitirlo ejecuta el barrido directo.
- `--confirmation-of`: evalúa un perfil previamente seleccionado en los casos reservados.

## Comandos de ejecución

Desde la carpeta del caso, con Python 3.12, MLX y los pesos fijados en caché:

```sh
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python utils/inference_tuning.py --model qwen3-8b --thinking
```

Para repetir el barrido directo, omitir `--thinking`; `--model qwen3-32b` usa el modelo mayor. La confirmación requiere una ejecución de ajuste que cumpla el criterio y conserve fuentes, pesos, política y casos:

```sh
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python utils/inference_tuning.py --model qwen3-8b --confirmation-of results/RUN_NAME
```

[Script](../utils/inference_tuning.py), [casos de confirmación](../inference-confirmation-cases.yaml) y [pruebas anteriores](../notebooks/local-model-test.ipynb). Los nombres exactos de las ejecuciones utilizadas figuran en la primera celda.

Para repetir el control API se necesita `OPENAI_API_KEY` en el entorno:

```sh
python utils/api_reference_test.py --allow-live --temperature 0
```

[Script API](../utils/api_reference_test.py). Límite: 36 llamadas, 50.000 tokens, 900 segundos y USD 0,25 estimados. La lectura del notebook no consume API. Tarifas registradas en esta prueba: USD 0,15/M de entrada y 0,60/M de salida, sin descontar caché. [Ficha oficial](https://developers.openai.com/api/docs/models/gpt-4o-mini).

