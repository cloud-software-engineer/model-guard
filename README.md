# Model Guard

**La puerta de seguridad para los modelos de IA en tu pipeline de CI/CD.**

Los modelos de IA descargados de repositorios públicos (como Hugging Face) a menudo vienen en formatos ejecutables como `.pkl` (Pickle). Estos archivos pueden contener código malicioso que se ejecuta silenciosamente al cargar el modelo en producción.

**Model Guard** es una GitHub Action que escanea automáticamente los artefactos de tus modelos en cada Pull Request. Si detecta código malicioso, **bloquea el merge** y te deja un comentario explicativo en el PR.

##  Quick Start (Empieza en 3 minutos)

Añade el siguiente workflow a tu repositorio en `.github/workflows/model-security.yml`:

```yaml
name: AI Model Security
on:
  pull_request:
    paths:
      - '**/*.bin'
      - '**/*.pt'
      - '**/*.pkl'
      - '**/*.safetensors'
      - '**/*.gguf'
      - '**/*.onnx'

jobs:
  scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: cloud-software-engineer/model-guard@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}