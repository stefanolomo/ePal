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

// Extra elements for dark mode and instruction toggle
const darkToggle = document.getElementById("toggle-dark");
const toggleBtn = document.getElementById("toggle-instruction");
const instruction = toggleBtn?.closest("h4");

function resetFeedback() {
  inputElem.classList.remove("correct", "incorrect");
  inputElem.style.background = "";
  inputElem.style.color = "";
}

async function loadTasks() {
  const res = await fetch("./questions/tasks.json");
  tasks = await res.json();
  renderTask(0);
}

function renderTask(index) {
  currentIndex = index;
  const task = tasks[index];
  leftElem.textContent = task.prompt.left;
  rightElem.textContent = task.prompt.right;
  keywordElem.textContent = task.keyword;
  sentenceElem.textContent = task.original;
  inputElem.value = "";
  resetFeedback();

  // Cancel any pending answer timeout
  if (answerTimeoutId !== null) {
    clearTimeout(answerTimeoutId);
    answerTimeoutId = null;
  }

  // Update tags
  const tagElements = Array.from(tagsContainer.querySelectorAll("p"));
  tagElements.forEach(p => {
    if (p.querySelector("h3")) return; // Skip the header
    p.remove();
  });
  task.tags.forEach(tag => {
    const p = document.createElement("p");
    p.textContent = tag;
    tagsContainer.appendChild(p);
  });

  // Hide answer box
  answerBox.style.display = "none";
  answerText.textContent = "";
}


function checkAnswer() {
  const task = tasks[currentIndex];
  const userAnswer = inputElem.value.trim().toLowerCase();
  const correct = task.answers.some(ans => userAnswer === ans.trim().toLowerCase());
  inputElem.classList.remove("correct", "incorrect");

  if (correct) {
    inputElem.classList.add("correct");
    inputElem.style.background = "#24e956";
    inputElem.style.color = "#fff";
    setTimeout(() => {
      resetFeedback();
      nextTask();
    }, 400);
  } else {
    inputElem.classList.add("incorrect");
    inputElem.style.background = "#ff3357";
    inputElem.style.color = "#fff";
    setTimeout(() => {
      resetFeedback();
    }, 400);
  }
}

function nextTask() {
  let nextIndex = (currentIndex + 1) % tasks.length;
  renderTask(nextIndex);
}

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

  // Cancel previous timeout if any
  if (answerTimeoutId !== null) {
    clearTimeout(answerTimeoutId);
  }

  // Hide after 5 seconds
  answerTimeoutId = setTimeout(() => {
    answerBox.style.display = "none";
    answerText.textContent = "";
    answerTimeoutId = null;
  }, 5000);
}

// Attach listeners
buttons[0].addEventListener("click", checkAnswer);      // Evaluate
buttons[1].addEventListener("click", showAnswer);       // Show Answer
buttons[2].addEventListener("click", nextTask);         // Next

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

window.addEventListener("DOMContentLoaded", loadTasks);