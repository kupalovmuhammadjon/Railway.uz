        
        
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import mysql.connector as myc
from datetime import datetime
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
    trains(train_id int primary key auto_increment, tr_name varchar(50),
    cur_city varchar(50), going_date date, time varchar(30), avb_seats int, price int)""")
    
    cursor.execute("""create table if not exists
    orders(order_id int primary key auto_increment, train_id int, user_id int, 
    dest_city varchar(30))""")
    con.commit()
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        regions = ["Nukus", "Xorazm", "Buxoro", "Navoiy", "Jizzax", "Termiz", "Toshkent",
                   "Guliston", "Farg'ona", "Andijon", "Namangan", ]
        self.back_forth = True
        self.insertAvailableTrains()
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
        
        
        self.backforth = QRadioButton(self.label)
        self.backforth.move(25, 700)
        self.backforth.setStyleSheet("background-color: transparent;")
        self.backforth.setChecked(True)
        self.backforth.toggled.connect(self.forthback)

        self.forth = QRadioButton(self.label)
        self.forth.move(25, 743)
        self.forth.setStyleSheet("background-color: transparent;")
        self.forth.toggled.connect(self.forths)
        
        self.loc_error = QLabel(self)
        self.loc_error.setGeometry(251, 645, 300, 40)
        self.loc_error.setFont(QFont("Montserrat", 12))
        self.loc_error.setStyleSheet("color: red; background-color: transparent;")
        
        self.cur_location = QComboBox(self)
        self.cur_location.setGeometry(251, 695, 290, 76)
        self.cur_location.setFont(QFont("Montserrat", 12))
        self.cur_location.setStyleSheet("border-radius: 5px;")
        self.cur_location.addItems(regions)
        
        self.des_location = QComboBox(self)
        self.des_location.setGeometry(541, 695, 295, 76)
        self.des_location.setFont(QFont("Montserrat", 12))
        self.des_location.setStyleSheet("border-radius: 5px;")
        self.des_location.addItems(regions)
        
        self.date_error = QLabel(self)
        self.date_error.setGeometry(860, 645, 300, 40)
        self.date_error.setFont(QFont("Montserrat", 12))
        self.date_error.setStyleSheet("color: red; background-color: transparent;")
        
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
        
        self.findTickets = QPushButton("Find tickets", self)
        self.findTickets.setGeometry(1473, 696, 234, 64)
        self.findTickets.setStyleSheet("border-radius: 30px; background-color: #2E77CC;")
        self.findTickets.setFont(QFont("Montserrat", 12))
        self.findTickets.clicked.connect(self.checkInput)
        
        self.myTickets = QPushButton("My tickets", self)
        self.myTickets.setGeometry(800, 780, 150, 50)
        self.myTickets.setStyleSheet("border-radius: 25px; background-color: #2E77CC;")
        self.myTickets.setFont(QFont("Montserrat", 12))
        self.myTickets.clicked.connect(self.showTickets)
        
        
        
    def forths(self):
        self.back_forth = False
        self.comingdate.setPlaceholderText("")
        self.comingdate.setEnabled(False)
    
    def forthback(self):
        self.back_forth = True
        self.comingdate.setPlaceholderText("Coming date (2024-10-24)")
        self.comingdate.setEnabled(True)
    
        
    def insertAvailableTrains(self):
        
        if self.isTrainsEmpty():
            return
        
        query = """insert into trains (tr_name, cur_city, going_date, time, avb_seats, price)
        values (%s, %s, %s, %s, %s, %s)"""
        values = ("Afrosiyob", "Xorazm","2024-02-11", "19:00", 100, 200000)
        cursor.execute(query, values)
        
        query = """insert into trains (tr_name, cur_city, going_date, time, avb_seats, price)
        values (%s, %s, %s, %s, %s, %s)"""
        values = ("PKD-234-345", "Toshkent","2024-03-28", "15:00", 80, 100000)
        cursor.execute(query, values)
        
        query = """insert into trains (tr_name, cur_city, going_date, time, avb_seats, price)
        values (%s, %s, %s, %s, %s, %s)"""
        values = ("Afrosiyob", "Buxoro", "2024-02-17", "22:00", 140, 220000)
        cursor.execute(query, values)
        
        query = """insert into trains (tr_name, cur_city, going_date, time, avb_seats, price)
        values (%s, %s, %s, %s, %s, %s)"""
        values = ("QSHAK", "Nukus", "2024-05-15", "09:00", 111, 111222)
        cursor.execute(query, values)
        
        query = """insert into trains (tr_name, cur_city, going_date, time, avb_seats, price)
        values (%s, %s, %s, %s, %s, %s)"""
        values = ("Afrosiyob", "Termiz", "2024-04-21", "12:00", 200, 150000)
        cursor.execute(query, values)
        
        query = """insert into trains (tr_name, cur_city, going_date, time, avb_seats, price)
        values (%s, %s, %s, %s, %s, %s)"""
        values = ("KALAYDI", "Xorazm", "2024-11-11", "11:00", 124, 204522)
        cursor.execute(query, values)
        
        query = """insert into trains (tr_name, cur_city, going_date, time, avb_seats, price)
        values (%s, %s, %s, %s, %s, %s)"""
        values = ("LUKSSHINE","Toshkent", "2024-3-14", "13:20", 111, 777777)
        cursor.execute(query, values)
        
        query = """insert into trains (tr_name, cur_city, going_date, time, avb_seats, price)
        values (%s, %s, %s, %s, %s, %s)"""
        values = ("CHEAQA","Toshkent", "2024-3-14", "16:45", 99, 222222)
        cursor.execute(query, values)
        
        con.commit()
    
    
    def isTrainsEmpty(self):
        cursor.execute("select * from trains")
        data = cursor.fetchall()
        if len(data) == 0:
            return False
        else:
            return True
    
    def checkInput(self):
        cur = self.cur_location.currentText()
        des = self.des_location.currentText()
        if self.back_forth:
            try:
                goingdate = self.goingdate.text().strip()
                goingdate = datetime.strptime(goingdate, "%Y-%m-%d")
                comingdate = self.comingdate.text().strip()
                comingdate = datetime.strptime(comingdate, "%Y-%m-%d")
                current_date = datetime.now()
            except:
                self.date_error.setText("Invalid date range")
                return
        else:
            comingdate = self.comingdate.text().strip()
            try:
                goingdate = self.goingdate.text().strip()
                goingdate = datetime.strptime(goingdate, "%Y-%m-%d")
                current_date = datetime.now()
            except:
                self.date_error.setText("Invalid date range")
                return
            
        
        if len(des) == 0 or len(cur) == 0:
            self.loc_error.setText("Fields must be filled")
            return
        else:
            if cur == des:
                self.loc_error.setText("Cities have to be different")
                return
            else:
                self.loc_error.setText("")
        
        if len(str(goingdate)) == 0 or len(str(comingdate)) == 0 and self.back_forth:
            self.date_error.setText("Fields must be filled")
            return
        
        try:
            if self.back_forth and ((len(str(goingdate)) == 0 or len(str(comingdate)) == 0)) or \
                (goingdate < current_date or goingdate >= comingdate):
                    self.date_error.setText("Invalid date range")
                    return
            else:
                self.date_error.setText("")
        except:
            self.date_error.setText("Invalid date range")
            
            
            
        if (len(str(goingdate)) == 0 or goingdate < current_date) and not self.back_forth:
            self.date_error.setText("Fields must be filled")
            return
        
        else:
            self.date_error.setText("")
            
        if not self.back_forth: 
            query = """SELECT tr_name, cur_city, going_date, time, avb_seats, price FROM trains
            WHERE cur_city = %s AND going_date = %s"""
            cursor.execute(query, (cur, goingdate)) 


            forthtrains = cursor.fetchall()
            avt = AvailableTickets(forthtrains, cur, des)
            avt.exec_()
            
        elif self.back_forth:
            query = """select tr_name, cur_city, going_date, time, avb_seats, price from trains
            where cur_city = %s and going_date = %s"""
            cursor.execute(query, (cur, goingdate))
            goingtrains = cursor.fetchall()
            
            query2 = """select tr_name, cur_city, going_date, time, avb_seats, price from trains
            where cur_city = %s and going_date = %s"""
            cursor.execute(query2, (des, comingdate))
            comingtrains = cursor.fetchall()
        
            avt = AvailableTickets(goingtrains, cur, des, comingtrains)
            avt.exec_()
    
    def showTickets(self):
        
        query = """ select t.cur_city, o.dest_city, t.going_date, t.time,  t.price from trains as t
        left join orders as o on t.train_id = o.train_id
        where o.user_id = %s"""
        cursor.execute(query, (user_id,))
        tickets_ls = cursor.fetchall()
        
        MyTicketsList = MyTickets(tickets_ls)
        MyTicketsList.exec_()
        

class AvailableTickets(QDialog):
    def __init__(self, goingtrains, cur, des, comingtrains=None):
        super().__init__()
        self.goingtrains = goingtrains
        self.cur = cur
        self.des = des
        self.comingtrains = comingtrains if comingtrains else []
        self.goingbtns = []
        self.comingbtns = []
        self.setMinimumSize(1000, 700)
        self.setMaximumSize(1000, 700)
        self.setStyleSheet("background-color: #FFFFFF")
        self.setWindowTitle("Available Tickets")
        self.setWindowIcon(QIcon("icon.ico"))

        self.layout = QVBoxLayout(self)

        self.going_scroll_area = QScrollArea(self)
        self.going_scroll_area.setWidgetResizable(True)
        self.going_scroll_area_content = QWidget(self.going_scroll_area)
        self.going_scroll_area_layout = QVBoxLayout(self.going_scroll_area_content)
        self.going_scroll_area.setWidget(self.going_scroll_area_content)

        self.layout.addWidget(QLabel("Going Trains  |  Train Name  | Going city | Going date | Time | Price | Destination"))
        self.layout.addWidget(self.going_scroll_area)

        if self.comingtrains:
            self.coming_scroll_area = QScrollArea(self)
            self.coming_scroll_area.setWidgetResizable(True)
            self.coming_scroll_area_content = QWidget(self.coming_scroll_area)
            self.coming_scroll_area_layout = QVBoxLayout(self.coming_scroll_area_content)
            self.coming_scroll_area.setWidget(self.coming_scroll_area_content)

            self.layout.addWidget(QLabel("Coming Trains |  Train Name  | Going city | Going date | Time | Price | Destination"))
            self.layout.addWidget(self.coming_scroll_area)
            self.place_coming_buttons()

        self.place_going_buttons()

        orderbtn = QPushButton("Order")
        orderbtn.setGeometry(450, 650, 100, 40)
        orderbtn.setStyleSheet("background-color: #94F9FF")
        orderbtn.clicked.connect(self.place_order)
        self.layout.addWidget(orderbtn)

    def place_going_buttons(self):
        for i in self.goingtrains:
            btntext = "  |  ".join(map(str, i))
            btntext += "  |  " + self.des
            btn = QPushButton(btntext, self)
            btn.setFont(QFont("Montserrat", 10))
            btn.setStyleSheet("background-color: #94F9FF")
            btn.setFixedHeight(40)
            btn.clicked.connect(lambda _, btn=btn: self.going_checked(btn))
            self.goingbtns.append(btn)
            self.going_scroll_area_layout.addWidget(btn)

    def place_coming_buttons(self):
        for i in self.comingtrains:
            btntext = "  |  ".join(map(str, i))
            btntext += "  |  " + self.cur
            btn = QPushButton(btntext, self)
            btn.setFont(QFont("Montserrat", 10))
            btn.setFixedHeight(40)
            btn.setStyleSheet("background-color: #94F9FF")
            btn.clicked.connect(lambda _, btn=btn: self.coming_checked(btn))
            self.comingbtns.append(btn)
            self.coming_scroll_area_layout.addWidget(btn)

    def going_checked(self, btn):
        for i in self.goingbtns:
            i.setFixedHeight(40)
            i.setStyleSheet("border: 0px solid; background-color: #94F9FF")
        btn.setFixedHeight(40)
        btn.setStyleSheet("border: 2px solid; background-color: #94F9FF")

    def coming_checked(self, btn):
        for i in self.comingbtns:
            i.setFixedHeight(40)
            i.setStyleSheet("border: 0px solid; background-color: #94F9FF")
        btn.setFixedHeight(40)
        btn.setStyleSheet("border: 2px solid; background-color: #94F9FF")
        
    
    def place_order(self):
        going = None
        coming = None
        try:
            if self.goingtrains:
                for i in self.goingbtns:
                    button_style = i.styleSheet()
                    if 'border: 2px solid' in button_style:
                        going = i
                        
            if self.comingtrains:
                for i in self.comingbtns:
                    button_style = i.styleSheet()
                    if 'border: 2px solid' in button_style:
                        coming = i
                        
            goingtxt = going.text().split("|")        
            comingtxt = coming.text().split("|") 
        except:
            if not self.comingtrains:
                self.single_order()
            return
        
        if int(goingtxt[4]) == 0:
            msg = QMessageBox(self)
            msg.setWindowTitle("No tickets found")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No tickets found\nTrain is full")
        
        if int(comingtxt[4]) == 0:
            msg = QMessageBox(self)
            msg.setWindowTitle("No tickets found")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No tickets found,\nTrain is full")
            
        #['Afrosiyob  ', '  Xorazm  ', '  2024-02-11  ', '  19:00  ', '  100  ', '  200000  ', '  Toshkent']   
        going_query = """SELECT train_id FROM trains
                          WHERE tr_name = %s AND cur_city = %s AND time = %s AND price = %s"""
        going_values = (goingtxt[0].strip(), goingtxt[1].strip(), goingtxt[3].strip(), int(goingtxt[5].strip()))
        cursor.execute(going_query, going_values)
        goingdata = cursor.fetchone()

        coming_query = """SELECT train_id FROM trains
                           WHERE tr_name = %s AND cur_city = %s AND time = %s AND price = %s"""
        coming_values = (comingtxt[0].strip(), comingtxt[1].strip(), comingtxt[3].strip(), int(comingtxt[5].strip()))
        cursor.execute(coming_query, coming_values)
        comingdata = cursor.fetchone()

        order_query = """INSERT INTO orders (train_id, user_id, dest_city) 
                         VALUES (%s, %s, %s)"""
        cursor.execute(order_query, (goingdata[0], user_id, self.des))
        cursor.execute(order_query, (comingdata[0], user_id, self.cur))
        con.commit()
        
        cursor.execute(f"update trains set avb_seats = avb_seats-1 where {int(comingdata[0])} = train_id")
        cursor.execute(f"update trains set avb_seats = avb_seats-1 where {int(goingdata[0])} = train_id")
        con.commit()

        self.close()
    
    def single_order(self):
        going = None
        try:
            if self.goingtrains:
                for i in self.goingbtns:
                    button_style = i.styleSheet()
                    if 'border: 2px solid' in button_style:
                        going = i
                        
            goingtxt = going.text().split("|")        
        except:
            return
        
        if int(goingtxt[4]) == 0:
            msg = QMessageBox(self)
            msg.setWindowTitle("No tickets found")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No tickets found\nTrain is full")
    
            
        #['Afrosiyob  ', '  Xorazm  ', '  2024-02-11  ', '  19:00  ', '  100  ', '  200000  ', '  Toshkent']   
        going_query = """SELECT train_id FROM trains
                          WHERE tr_name = %s AND cur_city = %s AND time = %s AND price = %s"""
        going_values = (goingtxt[0].strip(), goingtxt[1].strip(), goingtxt[3].strip(), int(goingtxt[5].strip()))
        cursor.execute(going_query, going_values)
        goingdata = cursor.fetchone()

    
        order_query = """INSERT INTO orders (train_id, user_id, dest_city) 
                         VALUES (%s, %s, %s)"""
        cursor.execute(order_query, (goingdata[0], user_id, self.des))
        con.commit()
        
        cursor.execute(f"update trains set avb_seats = avb_seats-1 where {int(goingdata[0])} = train_id")
        con.commit()

        self.close()
        

class MyTickets(QDialog):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setMinimumSize(1000, 700)
        self.setMaximumSize(1000, 700)
        self.setStyleSheet("background-color: #FFFFFF")
        self.setWindowTitle("Tickets List")
        self.setWindowIcon(QIcon("icon.ico"))

        self.place_order_labels()

    def place_order_labels(self):
        scroll_area = QScrollArea(self)
        scroll_area.setGeometry(10, 10, 680, 680)
        #t.cur_city, o.dest_city, t.going_date, t.time,  t.price
        scroll_contents = QWidget()
        scroll_area.setWidget(scroll_contents)
        scroll_layout = QVBoxLayout(scroll_contents)
        print(self.data)
        for i in range(len(self.data)):
            whole = f"{self.data[i][0]} {str(self.data[i][1])} {str(self.data[i][2])} {str(self.data[i][3])} {str(self.data[i][4])}"
            ticket = QLabel(whole)
            ticket.setFont(QFont("Montserrat", 10))
            
            scroll_layout.addWidget(ticket)


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
        # self.show_main_window()
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

