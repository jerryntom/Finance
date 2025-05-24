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

# DB columns numbers
hashedPasswordColumn = 0
saltColumn = 1

class LogInView(QWidget):
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
        
        # Log in button
        self.logInButton = QPushButton()
        self.logInButton.setObjectName("logInButton")
        self.logInButton.setMinimumHeight(buttonMinimumHeight)
        self.logInButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
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
        self.formLayout.addWidget(self.logInButton)
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
        self.logInButton.setText(QCoreApplication.translate("logInView", "Log in", None))
        self.goBackButton.setText(QCoreApplication.translate("logInView", "Go Back", None))
        self.titleLabel.setText(QCoreApplication.translate("logInView", "Log in to your account", None))
        
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

            if emailCheckResult is None:
                self.setError("Invalid e-mail address")
            else:        
                self.setError("")
                self.setSuccess("")
                
            self.db.close()
        
    def isPasswordValid(self):
        password = self.passwordField.text()
        
        if password == '':
            self.setError("Password cannot be empty")
        else:
            self.connectToMysql()
            self.cursor.execute('use finedu')
            accountCredentialsQuery = ('select pass, salt from users where email = %s')
            self.cursor.execute(accountCredentialsQuery, (self.email,))
            accountCredentials = self.cursor.fetchone()

            password = password.encode('utf-8')
            salt = accountCredentials[saltColumn].encode('utf-8')
            password = password + salt
            print(password)
            passwordTest = hashlib.sha256(password).hexdigest()
            hashedPassword = accountCredentials[hashedPasswordColumn]
            
            print(passwordTest, hashedPassword)
            
            if passwordTest != hashedPassword:
                self.setError("Invalid password")
            else:
                self.setError("")
                self.setSuccess("")

            self.db.close()

        
    def logIn(self):
        self.isEmailValid()

        if self.errorLabel.text() == "":
            self.isPasswordValid()
        
        # No error messages, proceed to log in procedure
        if self.errorLabel.text() == "":
            self.getUserId()
            self.clearView()
            self.setSuccess('Logged in successfully!')
            return self.user_id
        else:
            self.setError('Log in failed!')
            return None
            
    def clearView(self):
        self.emailField.setText('')
        self.passwordField.setText('')
        self.errorLabel.setText('')
        self.successLabel.setText('')
        self.email = ''
        self.salt = ''
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
                database="finedu"
            )
            print("Connected to MySQL")
            self.cursor = self.db.cursor()
        except mysql.Error as err:
            print("Failed to connect to MySQL:", err)
            
    def getUserId(self):
        """Return the user_id for the currently logged-in user (by email)."""
        email = self.emailField.text() if hasattr(self, 'emailField') else getattr(self, 'email', None)
        if not email:
            return None
        try:
            self.connectToMysql()
            self.cursor.execute('SELECT user_id FROM users WHERE email = %s', (email,))
            result = self.cursor.fetchone()
            self.db.close()
            if result:
                self.user_id = result[0]
        except Exception as e:
            print(f"Error fetching user_id: {e}")
        return None