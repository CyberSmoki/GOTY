let sortDirections = [];

function sortTable(columnIndex, tableName = "sortableTable") {
    const table = document.getElementById(tableName);
    const rows = Array.from(table.rows).slice(1);

    if (sortDirections[columnIndex] === undefined) {
        sortDirections[columnIndex] = true;
    }

    const isAscending = sortDirections[columnIndex];
    const isDateColumn = columnIndex === 4;
    const isNumeric = !isNaN(rows[0].cells[columnIndex].innerText.trim()) && !isDateColumn;

    const sortedRows = rows.sort((a, b) => {
        const aText = a.cells[columnIndex].innerText.trim();
        const bText = b.cells[columnIndex].innerText.trim();

        if (isDateColumn) {
            return isAscending
                ? new Date(aText) - new Date(bText)
                : new Date(bText) - new Date(aText);
        }

        if (isNumeric) {
            return isAscending
                ? parseFloat(aText) - parseFloat(bText)
                : parseFloat(bText) - parseFloat(aText);
        }

        return isAscending
            ? aText.localeCompare(bText)
            : bText.localeCompare(aText);
    });

    sortDirections[columnIndex] = !isAscending;

    const tbody = table.querySelector("tbody");
    tbody.innerHTML = "";
    sortedRows.forEach(row => tbody.appendChild(row));

    updateSortArrows(columnIndex, isAscending, tableName);
}

function updateSortArrows(activeColumnIndex, isAscending, tableName) {
    document.querySelectorAll(`table#${tableName} .sort-arrow`).forEach(arrow => {
        arrow.classList.remove("asc", "desc");
    });

    const arrow = document.getElementById(`${tableName}-arrow-${activeColumnIndex}`);
    if (arrow) {
        arrow.classList.add(isAscending ? "asc" : "desc");
    }
}

function filterTable() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const table = document.getElementById('sortableTable');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let match = false;

        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell && cell.innerText.toLowerCase().includes(filter)) {
                match = true;
                break;
            }
        }

        rows[i].style.display = match ? '' : 'none';
    }
}
