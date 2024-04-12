import sys

from PyQt6.QtWidgets import QApplication

from .database import createConnection
from .views import Window


def main():
    """RP Contacts main function."""
    # Create the application
    app = QApplication(sys.argv)
    if not createConnection('contacts.sqlite'):
        sys.exit(1)
    win = Window()
    win.show()
    sys.exit(app.exec())