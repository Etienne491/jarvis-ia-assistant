import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
app.config["APP_NAME"] = os.getenv("APP_NAME", "JARVIS")
app.config["APP_MODEL"] = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def local_reply(message: str) -> str:
    msg = message.lower().strip()

    if not msg:
        return "Estoy listo para ayudarte. ¿Qué deseas hacer?"

    if "hola" in msg or "buenas" in msg or "hello" in msg:
        return "Buenos días. JARVIS en línea. ¿En qué puedo ayudarte hoy?"

    if "hora" in msg:
        now = datetime.now()
        return f"Son las {now.strftime('%H:%M:%S')} y hoy es {now.strftime('%A %d de %B del %Y')}."

    if "tarea" in msg or "lista" in msg or "recordatorio" in msg:
        return "Tengo estas tareas prioritarias: revisar correos, analizar datos y preparar una respuesta. ¿Quieres que te ayude a organizarlas?"

    if "abrir" in msg or "navegar" in msg or "web" in msg:
        return "Puedo ayudarte a buscar o preparar contenido web, pero para abrir sitios necesito un navegador o una acción concreta del sistema."

    if "estado" in msg or "sistema" in msg:
        return "Todo el sistema está operativo. Los módulos de IA, voz y lógica están preparados para atender tus instrucciones."

    if "adiós" in msg or "bye" in msg or "chau" in msg:
        return "Hasta luego. JARVIS sigue activo y listo cuando me necesites."

    return (
        f"Entendido. Estoy ejecutando el protocolo de asistencia para: '{message}'. "
        "Puedo ayudarte a responder, organizar tareas, investigar información o generar ideas."
    )


def generate_ai_reply(message: str, history: list[dict] | None = None) -> str:
    if client is None:
        return local_reply(message)

    messages = [
        {
            "role": "system",
            "content": (
                "Eres JARVIS, un asistente personal avanzado. Responde con tono profesional, claro y útil. "
                "Haz respuestas concisas, pero útiles. Si no sabes algo, dilo con honestidad."
            ),
        }
    ]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=app.config["APP_MODEL"],
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return local_reply(message)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify({
        "name": app.config["APP_NAME"],
        "status": "online",
        "model": app.config["APP_MODEL"],
        "openai_configured": bool(client is not None),
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not message:
        return jsonify({"error": "Debes enviar un mensaje."}), 400

    reply = generate_ai_reply(message, history)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
