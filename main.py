import tkinter 
from tkinter import ttk
import customtkinter 
import time
from pymongo import MongoClient
import os
from PIL import Image
staff_entry_window_is_open = False 
colour_theme = None
colour_changed = None
class Login(customtkinter.CTk):
    def __init__(self):
        global colour_theme
        super().__init__()
        if not(isDefined(colour_theme)):
            colour_theme = "blue"
        customtkinter.set_default_color_theme(colour_theme)
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

        self.login_button = customtkinter.CTkButton(self.login_frame, text = "Login", command = self.login)
        self.login_button.pack(pady=12,padx=10)
        self.mainloop()
    
    def login(self):
        if (self.username_entry.get() == "" and self.password_entry.get() == ""):
            global name 
            name = self.username_entry.get()
            self.destroy()
            
            
            Main = MainScreen()
            
        else:
            tkinter.messagebox.showinfo("Error","incorrect username or password")


class StaffEntryWindow(customtkinter.CTkToplevel):
    global staff_entry_window_is_open
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add New Staff Entry")
        self.rowconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.columnconfigure(0, weight=1)
        self.geometry("600x200")
        self.frame = customtkinter.CTkFrame(self, corner_radius=3)
        self.frame.grid(row=0, column=0)
       
        self.first_name_label = customtkinter.CTkLabel(self.frame, text="First Name:")
        self.first_name_label.grid(row=0, column=0, padx=2, pady=5)
        self.first_name_entry = customtkinter.CTkEntry(self.frame)
        self.first_name_entry.grid(row=0, column=1, padx=2, pady=5)
        
        self.last_name_label = customtkinter.CTkLabel(self.frame, text="Last Name:")
        self.last_name_label.grid(row=0, column=4, padx=1, pady=5)
        self.last_name_entry = customtkinter.CTkEntry(self.frame)
        self.last_name_entry.grid(row=0, column=5, padx=10, pady=5)
        
        self.department_label = customtkinter.CTkLabel(self.frame, text="Department:")
        self.department_label.grid(row=2, column=0, padx=10, pady=5)
        self.department_entry = customtkinter.CTkEntry(self.frame)
        self.department_entry.grid(row=2, column=1, padx=10, pady=5)
        
        self.submit_button = customtkinter.CTkButton(self.frame, text="Submit", command=self.submit_staff_entry)
        self.submit_button.grid(row=3, column=4, pady=10)

        self.cancel_button = customtkinter.CTkButton(self.frame, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=3, column=1, pady=10)
        
    def submit_staff_entry(self):
        global staff_entry_window_is_open
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        department = self.department_entry.get()
        self.cancel()
        self.destroy()
        # Add the staff entry to your database or data structure here
    def cancel(self):
        global staff_entry_window_is_open
        staff_entry_window_is_open = False 
        self.destroy()
class MainScreen(customtkinter.CTk):
    def __init__(self):
        global colour_theme
        global colour_changed
        global staff_entry_window_is_open 
        super().__init__()
        customtkinter.set_default_color_theme(colour_theme)
        self.title("Stock and staff system")
        self.geometry("700x450")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.name = name 
          # Themes: blue (default), dark-blue, green
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=name, image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=6, column=0, sticky="ew")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        

        # create third frame
        self.staff_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.staff_frame.grid_columnconfigure(0, weight=1)

        self.staff_frame_add_staff_button = customtkinter.CTkButton(self.staff_frame, text="New Staff Entry", command=self.new_staff_entry)
        self.staff_frame_add_staff_button.grid(row=0, column=0)
        # create settings frame 
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame_theme = customtkinter.CTkLabel(self.settings_frame, text="Theme", anchor="w", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.settings_frame_theme.grid(row=0, column=0, padx=15, pady=5, sticky = "W")
        
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.settings_frame, values=["Dark", "Light", "System"],command=self.change_appearance_mode_event) 
        self.appearance_mode_menu.grid(row=0, column=6, padx=20, pady=5, sticky="E")
        
        self.separator = ttk.Separator(self.settings_frame, orient='horizontal')
        self.separator.grid(row=1, column=0, columnspan=7, sticky='ew', padx=10, pady=5)

        self.settings_frame_colour_theme = customtkinter.CTkLabel(self.settings_frame, text="Colour Theme", anchor="w", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.settings_frame_colour_theme.grid(row=2, column=0, padx=15, pady=5, sticky="W")
        self.settings_frame_colour_theme_menu = customtkinter.CTkOptionMenu(self.settings_frame, values=["Blue","Dark-Blue","Green"], command=self.change_colour_theme_event)
        self.settings_frame_colour_theme_menu.grid(row=2, column=6, padx=20, pady=5, sticky="E")

        self.settings_frame_logout_button = customtkinter.CTkButton(self.settings_frame, text="Logout",anchor="s", command=self.logout)
        self.settings_frame_logout_button.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        # select default frame
        if isDefined(colour_changed):
            default_frame = "settings"
            colour_changed = None
        else:
            default_frame = "home"
        self.select_frame_by_name(default_frame)
        
        self.mainloop()

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
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
        if name == "frame_3":
            self.staff_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.staff_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()
        

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
    
    def settings_button_event(self):
        self.select_frame_by_name("settings")
    
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def change_colour_theme_event(self, new_colour_theme):
        global colour_theme
        global colour_changed
        colour_changed = True
        colour_theme = new_colour_theme.lower()
        self.destroy()
        Main = MainScreen()
    def new_staff_entry(self):
        global staff_entry_window_is_open
        global staff_entry_window
        if not staff_entry_window_is_open:
            staff_entry_window = StaffEntryWindow(self)
            staff_entry_window_is_open = True
        else:
            staff_entry_window.lift()
            
    def logout(self):
        self.destroy()
        Sys = Login()

def isDefined(variable):
    if variable is not None:
        return True
    else:
        return False
if __name__=="__main__":
    Sys = Login()

'''
#xAVAnVOSWLjYNjY6
client = MongoClient("mongodb+srv://admin:xAVAnVOSWLjYNjY6@cluster0.rr3bbtz.mongodb.net/?retryWrites=true&w=majority")

db = client.ManagementSoftware
Staff = db.Staff
Customers = db.Customers

staff_entry=[{
                "name": { "first": "John", "last": "Doe" },
                "password": { "hash": hash("Fdsf"), "salt": "salt" }
            },
            {
                "name": { "first": "Doe", "last": "John" },
                "password": { "hash": hash("password"), "salt": "salt" }
            }]
Staff.insert_one(staff_entry)

'''