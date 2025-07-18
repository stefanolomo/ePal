// script.js

let tasks = [];
let currentIndex = 0;
let userPassword = "";

const leftElem = document.getElementById("left");
const rightElem = document.getElementById("right");
const keywordElem = document.getElementById("keyword");
const sentenceElem = document.getElementById("sentence");
const tagsContainer = document.querySelector(".tags");
const inputElem = document.querySelector("input");
const buttons = document.querySelectorAll(".ControlSection button");

// --- CryptoJS para descifrado por campo ---
function decryptField(enc, password) {
  try {
    return CryptoJS.AES.decrypt(enc, password).toString(CryptoJS.enc.Utf8);
  } catch (e) {
    return "";
  }
}
function decryptArray(arr, password) {
  return arr.map(x => decryptField(x, password));
}
function decryptTask(task, password) {
  return {
    ...task,
    original: decryptField(task.original, password),
    keyword: decryptField(task.keyword, password),
    answers: decryptArray(task.answers, password),
    prompt: {
      left: decryptField(task.prompt.left, password),
      right: decryptField(task.prompt.right, password)
    },
    tags: task.tags ? decryptArray(task.tags, password) : []
  };
}

// --- Solicita contraseña y carga tasks_encrypted.json ---
async function requirePasswordAndLoad() {
  // Asegúrate de incluir CryptoJS en tu HTML:
  // <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
  while (true) {
    userPassword = prompt("Ingrese la contraseña para acceder:");
    if (!userPassword) {
      document.body.innerHTML = "<h2>Acceso cancelado.</h2>";
      return;
    }
    try {
      const res = await fetch("./questions/tasks_encrypted.json");
      const encryptedTasks = await res.json();
      // Probar descifrado de la primera pregunta
      const prueba = decryptField(encryptedTasks[0].original, userPassword);
      if (!prueba) throw new Error();
      tasks = encryptedTasks.map(t => decryptTask(t, userPassword));
      renderTask(0);
      break;
    } catch (e) {
      alert("Contraseña incorrecta o archivo corrupto.");
    }
  }
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
  (task.tags || []).forEach(tag => {
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

window.addEventListener("DOMContentLoaded", requirePasswordAndLoad);