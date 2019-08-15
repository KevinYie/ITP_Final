from tkinter import *
import tkinter.messagebox as box
import pickle
import os


class Authenticator:

    def __init__(self, message):

        # Pickles in and out account information
        try:
            self.accounts = pickle.load(open("accounts.pickle", "rb"))
        except (OSError, IOError) as e:
            self.accounts = {"username": "password"}
            pickle_out = open("accounts.pickle", "wb")
            pickle.dump(self.accounts, pickle_out)
            pickle_out.close()
            pickle_in = open("accounts.pickle", "rb")
            self.accounts = pickle.load(pickle_in)

        # Open root window
        self.root = Tk()
        self.root.title("User Authentication")

        # Sets the window in the middle of screen
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()
        positionRight = int(self.root.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(self.root.winfo_screenheight() / 2 - windowHeight / 2)
        self.root.geometry("+{}+{}".format(positionRight, positionDown))

        # Creates the frame
        frame = Frame(self.root, width=600, height=300)
        frame.pack()

        # Layout of authenticator
        self.userLabel = Label(frame, text="Username")
        self.passwordLabel = Label(frame, text="Password")
        self.userLabel.grid(row=0, column=0)
        self.passwordLabel.grid(row=1, column=0)

        self.userEntry = Entry(frame)
        self.passwordEntry = Entry(frame)
        self.userEntry.grid(row=0, column=1)
        self.passwordEntry.grid(row=1, column=1)

        self.loginButton = Button(frame, text="Login", command=self.authenticate)
        self.loginButton.grid(row=3, column=0)

        self.newUserButton = Button(frame, text="Create New Account", command=self.createUser)
        self.newUserButton.grid(row=3, column=1)

        if message == "creation success":
            self.root.destroy()
            temp = Tk()
            temp.withdraw()
            box.showinfo("Account Creation Successful", "Your account has been successfully created!")

            MainWindow()

        elif message == "success":
            self.root.destroy()
            temp = Tk()
            temp.withdraw()
            box.showinfo("Successful Login", "Login Successful!")

            MainWindow()

        elif message == "":
            pass

        elif message == "main window":
            main = MainWindow()
            main.loadUp()

        else:
            self.root.destroy()
            temp = Tk()
            temp.withdraw()
            box.showinfo("Error", message)
            Authenticator("")

        self.root.mainloop()

    # Functions for authenticator

    def authenticate(self):

        enteredUser = self.userEntry.get()
        enteredUser = str(enteredUser)
        enteredPassword = self.passwordEntry.get()
        enteredPassword = str(enteredPassword)

        if enteredUser in list(self.accounts.keys()):
            if str(enteredPassword) == str(self.accounts[enteredUser]):
                global account
                account = str(self.userEntry.get())

                self.root.destroy()
                Authenticator("success")
            else:
                self.root.destroy()
                Authenticator("The username you entered does not exist")
        else:
            self.root.destroy()
            Authenticator("The username you entered does not exist")




    def createUser(self):
        enteredUser = self.userEntry.get()
        enteredUser = str(enteredUser)
        enteredPassword = self.passwordEntry.get()
        enteredPassword = str(enteredPassword)

        if enteredUser in list(self.accounts.keys()):
            self.root.destroy()
            Authenticator("The username you entered already exists")
        else:
            self.accounts.update({str(enteredUser): str(enteredPassword)})
            pickle_out = open("accounts.pickle", "wb")
            pickle.dump(self.accounts, pickle_out)
            pickle_out.close()

            global account
            account = str(self.userEntry.get())

            self.root.destroy()

            Authenticator("creation success")



## TODO create different lists of Text object for each account. Will have to add function into MainWindow that takes username and password as arguments and use string formatting to open correct pickle list
class MainWindow:
    def __init__(self):
        self.account = account
        self.loadUp()
    # Function to create window

    def loadUp(self):
        try:
            os.mkdir("{}".format(self.account))
        except OSError:
            pass

        os.chdir("{}/{}".format(os.getcwd(), self.account))
        root = Tk()
        frame = Frame(root)
        frame.pack()
        files = os.listdir("{}".format(os.getcwd()))
        listbox = Listbox(frame)
        for i in range(0, len(files)):
            listbox.insert(i, files[i])

        def openFile():
            textWidget = Text(frame, width = 100)
            with open(listbox.get( listbox.curselection() ), 'r') as note:
                textWidget.insert(INSERT, note.read())
            textWidget.pack()

        openButton = Button(frame, text='View Note', command=openFile)
        openButton.pack()
        listbox.pack()
        root.mainloop()



account = ""
Authenticator("")