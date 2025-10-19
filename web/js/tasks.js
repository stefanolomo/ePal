// script.js

let tasks = [];
let currentIndex = 0;
let answerTimeoutId = null;

const leftElem = document.getElementById("left");
const rightElem = document.getElementById("right");
const keywordElem = document.getElementById("keyword");
const sentenceElem = document.getElementById("sentence");
const tagsContainer = document.querySelector(".tags");
const inputElem = document.querySelector("input");
const buttons = document.querySelectorAll(".ControlSection button");
const answerBox = document.getElementById("answerBox");
const answerText = document.getElementById("answerText");
const tagSelect = document.getElementById("tagSelect");
const startTagBtn = document.getElementById("startTagPractice");

// Extra elements for dark mode and instruction toggle
const darkToggle = document.getElementById("toggle-dark");
const toggleBtn = document.getElementById("toggle-instruction");
const instruction = toggleBtn?.closest("h4");

let correctCount = 0;
let incorrectCount = 0;
let filteredTasks = [];
let isFiltering = false;
let hasSeenAnswer = false;

const statsElem = document.getElementById("stats");
const keywordSelect = document.getElementById("keywordSelect");
const startKeywordBtn = document.getElementById("startKeywordPractice");

function resetFeedback() {
  inputElem.classList.remove("correct", "incorrect");
  inputElem.style.background = "";
  inputElem.style.color = "";
}

function updateTagDropdown() {
  tagSelect.innerHTML = '<option value="all">All</option>';

  const tagCounts = {};

  tasks.forEach((task) => {
    if (!Array.isArray(task.tags) || task.tags.length === 0) {
      tagCounts["no tag"] = (tagCounts["no tag"] || 0) + 1;
    } else {
      task.tags.forEach((tag) => {
        tagCounts[tag] = (tagCounts[tag] || 0) + 1;
      });
    }
  });

  Object.entries(tagCounts)
    .sort(([a], [b]) => a.localeCompare(b))
    .forEach(([tag, count]) => {
      const option = document.createElement("option");
      option.value = tag;
      option.textContent = `${tag} (${count})`;
      tagSelect.appendChild(option);
    });
}

async function loadTasks() {
  const res = await fetch("./questions/tasks.json");
  tasks = await res.json();
  updateKeywordDropdown();
  updateTagDropdown(); // <- aquí
  filteredTasks = tasks;
  renderTask(0);
}

function updateKeywordDropdown() {
  // Limpiar el dropdown excepto la opción "all"
  keywordSelect.innerHTML = '<option value="all">All</option>';

  // Contar cuántas tareas tiene cada keyword
  const keywordCounts = {};
  tasks.forEach((task) => {
    keywordCounts[task.keyword] = (keywordCounts[task.keyword] || 0) + 1;
  });

  // Ordenar keywords y agregarlas al <select>
  Object.entries(keywordCounts)
    .sort()
    .forEach(([kw, count]) => {
      const option = document.createElement("option");
      option.value = kw;
      option.textContent = `${kw} (${count})`;
      keywordSelect.appendChild(option);
    });
}

function updateStats() {
  const total = correctCount + incorrectCount;
  const accuracy = total ? ((correctCount / total) * 100).toFixed(1) : 0;
  statsElem.textContent = `Correct: ${correctCount} | Incorrect: ${incorrectCount} | Accuracy: ${accuracy}%`;
}

function renderTask(index) {
  currentIndex = index;
  const task = filteredTasks[index];
  if (!task) return;

  leftElem.textContent = task.prompt.left;
  rightElem.textContent = task.prompt.right;
  keywordElem.textContent = task.keyword;
  sentenceElem.textContent = task.original;
  inputElem.value = "";
  resetFeedback();

  // Clean tags
  const tagElements = Array.from(tagsContainer.querySelectorAll("p"));
  tagElements.forEach((p) => {
    if (p.querySelector("h3")) return;
    p.remove();
  });

  if (Array.isArray(task.tags)) {
    task.tags.forEach((tag) => {
      const p = document.createElement("p");
      p.textContent = tag;
      tagsContainer.appendChild(p);
    });
  }

  answerBox.style.display = "none";
  answerText.textContent = "";

  if (answerTimeoutId !== null) {
    clearTimeout(answerTimeoutId);
    answerTimeoutId = null;
  }

  hasSeenAnswer = false;
}

