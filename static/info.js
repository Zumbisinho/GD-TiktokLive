const socket = io();

// Fila de mensagens
const messageQueue = [];
let isShowing = false;

function ShowText(type, UserName) {
    // Adiciona o pedido à fila
    messageQueue.push({ type, UserName });

    // Se não tiver nada sendo mostrado, inicia o processamento da fila
    if (!isShowing) {
        processQueue();
    }
}

function processQueue() {
    // Se a fila estiver vazia, termina
    if (messageQueue.length === 0) {
        isShowing = false;
        return;
    }

    isShowing = true;

    // Pega o primeiro item da fila
    const { type, UserName } = messageQueue.shift();

    const list = document.getElementById('List');
    const elemento = list.querySelector(`.${type}`);

    elemento.style.display = 'flex';
    elemento.querySelector('span').innerText = UserName;

    // Tempo que o texto fica visível
    setTimeout(() => {
        elemento.style.display = 'none';

        // Espera um pequeno intervalo antes de mostrar o próximo (opcional)
        setTimeout(processQueue, 200);
    }, 3950);
}
socket.on("RunningRequest", (data) => {

    ShowText('Running',data)
});
socket.on("InvalidRequest", (data) => {
    ShowText('Error',data)
});
socket.on("AddLevel", (data) => {
    const DataOBJ = data
    ShowText('Success',DataOBJ.userName)
});
//Stanley me aqjuda com esse teste unitário

