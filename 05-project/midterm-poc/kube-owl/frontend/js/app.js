/**
 * KubeOps Agent — Ana Uygulama
 * Başlatma, global state, event listener'lar, notification sistemi.
 */

// ═══════════ BAŞLATMA ═══════════

document.addEventListener('DOMContentLoaded', async () => {
    console.log('KubeOps Agent başlatılıyor...');

    // Event listener'ları kur
    initEventListeners();

    // Dosya yükleme alanını başlat
    initFileUpload();

    // Paralel olarak başlangıç verilerini çek
    await Promise.allSettled([
        loadDocuments(),
        loadK8sStatus(),
        loadConfig(),
    ]);

    console.log('KubeOps Agent hazır!');
});

// ═══════════ EVENT LISTENERS ═══════════

function initEventListeners() {
    const chatInput = document.getElementById('chat-input');

    // Enter ile gönderme (Shift+Enter = yeni satır)
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    // Textarea auto-resize
    chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
    });

    // Provider değişikliği
    document.getElementById('provider-select').addEventListener('change', (e) => {
        const provider = e.target.value;
        showNotification(`Provider değiştirildi: ${provider}`, 'info');
    });

    // SSH Modal Açma
    document.getElementById('k8s-settings-btn').addEventListener('click', () => {
        document.getElementById('ssh-modal').classList.add('is-active');
        refreshSshSessionsList();
    });

    // Config Modal Tabs
    const tabs = document.querySelectorAll('#config-tabs li');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('is-active'));
            tab.classList.add('is-active');
            const target = tab.dataset.target;
            document.querySelectorAll('.config-tab-content').forEach(content => {
                content.classList.add('is-hidden');
            });
            document.getElementById(target).classList.remove('is-hidden');
        });
    });

    // Terminal Input Event Listener
    const termInput = document.getElementById('terminal-input');
    if (termInput) {
        termInput.addEventListener('keydown', handleTerminalKeydown);
    }
}

// ═══════════ K8s DURUMU ═══════════

async function loadK8sStatus() {
    const badge = document.getElementById('k8s-status');

    try {
        const status = await getK8sStatus();

        if (status.mode === 'real') {
            badge.className = 'tag kubeops-k8s-badge is-real';
            badge.innerHTML = '<i class="ti ti-circle-filled" style="font-size:0.5rem"></i>&nbsp; Real K8s';
        } else {
            badge.className = 'tag kubeops-k8s-badge is-mock';
            badge.innerHTML = '<i class="ti ti-circle-filled" style="font-size:0.5rem"></i>&nbsp; Mock K8s';
        }
    } catch (error) {
        badge.className = 'tag kubeops-k8s-badge is-mock';
        badge.innerHTML = '<i class="ti ti-circle-filled" style="font-size:0.5rem"></i>&nbsp; Mock K8s';
    }
}

// ═══════════ KONFİGÜRASYON ═══════════

async function loadConfig() {
    try {
        const config = await getConfig();

        // Provider dropdown'u ayarla
        const select = document.getElementById('provider-select');
        if (config.default_provider) {
            select.value = config.default_provider;
        }
    } catch (error) {
        console.warn('Config yüklenemedi:', error);
    }
}

// ═══════════ BİLDİRİM SİSTEMİ ═══════════

/**
 * Bildirim gösterir.
 * @param {string} message — Bildirim mesajı
 * @param {string} type — 'success', 'error', 'info', 'warning'
 * @param {number} duration — Otomatik kapanma süresi (ms)
 */
function showNotification(message, type = 'info', duration = 4000) {
    const container = document.getElementById('notification-container');

    // İkon seç
    let icon;
    switch (type) {
        case 'success': icon = 'ti-check'; break;
        case 'error': icon = 'ti-alert-circle'; break;
        case 'warning': icon = 'ti-alert-triangle'; break;
        default: icon = 'ti-info-circle';
    }

    const notifEl = document.createElement('div');
    notifEl.className = `kubeops-notification ${type}`;
    notifEl.innerHTML = `
        <i class="ti ${icon}"></i>
        <span>${escapeHtml(message)}</span>
    `;

    container.appendChild(notifEl);

    // Otomatik kapanma
    setTimeout(() => {
        notifEl.style.opacity = '0';
        notifEl.style.transform = 'translateX(20px)';
        notifEl.style.transition = 'all 0.3s ease';
        setTimeout(() => notifEl.remove(), 300);
    }, duration);
}

// ═══════════ SSH MODAL MANTIĞI ═══════════

