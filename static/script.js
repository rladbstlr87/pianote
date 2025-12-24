const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const statusContainer = document.getElementById('status-container');
const resultContainer = document.getElementById('result-container');
const downloadLink = document.getElementById('download-link');
const resetBtn = document.getElementById('reset-btn');
const statusText = document.getElementById('status-text');

uploadBtn.addEventListener('click', () => fileInput.click());

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
    if (files.length > 0) handleUpload(files[0]);
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) handleUpload(fileInput.files[0]);
});

function handleUpload(file) {
    const isAudio = file.type.startsWith('audio/');
    const isVideo = file.type.startsWith('video/');

    if (!isAudio && !isVideo) {
        alert('지원되는 오디오 또는 동영상 파일만 업로드 가능합니다.');
        return;
    }
    dropZone.classList.add('hidden');
    statusContainer.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', file);

    fetch('/transcribe', { method: 'POST', body: formData })
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
