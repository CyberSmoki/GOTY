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

function handleRadioChange(selectedRadio) {
    const gameId = selectedRadio.value;
    const groupName = selectedRadio.name;
    const checked = selectedRadio.checked;

    if (selectedRadio.dataset.picked == "1") {
        selectedRadio.checked = false;
    } else {
        selectedRadio.checked = true;
    }

    selectedRadio.dataset.picked ^= true;

    const voteData = {
        stage: 2,
        gameId: gameId,
        vote: groupName,
    };

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