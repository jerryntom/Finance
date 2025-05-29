from PySide6.QtCore import QMetaObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QWidget, QVBoxLayout, QStackedWidget)
import os
import sys
from QtViews.MainUI import MainView
from QtViews.LogInUI import LogInView
from QtViews.CreateUserAccountUI import CreateAccountView
from QtViews.DashboardUI import DashboardView
from QtViews.TransactionsViewUI import TransactionView

# Size contants for layout
initWidth = 800
initHeight = 600
horizontalSpacerWidth = 40    
horizontalSpacerHeight = 20
verticalSpacerWidth = 20
verticalSpacerHeight = 10
formWidgetsFrameMinimumWidth = 250
formWidgetsFrameMaximumWidth = 400
logInButtonMinimumHeight = 50

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainWindow():
    def setupUi(self, mainWindow):
        #Set up the main window
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(initWidth, initHeight)
        self.centralWidget = QWidget(mainWindow)
        self.centralWidget.setObjectName("centralWidget")
        mainWindow.setCentralWidget(self.centralWidget)
        
        # Set up navigation as stacked widget
        self.navigation = QStackedWidget(self.centralWidget)
        self.navigation.setObjectName("navigation")
        
        # Add vertical layout to the main window
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.addWidget(self.navigation)
        
        # Set up main view
        self.mainView = MainView()
        self.mainView.setUpUI()
        self.mainView.logInButton.clicked.connect(lambda: self.showLoginView())
        self.mainView.registerButton.clicked.connect(lambda: self.showCreateAccountView())
        
        # Set up log in view
        self.logInView = LogInView()
        self.logInView.setUpUI()
        self.logInView.logInButton.clicked.connect(self.handleLogin)
        self.logInView.goBackButton.clicked.connect(lambda: self.showMainView())
        
        # Set up create account view
        self.createAccountView = CreateAccountView()
        self.createAccountView.setUpUI()
        self.createAccountView.createAccountButton.clicked.connect(lambda: self.createAccountView.createAccount())
        self.createAccountView.goBackButton.clicked.connect(lambda: self.navigation.setCurrentWidget(self.mainView))
        
        # Set up dashboard view
        self.dashboardView = DashboardView()
        self.dashboardView.setUpUI()
        self.dashboardView.logoutButton.clicked.connect(self.handleLogout)

        # Set up transaction view
        self.transactionView = TransactionView()
        self.transactionView.goBackButton.clicked.connect(lambda: self.showDashboardView())

        # Add views to navigation
        self.navigation.addWidget(self.mainView)
        self.navigation.addWidget(self.logInView)
        self.navigation.addWidget(self.createAccountView)
        self.navigation.addWidget(self.dashboardView)
        self.navigation.addWidget(self.transactionView)
        self.navigation.setCurrentWidget(self.mainView)
        
        mainWindow.setWindowTitle("FinEdu")
        mainWindow.setWindowIcon(QIcon(resource_path("icon.png")))
        QMetaObject.connectSlotsByName(mainWindow)
    
    def handleLogin(self):
        user_id = self.logInView.logIn()
        if user_id:
            print(f"User ID: {user_id}")
            self.dashboardView.setUserId(user_id)
            self.showDashboardView()
    
    def handleLogout(self):
        self.showMainView()
    
    def showMainView(self):
        self.navigation.setCurrentWidget(self.mainView)
        
    def showCreateAccountView(self):
        self.createAccountView.clearView()
        self.navigation.setCurrentWidget(self.createAccountView)

    def showLoginView(self):
        self.logInView.clearView()
        self.navigation.setCurrentWidget(self.logInView)
    
    def showDashboardView(self):
        self.dashboardView.loadAccountsFromDB()
        self.navigation.setCurrentWidget(self.dashboardView)

    def showTransactionView(self, account_id, transactions):
        self.transactionView.setAccount(account_id, transactions)
        self.navigation.setCurrentWidget(self.transactionView)


class MainWindowSetUp(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindowSetUp, self).__init__(parent)
        self.mainWindow = MainWindow()
        self.mainWindow.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindowSetUp()
    mainWindow.show()
    sys.exit(app.exec())