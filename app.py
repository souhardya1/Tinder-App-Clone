from tkinter import *
from dbhelper import DBHelper
from tkinter import messagebox
from PIL import Image,ImageTk
from tkinter import filedialog
import shutil, os

class Tinder:
    def __init__(self):
        #calling database connection function
        self._db=DBHelper()

        self.load_login_window()


        # load GUI
    def load_login_window(self):
        self._root = Tk()


        # titlebox
        self._root.title("Beloved |Match.Chat.Date")

        # Dialouge box size
        self._root.minsize(500,500)
        self._root.maxsize(800,800)

        # colouring the background
        self._root.config(background="#FC0378")
        self._label1 = Label(self._root, text="Beloved", fg="#fff", bg="#FC0378")
        self._label1.config(font=("Chalet-LondonNineteenSeventy", 30))
        self._label1.pack(pady=(10, 60))

        # emailLabel
        self._email = Label(self._root, text="Email", fg="#fff", bg="#FC0378")
        self._email.config(font=("Chalet-LondonNineteenSeventy", 15))
        self._email.pack(pady=(30, 5))

        # emailBox
        self._emailInput = Entry(self._root)
        self._emailInput.pack(pady=(2, 5), ipadx=30)

        # passwordLabel
        self._password = Label(self._root, text="Password", fg="#fff", bg="#FC0378")
        self._password.config(font=("Chalet-LondonNineteenSeventy", 15))
        self._password.pack(pady=(30, 5))

        # PasswordBox
        self._passwordInput = Entry(self._root)
        self._passwordInput.pack(pady=(2, 5), ipadx=30)

        # LoginButton
        self._login = Button(self._root, text="Login", fg="#FC0378", bg="#fff", command=lambda: self.check_login())
        self._login.pack(pady=(20, 5))

        #registration Button
        self._reg = Button(self._root, text="Register Now", fg="#FC0378", bg="#fff", command=lambda: self.regWindow())
        self._reg.pack(pady=(10, 5))


        self._root.mainloop()



    def check_login(self):
        email=self._emailInput.get()
        password=self._passwordInput.get()
        data=self._db.check_login(email,password)

        if len(data)==0: #because if the credentials are wrong then it will return an empty list
            #print("Invalid Credentials")
            messagebox.showerror("Error","Invalid Credentials")
        else:
            self.user_id=data[0][0]
            self.is_logged_in=1
            self.login_handler()

    def mainWindow(self,data,flag=0,index=0):


        #display information


        name=str(data[index][1])
        email =str(data[index][2])


        age=str(data[index][4])
        gender=data[index][5]
        city=data[index][6]
        dp=data[index][7]
        about=data[index][8]
        about = about.replace(",", ".")
        intro = ""
        intro_sent = about.split('.')
        for sent in intro_sent:
            intro = intro + "\n" + sent
        intro = intro.strip()
        intro = "\u201C" + intro + "\u201D"


        # adding a image
        imageUrl = "images/{}".format(data[index][7])
        load = Image.open(imageUrl)
        load = load.resize((200, 200), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        img = Label(image=render)
        img.image = render
        img.pack(pady=(20, 25))

        # name display
        name_label = Label(self._root, text="{} , {}".format(name,age),fg="#000", bg="#fff")
        name_label.config(font=("QDBetterComicSans", 14))
        name_label.pack(pady=(2,0),ipadx=500,ipady=10)

        #email display
        email_label = Label(self._root, text="{}  |  {}".format(gender,city), fg="#000", bg="#fff")
        email_label.config(font=("Arial", 11))
        email_label.pack(pady=(0, 10),ipadx=500,ipady=10)

        #about display
        intro_label=Label(self._root,text=intro,fg="#fff",bg="#FC0378")
        intro_label.config(font=("QDBetterComicSans", 11))
        intro_label.pack(pady=(0, 10),ipadx=500,ipady=10)

        # gender display
        #gender_label = Label(self._root, text=gender, fg="#fff", bg="#FC0378")
        #gender_label.config(font=("QDBetterComicSans", 12))
        #gender_label.pack(pady=(2, 10))

        # age display
        #age_label = Label(self._root, text=age, fg="#fff", bg="#FC0378")
        #age_label.config(font=("QDBetterComicSans", 12))
        #age_label.pack(pady=(2, 10))

        # city display
        #city_label = Label(self._root, text=city, fg="#fff", bg="#FC0378")
        #city_label.config(font=("QDBetterComicSans", 12))
        #city_label.pack(pady=(2, 10))

        #to view others
        if flag==1:
            frame = Frame(self._root)
            frame.pack()

            # previous button
            previous = Button(frame, text="<<<Previous",command=lambda :self.view_others(index-1),fg="#000",bg="#FC0378")

            previous.config(font=("Comic Sans MS", 11))
            previous.pack(side=LEFT)

            # propose button
            propose = Button(frame, text="♡♡Match It♡♡",command=lambda:self.propose(self.user_id,data[index][0]),fg="#000",bg="#FC0378")
            propose.config(font=("Comic Sans MS", 11))
            propose.pack(side=LEFT)

            # next button
            next = Button(frame, text="Next>>>",command=lambda :self.view_others(index+1),fg="#000",bg="#FC0378")
            next.config(font=("Comic Sans MS", 11))
            next.pack(side=LEFT)

        #to view my proposals
        elif flag==2:
            frame = Frame(self._root)
            frame.pack()

            # previous button
            previous = Button(frame, text="Previous", command=lambda: self.view_proposals(index - 1),fg="#000",bg="#FC0378")
            previous.config(font=("Comic Sans MS", 11))
            previous.pack(side=LEFT)

            # propose button
            propose = Button(frame, text="Match It!", command=lambda: self.propose(self.user_id, data[index][0]),fg="#000",bg="#FC0378")
            propose.config(font=("Comic Sans MS", 11))
            propose.pack(side=LEFT)

            # next button
            next = Button(frame, text="Next", command=lambda: self.view_proposals(index + 1),fg="#000",bg="#FC0378")
            next.config(font=("Comic Sans MS", 11))
            next.pack(side=LEFT)

        #to view my requests
        elif flag==3:
            frame = Frame(self._root)
            frame.pack()

            # previous button
            previous = Button(frame, text="Previous", command=lambda: self.view_request(index - 1),fg="#000",bg="#FC0378")
            previous.config(font=("Comic Sans MS", 11))
            previous.pack(side=LEFT)



            # next button
            next = Button(frame, text="Next", command=lambda: self.view_request(index + 1),fg="#000",bg="#FC0378")
            next.config(font=("Comic Sans MS", 11))
            next.pack(side=LEFT)

        #to my matches
        elif flag==4:
            frame = Frame(self._root)
            frame.pack()

            # previous button
            previous = Button(frame, text="Previous", command=lambda: self.view_matches(index - 1),fg="#000",bg="#FC0378")
            previous.config(font=("Comic Sans MS", 11))
            previous.pack(side=LEFT)

            # next button
            next = Button(frame, text="Next", command=lambda: self.view_matches(index + 1),fg="#000",bg="#FC0378")
            next.config(font=("Comic Sans MS", 11))
            next.pack(side=LEFT)

    #propose from db
    def propose(self,romeo,juliet):
        flag=self._db.insert_proposal(romeo,juliet)
        if flag==1:
            messagebox.showinfo("Congrats"," ♡ Request sent ♡")
        elif flag==2:
            messagebox.showerror("Denied","Done Already")
        else:
            messagebox.showinfo("Denied", "Not your day")





    def login_handler(self):
        #to load user profiles

        self.clear()
        self.headerMenu()
        data = self._db.fetch_userdata(self.user_id)
        self.mainWindow(data,flag=0)



    # clear the screen/new page in dialouge box
    def clear(self):
        for i in self._root.pack_slaves(): #all the things in root for example use print(i)
            #print(i)
            print(i.destroy())

    #view others profile
    def view_others(self,index=0):


        #fetch data from all other users from database
        data=self._db.fetch_otheruserdata(self.user_id)
        if index==0:
            self.clear()
            self.mainWindow(data,flag=1,index=0)
        else:
            if index<0:
                messagebox.showerror("Error","No users Left")
            elif index==len(data):
                messagebox.showerror("Error", "No users Left")
            else:
                self.clear()
                self.mainWindow(data,flag=1,index=index)



    #log out
    def logout(self):
        self.is_logged_in=0
        self._root.destroy()
        self.load_login_window()


    #all options
    def headerMenu(self):
        menu = Menu(self._root)
        self._root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="Home", menu=filemenu)
        filemenu.add_command(label="My Profile",command=lambda: self.login_handler())
        filemenu.add_command(label="Edit Profile")
        filemenu.add_command(label="View Profile", command=lambda: self.view_others())
        filemenu.add_command(label="LogOut", command=lambda: self.logout())

        helpmenu = Menu(menu)
        menu.add_cascade(label="Proposals", menu=helpmenu)
        helpmenu.add_command(label="My Proposals",command=lambda:self.view_proposals())
        helpmenu.add_command(label="My Requests",command=lambda:self.view_request())
        helpmenu.add_command(label="My Matches",command=lambda:self.view_matches())

    #view proposals
    def view_proposals(self,index=0):

        data = self._db.fetch_proposals(self.user_id)
        new_data=[]
        for i in data:
            new_data.append(i[3:])
        if index==0:
            self.clear()
            self.mainWindow(new_data,flag=2,index=0)
        else:
            if index<0:
                messagebox.showerror("Error","No user left")

            elif index==len(new_data):
                messagebox.showerror("Error","No users left")
            else:
                self.clear()
                self.mainWindow(new_data, flag=2, index=index)

    #view requests
    def view_request(self,index=0):

        data = self._db.fetch_request(self.user_id)
        new_data=[]
        for i in data:
            new_data.append(i[3:])
        if index==0:
            self.clear()
            self.mainWindow(new_data,flag=3,index=0)
        else:
            if index<0:
                messagebox.showerror("Error","No user left")

            elif index==len(new_data):
                messagebox.showerror("Error","No users left")
            else:
                self.clear()
                self.mainWindow(new_data, flag=3, index=index)

    #my matches
    def view_matches(self,index=0):
        data = self._db.fetch_matches(self.user_id)

        new_data = []

        for i in data:
            new_data.append(i[3:])

        if index == 0:
            self.clear()
            self.mainWindow(new_data, flag=4, index=0)
        else:
            if index < 0:
                messagebox.showerror("Error", "No user left")
            elif index == len(new_data):
                messagebox.showerror("Error", "No user left")
            else:
                self.clear()
                self.mainWindow(new_data, flag=4, index=index)

    #registration
    def regWindow(self):
        self.clear()
        self._root.config(background="#FC0378")
        self._label1 = Label(self._root, text="Beloved", fg="#fff", bg="#FC0378")
        self._label1.config(font=("Chalet-LondonNineteenSeventy", 30))
        self._label1.pack(pady=(10, 10))

        #nameLabel
        self._name = Label(self._root, text="Name", fg="#fff", bg="#FC0378")
        self._name.config(font=("Chalet-LondonNineteenSeventy", 15))
        self._name.pack(pady=(5, 5))

        # nameBox
        self._nameInput = Entry(self._root)
        self._nameInput.pack(pady=(2, 5), ipadx=20)

        # emailLabel
        self._email = Label(self._root, text="Email", fg="#fff", bg="#FC0378")
        self._email.config(font=("Chalet-LondonNineteenSeventy", 15))
        self._email.pack(pady=(5, 5))

        # emailBox
        self._emailInput = Entry(self._root)
        self._emailInput.pack(pady=(2, 5), ipadx=20)

        # passwordLabel
        self._password = Label(self._root, text="Password", fg="#fff", bg="#FC0378")
        self._password.config(font=("Chalet-LondonNineteenSeventy", 15))
        self._password.pack(pady=(5, 5))

        # PasswordBox
        self._passwordInput = Entry(self._root)
        self._passwordInput.pack(pady=(2, 5), ipadx=20)

        #AgeLabel
        self._age = Label(self._root, text="Age", fg="#fff", bg="#FC0378")
        self._age.config(font=("Chalet-LondonNineteenSeventy", 15))
        self._age.pack(pady=(5, 5))

        # AgeBox
        self._ageInput = Entry(self._root)
        self._ageInput.pack(pady=(2, 5), ipadx=20)

        # GenderLabel
        self._gender = Label(self._root, text="Gender", fg="#fff", bg="#FC0378")
        self._gender.config(font=("Chalet-LondonNineteenSeventy", 15))
        self._gender.pack(pady=(5, 5))

        # GenderBox
        self._genderInput = Entry(self._root)
        self._genderInput.pack(pady=(2, 5), ipadx=20)

        # CityLabel
        self._city = Label(self._root, text="City", fg="#fff", bg="#FC0378")
        self._city.config(font=("Chalet-LondonNineteenSeventy", 15))
        self._city.pack(pady=(5, 5))

        # CityBox
        self._cityInput = Entry(self._root)
        self._cityInput.pack(pady=(2, 5), ipadx=20)

        #upload dp
        self._dp=Button(self._root,text="Upload Profile Picture",fg="#FC0378", bg="#fff", command=lambda: self.select_dp())
        self._dp.pack(pady=(5, 5))
        self._filename=""

        self.dp_filename=Label(self._root)
        self.dp_filename.pack(pady=(5,5))

        # AboutLabel
        self._about = Label(self._root, text="Intro(use . for next line)", fg="#fff", bg="#FC0378")
        self._about.config(font=("Chalet-LondonNineteenSeventy", 15))
        self._about.pack(pady=(5, 5))

        # AboutBox
        self._aboutInput = Entry(self._root)
        self._aboutInput.pack(pady=(2, 5), ipadx=20)

        # registration Button
        self._reg = Button(self._root, text="Register Now", fg="#FC0378", bg="#fff", command=lambda: self.reg_handler())
        self._reg.pack(pady=(50, 5))

    #Image Process
    def select_dp(self):
        self.filename = filedialog.askopenfilename(initialdir="/images", title="Somrhting")
        self.dp_filename.config(text=self.filename)

    def reg_handler(self):

        actual_filename = self.filename.split("/")[-1]

        flag = self._db.register(self._nameInput.get(), self._emailInput.get(), self._passwordInput.get(),
                                self._ageInput.get(), self._genderInput.get(), self._cityInput.get(), actual_filename,self._aboutInput.get())

        if flag == 1:
            # File upload
            destination = "E:\\Python\\Anaconda Python\\tinder\\images\\" + actual_filename
            shutil.copyfile(self.filename, destination)
            messagebox.showinfo("Success", "You are Beloved One")
            self._root.destroy()
            self.load_login_window()
        else:
            messagebox.showerror("Error", "Try again!")

obj=Tinder()