function addTurn() {
    const turnDiv = document.createElement('div');
    turnDiv.classList.add('turn');

    const userLabel = document.createElement('label');
    userLabel.textContent = 'User Prompt:';
    const userTextarea = document.createElement('textarea');
    userTextarea.name = 'user_prompt[]';
    userTextarea.rows = 3;
    userTextarea.cols = 50;

    const assistantLabel = document.createElement('label');
    assistantLabel.textContent = 'Assistant Response:';
    const assistantTextarea = document.createElement('textarea');
    assistantTextarea.name = 'assistant_response[]';
    assistantTextarea.rows = 3;
    assistantTextarea.cols = 50;

    const weightLabel = document.createElement('label');
    weightLabel.textContent = 'Assistant Message Weight (0 or 1):';
    const weightInput = document.createElement('input');
    weightInput.type = 'number';
    weightInput.name = 'assistant_weight[]';
    weightInput.value = 1; // Default weight is 1
    weightInput.min = 0;
    weightInput.max = 1;

    turnDiv.appendChild(userLabel);
    turnDiv.appendChild(document.createElement('br'));
    turnDiv.appendChild(userTextarea);
    turnDiv.appendChild(document.createElement('br'));
    turnDiv.appendChild(assistantLabel);
    turnDiv.appendChild(document.createElement('br'));
    turnDiv.appendChild(assistantTextarea);
    turnDiv.appendChild(document.createElement('br'));
    turnDiv.appendChild(weightLabel);
    turnDiv.appendChild(document.createElement('br'));
    turnDiv.appendChild(weightInput);
    turnDiv.appendChild(document.createElement('br'));

    document.getElementById('turns').appendChild(turnDiv);
}

function clearTurns() {
    const turnsDiv = document.getElementById('turns');
    while (turnsDiv.children.length > 1) {
        turnsDiv.removeChild(turnsDiv.lastChild);
    }
}

function formatEntry() {
    const formData = new FormData(document.getElementById('entryForm'));

    fetch('/format', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const orderedData = {
            messages: data.messages.map(message => ({
                role: message.role,
                content: message.content,
                ...(message.weight !== undefined ? { weight: message.weight } : {})
            }))
        };
        
        entries.push(orderedData);
        document.getElementById('formattedEntries').textContent = JSON.stringify(entries, null, 2);
    });
}

function downloadFile() {
    const blob = new Blob(entries.map(entry => JSON.stringify(entry) + '\n'), { type: 'application/jsonl' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'conversations.jsonl';
    a.click();
    URL.revokeObjectURL(url);
}

let entries = [];

// Automatically add the first user-assistant turn when the page loads
window.onload = function() {
    addTurn();
};