function checkAnswer() {
  if (hasSeenAnswer) {
    alert("You already saw the answer. Try the next task!");
    return;
  }

  const task = filteredTasks[currentIndex];
  const userAnswer = inputElem.value.trim().toLowerCase();
  const correct = task.answers.some(
    (ans) => userAnswer === ans.trim().toLowerCase()
  );
  inputElem.classList.remove("correct", "incorrect");

  if (correct) {
    inputElem.classList.add("correct");
    inputElem.style.background = "#24e956";
    inputElem.style.color = "#fff";
    correctCount++;
    updateStats();
    setTimeout(() => {
      resetFeedback();
      nextTask();
    }, 400);
  } else {
    inputElem.classList.add("incorrect");
    inputElem.style.background = "#ff3357";
    inputElem.style.color = "#fff";
    incorrectCount++;
    updateStats();
    setTimeout(() => {
      resetFeedback();
    }, 400);
  }
}

function nextTask() {
  resetFeedback();
  let nextIndex = (currentIndex + 1) % filteredTasks.length;
  renderTask(nextIndex);
}

startKeywordBtn.addEventListener("click", () => {
  const selected = keywordSelect.value;
  isFiltering = selected !== "all";

  filteredTasks = isFiltering
    ? tasks.filter((t) => t.keyword === selected)
    : tasks;

  if (filteredTasks.length === 0) {
    alert("No tasks available for this keyword.");
    return;
  }

  correctCount = 0;
  incorrectCount = 0;
  updateStats();
  renderTask(0);
});

function randomTask() {
  let randIndex = Math.floor(Math.random() * tasks.length);
  renderTask(randIndex);
}

function showAnswer() {
  const task = tasks[currentIndex];
  answerText.textContent = Array.isArray(task.answers)
    ? task.answers.join(" ; ")
    : task.answers;
  answerBox.style.display = "block";

  hasSeenAnswer = true; // <-- IMPORTANTE

  if (answerTimeoutId !== null) {
    clearTimeout(answerTimeoutId);
  }

  answerTimeoutId = setTimeout(() => {
    answerBox.style.display = "none";
    answerText.textContent = "";
    answerTimeoutId = null;
  }, 5000);
}

// Attach listeners
buttons[0].addEventListener("click", checkAnswer); // Evaluate
buttons[1].addEventListener("click", showAnswer); // Show Answer
buttons[2].addEventListener("click", nextTask); // Next

// Dark mode toggle
if (darkToggle) {
  if (localStorage.getItem("dark-mode") === "true") {
    document.body.classList.add("dark");
    darkToggle.textContent = "☀️ Light Mode";
  }

  darkToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    const isDark = document.body.classList.contains("dark");
    localStorage.setItem("dark-mode", isDark);
    darkToggle.textContent = isDark ? "☀️ Light Mode" : "🌙 Dark Mode";
  });
}

// Instruction toggle
if (toggleBtn && instruction) {
  toggleBtn.addEventListener("click", () => {
    if (instruction.style.display === "none") {
      instruction.style.display = "";
      toggleBtn.textContent = "Shut up!";
    } else {
      instruction.style.display = "none";
      toggleBtn.textContent = "speak";
      toggleBtn.style.fontSize = "0.5rem";
    }
  });
}

startTagBtn.addEventListener("click", () => {
  const selectedTag = tagSelect.value;
  isFiltering = selectedTag !== "all";

  filteredTasks = isFiltering
    ? tasks.filter((t) =>
        !t.tags || t.tags.length === 0
          ? selectedTag === "no tag"
          : t.tags.includes(selectedTag)
      )
    : tasks;

  if (filteredTasks.length === 0) {
    alert("No tasks available for this tag.");
    return;
  }

  correctCount = 0;
  incorrectCount = 0;
  updateStats();
  renderTask(0);
});

window.addEventListener("DOMContentLoaded", loadTasks);
