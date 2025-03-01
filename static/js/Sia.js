// Section 1: Get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Section 2: Functions related to Scrolling.

// Add a function to scroll to the last message
function scrollToLastMessage() {
    var chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// Section 3: Sending and Appending Messages

// sendMessage Function
function sendMessage() {
    // Get the message from the input box
    var message = document.getElementById("chat-input").value;

    // If the message is not empty or whitespace
    if (message.trim().length > 0) {
        // Trim the message
        message = message.trim();

        // Clear the input box
        document.getElementById("chat-input").value = "";

        // Now Call the function to append the message to the chat
        appendMessage(message, "user", userName);

        // Scroll to the bottom of the chat
        scrollToLastMessage();

        // Send the message to the server
        $.ajax({
            url: "/sia",
            type: "POST",
            data: {
                text_input: message,
                csrfmiddlewaretoken: getCookie("csrftoken"),
            },
            success: function (json) {

                console.log("Sia Response:", json["response"], typeof(json["response"]))
                // If there is a response from the server
                if (json && json["response"]) {
                    // Now Call the function to append the message to the chat
                    // console.log("Sia Response:", json["response"])
                    appendMessage(json["response"], "assistant", "Sia");

                    scrollToLastMessage();
                }
            },
        });
    }
}

// Modify the appendMessage function
function appendMessage(response, sender, userName) {
    // console.log("Response:", response)

    if (sender === "assistant") {
        var message = response["text"];
        var buttons = response["buttons"];
    } else {
        var message = response;
        var buttons = "";
    }

    // console.log("Message:", message, "Buttons:", buttons)

    var messageElement = document.createElement("div");
    messageElement.className = "chat-message " + sender.toLowerCase();

    var messageHeader = document.createElement("div");
    messageHeader.className = "chat-message-header";
    messageHeader.textContent = userName;
    messageElement.appendChild(messageHeader);
    
    var messageBody = document.createElement("div");
    messageBody.className = "chat-message-body";
    messageBody.textContent = message;
    messageElement.appendChild(messageBody);
    
    if (buttons !== "") {
        var messageButtons = document.createElement("div");
        messageHeader.className = "chat-message-options";
        messageButtons.innerHTML = buttons;
        messageElement.appendChild(messageButtons);
    }

    document.getElementById("chat-messages").appendChild(messageElement);

    // Scroll to the last message after appending a new message
    scrollToLastMessage();
}

// Section 4: Function Call

// Speech to text.
const recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = "en-US";

recognition.onstart = function () {

    // Change the button icon to a stop button
    document.getElementById('mic-button-container').classList.add('active');

    recognition.start();

};

recognition.onend = function () {

    // Change the button icon back to mic
    document.getElementById('mic-button-container').classList.remove('active');

    recognition.stop();

};

recognition.onresult = function (event) {

    var message = event.results[0][0].transcript;

    // Now set the value of the input box to the message
    document.getElementById('chat-input').value = message;
    sendMessage();

};

var chatContainer = document.getElementById('chat-container');

// Create a container element for all the messages
var chatMessages = document.getElementById('chat-messages');

chatContainer.addEventListener("click", function (event) {
    if (event.target.closest("#send-button") || event.target.closest("svg")) {
        sendMessage();
    } else if (event.target.closest("#mic-button")) {
        if (!document.getElementById("mic-button-container").classList.contains("active")) {
            recognition.start();
        } else if (document.getElementById("mic-button-container").classList.contains("active")) {
            recognition.stop();
        }
    } else if (event.target.matches(".sia-option")) {
        // Button text is sent as user message
        document.getElementById('chat-input').value = event.target.textContent;
        sendMessage();
    }
});

// Use a debounce function to delay the execution of the sendMessage function
var debounceTimeout;
chatContainer.addEventListener('keyup', function (event) {
    if (event.target.id === 'chat-input' && event.key === 'Enter') {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(sendMessage, 500);
    }
});

// Call the updateChatMessageStyles function after the page has loaded
window.onload = function () {
    // updateChatMessageStyles();
    scrollToLastMessage();
};

// // Section 5: Delete User Conversation, before closing.
// window.addEventListener("beforeunload", (event) => {
//     // Beacon API
//     const formData = new FormData();
//     formData.append("csrfmiddlewaretoken", getCookie("csrftoken"));

//     navigator.sendBeacon("/delete_user_conversation/", formData);
// });