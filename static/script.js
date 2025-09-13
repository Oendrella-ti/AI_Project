async function sendMessage() {
    const input = document.getElementById('user-input').value;
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
    });

    const data = await response.json();
    const chatBox = document.getElementById('chat-box');

    chatBox.innerHTML += `<p><strong>You:</strong> ${input}</p>`;
    chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
    document.getElementById('user-input').value = '';
}