function closeSshModal() {
    document.getElementById('ssh-modal').classList.remove('is-active');
}

function toggleAuthType() {
    const isPassword = document.querySelector('input[name="ssh_auth"]:checked').value === 'password';
    document.getElementById('ssh-pass-field').style.display = isPassword ? 'block' : 'none';
    document.getElementById('ssh-key-field').style.display = !isPassword ? 'block' : 'none';
}

async function refreshSshSessionsList() {
    try {
        const res = await listSshSessions();
        const select = document.getElementById('ssh-session-select');
        
        // Lokal opsiyonu koru
        select.innerHTML = '<option value="">💻 Lokal Çevre (Kubeconfig)</option>';
        
        for (const s of res.sessions) {
            const opt = document.createElement('option');
            opt.value = s.id;
            opt.textContent = `🌐 ${s.name} (${s.username}@${s.host})`;
            select.appendChild(opt);
        }
        
        if (res.active_session_id) {
            select.value = res.active_session_id;
        }
        
        updateK8sBadge(res.active_session_id, res.sessions);
        
    } catch (error) {
        showNotification('Oturum bilgileri alınamadı: ' + error.message, 'error');
    }
}

async function handleSessionChange() {
    const select = document.getElementById('ssh-session-select');
    const sessionId = select.value;
    try {
        await setActiveSshSession(sessionId);
        showNotification(sessionId ? 'Uzak SSH bağlantısı seçildi.' : 'Lokal bağlantıya dönüldü.', 'success');
        refreshSshSessionsList();
    } catch (e) {
        showNotification('Bağlantı seçilemedi: ' + e.message, 'error');
    }
}

async function saveSshSession() {
    const name = document.getElementById('ssh-name').value;
    const host = document.getElementById('ssh-host').value;
    const port = document.getElementById('ssh-port').value;
    const user = document.getElementById('ssh-user').value;
    const authType = document.querySelector('input[name="ssh_auth"]:checked').value;
    const pass = document.getElementById('ssh-pass').value;
    const keyPath = document.getElementById('ssh-key').value;
    
    if (!name || !host || !user) {
        showNotification('Lütfen zorunlu alanları doldurun.', 'warning');
        return;
    }
    
    const sessionData = {
        id: crypto.randomUUID(),
        name, host, port: parseInt(port), username: user, auth_type: authType
    };
    
    if (authType === 'password') sessionData.password = pass;
    else sessionData.key_path = keyPath;
    
    try {
        await addSshSession(sessionData);
        showNotification('SSH oturumu kaydedildi!', 'success');
        document.getElementById('ssh-form').reset();
        refreshSshSessionsList();
    } catch (e) {
        showNotification('Oturum kaydedilemedi: ' + e.message, 'error');
    }
}

function updateK8sBadge(activeSessionId, sessions = []) {
    const icon = document.getElementById('k8s-status-icon');
    const text = document.getElementById('k8s-status-text');
    const btn = document.getElementById('k8s-settings-btn');
    
    if (activeSessionId) {
        const s = sessions.find(x => x.id === activeSessionId);
        btn.className = 'button is-small is-info kubeops-k8s-badge';
        icon.innerHTML = '<i class="ti ti-server-cog"></i>';
        text.innerHTML = `&nbsp; SSH: ${s ? s.name : 'Unknown'}`;
    } else {
        btn.className = 'button is-small is-light kubeops-k8s-badge';
        icon.innerHTML = '<i class="ti ti-device-laptop"></i>';
        text.innerHTML = '&nbsp; Lokal Çevre';
    }
}

// Override loadK8sStatus from init
async function loadK8sStatus() {
    refreshSshSessionsList();
}

// ═══════════ CONFIG MODAL MANTIĞI ═══════════

async function openConfigModal() {
    try {
        const raw = await getRawConfig();
        
        document.getElementById('conf-default-provider').value = raw.default_provider || 'ollama';
        
        // Ollama
        document.getElementById('conf-ollama-url').value = raw.ollama_base_url || '';
        document.getElementById('conf-ollama-model').value = raw.ollama_model || '';
        document.getElementById('conf-ollama-embed').value = raw.ollama_embed_model || '';
        
        // Gemini
        document.getElementById('conf-gemini-key').value = raw.gemini_api_key || '';
        document.getElementById('conf-gemini-model').value = raw.gemini_model || '';
        document.getElementById('conf-gemini-embed').value = raw.gemini_embed_model || '';
        
        // Claude
        document.getElementById('conf-claude-key').value = raw.claude_api_key || '';
        document.getElementById('conf-claude-model').value = raw.claude_model || '';

        // OpenAI
        document.getElementById('conf-openai-key').value = raw.openai_api_key || '';
        document.getElementById('conf-openai-model').value = raw.openai_model || '';
        
        // Ollama Cloud
        document.getElementById('conf-ollama-cloud-url').value = raw.ollama_cloud_url || '';
        document.getElementById('conf-ollama-cloud-model').value = raw.ollama_cloud_model || '';
        
        document.getElementById('config-modal').classList.add('is-active');
    } catch (e) {
        showNotification('Ayarlar getirilemedi: ' + e.message, 'error');
    }
}

