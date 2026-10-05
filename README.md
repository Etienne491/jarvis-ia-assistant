# JARVIS Assistant

Un asistente IA tipo JARVIS creado con Flask, JavaScript y OpenAI.

## Características
- Interfaz web estilo HUD futurista
- Chat con IA
- Respuesta local si no hay API key
- Soporte para voz con Web Speech API
- Listo para expansion con comandos del sistema, automations y herramientas

## Requisitos
- Python 3.10+
- pip

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edita el archivo `.env` y añade tu `OPENAI_API_KEY` si quieres usar OpenAI.

## Ejecutar

```bash
python app.py
```

Abre en tu navegador:

```text
http://localhost:5000
```

## Variables de entorno
- `APP_NAME`: nombre del asistente
- `OPENAI_MODEL`: modelo de OpenAI a usar
- `OPENAI_API_KEY`: clave de API de OpenAI

## Prompt para Claude Code

Pega este mensaje en Claude Code:

```text
Instala este proyecto en la carpeta actual, crea el entorno virtual si hace falta, instala las dependencias con pip install -r requirements.txt, crea el archivo .env a partir de .env.example, y ejecuta la aplicación con python app.py. Si algo falla, corrige los errores y deja el proyecto listo para usarse.
```
