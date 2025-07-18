// script.js

let tasks = [];
let currentIndex = 0;

const leftElem = document.getElementById("left");
const rightElem = document.getElementById("right");
const keywordElem = document.getElementById("keyword");
const sentenceElem = document.getElementById("sentence");
const tagsContainer = document.querySelector(".tags");
const inputElem = document.querySelector("input");
const buttons = document.querySelectorAll(".ControlSection button");
const answerBox = document.getElementById("answerBox");
const answerText = document.getElementById("answerText");

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

  // Hide answer box on new question
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
  // Show the first answer (or all answers joined by "; ")
  answerText.textContent = Array.isArray(task.answers) ? task.answers.join(" ; ") : task.answers;
  answerBox.style.display = "block";
}

// Attach listeners
buttons[0].addEventListener("click", checkAnswer);      // Evaluate
buttons[1].addEventListener("click", showAnswer);       // Show Answer
buttons[2].addEventListener("click", nextTask);         // Next

window.addEventListener("DOMContentLoaded", loadTasks);