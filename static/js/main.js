const text = `I saw my life branching out before me like the green fig tree in the story.

From the tip of every branch, like a fat purple fig, a wonderful future beckoned and winked. One fig was a husband and a happy home and children, and another fig was a famous poet and another fig was a brilliant professor, and another fig was Ee Gee, the amazing editor, and another fig was Europe and Africa and South America, and another fig was Constantin and Socrates and Attila and a pack of other lovers with queer names and offbeat professions, and another fig was an Olympic lady crew champion, and beyond and above these figs were many more figs I couldn't quite make out.

I saw myself sitting in the crotch of this fig tree, starving to death, just because I couldn't make up my mind which of the figs I would choose. I wanted each and every one of them, but choosing one meant losing all the rest, and, as I sat there, unable to decide, the figs began to wrinkle and go black, and, one by one, they plopped to the ground at my feet.`;

function repeatText() {
  const backgroundText = document.querySelector(".background-text");
  const repeatCount = Math.ceil(window.innerHeight / 300) + 1; // Adjust 300 based on your font size and line height
  backgroundText.innerText = (text + "\n\n").repeat(repeatCount);
}

window.addEventListener("load", repeatText);
window.addEventListener("resize", repeatText);

function submitName() {
  const name = document.getElementById("name").value;
  if (name) {
    // Here you can add logic to handle the name submission
    console.log("Name submitted:", name);
    // You might want to redirect to the next page or start the game here
  }
}

function getUserId() {
  return localStorage.getItem("userId");
}

function setUserId(userId) {
  localStorage.setItem("userId", userId);
}

function initSession() {
  fetch("/init", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      setUserId(data.user_id);
      updateContent("Welcome to the Fig Tree! Make your first choice:");
    });
}

function makeChoice(choice) {
  const userId = getUserId();
  fetch(`/choice/${choice}`, {
    method: "POST",
    headers: { "X-User-ID": userId },
  })
    .then((response) => response.json())
    .then((data) => updateContent(data.message, data.age, data.stage));
}

function updateContent(message, age, stage) {
  const content = document.getElementById("content");
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

document.addEventListener("DOMContentLoaded", function () {
  if (!getUserId()) {
    initSession();
  }
});
