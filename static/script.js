
document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('file-list-body');

    // Hàm định dạng kích thước file
    function formatSize(bytes) {
        if (bytes === null || bytes === undefined) return '';
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Hàm định dạng ngày tháng
    function formatDate(isoString) {
        const date = new Date(isoString);
        return date.toLocaleString();
    }

    let counter = 0;

    // Hàm đệ quy để render cây thư mục
    function renderTree(nodes, parentElement, level) {
        nodes.forEach(node => {
            counter++;
            const row = document.createElement('tr');
            const isFolder = node.type === 'Folder';

            row.innerHTML = `
                <td class="col-no">${counter}</td>
                <td class="col-name" style="padding-left: ${level * 20 + 8}px;">
                    <span class="icon">${isFolder ? '&#128193;' : '&#128196;'}</span>
                    ${node.name}
                </td>
                <td class="col-date">${formatDate(node.date_create)}</td>
                <td class="col-type">${node.type}</td>
                <td class="col-size">${formatSize(node.size)}</td>
            `;

            if (isFolder) {
                row.classList.add('folder-row');
                row.dataset.path = node.name; // Dùng để định danh
            }

            parentElement.appendChild(row);

            if (isFolder && node.children && node.children.length > 0) {
                const childrenContainer = document.createElement('tbody');
                childrenContainer.classList.add('hidden');
                parentElement.appendChild(childrenContainer);
                renderTree(node.children, childrenContainer, level + 1);
                
                row.addEventListener('click', (e) => {
                    e.stopPropagation();
                    childrenContainer.classList.toggle('hidden');
                });
            }
        });
    }

    // Lấy dữ liệu và bắt đầu render
    fetch('/api/files')
        .then(response => response.json())
        .then(data => {
            tbody.innerHTML = ''; // Xóa nội dung cũ (nếu có)
            renderTree(data, tbody, 0);
        })
        .catch(error => {
            console.error('Error fetching file data:', error);
            tbody.innerHTML = '<tr><td colspan="5">Error loading files.</td></tr>';
        });
});
