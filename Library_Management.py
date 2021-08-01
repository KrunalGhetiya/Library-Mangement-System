from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter.ttk import Combobox
import mysql.connector as connect
import datetime
from datetime import date


class Library_Management(Tk):

    userId, user_password, login_librarian, login_admin, new_userId, new_userName, new_userPassword, re_user_password, re_enter_password  = None, None, None, None, None, None, None, None, None
    book_Id, book_Title, book_Author, book_edition, book_copy, book_owner = None, None, None, None, None, None
    issue_date, expiry_date, issue_no = None, None, 0
    e1, e2, e3 = None, None, None
    book_list = []
    com1d, com1m, com1y, com2d, com2m, com2y = None, None, None, None, None, None
    day = list(range(1, 32))
    month = list(range(1, 13))
    year = list(range(2021, 2040))
    cur, win = None, None

    def connectdb(self):
        self.con = connect.connect(host="localhost",
                                   user="root",
                                   passwd="",
                                   database="library_management")

    def closedb(self):
        self.con.close()

    def create_Login(self):
        self.geometry("400x400+480+180")
        self.resizable(False, False)
        self.title("Library Management")
        self.wm_iconbitmap("1.ico")
        self.load = Image.open("bg.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.image = Label(self, image=self.render)
        self.image.pack()
        Label(self, text="User Id: ").place(x=70, y=100)
        Label(self, text="password : ").place(x=70, y=140)

        self.userId = Entry(self, textvariable=StringVar())
        self.user_password = Entry(self, textvariable=StringVar())
        self.userId.place(x=180,y=100)
        self.user_password.place(x=180, y=140)

        Button(self, text="Login As Librarian", height=1, width=18,relief=GROOVE, command=self.login_Librarian).place(x=180, y=180)
        Button(self, text="Login As Admin", height=1, width=18, relief=GROOVE, command=self.login_Admin).place(x=180, y=225)

    def login_Librarian(self):
        self.connectdb()
        query = "select * from login_librarian_tb"
        cur = self.con.cursor()
        cur.execute(query)
        for row in cur:
            if str(self.userId.get()) == str(row[0]):
                if str(self.user_password.get()) == str(row[2]):
                    self.librarian()
                    break
                else:
                    msg.showinfo("Incorrect", "Enter the correct password")
        else:
            self.closedb()
            self.create_Login()

    def librarian(self):
        self.withdraw()
        self.win = Tk()
        self.win.title("Library")
        self.win.geometry("400x400+480+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")

        Button(self.win, height=2, width=25, text=' Add Book ', relief=GROOVE, command=self.add_Book).place(x=110, y=80)
        Button(self.win, height=2, width=25, text=' View Book ', relief=GROOVE, command=self.view_Books).place(x=110,
                                                                                                               y=130)
        Button(self.win, height=2, width=25, text=' Issue Book ', relief=GROOVE, command=self.issue_Book).place(x=110,
                                                                                                                y=180)
        Button(self.win, height=2, width=25, text=' Return Book ', relief=GROOVE, command=self.return_Book).place(x=110,
                                                                                                                  y=230)
        Button(self.win, height=2, width=25, text=' Your Books ', relief=GROOVE, command=self.view_issueBook).place(
            x=110, y=280)
        Button(self.win, height=2, width=25, text=' Log out ', relief=GROOVE, command=self.logout).place(x=110, y=330)

        self.win.mainloop()

    def add_Book(self):
        self.win.destroy()
        self.win = Tk()
        self.win.title("Add Book")
        self.win.geometry("400x400+480+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")
        Label(self.win, text="BOOK ID: ").place(x=70, y=50)
        Label(self.win, text="TITLE: ").place(x=70, y=90)
        Label(self.win, text="AUTHOR: ").place(x=70, y=130)
        Label(self.win, text="EDITION: ").place(x=70, y=170)
        Label(self.win, text="COPY: ").place(x=70, y=210)
        Label(self.win, text="OWNER: ").place(x=70, y=250)

        self.book_Id = Entry(self.win, width=25, textvariable=StringVar())
        self.book_Id.place(x=180, y=50)
        self.book_Title = Entry(self.win, width=25, textvariable=StringVar())
        self.book_Title.place(x=180, y=90)
        self.book_Author = Entry(self.win, width=25, textvariable=StringVar())
        self.book_Author.place(x=180, y=130)
        self.book_edition = Entry(self.win, width=25, textvariable=StringVar())
        self.book_edition.place(x=180, y=170)
        self.book_copy = Entry(self.win, width=25, textvariable=StringVar())
        self.book_copy.place(x=180, y=210)
        self.book_owner = Entry(self.win, width=25, textvariable=StringVar())
        self.book_owner.place(x=180, y=250)

        Button(self.win, text="ADD BOOK", height=1, width=18, relief=GROOVE, command=self.add_Book_Data).place(x=180,
                                                                                                               y=290)
        Button(self.win, text="GO BACK", height=1, width=18, relief=GROOVE, command=self.go_Back).place(x=180, y=340)

        self.win.mainloop()

    def add_Book_Data(self):
        self.connectdb()
        query = f"insert into book_detail_tb(title, id, author, edition, copy, owner) values('{self.book_Title.get()}','{self.book_Id.get()}','{self.book_Author.get()}','{self.book_edition.get()}','{self.book_copy.get()}','{self.book_owner.get()}')"
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        self.win.destroy()
        msg.showinfo("Book", "Book added")
        self.librarian()

    def view_Books(self):
        self.win.destroy()
        self.win = Tk()
        self.win.title("User")
        self.win.geometry("800x300+270+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")

        user_data = ttk.Treeview(self.win)

        user_data['columns'] = ("b_id", "b_title", "author", "edition", "copy")

        user_data.column("#0", width=0, stretch=NO)
        user_data.column("b_id", anchor=CENTER, width=120)
        user_data.column("b_title", anchor=CENTER, width=120)
        user_data.column("author", anchor=CENTER, width=120)
        user_data.column("edition", anchor=CENTER, width=120)
        user_data.column("copy", anchor=CENTER, width=120)

        user_data.heading("#0", text="")
        user_data.heading("b_id", text="Book_Id", anchor=CENTER)
        user_data.heading("b_title", text="Book_Title", anchor=CENTER)
        user_data.heading("author", text="Author", anchor=CENTER)
        user_data.heading("edition", text="Edition", anchor=CENTER)
        user_data.heading("copy", text="Copy", anchor=CENTER)

        self.connectdb()
        query = f"select * from book_detail_tb"
        cur = self.con.cursor()
        cur.execute(query)
        index = 0
        iid = 0
        for row in cur:
            user_data.insert("", index, iid, values=row)
            index = iid = index + 1
        user_data.pack()

        Button(self.win, text="Go Back", height=1, width=20, relief=GROOVE, command=self.go_Back).place(x=212, y=210)

    def go_Back(self):
        self.win.destroy()
        self.librarian()

    def issue_Book(self):
        self.win.destroy()
        self.win = Tk()
        self.win.title("Library")
        self.win.geometry("400x400+480+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")

        Label(self.win, text="Issue Book", font="Helvetica 15 bold").place(x=150, y=30)

        Label(self.win, text="User Id: ").place(x=70, y=130)
        Label(self.win, text="Book Id: ").place(x=70, y=170)
        Label(self.win, text="Issue date: ").place(x=70, y=210)
        Label(self.win, text="Expiry data: ").place(x=70, y=240)

        self.e1 = Entry(self.win, textvariable=StringVar())
        self.e1.place(x=180, y=130)
        self.e2 = Entry(self.win, textvariable=StringVar())
        self.e2.place(x=180, y=170)

        self.com1d = Combobox(self.win, value=self.day, width=5)
        self.com1m = Combobox(self.win, value=self.month, width=5)
        self.com1y = Combobox(self.win, value=self.year, width=5)

        self.com2d = Combobox(self.win, value=self.day, width=5)
        self.com2m = Combobox(self.win, value=self.month, width=5)
        self.com2y = Combobox(self.win, value=self.year, width=5)

        self.now = datetime.datetime.now()

        self.com1y.set(self.now.year)
        self.com1m.set(self.now.month)
        self.com1d.set(self.now.day)

        self.com2y.set(self.now.year)
        self.com2m.set(self.now.month)
        self.com2d.set(self.now.day)

        self.com1d.place(x=180, y=210)
        self.com1m.place(x=230, y=210)
        self.com1y.place(x=280, y=210)
        self.com2d.place(x=180, y=240)
        self.com2m.place(x=230, y=240)
        self.com2y.place(x=280, y=240)

        Button(self.win, text="Issue Book", height=1, width=18, relief=GROOVE, command=self.book_issued).place(x=180,
                                                                                                               y=270)
        Button(self.win, text="Cancel", height=1, width=18, relief=GROOVE, command=self.go_Back).place(x=180, y=300)

    def book_issued(self):
        global book_title, book_remains
        if self.e1.get() == self.userId.get():

            self.issue_date = date(int(self.com1y.get()), int(self.com1m.get()), int(self.com1d.get()))
            self.expiry_date = date(int(self.com2y.get()), int(self.com2m.get()), int(self.com2d.get()))

            if self.issue_date < self.expiry_date:
                if (self.expiry_date - self.issue_date).days <= 15:
                    if self.issue_no < 3:
                        self.connectdb()
                        query = f"select copy from book_detail_tb where id='{self.e2.get()}'"
                        cur = self.con.cursor()
                        cur.execute(query)
                        for row in cur:
                            book_remains = int(row[0])
                        print(book_remains)

                        self.connectdb()
                        query = f"select title from book_detail_tb where id='{self.e2.get()}'"
                        cur = self.con.cursor()
                        cur.execute(query)
                        for row in cur:
                            book_title = row[0]

                        if int(book_remains) >= 1:
                            self.connectdb()
                            query = f"insert into issue_book(book_id, book_title, user_id, issue_data, expiry_data) values('{self.e2.get()}', '{book_title}', '{self.userId.get()}', '{self.issue_date}', '{self.expiry_date}')"
                            cur = self.con.cursor()
                            cur.execute(query)
                            self.con.commit()
                            msg.showinfo("", f"{self.e2.get()} - '{book_title}' BOOK ISSUED")

                            book_remains -= 1
                            self.connectdb()
                            query = f"update book_detail_tb set copy='{book_remains}' where id='{self.e2.get()}'"
                            cur = self.con.cursor()
                            cur.execute(query)
                            self.con.commit()
                            self.issue_no += 1

                            self.win.destroy()
                            self.librarian()
                        else:
                            msg.showinfo("", "out of the stocks...")
                    else:
                        msg.showinfo("", "You can issue maximum 3 books only.")
                else:
                    msg.showinfo("Invalid Date", "You can issue a book only for 15 days.")
            else:
                msg.showinfo("Invalid Date", "Enter proper date")
        else:
            msg.showinfo("Incorrect Id", f"Enter correct User Id !!!\nlogin Id is {self.userId.get()}")

    def return_Book(self):
        self.win.destroy()
        self.win = Tk()
        self.win.title("Return Book")
        self.win.geometry("400x400+480+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")

        Label(self.win, text="RETURN BOOK", font="Helvetica 15 bold").place(x=130, y=30)

        Label(self.win, text="Book Id:").place(x=70, y=150)

        self.e3 = Entry(self.win, textvariable=StringVar())
        self.e3.place(x=180, y=150)

        Button(self.win, text="Return Book", height=1, width=18, relief=GROOVE, command=self.book_returned).place(x=180,
                                                                                                                  y=190)
        Button(self.win, text="Cancel", height=1, width=18, relief=GROOVE, command=self.go_Back).place(x=180, y=230)

    def book_returned(self):
        global book_remains
        self.connectdb()
        query = f"delete from issue_book where book_id='{self.e3.get()}' AND user_id='{self.userId.get()}'"
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        msg.showinfo("Return", "Book Returned")

        query = f"select copy from book_detail_tb where id='{self.e3.get()}'"
        cur = self.con.cursor()
        cur.execute(query)
        for row in cur:
            book_remains = int(row[0]) + 1

        query = f"update book_detail_tb set copy='{book_remains}' where id='{self.e3.get()}'"
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        self.win.destroy()
        self.librarian()

    def view_issueBook(self):
        self.win.destroy()
        self.win = Tk()
        self.win.title("User")
        self.win.geometry("800x300+270+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")

        user_data = ttk.Treeview(self.win)

        user_data['columns'] = ("b_id", "b_title", "u_id", "i_d", "e_d")

        user_data.column("#0", width=0, stretch=NO)
        user_data.column("b_id", anchor=CENTER, width=120)
        user_data.column("b_title", anchor=CENTER, width=120)
        user_data.column("u_id", anchor=CENTER, width=120)
        user_data.column("i_d", anchor=CENTER, width=120)
        user_data.column("e_d", anchor=CENTER, width=120)

        user_data.heading("#0", text="")
        user_data.heading("b_id", text="Book_Id", anchor=CENTER)
        user_data.heading("b_title", text="Book_Title", anchor=CENTER)
        user_data.heading("u_id", text="User_Id", anchor=CENTER)
        user_data.heading("i_d", text="Issue Date", anchor=CENTER)
        user_data.heading("e_d", text="Expiry Date", anchor=CENTER)

        self.connectdb()
        query = f"select * from issue_book where user_id = '{self.userId.get()}' "
        cur = self.con.cursor()
        cur.execute(query)
        index = 0
        iid = 0
        for row in cur:
            user_data.insert("", index, iid, values=row)
            index = iid = index + 1
        user_data.pack()

        Button(self.win, text="Go Back", height=1, width=20, relief=GROOVE, command=self.go_Back).place(x=212, y=210)

    def logout(self):
        response = msg.askyesno("logout", "are you sure you want to logout?")
        if response:
            self.win.destroy()
        else:
            self.win.destroy()
            self.librarian()

    def login_Admin(self):
        self.connectdb()
        query = f"select * from login_admin_tb"
        cur = self.con.cursor()
        cur.execute(query)
        for row in cur:
            if self.userId.get() == row[0]:
                if self.user_password.get() == row[2]:
                    self.admin()
                    break
                else:
                    msg.showinfo("Incorrect", "Enter the correct password")
        else:
            self.closedb()
            self.create_Login()

    def admin(self):
        self.withdraw()
        self.win = Tk()
        self.win.title("Library")
        self.win.geometry("400x400+480+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")

        Button(self.win, text="ADD USER", height=2, width=25, command=self.add_user, relief=GROOVE).place(x=110, y=70)
        Button(self.win, text="VIEW USER", height=2, width=25, relief=GROOVE, command=self.view_user).place(x=110,
                                                                                                            y=120)
        Button(self.win, text="DELETE USER", height=2, width=25, relief=GROOVE, command=self.delete_user).place(x=110,
                                                                                                                y=170)
        Button(self.win, text="LOG OUT", height=2, width=25, relief=GROOVE, command=self.logout_Admin).place(x=110,
                                                                                                             y=220)

    def add_user(self):

        self.win.destroy()
        self.win = Tk()
        self.win.geometry("400x400+480+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")
        self.win.title("Add user")

        Label(self.win, text="User Id:").place(x=70, y=100)
        Label(self.win, text="User Name:").place(x=70, y=140)
        Label(self.win, text="Password:").place(x=70, y=180)
        Label(self.win, text="Re_Enter password:").place(x=70, y=220)

        self.new_userId = Entry(self.win, textvariable=StringVar())
        self.new_userId.place(x=180, y=100)
        self.new_userName = Entry(self.win, textvariable=StringVar())
        self.new_userName.place(x=180, y=140)
        self.new_userPassword = Entry(self.win, textvariable=StringVar())
        self.new_userPassword.place(x=180, y=180)
        self.re_enter_password = Entry(self.win, textvariable=StringVar())
        self.re_enter_password.place(x=180, y=220)

        Button(self.win, text="Add User", height=1, width=20, command=self.user_added, relief=GROOVE).place(x=180,
                                                                                                            y=260)
        Button(self.win, text="Cancel", height=1, width=20, command=self.cancel_adding, relief=GROOVE).place(x=180,
                                                                                                             y=300)

    def user_added(self):
        self.connectdb()
        query = f"select id from login_librarian_tb"
        cur = self.con.cursor()
        cur.execute(query)
        for row in cur:
            if self.new_userId.get() == row[0]:
                msg.showinfo("", "user already exists")
                self.win.destroy()
                self.admin()
                break
        else:
            if self.new_userPassword.get() == self.re_enter_password.get():
                query = f"insert into login_librarian_tb(id, name, password) values('{self.new_userId.get()}', '{self.new_userName.get()}', '{self.new_userPassword.get()}')"
                cur = self.con.cursor()
                cur.execute(query)
                self.con.commit()
                msg.showinfo("user", "User Added")
                self.win.destroy()
                self.admin()
            else:
                msg.showinfo("Error", "passwords are not same")

    def view_user(self):
        self.win.destroy()
        self.win = Tk()
        self.win.title("User")
        self.win.geometry("400x400+480+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")

        user_data = ttk.Treeview(self.win)

        user_data['columns'] = ("id", "name", "password")

        user_data.column("#0", width=0, stretch=NO)
        user_data.column("id", anchor=CENTER, width=120)
        user_data.column("name", anchor=CENTER, width=80)
        user_data.column("password", anchor=CENTER, width=120)

        user_data.heading("#0", text="")
        user_data.heading("id", text="User_Id", anchor=CENTER)
        user_data.heading("name", text="User_Name", anchor=CENTER)
        user_data.heading("password", text="Password", anchor=CENTER)

        self.connectdb()
        query = f"select * from login_librarian_tb"
        cur = self.con.cursor()
        cur.execute(query)
        index = 0
        iid = 0
        for row in cur:
            user_data.insert("", index, iid, values=row)
            index = iid = index + 1

        user_data.pack()

        Button(self.win, text="Go Back", height=1, width=20, relief=GROOVE, command=self.cancel_adding).place(x=212,
                                                                                                              y=210)

    def delete_user(self):
        self.win.destroy()
        self.win = Tk()
        self.win.title("Delete User")
        self.win.geometry("400x400+480+180")
        self.win.resizable(False, False)
        self.win.wm_iconbitmap("1.ico")

        Label(self.win, text="User Id:").place(x=80, y=100)
        Label(self.win, text="Admin\nPassword").place(x=80, y=140)

        self.new_userId = Entry(self.win, textvariable=StringVar())
        self.re_user_password = Entry(self.win, textvariable=StringVar())
        self.new_userId.place(x=180, y=100)
        self.re_user_password.place(x=180, y=140)

        Button(self.win, text="Delete User", height=1, width=20, relief=GROOVE, command=self.user_Deleted).place(x=180,
                                                                                                                 y=180)
        Button(self.win, text="Cancel", height=1, width=20, command=self.cancel_adding, relief=GROOVE).place(x=180,
                                                                                                             y=220)

    def user_Deleted(self):

        global book_remains
        self.connectdb()
        query = f"select book_id from issue_book where user_id='{self.new_userId.get()}'"
        cur = self.con.cursor()
        cur.execute(query)
        for row in cur:
            self.book_list.append(row[0])
        print(self.book_list)
        for row in self.book_list:
            self.connectdb()
            query = f"delete from issue_book where book_id='{row}' AND user_id='{self.new_userId.get()}'"
            cur = self.con.cursor()
            cur.execute(query)
            self.con.commit()

            query = f"select copy from book_detail_tb where id='{row}'"
            print(query)
            cur = self.con.cursor()
            cur.execute(query)
            for row1 in cur:
                book_remains = int(row1[0]) + 1

            query = f"update book_detail_tb set copy={book_remains} where id='{row}'"
            print(query)
            cur = self.con.cursor()
            cur.execute(query)
            self.con.commit()
        query = f"delete from issue_book where user_id='{self.new_userId.get()}'"
        print(query)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()

        if self.re_user_password.get() == self.user_password.get():
            query = f"delete from login_librarian_tb where id='{self.new_userId.get()}'"
            cur = self.con.cursor()
            cur.execute(query)
            self.con.commit()
            msg.showinfo("Delete", "User Deleted")
            self.win.destroy()
            self.admin()
        else:
            msg.showinfo("Incorrect", "Password was incorrect")

    def cancel_adding(self):
        self.win.destroy()
        self.admin()

    def logout_Admin(self):
        response = msg.askyesno("logout", "are you sure you want to ")
        if response:
            self.win.destroy()
        else:
            self.win.destroy()
            self.admin()


lib = Library_Management()
lib.create_Login()
lib.mainloop()
