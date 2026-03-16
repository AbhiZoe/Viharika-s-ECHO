const conversation = document.getElementById("conversation");
const commandForm = document.getElementById("commandForm");
const commandInput = document.getElementById("commandInput");
const statusText = document.getElementById("statusText");
const micBtn = document.getElementById("micBtn");
const micBtnLabel = document.getElementById("micBtnLabel");
const micSupport = document.getElementById("micSupport");
const clearBtn = document.getElementById("clearBtn");
const waveform = document.getElementById("waveform");
const thinking = document.getElementById("thinking");
const settingsBtn = document.getElementById("settingsBtn");
const closeSettingsBtn = document.getElementById("closeSettingsBtn");
const settingsModal = document.getElementById("settingsModal");
const sttMode = document.getElementById("sttMode");
const ttsMode = document.getElementById("ttsMode");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening = false;
let isProcessing = false;
let keepListening = false;

const settings = {
    sttMode: localStorage.getItem("echo.sttMode") || "browser",
    ttsMode: localStorage.getItem("echo.ttsMode") || "browser"
};

sttMode.value = settings.sttMode;
ttsMode.value = settings.ttsMode;

addMessage("Assistant", "Hello. Echo Mind is online and ready.");
setStatus("Ready");

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    micSupport.textContent = "Mic supported";

    recognition.onstart = () => {
        isListening = true;
        updateMicButton();
        setStatus("Listening");
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript.trim();
        commandInput.value = transcript;
        submitMessage(transcript);
    };

    recognition.onerror = () => {
        isListening = false;
        updateMicButton();
        setStatus("Idle");
        addMessage("Assistant", "Microphone recognition failed. Try again.");
    };

    recognition.onend = () => {
        if (keepListening) {
            try {
                recognition.start();
                return;
            } catch (error) {
                keepListening = false;
            }
        }
        isListening = false;
        updateMicButton();
        if (statusText.textContent === "Listening") {
            setStatus("Idle");
        }
    };
} else {
    micSupport.textContent = "Mic not supported in this browser";
}

commandForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = commandInput.value.trim();
    submitMessage(message);
});

micBtn.addEventListener("click", async () => {
    if (isProcessing) {
        return;
    }

    if (settings.sttMode === "backend") {
        if (isListening) {
            keepListening = false;
            setStatus("Idle");
            return;
        }

        keepListening = true;
        await listenWithBackendLoop();
        return;
    }

    if (!recognition) {
        addMessage("Assistant", "Browser speech recognition is unavailable.");
        return;
    }

    if (isListening) {
        keepListening = false;
        recognition.stop();
        return;
    }

    keepListening = true;
    recognition.start();
});

clearBtn.addEventListener("click", async () => {
    if (!window.confirm("Clear conversation transcript and memory?")) {
        return;
    }

    conversation.innerHTML = "";
    await fetch("/api/memory/clear", { method: "POST" });
    addMessage("Assistant", "Conversation cleared. Ready for the next command.");
    setStatus("Ready");
});

settingsBtn.addEventListener("click", () => {
    settingsModal.hidden = false;
});

closeSettingsBtn.addEventListener("click", () => {
    settingsModal.hidden = true;
});

settingsModal.addEventListener("click", (event) => {
    if (event.target === settingsModal) {
        settingsModal.hidden = true;
    }
});

sttMode.addEventListener("change", () => {
    settings.sttMode = sttMode.value;
    localStorage.setItem("echo.sttMode", settings.sttMode);
    addMessage("Assistant", `Voice input mode set to ${settings.sttMode}.`);
});

ttsMode.addEventListener("change", () => {
    settings.ttsMode = ttsMode.value;
    localStorage.setItem("echo.ttsMode", settings.ttsMode);
    addMessage("Assistant", `Voice output mode set to ${settings.ttsMode}.`);
});

function updateMicButton() {
    micBtn.classList.toggle("is-listening", isListening);
    waveform.classList.toggle("is-listening", isListening);
    micBtn.setAttribute("aria-pressed", String(isListening));
    micBtnLabel.textContent = isListening ? "Stop Listening" : "Start Listening";
}

function setStatus(status) {
    statusText.textContent = status;

    statusText.classList.remove("status-ready", "status-listening", "status-processing", "status-error");
    if (status === "Ready") statusText.classList.add("status-ready");
    if (status === "Listening") statusText.classList.add("status-listening");
    if (status === "Processing") statusText.classList.add("status-processing");
    if (status === "Error") statusText.classList.add("status-error");
}

function setThinking(active) {
    isProcessing = active;
    thinking.hidden = !active;
    micBtn.disabled = active;
    commandInput.disabled = active;
    document.getElementById("sendBtn").disabled = active;
}

function addMessage(role, text) {
    const message = document.createElement("article");
    message.className = `message message-${role.toLowerCase()}`;

    const label = document.createElement("span");
    label.className = "message-label";
    label.textContent = role;

    const body = document.createElement("div");
    body.className = "message-body";
    body.textContent = text;

    message.append(label, body);
    conversation.appendChild(message);
    conversation.scrollTop = conversation.scrollHeight;
}

async function submitMessage(message) {
    if (!message) {
        return;
    }

    addMessage("User", message);
    commandInput.value = "";
    setStatus("Processing");
    setThinking(true);

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Request failed.");
        }

        addMessage("Assistant", data.response);
        setStatus(data.status || "Ready");
        await speakResponse(data.response);
    } catch (error) {
        addMessage("Assistant", `Something went wrong: ${error.message}`);
        setStatus("Error");
    } finally {
        setThinking(false);
    }
}

async function listenWithBackend(manageState = true) {
    setStatus("Listening");
    if (manageState) {
        isListening = true;
        updateMicButton();
    }

    try {
        const response = await fetch("/api/listen", {
            method: "POST"
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Listening failed.");
        }

        if (data.text) {
            addMessage("User", data.text);
        }
        addMessage("Assistant", data.response);
        setStatus(data.status || "Ready");
        await speakResponse(data.response);
    } catch (error) {
        addMessage("Assistant", `Listening failed: ${error.message}`);
        setStatus("Error");
    } finally {
        if (manageState) {
            isListening = false;
            updateMicButton();
        }
    }
}

async function listenWithBackendLoop() {
    isListening = true;
    updateMicButton();

    while (keepListening) {
        await listenWithBackend(false);
        if (keepListening) {
            await sleep(200);
        }
    }

    isListening = false;
    updateMicButton();
    if (statusText.textContent === "Listening") {
        setStatus("Idle");
    }
}

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

async function speakResponse(text) {
    if (!text) {
        return;
    }

    if (settings.ttsMode === "backend") {
        try {
            await fetch("/api/speak", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text })
            });
            return;
        } catch (error) {
            addMessage("Assistant", "Backend voice output failed, using browser voice.");
        }
    }

    if (!window.speechSynthesis) {
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
}