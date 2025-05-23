from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QStackedWidget)
import sys
from QtViews.MainUI import MainView
from QtViews.LogInUI import LogInView
from QtViews.CreateAccountUI import CreateAccountView
from QtViews.DashboardUI import DashboardView

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

        # Add views to navigation
        self.navigation.addWidget(self.mainView)
        self.navigation.addWidget(self.logInView)
        self.navigation.addWidget(self.createAccountView)
        self.navigation.addWidget(self.dashboardView)
        self.navigation.setCurrentWidget(self.mainView)
        
        mainWindow.setWindowTitle("FinEdu")
        QMetaObject.connectSlotsByName(mainWindow)
    
    def handleLogin(self):
        self.user_id = self.logInView.logIn()
        if self.user_id:
            print(f"User ID: {self.user_id}")
            self.dashboardView.setUserId(self.user_id)
            self.showDashboardView()
    
    def loadUserDashboard(self):
        # Clear existing accounts
        self.dashboardView.clearAccounts()
        
        # Add mock accounts
        self.dashboardView.addAccount("Checking Account", 2435.67, "Checking")
        self.dashboardView.addAccount("Savings Account", 12750.42, "Savings")
        self.dashboardView.addAccount("Investment Account", 45320.18, "Investment")
        self.dashboardView.addAccount("Credit Card", -1250.30, "Credit")
    
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
        self.navigation.setCurrentWidget(self.dashboardView)

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