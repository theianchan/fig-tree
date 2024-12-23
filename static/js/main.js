const text = `I saw my life branching out before me like the green fig tree in the story.

From the tip of every branch, like a fat purple fig, a wonderful future beckoned and winked. One fig was a husband and a happy home and children, and another fig was a famous poet and another fig was a brilliant professor, and another fig was Ee Gee, the amazing editor, and another fig was Europe and Africa and South America, and another fig was Constantin and Socrates and Attila and a pack of other lovers with queer names and offbeat professions, and another fig was an Olympic lady crew champion, and beyond and above these figs were many more figs I couldn't quite make out.

I saw myself sitting in the crotch of this fig tree, starving to death, just because I couldn't make up my mind which of the figs I would choose. I wanted each and every one of them, but choosing one meant losing all the rest, and, as I sat there, unable to decide, the figs began to wrinkle and go black, and, one by one, they plopped to the ground at my feet.`;

let timerTimeout;

function repeatText() {
  const backgroundText = document.querySelector(".background-text");
  const repeatCount = Math.ceil(window.innerHeight / 300) + 1; 
  // Adjust 300 based on your font size and line height
  backgroundText.innerText = (text + "\n\n").repeat(repeatCount);
}

function submitName(currentOption) {
  const submitButton = document.getElementById('submit');
  submitButton.disabled = true;
  submitButton.classList.add('disabled');

  const name = document.getElementById("name").value;

  fetch("/submit_name", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: name, current_option: currentOption }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Success:", data);
      window.location.reload();
    })
    .catch((error) => {
      console.error("Error:", error);
      submitButton.disabled = false;
      submitButton.classList.remove('disabled');
    });
}

function initializeWindow() {
  const windowId = Date.now().toString();
  localStorage.setItem("activeWindowId", windowId);

  setInterval(() => {
    if (localStorage.getItem("activeWindowId") !== windowId) {
      deactivateWindow();
    }
  }, 1000);
}

function deactivateWindow() {
  clearTimeout(timerTimeout);

  const buttons = document.querySelectorAll("button");
  buttons.forEach((button) => {
    button.disabled = true;
    button.style.opacity = "0.5";
  });

  const timerCard = document.querySelector(".card.dark");
  if (timerCard) {
    timerCard.style.display = "none";
  }
}

function scrollToCurrentState() {
  const currentState = document.getElementById("currentState");
  if (currentState) {
    currentState.scrollIntoView({ behavior: "smooth" });
  }
}

function handleCommit(committed) {
  const commitButton = document.getElementById('commit');
  commitButton.disabled = true;
  commitButton.classList.add('disabled');

  fetch("/handle_commit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ committed: committed }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Success:", data);
      window.location.href = "/";
    })
    .catch((error) => {
      console.error("Error:", error);
      commitButton.disabled = false;
      commitButton.classList.remove('disabled');
    });
}

function commit() {
  handleCommit(true);
}

function noCommit() {
  handleCommit(false);
}

function printReceipt() {
  console.log("Print receipt");
}

function updateTimer() {
  const timerElement = document.getElementById("timer");
  if (!timerElement) return;

  const playerAge = parseInt(timerElement.dataset.age);
  if (playerAge >= 77) return;

  const timeStageStarted = new Date(timerElement.dataset.timeStageStarted).getTime();
  const currentTime =
    new Date().getTime() + new Date().getTimezoneOffset() * 60000;
  const elapsedTime = currentTime - timeStageStarted;
  const remainingTime = Math.max(5 * 60 * 1000 - elapsedTime, 0); // 5 minutes in milliseconds

  if (remainingTime === 0) {
    timerElement.textContent = "00:00";
    noCommit();
    return;
  }

  const minutes = Math.floor(remainingTime / 60000);
  const seconds = Math.floor((remainingTime % 60000) / 1000);
  timerElement.textContent = `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}`;

  timerTimeout = setTimeout(updateTimer, 1000);
}

function clearUrlParameters() {
  if (window.history.replaceState) {
    var newUrl =
      window.location.protocol +
      "//" +
      window.location.host +
      window.location.pathname;
    window.history.replaceState({ path: newUrl }, "", newUrl);
  }
}

window.addEventListener("load", repeatText);
window.addEventListener("load", updateTimer);
window.addEventListener("load", initializeWindow);
window.addEventListener("load", clearUrlParameters);
window.addEventListener("load", scrollToCurrentState);

window.addEventListener("resize", repeatText);