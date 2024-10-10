function getUserId() {
    return localStorage.getItem('userId');
}

function setUserId(userId) {
    localStorage.setItem('userId', userId);
}

function initSession() {
    fetch('/init', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            setUserId(data.user_id);
            updateContent('Welcome to the Fig Tree! Make your first choice:');
        });
}

function makeChoice(choice) {
    const userId = getUserId();
    fetch(`/choice/${choice}`, {
        method: 'POST',
        headers: { 'X-User-ID': userId }
    })
        .then(response => response.json())
        .then(data => updateContent(data.message, data.age, data.stage));
}

function updateContent(message, age, stage) {
    const content = document.getElementById('content');
    content.innerHTML = `
        <p>${message}</p>
        <p>Your age: ${age}</p>
        <p>Current stage: ${stage}</p>
    `;
    // Add more dynamic content updates here
}

// Initialize session when page loads
if (!getUserId()) {
    initSession();
}

document.addEventListener('DOMContentLoaded', function() {
    if (!getUserId()) {
        initSession();
    }
});
