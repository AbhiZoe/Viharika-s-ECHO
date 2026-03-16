from __future__ import annotations

import math

from PyQt6.QtCore import QPointF, QRectF, QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from config.config import ASSISTANT_NAME, ENV_FILE, GROQ_API_KEY, OPENAI_API_KEY
from modules.assistant_core import AssistantController
from utils.helpers import clear_memory, upsert_env_value


class WaveformWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumHeight(120)
        self._tick = 0
        self._active = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance)
        self._timer.start(80)

    def set_active(self, active: bool) -> None:
        self._active = active
        self.update()

    def _advance(self) -> None:
        self._tick += 1
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect().adjusted(8, 8, -8, -8))

        path = QPainterPath()
        path.addRoundedRect(rect, 28, 28)
        painter.fillPath(path, QColor("#111723"))

        bars = 22
        gap = rect.width() / (bars + 2)
        base_y = rect.center().y()
        for index in range(bars):
            amplitude = 0.15 if not self._active else 0.25 + 0.75 * abs(math.sin((self._tick + index * 2) / 4))
            height = rect.height() * 0.36 * amplitude
            x = rect.left() + gap * (index + 1)
            color = QColor("#1de9b6") if self._active else QColor("#38505a")
            pen = QPen(color, 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawLine(QPointF(x, base_y - height), QPointF(x, base_y + height))


class SettingsDialog(QDialog):
    saved = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("API Keys")
        title.setObjectName("panelTitle")
        layout.addWidget(title)

        self.openai_input = self._build_field(layout, "OpenAI API Key", OPENAI_API_KEY)
        self.groq_input = self._build_field(layout, "Groq API Key", GROQ_API_KEY)

        note = QLabel(f"Saved to {ENV_FILE}")
        note.setObjectName("hintText")
        note.setWordWrap(True)
        layout.addWidget(note)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        cancel = QPushButton("Close")
        cancel.clicked.connect(self.reject)
        save = QPushButton("Save")
        save.setObjectName("accentButton")
        save.clicked.connect(self._save)
        buttons.addWidget(cancel)
        buttons.addWidget(save)
        layout.addLayout(buttons)

    def _build_field(self, parent_layout: QVBoxLayout, label_text: str, value: str) -> QLineEdit:
        label = QLabel(label_text)
        parent_layout.addWidget(label)
        field = QLineEdit(value)
        field.setEchoMode(QLineEdit.EchoMode.Password)
        parent_layout.addWidget(field)
        return field

    def _save(self) -> None:
        upsert_env_value("OPENAI_API_KEY", self.openai_input.text().strip())
        upsert_env_value("GROQ_API_KEY", self.groq_input.text().strip())
        self.saved.emit()
        self.accept()


class EchoMindWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.controller = AssistantController()
        self.setWindowTitle(f"{ASSISTANT_NAME} Desktop Assistant")
        self.resize(1180, 760)
        self._build_ui()
        self._connect_signals()
        self._append_system_message("Echo-Mind is ready. Start listening or type a request below.")
        self._set_status("Ready")

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(20)

        left_panel = self._build_panel()
        right_panel = self._build_panel()
        root.addWidget(left_panel, 3)
        root.addWidget(right_panel, 2)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(28, 28, 28, 28)
        left_layout.setSpacing(18)

        header = QHBoxLayout()
        brand = QLabel("ECHO-MIND")
        brand.setObjectName("brandTitle")
        subtitle = QLabel("Advanced AI Voice Assistant")
        subtitle.setObjectName("subtleText")
        title_wrap = QVBoxLayout()
        title_wrap.setSpacing(2)
        title_wrap.addWidget(brand)
        title_wrap.addWidget(subtitle)

        settings = QToolButton()
        settings.setText("Settings")
        settings.clicked.connect(self._open_settings)
        self.settings_button = settings

        header.addLayout(title_wrap)
        header.addStretch(1)
        header.addWidget(settings)
        left_layout.addLayout(header)

        self.waveform = WaveformWidget()
        left_layout.addWidget(self.waveform)

        status_row = QHBoxLayout()
        self.status_chip = QLabel("Ready")
        self.status_chip.setObjectName("statusChip")
        self.tts_label = QLabel(f"Voice: {'On' if self.controller.tts_available else 'Off'}")
        self.tts_label.setObjectName("subtleText")
        status_row.addWidget(self.status_chip)
        status_row.addStretch(1)
        status_row.addWidget(self.tts_label)
        left_layout.addLayout(status_row)

        self.listen_button = QPushButton("Start Listening")
        self.listen_button.setObjectName("accentButton")
        self.listen_button.clicked.connect(self._toggle_listening)
        left_layout.addWidget(self.listen_button)

        self.transcript = QListWidget()
        self.transcript.setSpacing(12)
        left_layout.addWidget(self.transcript, 1)

        composer = QHBoxLayout()
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Type a message for Echo-Mind...")
        self.input_box.setFixedHeight(92)
        composer.addWidget(self.input_box, 1)
        send_button = QPushButton("Send")
        send_button.clicked.connect(self._send_text)
        composer.addWidget(send_button)
        left_layout.addLayout(composer)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(28, 28, 28, 28)
        right_layout.setSpacing(16)

        overview_title = QLabel("Mission Control")
        overview_title.setObjectName("panelTitle")
        right_layout.addWidget(overview_title)

        cards = QGridLayout()
        cards.setHorizontalSpacing(14)
        cards.setVerticalSpacing(14)
        cards.addWidget(self._info_card("Listening", "Voice-first desktop command loop"), 0, 0)
        cards.addWidget(self._info_card("Reasoning", "Groq-powered answers with short-term memory"), 0, 1)
        cards.addWidget(self._info_card("Automation", "Apps, sites, Google, YouTube, screenshots, and explicit wiki lookups"), 1, 0)
        cards.addWidget(self._info_card("Safety", "Graceful errors and modular services"), 1, 1)
        right_layout.addLayout(cards)

        quick_title = QLabel("Quick Actions")
        quick_title.setObjectName("panelTitle")
        right_layout.addWidget(quick_title)

        for label, prompt in (
            ("Open YouTube", "open youtube"),
            ("Play on YouTube", "open youtube and play believer song"),
            ("Take Screenshot", "take screenshot"),
            ("Wikipedia", "wiki artificial intelligence"),
        ):
            button = QPushButton(label)
            button.clicked.connect(lambda _, value=prompt: self._send_preset(value))
            right_layout.addWidget(button)

        clear_button = QPushButton("Clear Memory")
        clear_button.clicked.connect(self._clear_memory)
        right_layout.addWidget(clear_button)
        right_layout.addStretch(1)

        self.setStyleSheet(self._styles())

    def _build_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("glassPanel")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 120))
        panel.setGraphicsEffect(shadow)
        return panel

    def _info_card(self, title: str, body: str) -> QFrame:
        frame = QFrame()
        frame.setObjectName("infoCard")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)
        heading = QLabel(title)
        heading.setObjectName("cardTitle")
        copy = QLabel(body)
        copy.setObjectName("subtleText")
        copy.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(copy)
        return frame

    def _connect_signals(self) -> None:
        self.controller.status_changed.connect(self._set_status)
        self.controller.listening_changed.connect(self._update_listening_state)
        self.controller.transcript_added.connect(self._append_message)
        self.controller.error_occurred.connect(self._append_system_message)

    def _toggle_listening(self) -> None:
        if self.listen_button.property("active"):
            self.controller.stop_listening()
        else:
            self.controller.start_listening()

    def _send_text(self) -> None:
        text = self.input_box.toPlainText().strip()
        self.input_box.clear()
        self.controller.submit_text(text)

    def _send_preset(self, prompt: str) -> None:
        self.input_box.setPlainText(prompt)
        self._send_text()

    def _clear_memory(self) -> None:
        clear_memory()
        self._append_system_message("Conversation memory cleared.")

    def _open_settings(self) -> None:
        dialog = SettingsDialog(self)
        dialog.saved.connect(lambda: self._append_system_message("Settings saved. Restart the app to reload API keys."))
        dialog.exec()

    def _set_status(self, text: str) -> None:
        self.status_chip.setText(text)

    def _update_listening_state(self, active: bool) -> None:
        self.listen_button.setProperty("active", active)
        self.listen_button.setText("Stop Listening" if active else "Start Listening")
        self.listen_button.style().unpolish(self.listen_button)
        self.listen_button.style().polish(self.listen_button)
        self.waveform.set_active(active)

    def _append_message(self, role: str, message: str) -> None:
        item = QListWidgetItem()
        bubble = QLabel(message)
        bubble.setWordWrap(True)
        bubble.setObjectName("assistantBubble" if role == "assistant" else "userBubble")
        bubble.setMargin(14)
        item.setSizeHint(bubble.sizeHint())
        self.transcript.addItem(item)
        self.transcript.setItemWidget(item, bubble)
        self.transcript.scrollToBottom()

    def _append_system_message(self, message: str) -> None:
        self._append_message("assistant", message)

    def _styles(self) -> str:
        return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #070b11, stop:0.45 #09111b, stop:1 #030507);
            color: #edf7f7;
            font-family: Segoe UI;
        }
        QFrame#glassPanel {
            background: rgba(11, 18, 28, 0.92);
            border: 1px solid rgba(29, 233, 182, 0.18);
            border-radius: 30px;
        }
        QFrame#infoCard {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 22px;
        }
        QLabel#brandTitle {
            font-size: 28px;
            font-weight: 700;
            letter-spacing: 2px;
            color: #f5fffd;
        }
        QLabel#panelTitle {
            font-size: 18px;
            font-weight: 700;
            color: #f4fffe;
        }
        QLabel#cardTitle {
            font-size: 16px;
            font-weight: 700;
            color: #eafffb;
        }
        QLabel#subtleText, QLabel#hintText {
            color: #8aa1ac;
            font-size: 13px;
        }
        QLabel#statusChip {
            background: rgba(29, 233, 182, 0.14);
            color: #1de9b6;
            border: 1px solid rgba(29, 233, 182, 0.35);
            border-radius: 14px;
            padding: 8px 14px;
            font-weight: 700;
        }
        QPushButton, QToolButton {
            background: rgba(255, 255, 255, 0.05);
            color: #eff8f7;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 12px 18px;
            font-weight: 600;
        }
        QPushButton:hover, QToolButton:hover {
            border-color: rgba(29, 233, 182, 0.55);
        }
        QPushButton#accentButton {
            background: #1de9b6;
            color: #04110e;
            border: none;
            padding: 14px 18px;
        }
        QPushButton[active="true"] {
            background: #ff6b81;
            color: white;
        }
        QListWidget {
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 22px;
            padding: 14px;
        }
        QTextEdit, QLineEdit {
            background: rgba(255, 255, 255, 0.04);
            color: #eff8f7;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 12px;
        }
        QLabel#assistantBubble {
            background: rgba(29, 233, 182, 0.08);
            border: 1px solid rgba(29, 233, 182, 0.24);
            border-radius: 18px;
            color: #eafefd;
        }
        QLabel#userBubble {
            background: rgba(98, 182, 255, 0.08);
            border: 1px solid rgba(98, 182, 255, 0.24);
            border-radius: 18px;
            color: #eaf4ff;
        }
        """
