
from tkinter import *
import tkinter.messagebox as box
import pickle
import os
import datetime



# Setting up Authenticator class
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

        # Sets the dimensions of the window
        self.root.title('Authenticator')
        self.root.geometry("275x150")
        self.root.resizable(0, 0)

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

        self.gif = PhotoImage(file="chick.png")
        self.gifLabel = Label(frame, image=self.gif)
        self.gifLabel.grid(row=4, column=0)

        self.gif2 = PhotoImage(file="chick.png")
        self.gifLabel2 = Label(frame, image=self.gif2)
        self.gifLabel2.grid(row=4, column=1)

        # Message boxes depending on message argument
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

    # Checks if username and password match in the pickled dictionary
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



    # Checks if username exists in dictionary. If it does, return error
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








# Class for Main Window. Takes global variable account and sets it to self to specify user
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

        # Setting directory
        os.chdir("{}/{}".format(os.getcwd(), self.account))

        # Creating list out of directory
        files = os.listdir("{}".format(os.getcwd()))

        root = Tk()

        # Setting window dimensions
        root.title('Forever Note')
        root.geometry("450x300")
        root.resizable(0, 0)

        # Creating frames and properties
        leftFrame = Frame(root, width=350, height=400)
        leftFrame.pack(side=LEFT, fill=None, expand=False)
        leftFrame.pack_propagate(0)
        rightFrame = Frame(root, width=100, height=50)
        rightFrame.place(relx=.9, rely=.5, anchor="c")
        rightFrame.pack_propagate(0)

        # Formatting Window
        recentLabel = Label(leftFrame, text="All Files", font=("Arial", 16))
        recentLabel.pack()

        # Creates list of all files in directory
        listbox = Listbox(leftFrame, height=100, width=100)
        for i in range(0, len(files)):
            listbox.insert(i, files[i])
        listbox.pack(side=BOTTOM)

        # Views the hovered file
        def openFile():
            viewWindow = Tk()
            viewFrame = Frame(viewWindow)
            viewFrame.pack()
            textWidget = Text(viewFrame, width=100)
            with open(listbox.get(listbox.curselection()), 'r') as note:
                textWidget.insert(INSERT, note.read())
            textWidget.pack()
            viewWindow.mainloop()

        viewButton = Button(rightFrame, text='View Note', command=openFile)
        viewButton.pack(side=TOP)

        # Opens a text window to enter new note
        def newNote():
            textWindow = Tk()

            textWindow.title("New Note")
            textWindow.geometry("200x200")
            textWindow.resizable(0, 0)

            lframe = Frame(textWindow, width=150, height=200)
            lframe.pack(side=LEFT, fill=None, expand=False)
            lframe.pack_propagate(0)
            rframe = Frame(textWindow, width=50, height=200)
            rframe.pack(side=RIGHT, fill=None, expand=False)
            rframe.pack_propagate(0)

            userText = Text(lframe)
            userText.pack()

            # Writes a text file using date and time as title
            def save():
                textOut = open("{}.txt".format(datetime.datetime.now().strftime("%Y%m%d%H%M")), "w+")
                textOut.write(userText.get("1.0", END))
                textOut.close()

                temp = Tk()
                temp.withdraw()
                box.showinfo("Saved", "Your note was saved")

            saveButton = Button(rframe, text="Save", command=save)
            saveButton.pack()

            textWindow.mainloop()

        addButton = Button(rightFrame, text="New Note", command=newNote)
        addButton.pack()

        root.mainloop()


account = ""
Authenticator("")
