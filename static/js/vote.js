let sortDirections = [];

function sortTable(columnIndex) {
    const table = document.getElementById("sortableTable");
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

    updateSortArrows(columnIndex, isAscending);
}

function updateSortArrows(activeColumnIndex, isAscending) {
    document.querySelectorAll(".sort-arrow").forEach(arrow => {
        arrow.classList.remove("asc", "desc");
    });

    const arrow = document.getElementById(`arrow-${activeColumnIndex}`);
    if (arrow) {
        arrow.classList.add(isAscending ? "asc" : "desc");
    }
}

function handleCheckboxChange(selectedCheckbox, value) {
    const groupName = selectedCheckbox.name;
    const checkboxes = document.getElementsByName(groupName);

    const voteData = {
        stage: 1,
        gameId: selectedCheckbox.name,
        vote: Number(value)
    };

    checkboxes.forEach(checkbox => {
        if (Number(checkbox.value) !== value) { 
            checkbox.checked = false;
        }
    });
    
    if(!selectedCheckbox.checked){
        const emptyVoteCheckbox = document.querySelector(`input[name="${groupName}"][value="0"]`);
        emptyVoteCheckbox.checked = true;
        voteData.vote = 0;
    }

    sendVote(voteData)
        .then(result => {
            console.log('Vote sent:', voteData, result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function getVoteValue(groupName){
    const checkboxes = document.getElementsByName(groupName);

    let voteValue = 0;
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) { 
            voteValue = checkbox.value;
        }
    });
    return voteValue;
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

async function sendVote(voteData) {
    try {
        const response = await fetch('/app/vote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(voteData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        return result;
    } catch (error) {
        throw error;
    }
}