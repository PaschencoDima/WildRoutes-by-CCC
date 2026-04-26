const STORAGE_KEY = 'wildroutes_chat_history';

document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
});

function setMessage(text) {
    document.getElementById('userMessage').value = text;
    sendMessage();
}

function sendMessage() {
    const input = document.getElementById('userMessage');
    const text = input.value.trim();

    if (text) {
        addMessageToDisplay('user', text);
        saveMessageToStorage('user', text);

        input.value = '';

        setTimeout(() => {
            const botResponse = "Я зафиксировал ваш вопрос про '" + text + "'. Ищу лучшие маршруты...";
            addMessageToDisplay('bot', botResponse);
            saveMessageToStorage('bot', botResponse);
        }, 600);
    }
}

function addMessageToDisplay(role, text) {
    const container = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');

    const isBot = role === 'bot';
    messageDiv.className = `d-flex ${isBot ? 'justify-content-start' : 'justify-content-end'} mb-3`;

    messageDiv.innerHTML = `
        <div class="message-wrapper" style="max-width: 80%;">
            <div class="p-3 rounded-4 ${isBot ? 'bg-panel border text-white' : 'bg-accent text-dark fw-bold'}"
                 style="border-bottom-${isBot ? 'left' : 'right'}-radius: 4px !important;">
                <small class="d-block mb-1 opacity-75" style="font-size: 0.7rem;">
                    <i class="fas ${isBot ? 'fa-robot' : 'fa-user'} me-1"></i>
                    ${isBot ? 'WILDROUTES AI' : 'ВЫ'}
                </small>
                ${text}
            </div>
        </div>
    `;

    container.appendChild(messageDiv);
    container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
}

function saveMessageToStorage(role, text) {
    let history = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    history.push({ role, text });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
}

function loadHistory() {
    const history = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    const container = document.getElementById('chatMessages');
    container.innerHTML = '';

    if (history.length === 0) {
        const hello = "Привет! 👋 Я AI-помощник WildRoutes. Готов помочь с выбором путешествия!";
        addMessageToDisplay('bot', hello);
    } else {
        history.forEach(msg => {
            addMessageToDisplay(msg.role, msg.text);
        });
    }
}

function clearChat() {
    if (confirm('Очистить историю переписки?')) {
        localStorage.removeItem(STORAGE_KEY);
        loadHistory();
    }
}