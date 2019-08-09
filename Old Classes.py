from tkinter import *
import pickle

class Authenticator:

    def __init__(self):

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
        root = Tk()

# Sets the window in the middle of screen
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
        root.geometry("+{}+{}".format(positionRight, positionDown))

# Creates the frame
        frame = Frame(root, width=600, height=300)
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
        self.loginButton.grid(row=2, column=0)

        self.newUserButton = Button(frame, text="Create New Account", command=self.createUser)
        self.newUserButton.grid(row=2, column=1)

        root.mainloop()

# Functions for authenticator
    def authenticate(self):
        enteredUser = self.userEntry.get()
        enteredUser = str(enteredUser)
        enteredPassword = self.passwordEntry.get()
        enteredPassword = str(enteredPassword)

        if enteredUser in list(self.accounts.keys()):
            if str(enteredPassword) == str(self.accounts[enteredUser]):
                MainWindow()
            else:
                self.errorWindowCall("wrong password")
        else:
            self.errorWindowCall("wrong username")

    def errorWindowCall(self, reason):
        errorWindow = Tk()

# Sets the window in the middle of the screen
        windowWidth = errorWindow.winfo_reqwidth()
        windowHeight = errorWindow.winfo_reqheight()
        positionRight = int(errorWindow.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(errorWindow.winfo_screenheight() / 2 - windowHeight / 2)
        errorWindow.geometry("+{}+{}".format(positionRight, positionDown))

# Layout of error window
        frame = Frame(errorWindow, width=450, height=200)
        if reason == "wrong username":
            errorLabel = Label(frame, text="The username or password \n you have entered is incorrect", fg="red",
                               bg="white", font=("Comic Sans", 18))
            errorLabel.pack()
        elif reason == "wrong password":
            errorLabel = Label(frame, text="The username or password \n you have entered is incorrect", fg="red",
                               bg="white", font=("Comic Sans", 18))
            errorLabel.pack()
        elif reason == "user exists":
            errorLabel = Label(frame, text="That username already exists", fg="red",
                               bg="white", font=("Comic Sans", 18))
            errorLabel.pack()
        frame.pack()
        errorWindow.mainloop()

    def createUser(self):
        enteredUser = self.userEntry.get()
        enteredUser = str(enteredUser)
        enteredPassword = self.passwordEntry.get()
        enteredPassword = str(enteredPassword)

        if enteredUser in list(self.accounts.keys()):
            self.errorWindowCall("user exists")
        else:
            self.accounts.update({str(enteredUser): str(enteredPassword)})
            pickle_out = open("accounts.pickle", "wb")
            pickle.dump(self.accounts, pickle_out)
            pickle_out.close()
            successWindow = Tk()


# Sets the window in the middle of the screen
            windowWidth = successWindow.winfo_reqwidth()
            windowHeight = successWindow.winfo_reqheight()
            positionRight = int(successWindow.winfo_screenwidth() / 2 - windowWidth / 2)
            positionDown = int(successWindow.winfo_screenheight() / 2 - windowHeight / 2)
            successWindow.geometry("+{}+{}".format(positionRight, positionDown))

# Layout of success window
            frame = Frame(successWindow, width=450, height=200)
            successLabel = Label(frame, text="Your account has been created", fg="green",
                               bg="white", font=("Comic Sans", 18))
            successLabel.pack()
            frame.pack()
            successWindow.mainloop()

# TODO Make the error message print below the entry fields

class MainWindow:
# TODO create different lists of Text object for each account. Will have to add function into MainWindow that takes username and password as arguments and use string formatting to open correct pickle list
    def __init__(self):
        root = Tk()
        topFrame = Frame(root)
        topFrame.pack(side=TOP)
        root.mainloop()


Authenticator()