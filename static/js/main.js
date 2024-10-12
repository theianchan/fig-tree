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

function generateUniqueId() {
  return "id_" + Math.random().toString(36).substr(2, 9);
}

function getOrCreateUserId() {
  let userId = getCookie("userId");
  if (!userId) {
    userId = generateUniqueId();
    document.cookie = `userId=${userId}; path=/; max-age=${60 * 60 * 24 * 365}`; // 1 year expiry
  }
  return userId;
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function submitName() {
  const name = document.getElementById("name").value;

  fetch("/submit_name", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: name }),
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
    });
}

function commit() {
  fetch("/commit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
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
    });
}

function noCommit() {
  console.log("No commit");
}

function printReceipt() {
  console.log("Print receipt");
}

function updateTimer() {
  const timerElement = document.getElementById("timer");
  if (!timerElement) return;

  const lastStageTime = new Date(timerElement.dataset.lastStage).getTime();
  const currentTime = new Date().getTime();
  const elapsedTime = currentTime - lastStageTime;
  const remainingTime = Math.max(300000 - elapsedTime, 0); // 5 minutes in milliseconds

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

  setTimeout(updateTimer, 1000);
}

window.addEventListener("load", updateTimer);
