let body = document.querySelector("body");
let button = document.querySelector("#switch"); // Tugmani tanlash
let isToggled = false;

button.onclick = () => {
    isToggled = !isToggled; // Holatni o'zgartirish
    body.style.setProperty("--value", isToggled ? "gray" : "white");
};

  // Xabarlarni JavaScript-ga o'tkazish
  

  // Xabarlarni konsolga chiqarish
  document.addEventListener('DOMContentLoaded', function() {
    const messageContainer = document.getElementById('message-container');
    if (!messageContainer) return;

    const messages = messageContainer.querySelectorAll('.message-alert');

    // Function to animate message appearance
    function showMessages() {
        messages.forEach((message, index) => {
            setTimeout(() => {
                message.classList.add('show');
            }, index * 200); // Stagger the appearance of multiple messages
        });
    }

    // Function to animate message dismissal
    function hideMessage(message) {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            message.remove();
            if (messageContainer.children.length === 0) {
                messageContainer.remove();
            }
        }, 500);
    }

    // Show messages with animation
    showMessages();

    // Add click event listeners to close buttons
    messageContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-close')) {
            e.preventDefault();
            const message = e.target.closest('.alert');
            hideMessage(message);
        }
    });

    // Auto-dismiss messages after 5 seconds
    setTimeout(() => {
        messages.forEach(message => {
            hideMessage(message);
        });
    }, 2000);
});