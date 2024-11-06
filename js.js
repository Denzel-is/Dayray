
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchInput').addEventListener('input', function(e) {
        var searchTerm = e.target.value.toLowerCase();
        var products = document.querySelectorAll('.product');

        products.forEach(function(product) {
            var productName = product.querySelector('.product-title').textContent.toLowerCase();
            if (productName.includes(searchTerm)) {
                product.style.display = '';
            } else {
                product.style.display = 'none';
            }
        });
    });
});

function goBack() {
    if (document.referrer.indexOf(window.location.hostname) !== -1) {
        history.back();
    } else {
        window.location.href = '/'; // Перенаправление на главную страницу, если предыдущей страницы нет
    }
}


function redirectTo(url) {
    window.location.href = url;
}

        
        
        function scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }

        function scrollToProducts() {
            const productsSection = document.querySelector(".products");
            productsSection.scrollIntoView({
                behavior: "smooth"
            });
        }

        function scrollToContacts() {
            const footer = document.querySelector("footer");
            footer.scrollIntoView({
                behavior: "smooth"
            });
        }


        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
        
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        function toggleChat() {
            const chatBox = document.getElementById("chatBox");
            chatBox.style.display = (chatBox.style.display === "none" || chatBox.style.display === "") ? "flex" : "none";
        }
    
        function sendMessage() {
            const chatBody = document.getElementById("chatBody");
            const chatInput = document.getElementById("chatInput");
            const message = chatInput.value.trim();
    
            if (message) {
                appendMessage("Вы", message, "user-message");
    
                chatInput.value = ""; 

                const loadingId = appendMessage("AI", "Печатает...", "ai-message");
   
                fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    removeMessage(loadingId);
                    appendMessage("AI", data.reply, "ai-message");
                })
                .catch(error => {
                    console.error("Ошибка:", error);
                    removeMessage(loadingId);
                    appendMessage("AI", "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз.", "ai-message error");
                });
            }
        }
    
        function appendMessage(sender, text, className) {
            const chatBody = document.getElementById("chatBody");
            const messageElement = document.createElement("div");
            messageElement.className = `message ${className}`;
            messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
            chatBody.appendChild(messageElement);
            chatBody.scrollTop = chatBody.scrollHeight;
            return messageElement.id = `msg-${Date.now()}`;  // Возвращаем ID сообщения
        }
    
        function removeMessage(id) {
            const message = document.getElementById(id);
            if (message) {
                message.remove();
            }
        }