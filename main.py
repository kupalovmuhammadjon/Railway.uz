from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import mysql.connector as myc
import sys
import re

con = myc.connect(host="localhost", user="root", password="root")
cursor = con.cursor()
user_id = 0

def connect_database():
    cursor.execute("create database if not exists Railways")
    cursor.execute("use Railways")
    
    cursor.execute("""create table if not exists 
    users(user_id int primary key auto_increment, name varchar(30), surname varchar(30),
    pas_seriya varchar(30), email varchar(50), password varchar(30))""")
    
    cursor.execute("""create table if not exists 
    trains(train_id int primary key auto_increment, bk_name varchar(50), authour varchar(30),
    price int)""")
    
    cursor.execute("""create table if not exists
    orders(order_id int primary key auto_increment, train_id int,user_id int)""")
    con.commit()
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF")
        self.setWindowTitle("Railways.uz")
        self.setWindowIcon(QIcon("icon.ico"))

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap('back.png')
        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)
        self.setMinimumSize(pixmap.width(), pixmap.height())
        self.setMaximumSize(pixmap.width(), pixmap.height())
        print(pixmap.width(), pixmap.height())
        
        backforth = QRadioButton(self.label)
        backforth.move(25, 700)
        backforth.setStyleSheet("background-color: transparent;")
        
        forth = QRadioButton(self.label)
        forth.move(25, 743)
        forth.setStyleSheet("background-color: transparent;")
        
        cur_location = QComboBox(self)
        cur_location.setGeometry(251, 695, 290, 76)
        cur_location.setStyleSheet("border-radius: 5px;")
        
        des_location = QComboBox(self)
        des_location.setGeometry(541, 695, 295, 76)
        des_location.setStyleSheet("border-radius: 5px;")
        
        self.goingdate = QLineEdit(self)
        self.goingdate.setGeometry(860, 695, 293, 76)
        self.goingdate.setFont(QFont("Montserrat", 12))
        self.goingdate.setPlaceholderText("Going date (2024-10-24)")
        # self.goingdate.setStyleSheet("border-radius: 5px;")
        
        self.comingdate = QLineEdit(self)
        self.comingdate.setGeometry(1153, 695, 293, 76)
        self.comingdate.setFont(QFont("Montserrat", 12))
        self.comingdate.setPlaceholderText("Coming date (2024-10-24)")
        # self.comingdate.setStyleSheet("border-radius: 5px;")
        
        findTickets = QPushButton("Find tickets", self)
        findTickets.setGeometry(1473, 696, 234, 64)
        findTickets.setStyleSheet("border-radius: 30px; background-color: #2E77CC;")
        findTickets.setFont(QFont("Montserrat", 12))
        
        

        
    
    
    def user_info(self):
        query = """select name, surname from users where user_id = %s"""
        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
        self.name = data[0][0]
        self.surname = data[0][1]
    
    def isBooksEmpty(self):
        cursor.execute("select * from books")
        data = cursor.fetchall()
        if len(data) == 0:
            return False
        else:
            return True
        


class Myorders(QDialog):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setMinimumSize(700, 700)
        self.setMaximumSize(700, 700)
        self.setStyleSheet("background-color: #EAFFFF")
        self.setWindowTitle("Order List")
        self.setWindowIcon(QIcon("icon.ico"))

        self.place_order_labels()

    def place_order_labels(self):
        scroll_area = QScrollArea(self)
        scroll_area.setGeometry(10, 10, 680, 680)

        scroll_contents = QWidget()
        scroll_area.setWidget(scroll_contents)
        scroll_layout = QVBoxLayout(scroll_contents)

        for i in range(len(self.data)):
            name = QLabel(self.data[i][0])
            units = QLabel(str(self.data[i][1]))
            price = QLabel(str(self.data[i][2]))

            # Add labels to the layout
            scroll_layout.addWidget(name)
            scroll_layout.addWidget(units)
            scroll_layout.addWidget(price)

        scroll_contents.setLayout(scroll_layout)
        scroll_area.setWidgetResizable(True)


        
            
        
class TemporaryWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(450, 700)
        self.setMaximumSize(450, 700)
        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("icon.ico"))

        label = QLabel(self)
        label.setGeometry(25, 100, 400, 400)
        movie = QMovie('welcome.gif')
        movie.setScaledSize(label.size())
        label.setMovie(movie)
        movie.start()

        QTimer.singleShot(7000, self.close)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.show_temporary_window()
        connect_database()
        self.main_window = None
        self.show_main_window()
        self.setMinimumSize(450, 700)
        self.setMaximumSize(450, 700)
        self.setStyleSheet("background-color: #EAFFFF")
        self.setWindowTitle("Railways.uz")
        self.setWindowIcon(QIcon("icon.ico"))

        self.loginlb = QLabel(self)
        self.loginlb.setGeometry(150, 150, 150, 50)
        self.loginlb.setText("Login")
        self.loginlb.setFont(QFont("Montserrat", 20, weight=65))

        self.email_error = QLabel(self)
        self.email_error.setGeometry(50, 200, 250, 50)
        self.email_error.setFont(QFont("Montserrat", 9))
        self.email_error.setStyleSheet("color: red")
        
        
        self.email_edit = QLineEdit(self)
        self.email_edit.setGeometry(50, 250, 350, 50)
        self.email_edit.setFont(QFont("Montserrat", 12))
        self.email_edit.setPlaceholderText("Email")
        self.email_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        self.password_edit = QLineEdit(self)
        self.password_edit.setGeometry(50, 320, 350, 50)
        self.password_edit.setFont(QFont("Montserrat", 12))
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")
        
        self.pas_error = QLabel(self)
        self.pas_error.setGeometry(50, 370, 400, 100)
        self.pas_error.setFont(QFont("Montserrat", 8))
        self.pas_error.setStyleSheet("color: red")

        self.loginbtn = QPushButton("Login", self)
        self.loginbtn.setGeometry(50, 450, 350, 45)
        self.loginbtn.setFont(QFont("Montserrat", 12))
        self.loginbtn.setStyleSheet("border-radius: 10px; background-color: #B5FFFF")
        self.loginbtn.clicked.connect(self.check_login)

        self.regbtn = QPushButton("Register", self)
        self.regbtn.setGeometry(50, 510, 350, 45)
        self.regbtn.setFont(QFont("Montserrat", 12))
        self.regbtn.setStyleSheet("border-radius: 10px; background-color: #B5FFFF")
        self.regbtn.clicked.connect(self.showRegwindow)
        

    def show_temporary_window(self):
        temporary_window = TemporaryWindow()
        temporary_window.exec_()
        
        
        
    def check_login(self):
        self.__email = self.email_edit.text().strip()
        self.__password = self.password_edit.text().strip()
        
        if len(self.__email) == 0 or len(self.__password) == 0:
            self.email_error.setText("Fields must be filled")
        
        else:
            self.email_error.setText("")
            self.check_password(self.__password)
            self.check_email(self.__email)
        
        error1 = self.email_error.text().strip()
        error2 = self.pas_error.text().strip()
        if len(error1) == 0 and len(error2) == 0:
            self.check_data()
    
    def check_data(self):
        query = "SELECT user_id FROM users WHERE email = %s AND password = %s"

        try:
            cursor.execute(query, (self.__email, self.__password))
            data = cursor.fetchall()

            if len(data) > 0:
                global user_id
                user_id = data[0][0]
                self.show_main_window()
            else:
                self.email_error.setText("User does not exist")

        except myc.Error as e:
            print(f"Error: {e}")

    def show_main_window(self):
        
        self.close()

        if self.main_window is None:
            self.main_window = MainWindow()
            self.main_window.show()


            
    def check_email(self, email):
        reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not (re.fullmatch(reg, email)):
            self.email_error.setText("invalid email")
        else:
            self.email_error.setText("")
            
    def check_password(self, password):
        
        alpha = 0
        digits = 0
        symb = 0
        
        for i in password:
            if i.isdigit():
                digits += 1
            elif i.isalpha():
                alpha += 1
            else:
                symb += 1
        
        if not (alpha >= 6 and digits >= 1 and symb >= 1):
            self.pas_error.setText("Password must contain at least six alpha characters\none digit and one symbol")
        else:
            self.pas_error.setText("")
    
    
    def showRegwindow(self):
        reg = RegistrationWindow()
        if reg.exec_() == QDialog.Accepted:
            self.show()
        else:
            self.close()
    
        

