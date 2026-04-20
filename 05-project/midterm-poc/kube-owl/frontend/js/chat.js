/**
 * KubeOps Agent — Sohbet UI
 * Mesaj gönderme, ajan adımlarını render etme, loading durumu.
 */

let isAgentThinking = false;

/**
 * Kullanıcı mesajını chat alanına ekler.
 */
function addUserMessage(message) {
    const container = document.getElementById('chat-messages');
    hideWelcome();

    const msgEl = document.createElement('div');
    msgEl.className = 'kubeops-message user';
    msgEl.innerHTML = `
        <div class="kubeops-message-avatar">
            <i class="ti ti-user"></i>
        </div>
        <div class="kubeops-message-content">${escapeHtml(message)}</div>
    `;

    container.appendChild(msgEl);
    scrollToBottom();
}

/**
 * Ajan yanıtını chat alanına ekler.
 */
function addAgentMessage(data) {
    const container = document.getElementById('chat-messages');
    removeThinking();

    const msgEl = document.createElement('div');
    msgEl.className = 'kubeops-message agent';

    // Steps bölümünü oluştur
    let stepsHtml = '';
    if (data.steps && data.steps.length > 0) {
        const stepsListHtml = data.steps.map(step => renderStep(step)).join('');
        stepsHtml = `
            <div class="kubeops-steps-container">
                <button class="kubeops-steps-toggle" onclick="toggleSteps(this)">
                    <i class="ti ti-brain"></i>
                    Düşünce Adımları (${data.steps.length} adım)
                    <i class="ti ti-chevron-down chevron"></i>
                </button>
                <div class="kubeops-steps-list">
                    ${stepsListHtml}
                </div>
            </div>
        `;
    }

    // Sources bölümü
    let sourcesHtml = '';
    if (data.sources && data.sources.length > 0) {
        const tags = data.sources.map(s => `<span class="kubeops-source-tag"><i class="ti ti-file-text"></i> ${escapeHtml(s)}</span>`).join('');
        sourcesHtml = `
            <div class="kubeops-sources">
                <div class="kubeops-sources-label">Kaynaklar</div>
                ${tags}
            </div>
        `;
    }

    // Duration
    let durationHtml = '';
    if (data.duration_ms) {
        const seconds = (data.duration_ms / 1000).toFixed(1);
        durationHtml = `
            <div class="kubeops-duration">
                <i class="ti ti-clock"></i>
                ${seconds}s &bull; ${data.model || data.provider}
            </div>
        `;
    }

    // Ana cevap metnini formatla
    const formattedAnswer = formatAnswerText(data.answer);

    msgEl.innerHTML = `
        <div class="kubeops-message-avatar">
            <i class="ti ti-brand-kubernetes"></i>
        </div>
        <div class="kubeops-message-content">
            ${stepsHtml}
            <div class="kubeops-answer-text content" style="color: #e0e0e0; font-size: 0.95rem;">${formattedAnswer}</div>
            ${sourcesHtml}
            ${durationHtml}
        </div>
    `;

    container.appendChild(msgEl);
    scrollToBottom();
}

/**
 * Ajan hata mesajını ekler.
 */
function addErrorMessage(errorText) {
    const container = document.getElementById('chat-messages');
    removeThinking();

    const msgEl = document.createElement('div');
    msgEl.className = 'kubeops-message agent';
    msgEl.innerHTML = `
        <div class="kubeops-message-avatar" style="border-color: var(--accent-red); color: var(--accent-red);">
            <i class="ti ti-alert-circle"></i>
        </div>
        <div class="kubeops-message-content" style="border-color: var(--accent-red);">
            <strong>Hata:</strong> ${escapeHtml(errorText)}
        </div>
    `;

    container.appendChild(msgEl);
    scrollToBottom();
}

/**
 * Bir adımı HTML olarak render eder.
 */
