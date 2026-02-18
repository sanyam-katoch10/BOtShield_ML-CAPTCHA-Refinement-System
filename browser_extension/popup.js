/* ══════════════════════════════════════════════════════════════════════════════
   BotShield Extension — Popup Logic
   ══════════════════════════════════════════════════════════════════════════════ */

const API_BASE = "http://localhost:8000";

// ── DOM Elements ──
const statusEl = document.getElementById("status");
const statusText = document.getElementById("status-text");
const tabs = document.querySelectorAll(".tab");
const tabContents = document.querySelectorAll(".tab-content");

// Generator
const difficultySelect = document.getElementById("difficulty");
const generateBtn = document.getElementById("generate-btn");
const generateResult = document.getElementById("generate-result");
const captchaImg = document.getElementById("captcha-img");
const captchaText = document.getElementById("captcha-text");
const captchaDiff = document.getElementById("captcha-diff");
const captchaConf = document.getElementById("captcha-conf");

// Analyzer
const uploadArea = document.getElementById("upload-area");
const fileInput = document.getElementById("file-input");
const analyzeResult = document.getElementById("analyze-result");
const analyzeImg = document.getElementById("analyze-img");
const analyzeText = document.getElementById("analyze-text");
const analyzeDiff = document.getElementById("analyze-diff");
const analyzeConf = document.getElementById("analyze-conf");


// ══════════════════════════════════════════════════════════════════════════════
//  HEALTH CHECK
// ══════════════════════════════════════════════════════════════════════════════

async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
        if (res.ok) {
            statusEl.className = "status online";
            statusText.textContent = "Online";
        } else {
            throw new Error("Not OK");
        }
    } catch {
        statusEl.className = "status offline";
        statusText.textContent = "Offline";
    }
}

checkHealth();
setInterval(checkHealth, 10000);


// ══════════════════════════════════════════════════════════════════════════════
//  TAB SWITCHING
// ══════════════════════════════════════════════════════════════════════════════

tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("active"));
        tabContents.forEach(tc => tc.classList.remove("active"));
        tab.classList.add("active");
        document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
    });
});


// ══════════════════════════════════════════════════════════════════════════════
//  GENERATE CAPTCHA
// ══════════════════════════════════════════════════════════════════════════════

generateBtn.addEventListener("click", async () => {
    const btnText = generateBtn.querySelector(".btn-text");
    const btnLoader = generateBtn.querySelector(".btn-loader");

    btnText.style.display = "none";
    btnLoader.style.display = "inline";
    generateBtn.disabled = true;
    generateResult.style.display = "none";

    try {
        const res = await fetch(`${API_BASE}/generate?difficulty=${difficultySelect.value}`);
        if (!res.ok) throw new Error(`Server error: ${res.status}`);

        const data = await res.json();

        captchaImg.src = `data:image/png;base64,${data.image}`;
        captchaText.textContent = data.text;

        captchaDiff.textContent = data.difficulty.toUpperCase();
        captchaDiff.className = `result-value diff-${data.difficulty}`;

        captchaConf.textContent = (data.confidence * 100).toFixed(1) + "%";

        generateResult.style.display = "block";
    } catch (err) {
        showError("generate-result", err.message);
    } finally {
        btnText.style.display = "inline";
        btnLoader.style.display = "none";
        generateBtn.disabled = false;
    }
});


// ══════════════════════════════════════════════════════════════════════════════
//  ANALYZE IMAGE
// ══════════════════════════════════════════════════════════════════════════════

uploadArea.addEventListener("click", () => fileInput.click());

uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
    if (e.dataTransfer.files.length) {
        analyzeFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
        analyzeFile(fileInput.files[0]);
    }
});

async function analyzeFile(file) {
    analyzeResult.style.display = "none";

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => { analyzeImg.src = e.target.result; };
    reader.readAsDataURL(file);

    try {
        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch(`${API_BASE}/predict`, {
            method: "POST",
            body: formData,
        });
        if (!res.ok) throw new Error(`Server error: ${res.status}`);

        const data = await res.json();

        analyzeText.textContent = data.text || "—";
        analyzeDiff.textContent = data.difficulty.toUpperCase();
        analyzeDiff.className = `result-value diff-${data.difficulty}`;
        analyzeConf.textContent = (data.confidence * 100).toFixed(1) + "%";

        analyzeResult.style.display = "block";
    } catch (err) {
        showError("analyze-result", err.message);
    }
}


// ══════════════════════════════════════════════════════════════════════════════
//  HELPERS
// ══════════════════════════════════════════════════════════════════════════════

function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="error-msg">❌ ${message}<br><small>Make sure the API server is running: <code>uvicorn api:app</code></small></div>`;
    container.style.display = "block";
}