class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()
        connect_database()
        self.setMinimumSize(450, 700)
        self.setMaximumSize(450, 700)
        self.setStyleSheet("background-color: #EAFFFF")
        self.setWindowTitle("Book Store")
        self.setWindowIcon(QIcon("icon.ico"))

        self.namelb = QLabel(self)
        self.namelb.setGeometry(50, 20, 300, 40)
        self.namelb.setFont(QFont("Montserrat", 10))
        self.namelb.setStyleSheet("color:red")

        self.name_edit = QLineEdit(self)
        self.name_edit.setGeometry(50, 60, 350, 50)
        self.name_edit.setFont(QFont("Montserrat", 12))
        self.name_edit.setPlaceholderText("Name")
        self.name_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        self.surnamelb = QLabel(self)
        self.surnamelb.setGeometry(50, 110, 320, 40)
        self.surnamelb.setFont(QFont("Montserrat", 10))
        self.surnamelb.setStyleSheet("color:red")
        
        self.surname_edit = QLineEdit(self)
        self.surname_edit.setGeometry(50, 150, 350, 50)
        self.surname_edit.setFont(QFont("Montserrat", 12))
        self.surname_edit.setPlaceholderText("Surname")
        self.surname_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")
        
        self.passeriyalb = QLabel(self)
        self.passeriyalb.setGeometry(50, 200, 320, 40)
        self.passeriyalb.setFont(QFont("Montserrat", 10))
        self.passeriyalb.setStyleSheet("color:red")
        
        self.passeriya_edit = QLineEdit(self)
        self.passeriya_edit.setGeometry(50, 240, 350, 50)
        self.passeriya_edit.setFont(QFont("Montserrat", 12))
        self.passeriya_edit.setPlaceholderText("Passport Number")
        self.passeriya_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")
        
        self.emaillb = QLabel(self)
        self.emaillb.setGeometry(50, 290, 200, 40)
        self.emaillb.setFont(QFont("Montserrat", 10))
        self.emaillb.setStyleSheet("color:red")

        self.email_edit = QLineEdit(self)
        self.email_edit.setGeometry(50, 330, 350, 50)
        self.email_edit.setFont(QFont("Montserrat", 12))
        self.email_edit.setPlaceholderText("Email")
        self.email_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        self.passwordlb = QLabel(self)
        self.passwordlb.setGeometry(50, 380, 360, 40)
        self.passwordlb.setFont(QFont("Montserrat", 10))
        self.passwordlb.setStyleSheet("color:red")
        
        self.password_edit = QLineEdit(self)
        self.password_edit.setGeometry(50, 430, 350, 50)
        self.password_edit.setFont(QFont("Montserrat", 12))
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        self.repasswordlb = QLabel(self)
        self.repasswordlb.setGeometry(50, 480, 250, 40)
        self.repasswordlb.setFont(QFont("Montserrat", 10))
        self.repasswordlb.setStyleSheet("color:red")
        
        self.repassword_edit = QLineEdit(self)
        self.repassword_edit.setGeometry(50, 520, 350, 50)
        self.repassword_edit.setFont(QFont("Montserrat", 12))
        self.repassword_edit.setPlaceholderText("Re-enter Password")
        self.repassword_edit.setStyleSheet("border: 1px solid #00FFFF; border-radius: 10px")

        register_button = QPushButton("Register", self)
        register_button.setGeometry(50, 600, 350, 45)
        register_button.setFont(QFont("Montserrat", 12))
        register_button.setStyleSheet("border-radius: 10px; background-color: #B5FFFF")
        register_button.clicked.connect(self.register_button_clicked)

    def register_button_clicked(self):
        
        registration_successful = self.check_info()

        if registration_successful:
            self.accept()  # Set the result to QDialog.Accepted
            
    def check_info(self):
        
        self.__name = self.name_edit.text().strip()
        self.__surname = self.surname_edit.text().strip()
        self.__pass_seriya = self.passeriya_edit.text().strip()
        self.__email = self.email_edit.text().strip()
        self.__password = self.password_edit.text().strip()
        self.__repassword = self.repassword_edit.text().strip()
        isValid = 1
        
        if len(self.__name) < 3:
            self.namelb.setText("Name cannot be that much short")
            isValid = 0
        
        if len(self.__surname) < 3:
            self.surnamelb.setText("Surname cannot be that much short")
            isValid = 0
            
        if len(self.__pass_seriya) < 3:
            self.passeriyalb.setText("Passport seria cannot be much short")
            isValid = 0
        
        reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not (re.fullmatch(reg, self.__email)):
            self.emaillb.setText("Invalid email address")
            isValid = 0
        
        if self.check_password(self.__password):
            isValid = 0
        
        if not self.check_password(self.__password) and self.__password != self.__repassword:
            self.repasswordlb.setText("Password does not match")
            isValid = 0
        
        if isValid:
            if self.check_data():
                self.emaillb.setText("User already exists")
                QTimer.singleShot(5000, self.accept)
                return 0
            
            self.write_data()
            return True
        
        else:
            return False
    
    def check_data(self):
        query = "SELECT user_id FROM users WHERE email = %s"

        try:
            cursor.execute(query, (self.__email,))
            data = cursor.fetchall()
            
            if len(data) > 0:
                return 1
            else:
                return 0

        except myc.Error as e:
            print(f"Error: {e}")
        
    def check_password(self, password):
        
        alpha = 0
        digits = 0
        symb = 0
        
        for i in password:
            if i.isdigit():
                digits += 1
            elif i.isalpha():
                alpha += 1
            else:
                symb += 1
        
        if not (alpha >= 6 and digits >= 1 and symb >= 1):
            self.passwordlb.setText("Password must contain at least six alpha characters\none digit and one symbol")
            return 1
        else:
            return 0
    
    def write_data(self):
        
        query = f"""insert into users(name, surname,pas_seriya, email, password) values(%s, %s, %s, %s, %s)"""
        values = (self.__name, self.__surname,self.__pass_seriya, self.__email, self.__password)
        cursor.execute(query, values)
        con.commit()
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = LoginWindow()
    win.show()

    sys.exit(app.exec_())

