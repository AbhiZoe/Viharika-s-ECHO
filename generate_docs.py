"""Generate a detailed PDF documentation for the Echo-Mind Voice Assistant project."""
from fpdf import FPDF


class DocPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "Echo-Mind Voice Assistant - Project Documentation", align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(140, 140, 140)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(20, 60, 120)
        self.cell(0, 12, title)
        self.ln(6)
        self.set_draw_color(20, 60, 120)
        self.set_line_width(0.6)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(8)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, title)
        self.ln(8)

    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6.5, text)
        self.ln(4)

    def bullet(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(30, 30, 30)
        self.cell(8, 6.5, "-")
        self.multi_cell(0, 6.5, text)
        self.ln(1)

    def code_block(self, text):
        self.set_font("Courier", "", 9)
        self.set_fill_color(240, 240, 245)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.2, text, fill=True)
        self.ln(4)


def build_pdf():
    pdf = DocPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── COVER PAGE ──
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(20, 60, 120)
    pdf.cell(0, 15, "Echo-Mind", align="C")
    pdf.ln(14)
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, "Advanced AI Voice Assistant", align="C")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Project Documentation", align="C")
    pdf.ln(8)
    pdf.cell(0, 8, "Desktop Application built with Python & PyQt6", align="C")
    pdf.ln(30)
    pdf.set_draw_color(20, 60, 120)
    pdf.set_line_width(0.4)
    x_start = pdf.w / 2 - 40
    pdf.line(x_start, pdf.get_y(), x_start + 80, pdf.get_y())
    pdf.ln(12)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 7, "B.Tech Mini Project", align="C")
    pdf.ln(7)
    pdf.cell(0, 7, "Viharika  |  Echo-Mind", align="C")

    # ── TABLE OF CONTENTS ──
    pdf.add_page()
    pdf.section_title("Table of Contents")
    toc = [
        "1. Project Overview",
        "2. System Architecture",
        "3. Project Structure",
        "4. Detailed File Descriptions",
        "    4.1  main.py - Application Entry Point",
        "    4.2  config/config.py - Configuration Management",
        "    4.3  modules/assistant_core.py - Core Controller",
        "    4.4  modules/llm_engine.py - LLM Integration",
        "    4.5  modules/speech_to_text.py - Speech Recognition",
        "    4.6  modules/text_to_speech.py - Text-to-Speech Service",
        "    4.7  modules/tts_worker.py - TTS Subprocess Worker",
        "    4.8  modules/task_router.py - Command Router",
        "    4.9  modules/system_control.py - System Automation",
        "    4.10 modules/web_tasks.py - Wikipedia & Web Tasks",
        "    4.11 ui/main_window.py - Desktop GUI",
        "    4.12 utils/helpers.py - Utility Functions",
        "5. Technology Stack & Dependencies",
        "6. Key Design Patterns",
        "7. Data Flow",
        "8. Configuration Reference",
        "9. Setup & Usage Instructions",
    ]
    for entry in toc:
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 8, entry)
        pdf.ln(6)

    # ── 1. PROJECT OVERVIEW ──
    pdf.add_page()
    pdf.section_title("1. Project Overview")
    pdf.body_text(
        "Echo-Mind is a modern, AI-powered desktop voice assistant built with Python. "
        "It combines speech recognition, large language model (LLM) reasoning, text-to-speech "
        "synthesis, and system automation into a single, user-friendly desktop application."
    )
    pdf.body_text(
        "The assistant listens for voice commands through the microphone, converts speech to text "
        "using Google's Speech Recognition API, processes commands through an intelligent routing "
        "system, and responds both visually (in the chat transcript) and audibly (via pyttsx3 "
        "text-to-speech with a female voice)."
    )
    pdf.sub_title("Key Features")
    features = [
        "Voice-first interaction with continuous listening mode",
        "LLM-powered conversational AI (Groq / OpenAI integration)",
        "Text-to-Speech with female voice output and stop control",
        "YouTube search and direct video playback",
        "Google search integration",
        "Screenshot capture with automatic timestamped filenames",
        "Application launching (Chrome, Notepad, Calculator, VS Code, etc.)",
        "Wikipedia topic lookup with smart alias resolution",
        "Conversation memory with JSON persistence (up to 20 messages)",
        "Modern dark-themed PyQt6 desktop GUI with glassmorphism design",
        "Real-time animated waveform visualization",
        "Settings dialog for API key management",
    ]
    for f in features:
        pdf.bullet(f)

    # ── 2. SYSTEM ARCHITECTURE ──
    pdf.add_page()
    pdf.section_title("2. System Architecture")
    pdf.body_text(
        "Echo-Mind follows a modular, layered architecture with clear separation of concerns. "
        "The application is divided into four main layers:"
    )
    pdf.sub_title("Presentation Layer (ui/)")
    pdf.body_text(
        "The PyQt6-based desktop GUI provides the visual interface. It includes a two-panel layout "
        "with the main conversation area on the left and a control panel on the right. The GUI "
        "communicates with the backend via Qt signals and slots, ensuring thread-safe UI updates."
    )
    pdf.sub_title("Controller Layer (modules/assistant_core.py)")
    pdf.body_text(
        "The AssistantController acts as the central orchestrator. It manages the listening loop, "
        "dispatches commands to the task router or LLM, triggers text-to-speech, and emits signals "
        "to update the UI. All blocking operations run on background threads to keep the UI responsive."
    )
    pdf.sub_title("Service Layer (modules/)")
    pdf.body_text(
        "Individual service modules handle specific responsibilities: speech-to-text conversion, "
        "text-to-speech synthesis, LLM API communication, command routing, system automation, and "
        "web tasks. Each service is implemented as a class or set of functions with a singleton pattern."
    )
    pdf.sub_title("Data Layer (utils/, memory/, config/)")
    pdf.body_text(
        "Configuration is loaded from environment variables (.env file). Conversation history is "
        "persisted as JSON in the memory/ directory. Utility functions provide thread-safe file "
        "operations for both memory and environment management."
    )

    # ── 3. PROJECT STRUCTURE ──
    pdf.add_page()
    pdf.section_title("3. Project Structure")
    tree = (
        "voice-assistant/\n"
        "|-- main.py                     # Application entry point\n"
        "|-- requirements.txt            # Python dependencies\n"
        "|-- .env                        # Environment variables (API keys)\n"
        "|-- .gitignore                  # Git ignore rules\n"
        "|-- README.md                   # Project documentation\n"
        "|\n"
        "|-- config/\n"
        "|   |-- config.py               # Configuration loader\n"
        "|\n"
        "|-- modules/\n"
        "|   |-- assistant_core.py       # Central controller\n"
        "|   |-- llm_engine.py           # LLM API integration\n"
        "|   |-- speech_to_text.py       # Speech recognition\n"
        "|   |-- text_to_speech.py       # TTS service manager\n"
        "|   |-- tts_worker.py           # TTS subprocess worker\n"
        "|   |-- task_router.py          # Command pattern matcher\n"
        "|   |-- system_control.py       # OS-level automation\n"
        "|   |-- web_tasks.py            # Wikipedia lookups\n"
        "|\n"
        "|-- ui/\n"
        "|   |-- main_window.py          # PyQt6 desktop GUI\n"
        "|\n"
        "|-- utils/\n"
        "|   |-- helpers.py              # Memory & env utilities\n"
        "|\n"
        "|-- memory/\n"
        "|   |-- conversation_memory.json  # Chat history\n"
        "|\n"
        "|-- screenshots/                # Captured screenshots\n"
    )
    pdf.code_block(tree)

    # ── 4. DETAILED FILE DESCRIPTIONS ──
    pdf.add_page()
    pdf.section_title("4. Detailed File Descriptions")

    # 4.1 main.py
    pdf.sub_title("4.1  main.py - Application Entry Point")
    pdf.body_text(
        "This is the entry point of the Echo-Mind application. It creates a PyQt6 QApplication "
        "instance, sets the application name and organization, instantiates the main window "
        "(EchoMindWindow), displays it, and starts the Qt event loop."
    )
    pdf.body_text("Key responsibilities:")
    pdf.bullet("Initialize the Qt application framework")
    pdf.bullet("Create and display the main window")
    pdf.bullet("Run the event loop until the user closes the window")
    pdf.code_block(
        'def main() -> int:\n'
        '    app = QApplication(sys.argv)\n'
        '    app.setApplicationName("Echo-Mind")\n'
        '    window = EchoMindWindow()\n'
        '    window.show()\n'
        '    return app.exec()'
    )

    # 4.2 config.py
    pdf.sub_title("4.2  config/config.py - Configuration Management")
    pdf.body_text(
        "Manages all application configuration by loading values from environment variables "
        "defined in a .env file. Uses python-dotenv for loading. Every configurable parameter "
        "has a sensible default value so the app can start even without a .env file."
    )
    pdf.body_text("Configuration categories:")
    pdf.bullet("Assistant identity: ASSISTANT_NAME (default: 'Echo-Mind'), USER_NAME")
    pdf.bullet("Audio settings: VOICE_RATE (175 WPM), LISTEN_TIMEOUT (6s), LISTEN_PHRASE_LIMIT (8s)")
    pdf.bullet("LLM settings: LLM_PROVIDER (groq/openai), API keys, model names, timeout")
    pdf.bullet("Engine selection: STT_ENGINE (google), TTS_ENGINE (pyttsx3)")
    pdf.bullet("Storage: MAX_MEMORY (20 messages), SCREENSHOT_DIR")
    pdf.bullet("Debug: DEBUG_MODE flag for development logging")

    # 4.3 assistant_core.py
    pdf.add_page()
    pdf.sub_title("4.3  modules/assistant_core.py - Core Controller")
    pdf.body_text(
        "The AssistantController is the heart of the application. It is a QObject subclass that "
        "orchestrates all voice assistant operations and communicates with the UI through Qt signals."
    )
    pdf.body_text("PyQt Signals emitted:")
    pdf.bullet("transcript_added(role, text) - when a user or assistant message should appear")
    pdf.bullet("status_changed(text) - status updates (Listening, Thinking, Speaking, Ready, Idle)")
    pdf.bullet("listening_changed(bool) - toggle listening state in UI")
    pdf.bullet("response_ready(text) - full response text for external consumers")
    pdf.bullet("error_occurred(text) - error messages for UI display")
    pdf.body_text("Core methods:")
    pdf.bullet("start_listening() - spawns a daemon thread running the continuous listening loop")
    pdf.bullet("stop_listening() - sets stop event to break the listening loop")
    pdf.bullet("stop_speaking() - terminates the TTS subprocess to stop speech immediately")
    pdf.bullet("submit_text(text) - handles typed text input on a background thread")
    pdf.bullet("_listen_loop() - continuous loop: listen -> recognize -> handle -> repeat")
    pdf.bullet("_handle_command(command) - routes command through TaskRouter or LLM, then speaks reply")
    pdf.body_text(
        "Threading model: The listening loop runs on a dedicated daemon thread. Each voice command "
        "spawns a separate handler thread to avoid blocking the listener. An Event-based synchronization "
        "mechanism ensures commands complete (including speech) before the listener resumes."
    )

    # 4.4 llm_engine.py
    pdf.sub_title("4.4  modules/llm_engine.py - LLM Integration")
    pdf.body_text(
        "Provides the LLMEngine class that connects to either Groq or OpenAI APIs for generating "
        "intelligent conversational responses. The engine maintains conversation context by loading "
        "prior messages from the memory system."
    )
    pdf.body_text("How it works:")
    pdf.bullet("Builds a message array: system prompt + conversation history + current user prompt")
    pdf.bullet("Creates the appropriate API client based on LLM_PROVIDER setting")
    pdf.bullet("Sends a chat completion request with temperature=0.5 and max_tokens=450")
    pdf.bullet("Saves both user prompt and assistant response to conversation memory")
    pdf.bullet("Handles API errors, missing keys, and empty responses gracefully")
    pdf.body_text(
        "System prompt: 'You are Echo-Mind, a modern desktop AI voice assistant. Be concise, "
        "helpful, and safe. If a local task already handled the request, do not invent extra actions.'"
    )

    # 4.5 speech_to_text.py
    pdf.add_page()
    pdf.sub_title("4.5  modules/speech_to_text.py - Speech Recognition")
    pdf.body_text(
        "Wraps the SpeechRecognition library to provide microphone-based voice input. The "
        "SpeechToTextService class captures audio from the microphone and converts it to text "
        "using Google's free Speech Recognition API."
    )
    pdf.body_text("Process flow:")
    pdf.bullet("Opens the microphone and adjusts for ambient noise (0.35s calibration)")
    pdf.bullet("Listens for speech with configurable timeout and phrase length limits")
    pdf.bullet("Sends audio to Google Speech Recognition API for transcription")
    pdf.bullet("Returns a SpeechResult dataclass containing either text or an error message")
    pdf.body_text("Error handling covers:")
    pdf.bullet("No speech detected (timeout)")
    pdf.bullet("Microphone not available (OSError)")
    pdf.bullet("Unrecognizable audio")
    pdf.bullet("Network/service unavailability")
    pdf.bullet("Missing Python module (setuptools on Python 3.12+)")

    # 4.6 text_to_speech.py
    pdf.sub_title("4.6  modules/text_to_speech.py - Text-to-Speech Service")
    pdf.body_text(
        "Manages text-to-speech output using a subprocess-based architecture. Instead of running "
        "pyttsx3 directly in the main process (which causes thread-safety issues), it spawns a "
        "persistent worker subprocess (tts_worker.py) that handles all speech synthesis."
    )
    pdf.body_text("Architecture:")
    pdf.bullet("On initialization, starts a subprocess running tts_worker.py")
    pdf.bullet("speak_async(text, on_done) sends text via stdin pipe to the worker")
    pdf.bullet("The worker speaks the text and writes 'DONE' to stdout when finished")
    pdf.bullet("A monitoring thread waits for 'DONE' and calls the on_done callback")
    pdf.bullet("stop() terminates the worker process (instantly stopping speech) and restarts it")
    pdf.body_text(
        "This design ensures the stop button works reliably - terminating a process is guaranteed "
        "to stop all audio output immediately, unlike trying to interrupt pyttsx3 across threads."
    )

    # 4.7 tts_worker.py
    pdf.sub_title("4.7  modules/tts_worker.py - TTS Subprocess Worker")
    pdf.body_text(
        "A standalone Python script that runs as a child process for speech synthesis. It initializes "
        "pyttsx3 once on startup, selects a female voice (Microsoft Zira or similar), and then "
        "enters a read-speak loop."
    )
    pdf.body_text("Lifecycle:")
    pdf.bullet("Receives voice rate as a command-line argument")
    pdf.bullet("Initializes pyttsx3 engine and selects female voice")
    pdf.bullet("Writes 'READY' to stdout to signal successful initialization")
    pdf.bullet("Reads text lines from stdin, speaks each one, writes 'DONE' after each")
    pdf.bullet("Runs until the parent process terminates it")

    # 4.8 task_router.py
    pdf.add_page()
    pdf.sub_title("4.8  modules/task_router.py - Command Router")
    pdf.body_text(
        "The TaskRouter uses regex pattern matching to detect and dispatch specific voice commands "
        "to their appropriate handlers. If no pattern matches, the command falls through to the "
        "LLM for a conversational response."
    )
    pdf.body_text("Supported command categories:")
    pdf.bullet("YouTube: 'open youtube', 'play [song] on youtube', 'search youtube for [query]'")
    pdf.bullet("Google: 'open google', 'google [query]', 'search google for [query]'")
    pdf.bullet("Screenshots: 'take screenshot', 'capture screenshot'")
    pdf.bullet("App launching: 'open [app]', 'launch [app]', 'start [app]'")
    pdf.bullet("Web search: 'search for [topic]', 'search [topic]'")
    pdf.bullet("Wikipedia: 'wikipedia [topic]', 'wiki [topic]'")
    pdf.body_text(
        "Returns a RouteResult dataclass with a 'handled' flag and response text. The assistant "
        "controller checks this flag to decide whether to forward the command to the LLM."
    )

    # 4.9 system_control.py
    pdf.sub_title("4.9  modules/system_control.py - System Automation")
    pdf.body_text(
        "Provides functions for OS-level automation including application launching, browser "
        "operations, and screenshot capture. Designed for Windows with appropriate subprocess commands."
    )
    pdf.body_text("Functions:")
    pdf.bullet("open_application(target) - launches apps via APP_ALIASES dictionary (Chrome, Notepad, Calc, VS Code, etc.)")
    pdf.bullet("open_url(target) - opens known sites or arbitrary URLs in the default browser")
    pdf.bullet("open_youtube(query) - opens YouTube homepage or search results")
    pdf.bullet("play_on_youtube(query) - scrapes YouTube search results to find and play the first video directly")
    pdf.bullet("open_google(query) - opens Google homepage or search results")
    pdf.bullet("search_web(query) - performs a Google search via browser")
    pdf.bullet("take_screenshot() - captures full screen using PyAutoGUI, saves as timestamped PNG")
    pdf.body_text(
        "The module maintains two lookup dictionaries: APP_ALIASES maps application names to their "
        "subprocess commands, and KNOWN_SITES maps site names to URLs."
    )

    # 4.10 web_tasks.py
    pdf.sub_title("4.10  modules/web_tasks.py - Wikipedia & Web Tasks")
    pdf.body_text(
        "Handles Wikipedia topic lookups with intelligent query processing. Extracts the topic "
        "from natural language queries, resolves common abbreviations, and fetches concise summaries."
    )
    pdf.body_text("Processing pipeline:")
    pdf.bullet("_extract_topic() - strips prefixes like 'what is', 'who is', 'tell me about'")
    pdf.bullet("_normalize_topic() - resolves aliases (AI -> artificial intelligence, ML -> machine learning)")
    pdf.bullet("_resolve_topic() - handles acronyms by searching Wikipedia and matching results")
    pdf.bullet("search_wikipedia() - fetches a 2-sentence summary with disambiguation handling")

    # 4.11 main_window.py
    pdf.add_page()
    pdf.sub_title("4.11  ui/main_window.py - Desktop GUI")
    pdf.body_text(
        "Implements the full desktop interface using PyQt6. The window is 1180x760 pixels with a "
        "modern dark theme featuring glassmorphism effects, teal accent colors, and smooth animations."
    )
    pdf.body_text("Widget classes:")
    pdf.bullet("WaveformWidget - custom-painted animated waveform with 22 bars, teal when active, gray when idle")
    pdf.bullet("SettingsDialog - modal dialog for entering and saving API keys to .env file")
    pdf.bullet("EchoMindWindow - main application window with two-panel layout")
    pdf.body_text("Left panel (60% width):")
    pdf.bullet("Brand header with 'ECHO-MIND' title and Settings button")
    pdf.bullet("Animated waveform visualization")
    pdf.bullet("Status chip (Ready / Listening / Thinking / Speaking / Idle)")
    pdf.bullet("Start Listening button and Stop Speaking button side by side")
    pdf.bullet("Scrollable chat transcript with styled message bubbles")
    pdf.bullet("Text input composer with Send button")
    pdf.body_text("Right panel (40% width):")
    pdf.bullet("Mission Control overview with 4 info cards")
    pdf.bullet("Quick Action buttons (YouTube, Play on YouTube, Screenshot, Wikipedia)")
    pdf.bullet("Clear Memory button")
    pdf.body_text(
        "Styling: Comprehensive QSS stylesheet with dark navy/teal gradients, glassmorphism panels "
        "with semi-transparent backgrounds, rounded corners (30px), custom scrollbars, and distinct "
        "colors for user (blue) and assistant (teal) message bubbles."
    )

    # 4.12 helpers.py
    pdf.sub_title("4.12  utils/helpers.py - Utility Functions")
    pdf.body_text(
        "Provides thread-safe utility functions for conversation memory persistence and "
        "environment variable management."
    )
    pdf.body_text("Memory functions:")
    pdf.bullet("load_memory() - reads conversation history from JSON file with validation")
    pdf.bullet("save_memory(data) - writes validated messages, enforcing MAX_MEMORY limit")
    pdf.bullet("append_memory(role, content) - adds a single message to conversation history")
    pdf.bullet("clear_memory() - resets conversation history to empty")
    pdf.bullet("validate_message() - ensures messages have valid role and non-empty content")
    pdf.body_text("Environment functions:")
    pdf.bullet("upsert_env_value(key, value) - updates or inserts key-value pairs in .env file")
    pdf.body_text(
        "All memory operations use a threading Lock (MEMORY_LOCK) to prevent race conditions "
        "when multiple threads access the conversation history simultaneously."
    )

    # ── 5. TECHNOLOGY STACK ──
    pdf.add_page()
    pdf.section_title("5. Technology Stack & Dependencies")
    deps = [
        ("PyQt6 6.7.1", "Desktop GUI framework providing widgets, layouts, signals/slots, and styling"),
        ("SpeechRecognition 3.10.4", "Speech-to-text library supporting Google, Sphinx, and other APIs"),
        ("PyAudio 0.2.14", "Cross-platform audio I/O for microphone access"),
        ("pyttsx3 2.90", "Offline text-to-speech engine (uses Windows SAPI5)"),
        ("groq 0.9.0", "Python client for Groq API (fast LLM inference with Llama models)"),
        ("openai 1.51.2", "Python client for OpenAI API (GPT models)"),
        ("wikipedia 1.4.0", "Python wrapper for the Wikipedia API"),
        ("requests 2.32.3", "HTTP client library for web requests"),
        ("PyAutoGUI 0.9.54", "Cross-platform GUI automation for screenshots"),
        ("python-dotenv 1.0.1", "Loads environment variables from .env files"),
        ("psutil 6.0.0", "System and process utilities"),
        ("Pillow 10.3+", "Image processing library for screenshot handling"),
        ("httpx 0.27.2", "Modern async HTTP client (required by Groq SDK)"),
    ]
    for name, desc in deps:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(55, 7, name)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, desc)
        pdf.ln(2)

    # ── 6. KEY DESIGN PATTERNS ──
    pdf.add_page()
    pdf.section_title("6. Key Design Patterns")
    patterns = [
        ("Singleton Pattern",
         "TTS, STT, LLM, and TaskRouter services are instantiated once at module level as private "
         "singletons. Module-level convenience functions provide a clean public API."),
        ("Signal/Slot Pattern (Observer)",
         "PyQt6 signals decouple the backend controller from the UI. The controller emits signals "
         "(status_changed, transcript_added, etc.) and the UI connects slots to update widgets. "
         "This ensures thread-safe UI updates since signals can cross thread boundaries."),
        ("Command Pattern",
         "The TaskRouter implements command pattern matching using regex. Each command category "
         "has dedicated handler functions in system_control.py and web_tasks.py."),
        ("Subprocess Isolation",
         "Text-to-speech runs in a separate subprocess to avoid thread-safety issues with pyttsx3. "
         "This enables reliable stop functionality through process termination."),
        ("Graceful Degradation",
         "The app works even without a microphone, speakers, or API keys. Each service checks "
         "availability and returns informative error messages rather than crashing."),
        ("Thread-safe Data Access",
         "Conversation memory uses a threading Lock to prevent concurrent file access corruption. "
         "All memory read/write operations are serialized through this lock."),
    ]
    for name, desc in patterns:
        pdf.sub_title(name)
        pdf.body_text(desc)

    # ── 7. DATA FLOW ──
    pdf.add_page()
    pdf.section_title("7. Data Flow")
    pdf.sub_title("Voice Input Flow")
    steps_voice = [
        "1. User clicks 'Start Listening' -> AssistantController.start_listening()",
        "2. Listening loop starts on daemon thread, status = 'Listening'",
        "3. SpeechToTextService.listen_once() captures audio from microphone",
        "4. Audio sent to Google Speech API for transcription",
        "5. Recognized text passed to _handle_command() on a new thread",
        "6. TaskRouter.route() checks for pattern matches (YouTube, Google, etc.)",
        "7. If matched: execute handler, get response. If not: forward to LLMEngine.ask()",
        "8. LLM builds message history + prompt, calls Groq/OpenAI API",
        "9. Response displayed in transcript via transcript_added signal",
        "10. TTS subprocess speaks the response, status = 'Speaking'",
        "11. Speech completes, status = 'Ready', listening loop resumes",
    ]
    for s in steps_voice:
        pdf.bullet(s)

    pdf.sub_title("Text Input Flow")
    steps_text = [
        "1. User types message in input box and clicks 'Send'",
        "2. submit_text() spawns handler thread with the typed text",
        "3. Same processing pipeline as voice input (steps 6-11 above)",
    ]
    for s in steps_text:
        pdf.bullet(s)

    pdf.sub_title("Stop Speaking Flow")
    steps_stop = [
        "1. User clicks 'Stop Speaking' button (enabled when status = 'Speaking')",
        "2. AssistantController.stop_speaking() called",
        "3. TextToSpeechService.stop() terminates the TTS worker subprocess",
        "4. Speech stops immediately, new worker process starts for next use",
        "5. Status changes to 'Ready'",
    ]
    for s in steps_stop:
        pdf.bullet(s)

    # ── 8. CONFIGURATION ──
    pdf.add_page()
    pdf.section_title("8. Configuration Reference")
    pdf.body_text("All settings are defined in the .env file in the project root:")
    config_items = [
        ("ASSISTANT_NAME", "Echo-Mind", "Display name of the assistant"),
        ("USER_NAME", "User", "Display name of the user"),
        ("DEBUG_MODE", "false", "Enable debug logging"),
        ("VOICE_RATE", "175", "Speech rate in words per minute"),
        ("LISTEN_TIMEOUT", "6", "Seconds to wait for speech before timeout"),
        ("LISTEN_PHRASE_LIMIT", "8", "Max seconds for a single phrase"),
        ("LISTEN_RETRY_DELAY_MS", "600", "Delay between listen retries (ms)"),
        ("LLM_PROVIDER", "groq", "LLM backend: 'groq' or 'openai'"),
        ("GROQ_API_KEY", "", "API key for Groq"),
        ("GROQ_MODEL", "llama-3.3-70b-versatile", "Groq model identifier"),
        ("OPENAI_API_KEY", "", "API key for OpenAI"),
        ("OPENAI_MODEL", "gpt-4o-mini", "OpenAI model identifier"),
        ("MAX_MEMORY", "20", "Max conversation messages to retain"),
        ("SCREENSHOT_DIR", "screenshots", "Directory for saved screenshots"),
        ("STT_ENGINE", "google", "Speech-to-text engine"),
        ("TTS_ENGINE", "pyttsx3", "Text-to-speech engine"),
    ]
    pdf.set_font("Courier", "B", 9)
    pdf.set_fill_color(230, 235, 245)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(55, 7, "Variable", fill=True)
    pdf.cell(45, 7, "Default", fill=True)
    pdf.cell(0, 7, "Description", fill=True)
    pdf.ln()
    for var, default, desc in config_items:
        pdf.set_font("Courier", "", 9)
        pdf.cell(55, 6.5, var)
        pdf.cell(45, 6.5, default if default else "(empty)")
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 6.5, desc)
        pdf.ln()

    # ── 9. SETUP & USAGE ──
    pdf.add_page()
    pdf.section_title("9. Setup & Usage Instructions")
    pdf.sub_title("Prerequisites")
    pdf.bullet("Python 3.10 or higher")
    pdf.bullet("Windows OS (for SAPI5 text-to-speech and app launching)")
    pdf.bullet("Working microphone for voice input")
    pdf.bullet("Internet connection for speech recognition and LLM API calls")
    pdf.bullet("Groq or OpenAI API key")

    pdf.sub_title("Installation Steps")
    steps = [
        "1. Clone or download the project to your local machine",
        "2. Open a terminal in the voice-assistant directory",
        "3. Create a virtual environment:  python -m venv venv",
        "4. Activate the environment:  venv\\Scripts\\activate",
        "5. Install dependencies:  pip install -r requirements.txt",
        "6. Create a .env file and add your API key:",
        "       GROQ_API_KEY=your_api_key_here",
        "7. Run the application:  python main.py",
    ]
    for s in steps:
        pdf.body_text(s)

    pdf.sub_title("Using Echo-Mind")
    pdf.bullet("Click 'Start Listening' to activate voice input mode")
    pdf.bullet("Speak your command clearly into the microphone")
    pdf.bullet("Or type a message in the text box and click 'Send'")
    pdf.bullet("Use Quick Action buttons for common tasks")
    pdf.bullet("Click 'Stop Speaking' to interrupt the assistant's voice response")
    pdf.bullet("Say 'stop' or 'exit' to end the listening session")
    pdf.bullet("Click 'Settings' to update API keys")
    pdf.bullet("Click 'Clear Memory' to reset conversation history")

    # Save
    output_path = "Echo-Mind_Project_Documentation.pdf"
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    build_pdf()
