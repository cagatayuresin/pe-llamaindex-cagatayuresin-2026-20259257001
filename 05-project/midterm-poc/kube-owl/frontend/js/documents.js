/**
 * KubeOps Agent — Doküman Yönetimi UI
 * Doküman listesi, yükleme ve silme işlemleri.
 */

/**
 * Doküman listesini backend'den çekip sidebar'da gösterir.
 */
async function loadDocuments() {
    const listEl = document.getElementById('document-list');
    const emptyEl = document.getElementById('doc-empty');

    try {
        const data = await listDocuments();
        const docs = data.documents || [];

        // Mevcut doküman öğelerini temizle (empty hariç)
        listEl.querySelectorAll('.kubeops-doc-item').forEach(el => el.remove());

        if (docs.length === 0) {
            emptyEl.style.display = 'block';
            return;
        }

        emptyEl.style.display = 'none';

        docs.forEach(doc => {
            const item = createDocumentItem(doc);
            listEl.appendChild(item);
        });

    } catch (error) {
        console.error('Doküman listesi yüklenemedi:', error);
    }
}

/**
 * Tek bir doküman satırı oluşturur.
 */
function createDocumentItem(doc) {
    const item = document.createElement('div');
    item.className = 'kubeops-doc-item';
    item.dataset.docId = doc.id;

    // Dosya tipine göre ikon
    const iconClass = getFileIcon(doc.file_type || doc.filename);
    const fileSize = formatFileSize(doc.file_size || 0);
    const isEditable = ['.md', '.txt'].some(ext => (doc.filename || '').toLowerCase().endsWith(ext));

    item.innerHTML = `
        <i class="ti ${iconClass} kubeops-doc-icon"></i>
        <div class="kubeops-doc-info">
            <div class="kubeops-doc-name" title="${doc.filename}">${doc.filename}</div>
            <div class="kubeops-doc-meta">${doc.chunks || 0} chunk &bull; ${fileSize}</div>
        </div>
        <div class="kubeops-doc-actions">
            ${isEditable ? `<button class="kubeops-doc-edit" title="Düzenle" onclick="openDocEditModal('${doc.id}', '${doc.filename}')"><i class="ti ti-edit"></i></button>` : ''}
            <button class="kubeops-doc-delete" title="Sil" onclick="handleDeleteDocument('${doc.id}', '${doc.filename}')">
                <i class="ti ti-trash"></i>
            </button>
        </div>
    `;

    return item;
}

/**
 * Dosya tipine göre Tabler ikon class'ı döndürür.
 */
function getFileIcon(fileType) {
    if (!fileType) return 'ti-file-text';
    const type = fileType.toLowerCase().replace('.', '');
    switch (type) {
        case 'md': return 'ti-markdown';
        case 'pdf': return 'ti-file-type-pdf';
        case 'txt': return 'ti-file-text';
        default: return 'ti-file';
    }
}

/**
 * Dosya boyutunu okunabilir formata çevirir.
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

/**
 * Doküman silme işlemi.
 */
async function handleDeleteDocument(docId, filename) {
    if (!confirm(`"${filename}" dokümanını silmek istediğinize emin misiniz?`)) {
        return;
    }

    try {
        await deleteDocument(docId);
        showNotification(`"${filename}" silindi`, 'success');
        await loadDocuments();
    } catch (error) {
        showNotification(`Silme hatası: ${error.message}`, 'error');
    }
}

/**
 * Doküman editör modalını açar.
 */
let currentEditDocId = null;

async function openDocEditModal(docId, filename) {
    try {
        const response = await getDocumentContent(docId);
        document.getElementById('doc-edit-filename').textContent = filename;
        document.getElementById('doc-edit-textarea').value = response.content;
        currentEditDocId = docId;
        document.getElementById('document-edit-modal').classList.add('is-active');
    } catch (error) {
        showNotification(`Doküman okunamadı: ${error.message}`, 'error');
    }
}

function closeDocEditModal() {
    document.getElementById('document-edit-modal').classList.remove('is-active');
    currentEditDocId = null;
    document.getElementById('doc-edit-textarea').value = '';
}

async function saveDocEdit() {
    if (!currentEditDocId) return;
    
    const btn = document.getElementById('doc-save-btn');
    const content = document.getElementById('doc-edit-textarea').value;
    
    btn.classList.add('is-loading');
    try {
        await updateDocumentContent(currentEditDocId, content);
        showNotification('Doküman güncellendi ve RAG indexi yenilendi.', 'success');
        closeDocEditModal();
        await loadDocuments(); // Chunk sayısını vb. güncellemek için
    } catch (error) {
        showNotification(`Kaydetme hatası: ${error.message}`, 'error');
    } finally {
        btn.classList.remove('is-loading');
    }
}

/**
 * Dosya yükleme alanını başlatır (click + drag-drop).
 */
function initFileUpload() {
    const dropzone = document.getElementById('upload-dropzone');
    const fileInput = document.getElementById('file-input');

    // Click to upload
    dropzone.addEventListener('click', () => {
        fileInput.click();
    });

    // File selected
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
            fileInput.value = ''; // Reset
        }
    });

    // Drag & Drop
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
}

/**
 * Dosya yükleme işlemini gerçekleştirir.
 */
async function handleFileUpload(file) {
    const progressEl = document.getElementById('upload-progress');
    const statusEl = document.getElementById('upload-status');
    const dropzone = document.getElementById('upload-dropzone');

    // Dosya tipi kontrolü (frontend tarafı)
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'md', 'txt'].includes(ext)) {
        showNotification('Desteklenmeyen dosya formatı. Sadece .pdf, .md, .txt kabul edilir.', 'error');
        return;
    }

    // Boyut kontrolü
    if (file.size > 10 * 1024 * 1024) {
        showNotification('Dosya boyutu 10MB\'ı aşıyor.', 'error');
        return;
    }

    // UI güncelle
    dropzone.style.display = 'none';
    progressEl.style.display = 'block';
    statusEl.textContent = `"${file.name}" yükleniyor ve indexleniyor...`;

    try {
        const provider = document.getElementById('provider-select').value;
        const result = await uploadDocument(file, provider);

        showNotification(
            `"${result.filename}" başarıyla yüklendi (${result.chunks} chunk)`,
            'success'
        );

        await loadDocuments();

    } catch (error) {
        showNotification(`Yükleme hatası: ${error.message}`, 'error');
    } finally {
        dropzone.style.display = '';
        progressEl.style.display = 'none';
    }
}
