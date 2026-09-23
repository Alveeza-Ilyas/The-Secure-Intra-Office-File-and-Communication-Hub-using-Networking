// Modern Dashboard Interactivity & Micro-Interactions

document.addEventListener('DOMContentLoaded', () => {
    // 1. File Upload Dropzone & Selection Handling
    const fileInput = document.getElementById('fileInput');
    const dropzone = document.getElementById('dropzone');
    const filePreviewChip = document.getElementById('filePreviewChip');
    const chipFileName = document.getElementById('chipFileName');
    const chipFileSize = document.getElementById('chipFileSize');
    const uploadSubmitBtn = document.getElementById('uploadSubmitBtn');

    if (fileInput && dropzone) {
        function displaySelectedFile(file) {
            if (!file) return;
            chipFileName.textContent = file.name;
            const sizeFormatted = file.size > 1024 * 1024 
                ? (file.size / (1024 * 1024)).toFixed(2) + ' MB'
                : (file.size / 1024).toFixed(1) + ' KB';
            chipFileSize.textContent = sizeFormatted;
            filePreviewChip.style.display = 'block';
            uploadSubmitBtn.disabled = false;
        }

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                displaySelectedFile(fileInput.files[0]);
            }
        });

        const clearFileBtn = document.getElementById('clearFileBtn');
        if (clearFileBtn) {
            clearFileBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                fileInput.value = '';
                filePreviewChip.style.display = 'none';
                uploadSubmitBtn.disabled = true;
            });
        }

        // Drag & Drop event handling
        ['dragenter', 'dragover'].forEach(name => {
            dropzone.addEventListener(name, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(name => {
            dropzone.addEventListener(name, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropzone.classList.remove('dragover');
            });
        });

        dropzone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            if (dt && dt.files.length > 0) {
                fileInput.files = dt.files;
                displaySelectedFile(dt.files[0]);
            }
        });
    }

    // 2. Instant Table Search & Filter
    const searchInput = document.getElementById('fileSearchInput');
    const tableBody = document.getElementById('filesTableBody');
    const filterStatusText = document.getElementById('filterStatusText');

    if (searchInput && tableBody) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase().trim();
            const rows = tableBody.querySelectorAll('tr.file-row');
            let matchCount = 0;

            rows.forEach(row => {
                const name = (row.getAttribute('data-filename') || '').toLowerCase();
                const author = (row.getAttribute('data-uploader') || '').toLowerCase();

                if (name.includes(term) || author.includes(term)) {
                    row.style.display = '';
                    matchCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            if (filterStatusText) {
                filterStatusText.textContent = term 
                    ? `Found ${matchCount} of ${rows.length} files` 
                    : `Showing all ${rows.length} items`;
            }
        });
    }
});

// 3. Smooth Toast Notification Function
function showToast(message) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast-pill';
    toast.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12"/>
        </svg>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px) scale(0.95)';
        toast.style.transition = 'all 0.25s ease';
        setTimeout(() => toast.remove(), 250);
    }, 2500);
}

// 4. Copy Download Link with Clipboard API
function copyDownloadLink(btn, relativePath) {
    const fullUrl = window.location.origin + relativePath;
    navigator.clipboard.writeText(fullUrl).then(() => {
        showToast('Download link copied to clipboard!');
    }).catch(() => {
        prompt('Copy file link:', fullUrl);
    });
}
