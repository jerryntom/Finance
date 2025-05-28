from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QDoubleSpinBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import os
import sys

class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Account")
        self.setModal(True)
        self.setMinimumWidth(350)
        self.mapping = {1: "Bank", 2: "Savings", 3: "Investment", 4: "Credit", 5: "Cash"}
        self.selected_type_id = 1
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout(self)

        # Account Name
        nameLabel = QLabel("Account Name:")
        self.nameEdit = QLineEdit()
        self.nameEdit.setMaxLength(50)
        layout.addWidget(nameLabel)
        layout.addWidget(self.nameEdit)

        # Account Type
        typeLabel = QLabel("Account Type:")
        self.typeCombo = QComboBox()
        for type_id, type_name in self.mapping.items():
            self.typeCombo.addItem(type_name, type_id)
        layout.addWidget(typeLabel)
        layout.addWidget(self.typeCombo)

        # Initial Balance
        balanceLabel = QLabel("Initial Balance:")
        self.balanceSpin = QDoubleSpinBox()
        self.balanceSpin.setRange(-100000000, 100000000)
        self.balanceSpin.setDecimals(2)
        self.balanceSpin.setValue(0.00)
        layout.addWidget(balanceLabel)
        layout.addWidget(self.balanceSpin)

        # Error Label
        self.errorLabel = QLabel()
        self.errorLabel.setStyleSheet("color: red;")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.errorLabel)

        # Buttons
        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add")
        self.cancelButton = QPushButton("Cancel")
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)

        self.addButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def getData(self):
        name = self.nameEdit.text().strip()
        type_id = self.typeCombo.currentData()
        type_name = self.typeCombo.currentText()
        balance = self.balanceSpin.value()
        return name, type_id, type_name, balance

    def accept(self):
        name = self.nameEdit.text().strip()
        if not name:
            self.nameEdit.setToolTip("Account name cannot be empty.")
            self.errorLabel.setText("Account name cannot be empty.")
            return
        elif len(name) > 50:
            self.nameEdit.setToolTip("Account name must be at most 50 characters.")
            self.errorLabel.setText("Account name must be at most 50 characters.")
            return
        else:
            self.nameEdit.setToolTip("")
            self.errorLabel.setText("")
        super().accept()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
