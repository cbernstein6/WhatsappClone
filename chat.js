document.addEventListener('DOMContentLoaded', function() {
    const userList = document.querySelector('.user-list');
    const chatList = document.querySelector('.chat-list');
    const chatMessages = document.querySelector('.chat-messages');
    const messageInput = document.querySelector('.chat-footer input');
    const sendButton = document.querySelector('.chat-footer button');

    // Placeholder for chat data
    const chats = {
        'jane': [
            { from: 'Jane', text: 'Hi there!' },
            // More messages...
        ],
        // More chats...
    };

    document.getElementById('logout').addEventListener('click', function() {
      window.location.href = '/signin';
    });


    // Function to render the chat messages
    function renderMessages(chatId) {
        const messages = chats[chatId];
        chatMessages.innerHTML = ''; // Clear previous messages
        messages.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.textContent = message.text;
            chatMessages.appendChild(messageDiv);
        });
    }

    // Function to add a new message
    function addMessage(chatId, text) {
        chats[chatId].push({ from: 'You', text: text });
        renderMessages(chatId);
    }

    // Event listener for the send button
    sendButton.addEventListener('click', function() {
        const text = messageInput.value.trim();
        if(text) {
            addMessage('jane', text); // Assuming 'jane' is the current chat
            messageInput.value = ''; // Clear input field
        }
    });

    // Initialize chat list (this would be fetched from the server in a real app)
    const chatIds = Object.keys(chats);
    chatIds.forEach(chatId => {
        const li = document.createElement('li');
        li.textContent = chatId; // You would use user names in a real app
        li.addEventListener('click', function() {
            renderMessages(chatId);
        });
        chatList.appendChild(li);
    });




    // Load initial chat
    renderMessages('jane');


});


