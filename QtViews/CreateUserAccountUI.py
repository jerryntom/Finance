import os
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QLineEdit)
import re
import mysql.connector as mysql
import hashlib
import string
import random

# Size contants for layout
initWidth = 800
initHeight = 600
horizontalSpacerWidth = 40    
horizontalSpacerHeight = 20
verticalSpacerWidth = 20
verticalSpacerHeight = 10
formWidgetsFrameMinimumWidth = 250
formWidgetsFrameMaximumWidth = 400
buttonMinimumHeight = 50

# Validation constants
passwordMinimumLength = 8   

class CreateAccountView(QWidget):
    def setUpUI(self):
        self.setObjectName("logInView")
        
        # Vertical box layout for the main view window
        self.mainVerticalLayout = QVBoxLayout(self)
        
        # Horizontal box layout for the main view window
        self.mainHorizontalLayout = QHBoxLayout(self)
        
        # Spacer items for main view layouts
        self.verticalSpacerExpanding = QSpacerItem(verticalSpacerWidth, verticalSpacerHeight, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalSpacerFixed = QSpacerItem(verticalSpacerWidth, verticalSpacerHeight, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.horizontalSpacerExpanding = QSpacerItem(horizontalSpacerWidth, horizontalSpacerHeight, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Create widget group frame
        self.formWidgetsFrame = QFrame()
        self.formWidgetsFrame.setObjectName("formWidgetsFrame")
        self.formWidgetsFrame.setMinimumWidth(formWidgetsFrameMinimumWidth)
        self.formWidgetsFrame.setMaximumWidth(formWidgetsFrameMaximumWidth)
        
        # Layout for the main view form
        self.formLayout = QVBoxLayout(self.formWidgetsFrame)
        
        # Title label
        self.titleLabel = QLabel()
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # E-mail field
        self.emailField = QLineEdit()
        self.emailField.setObjectName("emailField")
        self.emailField.setPlaceholderText("E-mail")
        self.emailField.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Password field
        self.passwordField = QLineEdit()
        self.passwordField.setObjectName("passwordField")
        self.passwordField.setPlaceholderText("Password")
        self.passwordField.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Repeat password field
        self.repeatPasswordField = QLineEdit()
        self.repeatPasswordField.setObjectName("repeatPasswordField")
        self.repeatPasswordField.setPlaceholderText("Repeat password")
        self.repeatPasswordField.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Log in button
        self.createAccountButton = QPushButton()
        self.createAccountButton.setObjectName("createAccountButton")
        self.createAccountButton.setMinimumHeight(buttonMinimumHeight)
        self.createAccountButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Navigation button to go back to the main view
        self.goBackButton = QPushButton()
        self.goBackButton.setObjectName("goBackButton")
        self.goBackButton.setMinimumHeight(buttonMinimumHeight)
        self.goBackButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Error message label
        self.errorLabel = QLabel()
        self.errorLabel.setObjectName("errorLabel")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.errorLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.errorLabel.setStyleSheet("color: red;")
        
        # Success message label
        self.successLabel = QLabel()
        self.successLabel.setObjectName("successLabel")
        self.successLabel.setAlignment(Qt.AlignCenter)
        self.successLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.successLabel.setStyleSheet("color: green;")
        
        # Setting up layout for the main view form
        self.formLayout.addItem(self.verticalSpacerExpanding)
        self.formLayout.addWidget(self.titleLabel)
        self.formLayout.addItem(self.verticalSpacerFixed)
        self.formLayout.addWidget(self.emailField)
        self.formLayout.addItem(self.verticalSpacerFixed)
        self.formLayout.addWidget(self.passwordField)
        self.formLayout.addItem(self.verticalSpacerFixed)
        self.formLayout.addWidget(self.repeatPasswordField)
        self.formLayout.addItem(self.verticalSpacerFixed)
        self.formLayout.addWidget(self.createAccountButton)
        self.formLayout.addItem(self.verticalSpacerFixed)
        self.formLayout.addWidget(self.goBackButton)
        self.formLayout.addItem(self.verticalSpacerFixed)
        self.formLayout.addWidget(self.errorLabel)
        self.formLayout.addItem(self.verticalSpacerFixed)
        self.formLayout.addWidget(self.successLabel)
        self.formLayout.addItem(self.verticalSpacerFixed)
        
        # Setting up horizontal layout for the main view window
        self.mainHorizontalLayout.addItem(self.horizontalSpacerExpanding)
        self.mainHorizontalLayout.addWidget(self.formWidgetsFrame)
        self.mainHorizontalLayout.addItem(self.horizontalSpacerExpanding)
        
        # Setting up vertical layout for the main view window
        self.mainVerticalLayout.addItem(self.verticalSpacerExpanding)
        self.mainVerticalLayout.addLayout(self.mainHorizontalLayout)
        self.mainVerticalLayout.addItem(self.verticalSpacerExpanding)
        
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.createAccountButton.setText(QCoreApplication.translate("logInView", "Create an account", None))
        self.goBackButton.setText(QCoreApplication.translate("logInView", "Go Back", None))
        self.titleLabel.setText(QCoreApplication.translate("logInView", "Create an account", None))
      
    def isEmailValid(self):
        self.email = self.emailField.text()
        if self.email == '':
            self.setError("E-mail cannot be empty")
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.emailField.text()):
            self.setError("Invalid e-mail address")
        elif self.email != '':
            self.connectToMysql()
            self.cursor.execute('use finedu')
            emailCheckQuery = ('select 1 from users where email = %s')
            self.cursor.execute(emailCheckQuery, (self.email,))
            emailCheckResult = self.cursor.fetchone()
            print(emailCheckResult)

            if emailCheckResult is not None:
                self.setError("E-mail already exists!")
            else:        
                self.errorLabel.setText("")
                self.successLabel.setText('')

            self.db.close()
        
    def isPasswordValid(self):
        password = self.passwordField.text()
        repeatedPassword = self.repeatPasswordField.text()
        if password == '':
            self.setError("Password cannot be empty")
        elif len(password) < passwordMinimumLength:
            self.setError(f"Password must be at least {passwordMinimumLength} characters long")
        elif not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*[#?!@$%^&*-]).{8,}$", self.passwordField.text()):
            self.setError("Password must contain at least 1 big letter,\n1 number and 1 special character")
        elif repeatedPassword == '':
            self.setError("Please repeat your password")
        elif password != repeatedPassword:
            self.setError("Passwords are not the same")
        else:
            self.errorLabel.setText('')   
            self.successLabel.setText('')
        
    def createAccount(self):
        self.isEmailValid()

        if self.errorLabel.text() == "":
            self.isPasswordValid()
        
        # No error messages, proceed to create account
        if self.errorLabel.text() == "":
            self.generateHashedPassword()
            self.connectToMysql()
            self.cursor.execute('use finedu')
            userInsertQuery = ('insert into users (email, pass, salt) values (%s, %s, %s)')
            userData = (self.email, self.hashedPassword, self.saltString,)  # Use string version
            self.cursor.execute(userInsertQuery, userData)
            self.db.commit()
            self.db.close()
            self.clearView()
            self.successLabel.setText("Account created successfully!")
            
    def generateHashedPassword(self):
        self.salt = [random.choice(string.printable) for _ in range(16)]
        self.saltString = ''.join(self.salt)  # Store as string for database
        saltEncoded = self.saltString.encode('utf-8')  # Encode for hashing
        password = self.passwordField.text().encode('utf-8')
        password = password + saltEncoded
        print(password)
        self.hashedPassword = hashlib.sha256(password).hexdigest()
        
    def clearView(self):
        self.emailField.setText('')
        self.passwordField.setText('')
        self.repeatPasswordField.setText('')
        self.errorLabel.setText('')
        self.successLabel.setText('')
        self.email = ''
        self.salt = ''
        self.saltString = ''
        self.hashedPassword = ''
    
    def setError(self, errorMessage):
        self.errorLabel.setText(errorMessage)
        self.successLabel.setText('')
        
    def setSuccess(self, successMessage):
        self.successLabel.setText(successMessage)
        self.errorLabel.setText('')
    
    def connectToMysql(self):
        try:
            self.db = mysql.connect(
                host="localhost",
                user="root",
                password="",
            )
            print("Connected to MySQL")
            self.cursor = self.db.cursor()
        except mysql.Error as err:
            print("Failed to connect to MySQL:", err)