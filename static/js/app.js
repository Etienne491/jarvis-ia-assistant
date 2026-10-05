const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const statusText = document.getElementById('statusText');
const modelText = document.getElementById('modelText');
const appName = document.getElementById('appName');
const speakBtn = document.getElementById('speakBtn');
const microphoneBtn = document.getElementById('microphoneBtn');

let lastAssistantReply = '';

function appendMessage(role, text) {
  const msg = document.createElement('div');
  msg.className = `message ${role}`;

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;

  msg.appendChild(bubble);
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function loadStatus() {
  try {
    const response = await fetch('/api/status');
    const data = await response.json();
    appName.textContent = data.name || 'JARVIS';
    statusText.textContent = data.status === 'online' ? 'En línea' : 'Desconectado';
    modelText.textContent = data.model || 'Local';
  } catch (error) {
    statusText.textContent = 'Sin conexión';
    modelText.textContent = 'Local';
  }
}

async function sendMessage(message) {
  if (!message.trim()) return;

  appendMessage('user', message);
  messageInput.value = '';

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    if (data.error) {
      appendMessage('bot', data.error);
      return;
    }

    const reply = data.reply || 'No tengo respuesta disponible ahora mismo.';
    lastAssistantReply = reply;
    appendMessage('bot', reply);
  } catch (error) {
    appendMessage('bot', 'No puedo contactar con el servidor en este momento.');
  }
}

chatForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  sendMessage(message);
});

speakBtn.addEventListener('click', () => {
  if (!lastAssistantReply) {
    return;
  }

  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(lastAssistantReply);
    utterance.lang = 'es-ES';
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  }
});

microphoneBtn.addEventListener('click', () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    appendMessage('bot', 'Tu navegador no soporta reconocimiento de voz.');
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'es-ES';
  recognition.interimResults = false;
  recognition.start();

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    messageInput.value = transcript;
    sendMessage(transcript);
  };

  recognition.onerror = () => {
    appendMessage('bot', 'No se pudo usar el micrófono.');
  };
});

loadStatus();
