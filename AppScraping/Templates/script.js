document.addEventListener('DOMContentLoaded', () => {
    const terminalOutput = document.getElementById('terminal-output');

    const ws = new WebSocket('ws://localhost:8765');

    ws.onmessage = function(event) {
        terminalOutput.innerText += event.data + '\n';
        terminalOutput.scrollTop = terminalOutput.scrollHeight; // Scroll to the bottom
    };

    document.getElementById('command-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const commandInput = document.getElementById('command-input');
        const command = commandInput.value;

        // Envoyer la commande au serveur (si nécessaire)
        ws.send(command);

        // Effacer le champ de commande
        commandInput.value = '';
    });
});
