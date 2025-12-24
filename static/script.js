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
