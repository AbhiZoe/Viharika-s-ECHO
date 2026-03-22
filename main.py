from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from ui.main_window import EchoMindWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Echo-Mind")
    app.setOrganizationName("Echo-Mind")
    window = EchoMindWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
