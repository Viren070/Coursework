import hashlib
import os
import queue
import re
import threading
import tkinter
from tkinter import ttk

import customtkinter
import webbrowser
from PIL import Image
from pymongo import MongoClient

#pyinstaller --noconfirm --onedir --windowed --clean --add-data "c:\users\viren\appdata\local\programs\python\python311\lib\site-packages/customtkinter;customtkinter/"  "C:\Users\viren\Documents\School\Computer Science\nea\main.py"


def IsLatestVersion():
    APP_VERSION = "0.0.1-alpha"
    try:
        client = MongoClient("mongodb+srv://admin:xAVAnVOSWLjYNjY6@cluster0.rr3bbtz.mongodb.net/?retryWrites=true&w=majority")
        db = client.ManagementSoftware
        App = db.App
        app_info = App.find_one()
        if APP_VERSION != app_info["app_version"]:
            return False
        else:
            return True 
    except:
        tkinter.messagebox.showerror("Error","Unable to connect to the database")

    
    
class LoginScreen(customtkinter.CTk):
    def __init__(self, appearance_mode = "Dark", colour_theme="Blue"):
        self.colour_theme = colour_theme
        self.connection_time = 0
        self.timeout_time = 0
        super().__init__()
        customtkinter.set_default_color_theme(self.colour_theme.lower())
        self.appearance_mode = appearance_mode
        self.title("Login")
        self.geometry("500x350")
        
        self.login_frame = customtkinter.CTkFrame(self)
        self.login_frame.pack(pady=20, padx=60, fill="both", expand = True)

        self.login_title = customtkinter.CTkLabel(self.login_frame, text="Login System", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.login_title.pack(pady=12,padx=10)

        self.email_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text = "Enter E-Mail", width = 200)
        self.email_entry.pack(pady=12,padx=10)

        self.password_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text = "Enter Password", show = "*", width=200)
        self.password_entry.pack(pady=12,padx=10)

        self.login_button = customtkinter.CTkButton(self.login_frame, text = "Login", command = self.login_button_event )
        self.login_button.pack(pady=12,padx=10)
        self.mainloop()
    
    def login_button_event(self):
        
        self.change_widget_state("disabled")
        self.login_button.configure(text="Authorising...")
        self.login_button.update()

        self.result_queue = queue.Queue()
        self.new_thread = threading.Thread(target=self.search_database)
        self.new_thread.start()

    
        self.after(self.timeout_time, self.check_database_connection)
        
    
    def check_database_connection(self):
        if not self.result_queue.empty():
            #print(self.connection_time)
            self.connection_time = 0
            query = self.result_queue.get()
            if query is not None:
                self.handle_valid_login(query)
            else:
                tkinter.messagebox.showerror("Error", "Incorrect Password or Username")
                self.timeout_time= 100
             
            self.change_widget_state("normal")
            self.login_button.configure(text="Login")
        else:
            self.timeout_time+=100
            
            if self.timeout_time > 2000:
                tkinter.messagebox.showerror("Error", "Could not establish a connection with the database. Please check your network connection and try again.")
                self.timeout_time = 0
                self.change_widget_state("normal")
                self.login_button.configure(text="Login")
            else:
                self.connection_time += self.timeout_time
                self.after(self.timeout_time, self.check_database_connection)
            
    
    def search_database(self):
        try:
            client = MongoClient("mongodb+srv://admin:xAVAnVOSWLjYNjY6@cluster0.rr3bbtz.mongodb.net/?retryWrites=true&w=majority")
            db = client.ManagementSoftware
            Staff = db.Staff
            email = self.email_entry.get()
            query = Staff.find_one({"email": "{}".format(email)})
            self.result_queue.put(query)
        except:
            pass

    def handle_valid_login(self, query):
        password_guess = self.password_entry.get()
        name = query['name']['first']
        salt = query['password']['salt']
        guess_hash = hashlib.pbkdf2_hmac('sha256', password_guess.encode('utf-8'), salt, 100000, dklen=128 )
        if guess_hash == query['password']['hash']:
            self.destroy()
            MainScreen(name, self.appearance_mode, self.colour_theme)
        else:
            tkinter.messagebox.showerror("Error","Incorrect Password or Username")
    
        self.change_widget_state("normal")
    def change_widget_state(self, state):
        self.email_entry.configure(state=state)
        self.password_entry.configure(state=state)
        self.login_button.configure(state=state)
        




