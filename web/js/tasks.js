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
  inputElem.classList.remove("correct", "incorrect");

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
}

function checkAnswer() {
  const task = tasks[currentIndex];
  const userAnswer = inputElem.value.trim().toLowerCase();
  const correct = task.answers.some(ans => userAnswer === ans.trim().toLowerCase());
  inputElem.classList.remove("correct", "incorrect");
  inputElem.classList.add(correct ? "correct" : "incorrect");
  if (correct) {
    setTimeout(() => {
      nextTask();
    }, 800);
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

// Attach listeners
buttons[0].addEventListener("click", checkAnswer);      // Evaluate
buttons[1].addEventListener("click", randomTask);        // Random
buttons[2].addEventListener("click", nextTask);          // Next

window.addEventListener("DOMContentLoaded", loadTasks);
