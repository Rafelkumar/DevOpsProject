function uploadText() {
    const fileInput = document.getElementById('fileInput');
    fileInput.click();
    fileInput.onchange = function() {
        const file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('inputText').value = e.target.result;
        };
        reader.readAsText(file);
    };
}

function summarizeText() {
    const inputText = document.getElementById('inputText').value;
    const summaryLength = document.getElementById('summaryLength').value;

    if (!inputText || !summaryLength) {
        alert('Please enter both text and summary length.');
        return;
    }

    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: inputText, length: summaryLength })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('summaryText').innerText = data.summary;
        document.getElementById('senti-title').innerText = data.sentiment;
    })
    .catch(error => console.error('Error:', error));
}

function copySummary() {
    const summaryText = document.getElementById('summaryText').innerText;
    navigator.clipboard.writeText(summaryText).then(() => {
        alert('Summary copied to clipboard');
    }).catch(err => {
        alert('Failed to copy summary');
    });
}

function resetSummarizer() {
    document.getElementById('inputText').value = '';
    document.getElementById('summaryLength').value = '';
    document.getElementById('summaryText').innerText = '';
    document.getElementById('senti-title').innerText = '';
}