class StaffEntryWindow(customtkinter.CTkToplevel):
   
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add New Staff Entry")
        self.parent=parent
        self.rowconfigure(2, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.cancel_button_event)
        self.columnconfigure(0, weight=1)
        self.number_of_inputs=3
        self.minsize(width=500, height=180)
        #self.resizable(False, False)
        
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, pady=10)
        self.job_details_frame = customtkinter.CTkFrame(self)
        self.job_details_frame.grid(row=1, column=0, padx=10, pady=10)


       
        
        self.first_name_variable = customtkinter.StringVar()
        self.first_name_variable.trace_add("write", self.validate_inputs)
        self.first_name_label = customtkinter.CTkLabel(self.frame ,text="First Name:")
        self.first_name_label.grid(row=0, column=0, padx=10, pady=5)
        self.first_name_entry = customtkinter.CTkEntry(self.frame,  textvariable=self.first_name_variable)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.last_name_variable = customtkinter.StringVar()
        self.last_name_variable.trace_add("write", self.validate_inputs)
        self.last_name_label = customtkinter.CTkLabel(self.frame, text="Last Name:")
        self.last_name_label.grid(row=0, column=2, padx=10, pady=5)
        self.last_name_entry = customtkinter.CTkEntry(self.frame, textvariable=self.last_name_variable)
        self.last_name_entry.grid(row=0, column=3, padx=10, pady=5)
        #birth date, gender, email, location
        self.gender_variable = customtkinter.StringVar()
        self.gender_variable.set("Select Gender")
        self.gender_variable.trace_add("write", self.validate_inputs)
        self.gender_label = customtkinter.CTkLabel(self.frame, text="Gender: ")
        self.gender_optionmenu = customtkinter.CTkOptionMenu(self.frame, values=["Male","Female"], variable=self.gender_variable)       
        self.gender_label.grid(row=0, column=4, padx=10, pady=5)
        self.gender_optionmenu.grid(row=0, column=5, padx=10, pady=5)
       
        self.birth_date_variable = customtkinter.StringVar()
        self.birth_date_variable.trace_add("write", self.validate_inputs)
        self.birth_date_label = customtkinter.CTkLabel(self.frame, text="Birth Date: ")
        self.birth_date_entry = customtkinter.CTkEntry(self.frame, textvariable=self.birth_date_variable)
        self.birth_date_label.grid(row=2, column=0, padx=10, pady=5)
        self.birth_date_entry.grid(row=2, column=1, padx=10, pady=5)

        self.email_variable = customtkinter.StringVar()
        self.email_variable.trace_add("write", self.validate_inputs)
        self.email_label = customtkinter.CTkLabel(self.frame, text="E-Mail: ")
        self.email_entry = customtkinter.CTkEntry(self.frame, textvariable=self.email_variable, width=200)
        self.email_label.grid(row=2, column=2, padx=10, pady=5)
        self.email_entry.grid(row=2, column=3, padx=10, pady=5)

        self.department_variable = customtkinter.StringVar()
        self.department_variable.trace_add("write", self.validate_inputs)
        self.department_label = customtkinter.CTkLabel(self.job_details_frame, text="Department:")
        self.department_label.grid(row=0, column=0, padx=10, pady=5)
        self.department_entry = customtkinter.CTkEntry(self.job_details_frame, textvariable=self.department_variable)
        self.department_entry.grid(row=0, column=1, padx=10, pady=5)

        self.salary_variable = customtkinter.StringVar()
        self.salary_variable.trace_add("write", self.validate_inputs)
        self.salary_label = customtkinter.CTkLabel(self.job_details_frame, text="Salary:" )
        self.salary_entry = customtkinter.CTkEntry(self.job_details_frame, textvariable=self.salary_variable)
        self.salary_label.grid(row=0, column=2, padx=10, pady=5)
        self.salary_entry.grid(row=0, column=3, padx=10, pady=5)

        self.hire_date_variable = customtkinter.StringVar()
        self.hire_date_variable.trace_add("write", self.validate_inputs)
        self.hire_date_label = customtkinter.CTkLabel(self.job_details_frame, text="Hire Date: ")
        self.hire_date_entry = customtkinter.CTkEntry(self.job_details_frame, textvariable=self.hire_date_variable)
        self.hire_date_label.grid(row=0, column=4, padx=10, pady=5)
        self.hire_date_entry.grid(row=0, column=5, padx=10, pady=5)


        self.first_name_warning=customtkinter.CTkLabel(self.frame, text="a-z only", text_color="red")
        self.last_name_warning=customtkinter.CTkLabel(self.frame, text="a-z only", text_color="red")
        self.department_warning=customtkinter.CTkLabel(self.job_details_frame, text="a-z only", text_color="red")
    

        self.separator = ttk.Separator(self)
        self.separator.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.button_frame = customtkinter.CTkFrame(self, fg_color=self._fg_color)
        self.button_frame.grid(row=3,column=0, pady=10)

        self.button_frame.columnconfigure(0, weight=1)
        self.submit_button = customtkinter.CTkButton(self.button_frame, text="Submit", command=self.submit_staff_entry, state="disabled")
        self.submit_button.grid(row=0, column=2, padx=10, pady=5)

        self.button_frame.columnconfigure(1, weight=1)
        self.cancel_button = customtkinter.CTkButton(self.button_frame, text="Cancel", command=self.cancel_button_event)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=5)

        self.button_frame.columnconfigure(2, weight=1)  
    
    
  
 
    def submit_staff_entry(self):
        thread = threading.Thread(target=self.add_to_database)
        thread.start()
        

    def add_to_database(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        department = self.department_entry.get()
        gender = self.gender_variable.get()
        email = self.email_entry.get()
        birth_date = self.birth_date_entry.get()
        salary = self.salary_entry.get()
        hire_date = self.hire_date_entry.get()
        password = "Password"
        salt = os.urandom(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=128 )
        #xAVAnVOSWLjYNjY6
        try:
            client = MongoClient("mongodb+srv://admin:xAVAnVOSWLjYNjY6@cluster0.rr3bbtz.mongodb.net/?retryWrites=true&w=majority")

            db = client.ManagementSoftware
            Staff = db.Staff

            staff_entry={
                            "name": { "first": first_name, "last": last_name },
                            "password": { "hash": password_hash, "salt": salt },
                            "email": email,
                            "gender": gender,
                            "birthdate": birth_date,
                            "hire_date": hire_date,
                            "department": department, 
                            "salary": salary,
            }

            Staff.insert_one(staff_entry)
            tkinter.messagebox.showinfo("Success!","The new staff entry was successfully added into the database.")
        except:
            tkinter.messagebox.showerror("Error","Your request could not be completed at this time. Please try again later.", parent=self)
    def validate_inputs(self, var, index, mode):
        self.valid_inputs=0
        self.first_name_entry_is_valid = True
        self.last_name_entry_is_valid = True 
        self.department_entry_is_valid = True 
        

        if len(self.first_name_entry.get().strip()) > 0:
            if not re.match("^[a-zA-Z]*$", self.first_name_entry.get().strip()):
                self.first_name_entry.configure(text_color="red")
                self.first_name_warning.configure(text="A-Z only")
                self.first_name_warning.grid(row=1,column=1)
                self.first_name_entry_is_valid = False
    
            if self.first_name_entry_is_valid:
                self.first_name_entry.configure(text_color="white" if self.parent.appearance_mode=="Dark" else "black")
                self.first_name_warning.grid_forget()
                self.valid_inputs+=1
        else:
            self.first_name_entry_is_valid = False

        #---
        if len(self.last_name_entry.get().strip()) > 0:
            if not re.match("^[a-zA-Z]*$", self.last_name_entry.get().strip()):
                self.last_name_entry.configure(text_color="red")
                self.last_name_warning.configure(text="A-Z only")
                self.last_name_warning.grid(row=1,column=3)
                self.last_name_entry_is_valid = False
        
            if self.last_name_entry_is_valid:
                self.last_name_entry.configure(text_color="white" if self.parent.appearance_mode=="Dark" else "black")
                self.last_name_warning.grid_forget()
                self.valid_inputs+=1
        else:
            self.last_name_entry_is_valid = False

        #-----
        if len(self.department_entry.get().strip()) > 0:
            if len(self.department_entry.get().strip().split(" ")) > 3:
                self.department_entry.configure(text_color="red")
                self.department_warning.configure(text="3 words or smaller")
                self.department_warning.grid(row=1, column=1)
                self.department_entry_is_valid = False
            
            if not re.match("^[a-zA-Z]*$", self.department_entry.get().replace(" ","")):
                self.department_entry.configure(text_color="red")
                self.department_warning.configure(text="Alphabetical only")
                self.department_warning.grid(row=1, column=1)
                self.department_entry_is_valid = False
        else:
            self.department_entry_is_valid = False
        
        if self.department_entry_is_valid:
            self.department_entry.configure(text_color="white" if self.parent.appearance_mode=="Dark" else "black")
            self.department_warning.grid_forget()
            self.valid_inputs+=1
            
        if self.valid_inputs==self.number_of_inputs:
            self.submit_button.configure(state="normal")
        else:
            self.submit_button.configure(state="disabled")

    def cancel_button_event(self):
        self.parent.staff_entry_window_is_open = False 
        self.destroy()

class MainScreen(customtkinter.CTk):
    def __init__(self, name, appearance_mode="Dark", colour_theme="Blue", colour_changed = False, geometry_string="700x450"):
        self.name = name
        self.colour_changed = colour_changed
        self.colour_theme = colour_theme
        self.geometry_string=geometry_string
        self.staff_entry_window_is_open = False
        super().__init__()
        customtkinter.set_default_color_theme(self.colour_theme.lower())
        self.title("Stock and staff system")
        self.geometry(self.geometry_string)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
   
   
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.settings_image =  customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "settings_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "settings_light.png")), size=(20, 20))
        self.account_settings_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "account_settings_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "account_settings_light.png")), size=(20, 20))
        self.edit_data_image =  customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "edit_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "edit_light.png")), size=(15, 15))
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=self.name, image=self.logo_image,
                                                             compound="left", padx=10, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.staff_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Staff",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.staff_button.grid(row=3, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.settings_image,anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=6, column=0, sticky="ew")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        

        # create staff frame
        self.staff_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.staff_frame.grid_columnconfigure(0, weight=1)
        self.data_frame = customtkinter.CTkScrollableFrame(self.staff_frame, width=600, height=350, border_width=20, corner_radius=20)
        self.data_frame.grid(row=0,column=0)
        self.staff_data = self.fetch_staff_data()
        headers = ["First Name", "Last Name", "Email"]
        separator_column = 1
        data_column=0
        for header in (headers):
            customtkinter.CTkLabel(self.data_frame, text=header, width=20, font=customtkinter.CTkFont(size=15, weight="bold")).grid(row=0, column=data_column,padx=10,pady=10)
            ttk.Separator(self.data_frame, orient="vertical").grid(row=0, column=separator_column, sticky="sn", rowspan=1000)
            separator_column+=2
            data_column+=2
        # Add data rows
        separator_row = 1
        data_row=2
        for data in (self.staff_data):
            

            customtkinter.CTkLabel(self.data_frame, text=data["name"]["first"], width=20).grid(row=data_row, column=0,padx=10,pady=10)
            customtkinter.CTkLabel(self.data_frame, text=data["name"]["last"], width=20, corner_radius=100).grid(row=data_row, column=2,padx=10,pady=10)
            customtkinter.CTkLabel(self.data_frame, text=data["email"], width=20).grid(row=data_row, column=4,padx=5,pady=10)
            customtkinter.CTkButton(self.data_frame, text="", image=self.edit_data_image, width=25, height=25, command=lambda staff_id=data["_id"]: self.handle_edit_button_event(staff_id)).grid(row=data_row, column=6, padx=10)
            ttk.Separator(self.data_frame, orient='horizontal').grid(row=separator_row, sticky="ew", columnspan= 1000)
            separator_row,data_row = separator_row+2, data_row+2

        self.staff_frame_add_staff_button = customtkinter.CTkButton(self.staff_frame, text="New Staff Entry", command=self.new_staff_entry)
        self.staff_frame_add_staff_button.grid(row=1, column=0)
#
        # create settings frame 
        
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent", width=20)
        self.settings_frame.grid_columnconfigure(1, weight=1)
        self.settings_frame.grid_rowconfigure(0, weight=1)
        self.settings_navigation_frame = customtkinter.CTkFrame(self.settings_frame, corner_radius=0, width=20)
        self.settings_navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.settings_navigation_frame.grid_rowconfigure(4, weight=1)

        
        self.appearance_button = customtkinter.CTkButton(self.settings_navigation_frame, corner_radius=0, width=20, height=25, border_spacing=10, text="Appearance",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.settings_appearance_button_event)
        self.appearance_button.grid(row=1, column=0, sticky="ew")
        
        self.account_button = customtkinter.CTkButton(self.settings_navigation_frame, corner_radius=0, width=20, height=25, border_spacing=10, text="Account",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.account_settings_image, anchor="w", command=self.settings_account_button_event)
        self.account_button.grid(row=2, column=0, sticky="ew")
        
        self.settings_appearance_frame = customtkinter.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.settings_appearance_frame.grid_columnconfigure(0, weight=1)
        self.settings_appearance_frame_appearance_label = customtkinter.CTkLabel(self.settings_appearance_frame, text="Appearance", anchor="w", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.settings_appearance_frame_appearance_label.grid(row=0, column=0, padx=15, pady=5, sticky = "W")
        self.appearance_mode_var = customtkinter.StringVar()
        self.appearance_mode_var.set(appearance_mode)
        self.appearance_mode = self.appearance_mode_var.get()
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.settings_appearance_frame, values=["Dark", "Light"],command=self.change_appearance_mode_event, variable=self.appearance_mode_var) 
        self.appearance_mode_menu.grid(row=0, column=6, padx=20, pady=5, sticky="E")
        
        self.separator = ttk.Separator(self.settings_appearance_frame, orient='horizontal')
        self.separator.grid(row=1, column=0, columnspan=100, sticky='ew', padx=10, pady=5)

        self.colour_theme_var = customtkinter.StringVar()
        self.colour_theme_var.set(self.colour_theme)
        self.settings_frame_colour_theme = customtkinter.CTkLabel(self.settings_appearance_frame, text="Colour Theme", anchor="w", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.settings_frame_colour_theme.grid(row=2, column=0, padx=15, pady=5, sticky="W")
        self.settings_frame_colour_theme_menu = customtkinter.CTkOptionMenu(self.settings_appearance_frame, values=["Blue","Dark-Blue","Green"], command=self.change_colour_theme_event, variable=self.colour_theme_var)
        self.settings_frame_colour_theme_menu.grid(row=2, column=6, padx=20, pady=5, sticky="E")

        self.settings_account_frame = customtkinter.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.settings_frame_logout_button = customtkinter.CTkButton(self.settings_account_frame, text="Logout", command=self.logout)
        self.settings_frame_logout_button.grid(row=6, column=0, padx=10, pady=10)
        # select default frame
        opening_frames = ["home",None] if self.colour_changed == False else ["settings","appearance"]
        self.select_frame_by_name(opening_frames[0])
        self.select_settings_frame_by_name(opening_frames[1])
        self.mainloop()

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.staff_button.configure(fg_color=("gray75", "gray25") if name == "staff" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "staff":
            self.staff_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.staff_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()
            self.select_settings_frame_by_name(None)

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("staff")
    
    def settings_button_event(self):
        self.select_frame_by_name("settings")
        
    def select_settings_frame_by_name(self, name):
        # set button color for selected button
        self.appearance_button.configure(fg_color=("gray75", "gray25") if name == "appearance" else "transparent")
        self.account_button.configure(fg_color=("gray75", "gray25") if name == "account" else "transparent")
    
        # show selected frame
        if name == "appearance":
            self.settings_appearance_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "account":
            self.settings_account_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_account_frame.grid_forget()
        
    def settings_appearance_button_event(self):
        self.select_settings_frame_by_name("appearance")
    
    def settings_account_button_event(self):
        self.select_settings_frame_by_name("account")
    
    def change_appearance_mode_event(self, new_appearance_mode):
        self.appearance_mode = new_appearance_mode
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_colour_theme_event(self, new_colour_theme):
        if new_colour_theme==self.colour_theme:
            return
        if self.staff_entry_window_is_open == True:
            self.colour_theme_var.set(self.colour_theme)
            if tkinter.messagebox.askokcancel("Confirmation","The details you are currently entering will be deleted, continue?"):
                self.staff_entry_window.destroy()
            else:
                
                return
    
        
        self.colour_theme = new_colour_theme
        geometry_string="700x450+"+str(self.winfo_x())+"+"+str(self.winfo_y())
        self.destroy()
        MainScreen(self.name,self.appearance_mode, self.colour_theme, True, geometry_string)
    def new_staff_entry(self):
    

        if not self.staff_entry_window_is_open:
            self.staff_entry_window = StaffEntryWindow(self)
            self.staff_entry_window.attributes('-topmost',True)
            self.staff_entry_window_is_open = True
        else:
            self.staff_entry_window.deiconify()
    def handle_edit_button_event(self, staff_id=None):
        if staff_id is not None:
            print("handling edit for {}".format(staff_id))
        else:
            print("no id provided")
            
            
    def logout(self):
        self.destroy()
        LoginScreen(self.appearance_mode, self.colour_theme)
    def fetch_staff_data(self):
        try:
            client = MongoClient("mongodb+srv://admin:xAVAnVOSWLjYNjY6@cluster0.rr3bbtz.mongodb.net/?retryWrites=true&w=majority")
            db = client.ManagementSoftware
            Staff = db.Staff
            return Staff.find()
        except:
            tkinter.messagebox.showerror("Error","Could not establish connection to database")


if __name__=="__main__":
   if IsLatestVersion():
       LoginScreen()
   else:
       if tkinter.messagebox.askyesno("Update Needed","You do not have the latest version of the app installed, would you like to download the latest version?"):
           webbrowser.open("https://raw.githubusercontent.com/Viren070/Coursework/main/Installer.exe",2)
                
   

