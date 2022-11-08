import sys
from os.path import dirname, abspath

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QDesktopWidget
from PyQt5 import QtCore

from appUI import Ui_DialogAPP
from loginUI import Ui_Dialog
from registerUI import Ui_DialogRegister

parent_dir = dirname(dirname(abspath(__file__)))
sys.path.append(parent_dir)
from core.connections import UserService, PersonScraped


class MainWindow(QDialog, Ui_Dialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.center()
        self.close_btn.clicked.connect(lambda: self.close())
        self.pushButton.clicked.connect(self.connect_to_db)
        self.register_button.clicked.connect(self.go_to_register)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def connect_to_db(self):
        if len(self.email_field.text()) == 0:
            self.label_input.setText("Please type your email")
            self.label_input.adjustSize()
        elif len(self.password_field.text()) == 0:
            self.label_input.setText("Please type your password")
            self.label_input.adjustSize()
        elif UserService().login(email=self.email_field.text(), password=self.password_field.text()) == 200:
            self.go_to_app()
        elif UserService().login(email=self.email_field.text(), password=self.password_field.text()) == 400:
            self.label_input.setText("Email or password is incorrect")
            self.label_input.adjustSize()
        elif UserService().login(email=self.email_field.text(), password=self.password_field.text()) == 404:
            self.label_input.setText("You don't have an account")
            self.label_input.adjustSize()

    def go_to_register(self):
        self.close()
        register_window.show()

    def go_to_app(self):
        self.close()
        app_ui.show()


class RegisterWindow(QWidget, Ui_DialogRegister):

    def __init__(self):
        super(RegisterWindow, self).__init__()
        self.setupUi(self)
        self.center()
        self.close_btn.clicked.connect(lambda: self.close())
        self.pushButton.clicked.connect(self.register)
        self.back_button.clicked.connect(self.go_to_login)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def register(self):
        if len(self.email_field.text()) == 0:
            self.label_input_2.setText("Please type your email ")
            self.label_input_2.adjustSize()

        elif len(self.password_field.text()) == 0 and len(self.password_field_2.text()) == 0:
            self.label_input_2.setText("Please type your password")
            self.label_input_2.adjustSize()

        elif self.password_field.text() != self.password_field_2.text():
            self.label_input_2.setText("Passwords don't match")
            self.label_input_2.adjustSize()

        elif UserService().search(email=self.email_field.text()):
            self.label_input_2.setText("Account already exists")
            self.label_input_2.adjustSize()

        else:
            self.label_input_2.setStyleSheet("color: green;")
            self.label_input_2.setText("Account successfully created")
            UserService().register(email=self.email_field.text(), password=self.password_field.text())
            self.close()
            main_window.show()
        self.label_input_2.setAlignment(QtCore.Qt.AlignCenter)

    def go_to_login(self):
        self.close()
        main_window.show()


class Application(QDialog, Ui_DialogAPP):
    def __init__(self):
        super(Application, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.scrape)
        self.pushButton_2.clicked.connect(self.search_db)

    def scrape(self):
        if len(self.lineEdit.text()) == 0:
            self.label_2.setText("Please insert a link")
            self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        else:
            PersonScraped().take_data(link=self.lineEdit.text())
            self.label_2.setText("Scraped")
            self.label_2.setAlignment(QtCore.Qt.AlignCenter)


    def search_db(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    app_ui = Application()
    register_window = RegisterWindow()
    main_window.show()
    app.exec_()
