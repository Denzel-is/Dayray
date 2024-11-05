

function toggleChat() {
    const chatContainer = document.getElementById("chatContainer");
    if (chatContainer.style.display === "none" || chatContainer.style.display === "") {
        chatContainer.style.display = "flex"; // Открыть чат
    } else {
        chatContainer.style.display = "none"; // Закрыть чат
    }
}

function sendMessage() {
    const chatBody = document.getElementById("chatBody");
    const chatInput = document.getElementById("chatInput");
    const message = chatInput.value.trim();

    if (message) {
        // Добавляем сообщение пользователя в чат
        const userMessage = document.createElement("p");
        userMessage.textContent = "Вы: " + message;
        chatBody.appendChild(userMessage);

        // Очистка поля ввода
        chatInput.value = "";

        // Здесь отправьте сообщение на сервер
        fetch("/check_api", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Добавляем ответ AI в чат
            const aiMessage = document.createElement("p");
            aiMessage.textContent = "AI: " + data.reply;
            chatBody.appendChild(aiMessage);
        })
        .catch(error => console.error("Ошибка:", error));
    }
}


function checkApi() {
    const statusDiv = document.getElementById("status");
    statusDiv.textContent = "Проверка подключения...";

    fetch('/check_api')
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                statusDiv.textContent = data.message;
                statusDiv.style.color = "green";
            } else {
                statusDiv.textContent = data.message || "Ошибка при подключении";
                statusDiv.style.color = "red";
            }
        })
        .catch(error => {
            statusDiv.textContent = "Ошибка: " + error;
            statusDiv.style.color = "red";
        });
}