function renderStep(step) {
    const type = step.type || 'action';
    let icon, label, content;

    switch (type) {
        case 'thought':
            icon = 'ti-bulb';
            label = 'Düşünce';
            content = escapeHtml(step.content || '');
            break;
        case 'action':
            icon = 'ti-tool';
            label = `Araç: ${escapeHtml(step.tool || 'unknown')}`;
            const inputText = step.input ? `<div><strong>Girdi:</strong> ${escapeHtml(step.input)}</div>` : '';
            const outputText = step.output ? `<pre>${escapeHtml(step.output)}</pre>` : '';
            content = `${inputText}${outputText}`;
            break;
        case 'observation':
            icon = 'ti-eye';
            label = 'Gözlem';
            content = step.content ? `<pre>${escapeHtml(step.content)}</pre>` : '';
            break;
        default:
            icon = 'ti-info-circle';
            label = type;
            content = escapeHtml(step.content || JSON.stringify(step));
    }

    return `
        <div class="kubeops-step ${type}">
            <div class="kubeops-step-icon">
                <i class="ti ${icon}"></i>
            </div>
            <div class="kubeops-step-content">
                <div class="kubeops-step-label">${label}</div>
                <div class="kubeops-step-text">${content}</div>
            </div>
        </div>
    `;
}

/**
 * Düşünce adımlarını açıp kapatır.
 */
function toggleSteps(button) {
    button.classList.toggle('open');
    const list = button.nextElementSibling;
    list.classList.toggle('visible');
}

/**
 * Ajan düşünürken loading animasyonu gösterir.
 */
function showThinking() {
    const container = document.getElementById('chat-messages');

    const thinkingEl = document.createElement('div');
    thinkingEl.className = 'kubeops-message agent';
    thinkingEl.id = 'thinking-indicator';
    thinkingEl.innerHTML = `
        <div class="kubeops-message-avatar">
            <i class="ti ti-brand-kubernetes"></i>
        </div>
        <div class="kubeops-thinking">
            <div class="kubeops-thinking-dots">
                <span></span><span></span><span></span>
            </div>
            <span class="kubeops-thinking-text">Düşünüyorum...</span>
        </div>
    `;

    container.appendChild(thinkingEl);
    scrollToBottom();
}

/**
 * Loading animasyonunu kaldırır.
 */
function removeThinking() {
    const el = document.getElementById('thinking-indicator');
    if (el) el.remove();
}

/**
 * Hoş geldin mesajını gizler.
 */
function hideWelcome() {
    const el = document.getElementById('welcome-message');
    if (el) el.style.display = 'none';
}

/**
 * Sohbet alanını en alta kaydırır.
 */
function scrollToBottom() {
    const container = document.getElementById('chat-messages');
    // Smooth scroll
    requestAnimationFrame(() => {
        container.scrollTop = container.scrollHeight;
    });
}

/**
 * Cevap metnini markdown olarak formatlar.
 */
function formatAnswerText(text) {
    if (!text) return '';
    
    try {
        if (typeof marked !== 'undefined') {
            return marked.parse(text);
        } else {
            console.warn("Marked.js bulunamadı.");
            return escapeHtml(text).replace(/\n/g, '<br>');
        }
    } catch (e) {
        console.error("Markdown parsing error:", e);
        return escapeHtml(text).replace(/\n/g, '<br>');
    }
}

/**
 * HTML özel karakterlerini escape eder (XSS koruması).
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Mesaj gönderme işlemi.
 */
async function handleSend() {
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-button');
    const message = input.value.trim();

    if (!message || isAgentThinking) return;

    // UI güncelle
    isAgentThinking = true;
    input.value = '';
    input.style.height = 'auto';
    sendBtn.disabled = true;

    // Kullanıcı mesajını ekle
    addUserMessage(message);

    // Loading göster
    showThinking();

    try {
        const provider = document.getElementById('provider-select').value;
        const result = await queryAgent(message, provider);

        // Ajan yanıtını ekle
        addAgentMessage(result);

    } catch (error) {
        addErrorMessage(error.message);
    } finally {
        isAgentThinking = false;
        sendBtn.disabled = false;
        input.focus();
    }
}

/**
 * Öneri butonlarından mesaj gönderir.
 */
function sendSuggestion(message) {
    const input = document.getElementById('chat-input');
    input.value = message;
    handleSend();
}
