// script.js

// 1) Тоггл мобильного меню
function toggleMenu() {
    const navList = document.querySelector('.nav-list');
    if (navList) {
      navList.classList.toggle('open');
    }
  }
  
  // 2) Чат: открыть/закрыть
  function toggleChat() {
    const chatBox = document.getElementById("chatBox");
    if (!chatBox) return;
    chatBox.style.display = (chatBox.style.display === "none" || chatBox.style.display === "") 
      ? "flex" 
      : "none";
  }
  
  // 3) Чат: отправить сообщение
  function sendMessage() {
    const chatBody = document.getElementById("chatBody");
    const chatInput = document.getElementById("chatInput");
    if (!chatBody || !chatInput) return;
  
    const message = chatInput.value.trim();
    if (!message) return;
  
    const userMsgId = appendMessage("Вы", message, "user-message");
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
  
  // Добавить сообщение в чат
  function appendMessage(sender, text, className) {
    const chatBody = document.getElementById("chatBody");
    if (!chatBody) return "";
  
    const messageElement = document.createElement("div");
    messageElement.className = `message ${className}`;
    messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
  
    chatBody.appendChild(messageElement);
    chatBody.scrollTop = chatBody.scrollHeight;
  
    const id = `msg-${Date.now()}`;
    messageElement.id = id;
    return id;
  }
  
  // Удалить сообщение (например, «Печатает...»)
  function removeMessage(id) {
    const msg = document.getElementById(id);
    if (msg) {
      msg.remove();
    }
  }
  
  // 4) Google Maps
  function initMap() {
    const almaty = { lat: 43.238949, lng: 76.889709 };
    const mapEl = document.getElementById("map");
    if (!mapEl) return;
  
    const map = new google.maps.Map(mapEl, {
      center: almaty,
      zoom: 12
    });
  
    new google.maps.Marker({
      position: almaty,
      map: map,
      title: "Алматы",
    });
  }
  