function closeConfigModal() {
    document.getElementById('config-modal').classList.remove('is-active');
}

async function saveConfigToBackend() {
    const data = {
        default_provider: document.getElementById('conf-default-provider').value,
        ollama_base_url: document.getElementById('conf-ollama-url').value,
        ollama_model: document.getElementById('conf-ollama-model').value,
        ollama_embed_model: document.getElementById('conf-ollama-embed').value,
        gemini_api_key: document.getElementById('conf-gemini-key').value,
        gemini_model: document.getElementById('conf-gemini-model').value,
        gemini_embed_model: document.getElementById('conf-gemini-embed').value,
        claude_api_key: document.getElementById('conf-claude-key').value,
        claude_model: document.getElementById('conf-claude-model').value,
        openai_api_key: document.getElementById('conf-openai-key').value,
        openai_model: document.getElementById('conf-openai-model').value,
        ollama_cloud_url: document.getElementById('conf-ollama-cloud-url').value,
        ollama_cloud_model: document.getElementById('conf-ollama-cloud-model').value
    };
    
    try {
        await updateConfig(data);
        showNotification('Sistem ayarları başarıyla kaydedildi!', 'success');
        closeConfigModal();
        
        // Güncel ayarları yansıtmak için config'i tekrar yükle
        await loadConfig();
    } catch (e) {
        showNotification('Ayarlar kaydedilemedi: ' + e.message, 'error');
    }
}

// ═══════════ TERMINAL MANTIĞI ═══════════

let terminalHistory = [];
let terminalHistoryIndex = -1;
let isTerminalRunning = false;

function openTerminal() {
    document.getElementById('terminal-modal').classList.add('is-active');
    setTimeout(() => {
        document.getElementById('terminal-input').focus();
    }, 100);
}

function closeTerminal() {
    document.getElementById('terminal-modal').classList.remove('is-active');
}

function appendToTerminal(text, isCommand = false) {
    const outDiv = document.getElementById('terminal-output');
    const newEl = document.createElement('div');
    if (isCommand) {
        newEl.innerHTML = `<span style="color: #66ccff;">$ ${escapeHtml(text)}</span>`;
    } else {
        newEl.textContent = text;
    }
    outDiv.appendChild(newEl);
    outDiv.scrollTop = outDiv.scrollHeight;
}

async function handleTerminalKeydown(e) {
    if (isTerminalRunning) {
        if (e.key === 'Enter') e.preventDefault();
        return;
    }
    
    if (e.key === 'Enter') {
        const cmd = e.target.value.trim();
        if (cmd) {
            if (terminalHistory[terminalHistory.length - 1] !== cmd) {
                terminalHistory.push(cmd);
            }
            terminalHistoryIndex = terminalHistory.length;
            
            e.target.value = '';
            appendToTerminal(cmd, true);
            
            if (cmd === 'clear') {
                document.getElementById('terminal-output').innerHTML = '';
                return;
            }
            
            isTerminalRunning = true;
            document.getElementById('terminal-input').placeholder = "çalışıyor...";
            
            try {
                const res = await executeTerminalCommand(cmd);
                if (res.output) {
                    appendToTerminal(res.output);
                }
            } catch (err) {
                appendToTerminal(`Error: ${err.message}`);
                console.error(err);
            } finally {
                isTerminalRunning = false;
                document.getElementById('terminal-input').placeholder = "komut girin...";
                document.getElementById('terminal-input').focus();
            }
        }
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (terminalHistoryIndex > 0) {
            terminalHistoryIndex--;
            e.target.value = terminalHistory[terminalHistoryIndex];
        }
    } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (terminalHistoryIndex < terminalHistory.length - 1) {
            terminalHistoryIndex++;
            e.target.value = terminalHistory[terminalHistoryIndex];
        } else {
            terminalHistoryIndex = terminalHistory.length;
            e.target.value = '';
        }
    }
}
