function normalizeText(text) {
    return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

function filterContent() {
    let input = normalizeText(document.getElementById('search-input').value);
    let contentItems = document.querySelectorAll('.content-item');
    let cancelButton = document.getElementById('cancel-search');

    if (input) {
        cancelButton.style.display = 'inline';
        cancelButton.style.display = 'none';
    }

    contentItems.forEach(item => {
        let name = normalizeText(item.querySelector('.card-title').textContent);
        let description = normalizeText(item.querySelector('.card-text').textContent);

        if (name.includes(input) || description.includes(input)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

function cancelSearch() {
    document.getElementById('search-input').value = '';
    filterContent();
}