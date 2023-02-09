import tkinter 
import customtkinter 
import time
from pymongo import MongoClient

class Login(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("500x350")
        
        self.login_frame = customtkinter.CTkFrame(self)
        self.login_frame.pack(pady=20, padx=60, fill="both", expand = True)

        self.login_title = customtkinter.CTkLabel(self.login_frame, text="Login System", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.login_title.pack(pady=12,padx=10)

        self.username_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text = "Enter Username")
        self.username_entry.pack(pady=12,padx=10)

        self.password_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text = "Enter Password", show = "*")
        self.password_entry.pack(pady=12,padx=10)

        self.login_button = customtkinter.CTkButton(self.login_frame, text = "login", command = self.login)
        self.login_button.pack(pady=12,padx=10)
        self.mainloop()
    
    def login(self):
        if (self.username_entry.get() == "Username" and self.password_entry.get() == "Password"):
            self.destroy()
            Main = App()
            
        else:
            tkinter.messagebox.showinfo("Error","incorrect username or password")




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stock and staff system")
        self.geometry("700x500")
        self.logout_button = customtkinter.CTkButton(self, text = "logout", command = self.logout)
        self.logout_button.pack(pady=12,padx=10)
        self.mainloop()
    def logout(self):
        self.destroy()
        Sys = Login()

Sys = Login()

'''
#xAVAnVOSWLjYNjY6
client = MongoClient("mongodb+srv://admin:xAVAnVOSWLjYNjY6@cluster0.rr3bbtz.mongodb.net/?retryWrites=true&w=majority")

db = client.ManagementSoftware
Staff = db.Staff
Customers = db.Customers

staff_entry = {
                "name": { "first": "John", "last": "Doe" },
                "password": { "hash": hash("Fdsf"), "salt": "salt" }
            }
            Staff.insert_one(staff_entry)

'''