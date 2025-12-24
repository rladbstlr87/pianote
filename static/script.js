const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const statusContainer = document.getElementById('status-container');
const resultContainer = document.getElementById('result-container');
const downloadLink = document.getElementById('download-link');
const resetBtn = document.getElementById('reset-btn');
const statusText = document.getElementById('status-text');

// Trigger file input
uploadBtn.addEventListener('click', () => fileInput.click());

// Drag and drop handlers
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleUpload(files[0]);
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        handleUpload(fileInput.files[0]);
    }
});

function handleUpload(file) {
    if (!file.type.startsWith('audio/')) {
        alert('오디오 파일만 업로드 가능합니다.');
        return;
    }

    // Show status, hide upload
    dropZone.classList.add('hidden');
    statusContainer.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', file);

    fetch('/transcribe', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                statusContainer.classList.add('hidden');
                resultContainer.classList.remove('hidden');
                downloadLink.href = data.midi_url;
            } else {
                throw new Error(data.error || '변환 실패');
            }
        })
        .catch(error => {
            alert('오류 발생: ' + error.message);
            resetUI();
        });
}

function resetUI() {
    dropZone.classList.remove('hidden');
    statusContainer.classList.add('hidden');
    resultContainer.classList.add('hidden');
    fileInput.value = '';
}

resetBtn.addEventListener('click', resetUI);
