# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QAbstractItemView,
    QPushButton,
    QTableView,
    QVBoxLayout,
)
from .model import ContactsModel

class Window(QMainWindow):
    """Main Window"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('RP Contacts')
        self.resize(550, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.contactsModel = ContactsModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.resizeColumnsToContents()
        # Create buttons
        self.addButton = QPushButton('Add...')
        self.deleteButton = QPushButton('Delete')
        self.clearAllButton = QPushButton('Clear All')
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton.clicked.connect(self.deleteContact)
        self.clearAllButton.clicked.connect(self.clearContacts)
        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addLayout(layout)
        self.layout.addWidget(self.table)
        

    def openAddDialog(self):
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()

    def deleteContact(self):
        row = self.table.currentIndex().row()
        if row < 0:
            return
        
        messageBox = QMessageBox.warning(
            self,
            'Warning!',
            'Do you want to remove the selected contact?',
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        )
        if messageBox == QMessageBox.StandardButton.Ok:
            self.contactsModel.deleteContact(row)

    def clearContacts(self):
        messageBox = QMessageBox.warning(
            self,
            'Warning!',
            'Do you want to remove all contacts?',
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        if messageBox == QMessageBox.StandardButton.Ok:
            self.contactsModel.clearContact()


class AddDialog(QDialog):
    def __init__(self,parent=None) -> None:
        super().__init__(parent=parent)
        self.setWindowTitle('Add contact')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    def setupUI(self):
        self.nameField = QLineEdit()
        self.nameField.setObjectName('Name')
        self.jobField = QLineEdit()
        self.jobField.setObjectName('Job')
        self.emailField = QLineEdit()
        self.emailField.setObjectName('Email')
        layout = QFormLayout()
        layout.addRow('Name:', self.nameField)
        layout.addRow('Job:', self.jobField)
        layout.addRow('Email:', self.emailField)
        self.layout.addLayout(layout)
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)
    
    def accept(self) -> None:
        self.data = []
        for field in (self.nameField, self.jobField, self.emailField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    'Error!',
                    f'You mus provide a contact"s {field.objectName()}'
                )
                self.data = None
                return
            self.data.append(field.text())
        if not self.data:
            return
        
        super().accept()
    
        