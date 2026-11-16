#  Model Guard

**La puerta de seguridad para los modelos de IA en tu pipeline de CI/CD.**

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-Model%20Guard-purple.svg?logo=github)](https://github.com/marketplace) [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Los modelos de IA descargados de repositorios públicos (como Hugging Face) a menudo vienen en formatos ejecutables como `.pkl` (Pickle). Estos archivos pueden contener código malicioso (Remote Code Execution) que se ejecuta silenciosamente al cargar el modelo en producción.

**Model Guard** es una GitHub Action que escanea automáticamente los artefactos de tus modelos en cada Pull Request. Si detecta código malicioso, **bloquea el merge** y te deja un comentario explicativo en el PR.

##  El Problema
El 83.5% de los modelos en Hugging Face usan formatos basados en Pickle. Un solo archivo comprometido puede dar a un atacante acceso total a tu infraestructura.

##  La Solución
Escaneo estático (Zero-Execution) del flujo de opcodes de Pickle antes de que el modelo toque tu servidor.

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
      - uses: cloud-software-engineer/model-guard@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}