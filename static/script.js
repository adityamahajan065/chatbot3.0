const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
});

clearBtn.addEventListener("click", clearChat);

function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => typeWriter("bot", data.response));
}

function appendMessage(sender, text) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function typeWriter(sender, text) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    chatBox.appendChild(div);

    let i = 0;
    const speed = 20;

    function type() {
        if (i < text.length) {
            div.innerText += text.charAt(i);
            i++;
            chatBox.scrollTop = chatBox.scrollHeight;
            setTimeout(type, speed);
        } else {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    type();
}

function clearChat() {
    chatBox.innerHTML = "";
}
