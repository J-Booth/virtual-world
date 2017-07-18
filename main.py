# =============================================================================
# Author: Joshua Peter Booth
# Purpose: Game (GUI)
# File name: main.py
# From: 2016 - 2017
# =============================================================================
# Copyright (C) 2017  Joshua Peter Booth
#
# This program is free software: you can redistribute it and/or modify
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Full license in GNU Affero General Public License v3.0.txt
#
# Contact me:
# Email: joshb00th@icloud.com
#
# =============================================================================

from __init__ import *


class VirtualWorld(tk.Tk):

    def __init__(self, *args, **kwargs):
        """ Main body of the Virtual World Game """
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="img/virtualworld_logo.ico")
        tk.Tk.wm_title(self, "Virtual World")
        container = ttk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for file in (UserPage, LoginPage, SignUp, SettingsPage, ShopPage,
                     CoffeeShopPage):
            frame = file(container, self)
            self.frames[file] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)
        self.init_window()

    def init_window(self):
        """ Menu creation """
        _menu = tk.Menu(self.master)
        self.config(menu=_menu)

        file_menu = tk.Menu(_menu, tearoff=0)
        file_menu.add_command(label='Save')
        file_menu.add_command(label='Log out', command=lambda: self.logout())
        file_menu.add_command(label='Exit', command=lambda: self.destroy())
        _menu.add_cascade(label='File', menu=file_menu)

        edit_menu = tk.Menu(_menu, tearoff=0)
        edit_menu.add_command(label='Settings',
                              command=lambda: self.show_frame(SettingsPage))
        edit_menu.add_command(label='Test')
        _menu.add_cascade(label="Options", menu=edit_menu)

        help_menu = tk.Menu(_menu, tearoff=0)
        help_menu.add_command(label='General         F1')
        help_menu.add_command(label='Search')
        _menu.add_cascade(label="Help", menu=help_menu)

    def show_frame(self, cont):
        """ Bring frame to the user's view"""
        frame = self.frames[cont]
        frame.tkraise()

    def hide_frame(self, cont):
        frame = self.frames[cont]
        frame.lower()

    def menu_bar(self, controller):
        """ Menu bar creation """
        data = {}
        with open(current_user_file, 'r') as file:
            for line in file:
                _user, _pwd, _years, _money = line.strip().split(',')
                data[_user] = [_pwd, _years, _money]
        username = _user
        self.balance = data[username][2]

        hidden = True
        balance_formatted = 'Balance: $' + self.balance
        balance_label = ttk.Label(self, text=balance_formatted,
                                  font=MEDIUM_FONT)

        def current_user():
            """ Get the current user """
            nonlocal username
            username = User.get_current()['username']
            newest_balance = User.get_current()['balance']

            return {"username": username, "balance": newest_balance}

        def toggle_entry():
            """ Balance button toggling """
            nonlocal hidden
            newest_balance = current_user()["balance"]
            if self.balance == newest_balance:
                if hidden:
                    balance_label.grid(row=22, column=1, columnspan=11)
                else:
                    balance_label.grid_remove()
            elif self.balance != newest_balance:
                if hidden:
                    self.balance = newest_balance
                    balance_label.configure(text='Balance: $' + self.balance)
                    balance_label.grid(row=22, column=1, columnspan=11)
                else:
                    balance_label.grid_remove()
            else:
                raise ValueError("Balance not valid!")
            hidden = not hidden

        # Menu bar buttons

        balance_img = tk.PhotoImage(file="img/menu/balance_button.gif")
        balance_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                   width=30, height=30, image=balance_img,
                                   command=toggle_entry)
        balance_button.grid(row=22, column=1, sticky="W", pady=20)
        balance_button.image = balance_img

        setting_img = tk.PhotoImage(file="img/menu/settings_button.gif")
        setting_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                   width=30, height=30, image=setting_img,
                                   command=lambda:
                                   controller.show_frame(SettingsPage))
        setting_button.grid(row=22, column=0, sticky="E", pady=20)
        setting_button.image = setting_img

        help_img = tk.PhotoImage(file="img/menu/help_button.gif")
        help_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                width=30, height=30, image=help_img)
        help_button.grid(row=22, column=1, sticky="E", pady=20, padx=13)
        help_button.image = help_img

        home_img = tk.PhotoImage(file="img/menu/home_button.gif")
        home_button = tk.Button(self, compound=tk.TOP, relief="flat", width=30,
                                height=30, image=home_img, command=lambda:
                                controller.show_frame(UserPage))
        home_button.grid(row=22, column=0, sticky="W", padx=13, pady=20)
        home_button.image = home_img

        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=22, column=10, columnspan=5, sticky="E")
        back_button.image = back_img

    def back_button(self):
        self.controller.show_frame(UserPage)

    def logout(self):
        """ Appending current_user.txt with a guest user """
        user = "Guest" + ',' + "None" + ',' + "50" + ',' + "1000000"
        with open(current_user_file, 'w') as f:
            f.write(user)
        self.show_frame(LoginPage)


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        """ Where the user can login to Virtual World """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header Image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.login_page_logo = tk.Label(self, image=self.Logo)
        self.login_page_logo.grid(row=0, rowspan=12, column=0, columnspan=16)

        # Header
        login_label = ttk.Label(self, text="Login", font=LARGE_FONT)
        login_label.grid(row=14, rowspan=2, column=5, columnspan=6, pady=15)

        # Sign in Labels and Entries
        username_label = ttk.Label(self, text="Username:", font=MEDIUM_FONT)
        username_label.grid(row=16, column=5, columnspan=5, sticky="W")
        self.username = ttk.Entry(self)
        self.username.grid(row=16, column=9, sticky="e")

        password_label = ttk.Label(self, text="Password:", font=MEDIUM_FONT)
        password_label.grid(row=17, column=5, columnspan=5, sticky="W")
        self.password = ttk.Entry(self, show="*")
        self.password.grid(row=17, column=9, sticky="e")

        # ERROR Labels
        self.error_label = ttk.Label(self, text="")
        self.error_label.grid(row=16, column=10, columnspan=3)
        self.error_label2 = ttk.Label(self, text="")
        self.error_label2.grid(row=17, column=10, columnspan=6, padx=10,
                               sticky="W")

        # Buttons
        self.signup_img = tk.PhotoImage(file="img/menu/signup_button.gif")
        signup_command = (lambda: controller.show_frame(SignUp))
        self.signup_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                       width=80, height=40,
                                       image=self.signup_img,
                                       command=signup_command)
        self.signup_button.grid(row=18, column=5, columnspan=4, sticky="W",
                                pady=5)
        self.signup_button.image = self.signup_img

        sign_in_img = tk.PhotoImage(file="img/menu/submit_button.gif")
        sign_in_command = (lambda: self.sign_in_button())
        sign_in_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                   width=80, height=40, image=sign_in_img,
                                   command=sign_in_command)
        sign_in_button.grid(row=18, column=6, columnspan=5, sticky="E",
                            padx=20, pady=5)
        sign_in_button.image = sign_in_img

        guest_img = tk.PhotoImage(file="img/menu/guest_button.gif")
        guest_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                 width=150, height=40, image=guest_img,
                                 command=lambda: self.guest_button())
        guest_button.grid(row=19, column=2, columnspan=8, sticky="E", padx=35,
                          pady=5)
        guest_button.image = guest_img

    def sign_in_button(self):
        """ Check user's info and sign them in """
        username = self.username.get()
        password = self.password.get()
        name_and_pass = username + ',' + password
        full_user_data = Check.all_user_data(name_and_pass)
        print(name_and_pass)
        if username == '':
            if username == '' and password == '':
                print("Entering nothing will not work.")
            else:
                print("You must enter a username.")
            self.error_label.configure(text="Incorrect", foreground="red")
            self.error_label2.configure(text="Username/Password",
                                        foreground="red")
            return False
        elif Check.in_user_data(full_user_data):
            with open(current_user_file, 'w') as f:
                f.write(full_user_data)
            self.error_label.configure(text="User", foreground="green")
            self.error_label2.configure(text="Accepted!", foreground="green")
            success_command = (lambda: self.controller.show_frame(UserPage))
            self.error_label2.after(1250, success_command)
            print("User '{}' Exists!".format(self.username.get()))
        else:
            print("Incorrect Username/Password")
            self.error_label.configure(text="Incorrect", foreground="red")
            self.error_label2.configure(text="Username/Password",
                                        foreground="red")
            return False

    def guest_button(self):
        """" Takes the user (without a login) to the user homepage """
        print('guest button')
        with open(current_user_file, 'w') as f:
            f.write('Guest,None,50,1000000')
        self.controller.show_frame(UserPage)


class SignUp(tk.Frame):
    def __init__(self, parent, controller):
        """ A user can signup to Virtual World and have their info saved """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header Image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.sign_in_logo = tk.Label(self, image=self.Logo)
        self.sign_in_logo.grid(row=0, rowspan=12, column=0, columnspan=16)

        # Header
        signup_title = ttk.Label(self, text="Sign Up", font=LARGE_FONT)
        signup_title.grid(row=14, rowspan=2, column=5, columnspan=6, pady=15)

        # Sign up Entries
        username_label = ttk.Label(self, text="Username:", font=MEDIUM_FONT)
        username_label.grid(row=17, column=5, columnspan=5, sticky="W")
        self.username = ttk.Entry(self)
        self.username.grid(row=17, column=9, sticky="e")

        password_label = ttk.Label(self, text="Password:", font=MEDIUM_FONT)
        password_label.grid(row=18, column=5, columnspan=5, sticky="W")
        self.password = ttk.Entry(self)
        self.password.grid(row=18, column=9, sticky="e")

        age_label = ttk.Label(self, text="Age:", font=MEDIUM_FONT)
        age_label.grid(row=19, column=5, columnspan=5, sticky="W")
        self.age = ttk.Entry(self)
        self.age.grid(row=19, column=9, sticky="e")

        # ERROR Labels
        self.name_error_label = ttk.Label(self, text="", foreground="red")
        self.name_error_label.grid(row=17, column=11, columnspan=4)

        self.pwd_error_label = ttk.Label(self, text="", foreground="red")
        self.pwd_error_label.grid(row=18, column=11, columnspan=4)

        self.age_error_label = tk.Label(self, text="", foreground="red")
        self.age_error_label.grid(row=19, column=11, columnspan=4)

        # Buttons
        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=21, column=5, columnspan=4, sticky="W", pady=5)
        back_button.image = back_img

        submit_img = tk.PhotoImage(file="img/menu/submit_button.gif")
        submit_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                  width=80, height=40, image=submit_img,
                                  command=lambda: self.submit_button())
        submit_button.grid(row=21, column=6, columnspan=5, sticky="E",
                           padx=20, pady=5)
        submit_button.image = submit_img

    def back_button(self):
        """ Go back to the Login page """
        self.controller.show_frame(LoginPage)

    def create_user(self, username, password, age):
        """ Adds the user to the text file, shows a success message then
            returns the user back to the login page. """
        User.new(username, password, age)
        self.name_error_label.configure(text="")  # ttk label
        self.pwd_error_label.configure(text="", )  # ttk label
        self.age_error_label.configure(text="User Created!", fg="green")  # tk
        self.age_error_label.after(2500, self.back_button)

    def submit_button(self):
        """ Check user input then output a success/fail message """
        if Check.username(self.username.get()):
            username = self.username.get()
            if Check.password(self.password.get()):
                password = self.password.get()
                if Check.age(self.age.get()):
                    age = self.age.get()
                    self.create_user(username, password, age)
                else:
                    print("Age Failed")
                    self.name_error_label.configure(text="")
                    self.pwd_error_label.configure(text="")
                    self.age_error_label.configure(text="Invalid age",
                                                   foreground="red")
            else:
                print("Password Failed")
                self.name_error_label.configure(text="")
                self.pwd_error_label.configure(text="Invalid password",
                                               foreground="red")
        else:
            print("Username Failed.")
            self.name_error_label.configure(text="Invalid username",
                                            foreground="red")


class UserPage(tk.Frame):

    def __init__(self, parent, controller):
        """ User's Homepage """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header Image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.user_page_logo = tk.Label(self, image=self.Logo)
        self.user_page_logo.grid(row=0, rowspan=12, column=0, columnspan=16)

        # Header
        welcome_label = ttk.Label(self, text="Welcome", font=LARGE_FONT)
        welcome_label.grid(row=14, rowspan=2, column=1, columnspan=11, pady=15)

        # Buttons
        shop_img = tk.PhotoImage(file="img/shops/shop_button.gif")
        shop_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=shop_img,
                                command=lambda: self.shops_button())
        shop_button.grid(row=18, column=1, columnspan=11)
        shop_button.image = shop_img

        game_img = tk.PhotoImage(file="img/games/game_button.gif")
        game_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=game_img,
                                command=lambda: self.games_button())
        game_button.grid(row=19, column=1, columnspan=11)
        game_button.image = game_img

        task_img = tk.PhotoImage(file="img/tasks/task_button.gif")
        task_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=task_img,
                                command=lambda: self.tasks_button())
        task_button.grid(row=20, column=1, columnspan=11)
        task_button.image = task_img

        VirtualWorld.menu_bar(self, controller)

        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=22, column=10, columnspan=5, sticky="E")
        back_button.image = back_img

    def shops_button(self):
        self.controller.show_frame(ShopPage)

    def games_button(self):
        # self.controller.show_frame(GamePage)
        pass

    def tasks_button(self):
        # self.controller.show_frame(TaskPage)
        pass

    def back_button(self):
        """ Appending current_user.txt with a guest user """
        user = "Guest,None,50,1000000"
        with open(current_user_file, 'w') as f:
            f.write(user)
        self.controller.show_frame(LoginPage)


class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        """ For the user to change their settings """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header Image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.settings_page_logo = tk.Label(self, image=self.Logo)
        self.settings_page_logo.grid(row=0, rowspan=12, column=0,
                                     columnspan=16)

        # Header
        shops_label = ttk.Label(self, text="Settings", font=LARGE_FONT)
        shops_label.grid(row=14, rowspan=2, column=1, columnspan=11, pady=12)

        # Buttons
        name_change_link = "img/settings/change_name.gif"
        name_change_img = tk.PhotoImage(file=name_change_link)
        name_window = (lambda: self.open_window("Name"))
        name_change_button = tk.Button(self, relief="flat", width=120,
                                       height=30, image=name_change_img,
                                       command=name_window)
        name_change_button.grid(row=18, column=1, columnspan=11)
        name_change_button.image = name_change_img

        pwd_change_link = "img/settings/change_password.gif"
        pwd_change_img = tk.PhotoImage(file=pwd_change_link)
        pwd_window = (lambda: self.open_window("Password"))
        pwd_change_button = tk.Button(self, relief="flat", width=120,
                                      height=30, image=pwd_change_img,
                                      command=pwd_window)
        pwd_change_button.grid(row=19, column=1, columnspan=11)
        pwd_change_button.image = pwd_change_img

        age_change_link = "img/settings/change_age.gif"
        age_change_img = tk.PhotoImage(file=age_change_link)
        age_window = (lambda: self.open_window("Age"))
        age_change_button = tk.Button(self, relief="flat", width=120,
                                      height=30, image=age_change_img,
                                      command=age_window)
        age_change_button.grid(row=20, column=1, columnspan=11)
        age_change_button.image = age_change_img

        del_user_link = "img/settings/delete_user.gif"
        del_user_img = tk.PhotoImage(file=del_user_link)
        del_window = (lambda: self.open_window("Delete"))
        del_user_button = tk.Button(self, relief="flat", width=120, height=30,
                                    image=del_user_img, command=del_window)
        del_user_button.grid(row=21, column=1, columnspan=11)
        del_user_button.image = del_user_img

        self.toplevel = None

        VirtualWorld.menu_bar(self, controller)

        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=22, column=10, columnspan=5, sticky="E")
        back_button.image = back_img

    def open_window(self, setting):
        """ Username and Password window """
        if self.toplevel is None:
            current_user = Check.file()['current_user']
            if 'Guest,None,50,1000000' in list(current_user):
                print('Guest users cannot change their information!')
                return False
            else:
                pass

            self.toplevel = tk.Toplevel(self)
            self.toplevel.protocol('WM_DELETE_WINDOW',
                                   lambda: self.remove_window())
            self.toplevel.focus_set()
            self.toplevel.resizable(width=False, height=False)
            self.toplevel.setting = setting
            self.toplevel.title(setting)

            # Entries
            username_label = ttk.Label(self.toplevel, text="Username:",
                                       font=MEDIUM_FONT)
            username_label.grid(row=0, column=0, sticky="W", pady=5, padx=12)
            self.toplevel.username = ttk.Entry(self.toplevel)
            self.toplevel.username.grid(row=1, column=0, padx=15)

            password_label = ttk.Label(self.toplevel, text="Password:",
                                       font=MEDIUM_FONT)
            password_label.grid(row=2, column=0, sticky="W", pady=5, padx=12)
            self.toplevel.password = ttk.Entry(self.toplevel, show="*")
            self.toplevel.password.grid(row=3, column=0, padx=15)

            submit_command = (lambda: self.submit_button())
            cancel_command = (lambda: self.remove_window())

            # Buttons
            self.toplevel.submit = ttk.Button(self.toplevel, text="Submit",
                                              command=submit_command)
            self.toplevel.submit.grid(row=6, column=0, sticky="W", pady=5,
                                      padx=3)

            self.toplevel.cancel = ttk.Button(self.toplevel, text="Cancel",
                                              command=cancel_command)
            self.toplevel.cancel.grid(row=6, column=0, sticky="E", pady=5)

            # ERROR Labels
            self.toplevel.user_info = ttk.Label(self.toplevel, text="",
                                                font=MEDIUM_FONT)
            self.toplevel.user_info.grid(row=8, column=0)

            w = 157  # width for toplevel
            h = 220  # height for toplevel

            # get screen width and height
            ws = self.toplevel.winfo_screenwidth()  # width of the screen
            hs = self.toplevel.winfo_screenheight()  # height of the screen

            # calculate x and y coordinates for the Tk root window
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            # set the dimensions of the screen and where it is placed
            self.toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y - 30))
            self.toplevel.mainloop()

    def remove_window(self):
        """ Removes Username and Password window """
        self.toplevel.destroy()
        self.toplevel = None

    def back_button(self):
        """ Go back to the Login page """
        self.controller.hide_frame(SettingsPage)

    def submit_button(self):
        """ Check user input and change the setting window
            for the specified setting """
        username = self.toplevel.username.get()
        password = self.toplevel.password.get()
        user_info = username + ',' + password

        change_name = (lambda: self.change_name(new_name.get()))
        change_pwd = (lambda: self.change_password(new_password.get()))
        change_age = (lambda: self.change_age(self.toplevel.new_age.get()))
        del_user = (lambda: self.delete_user(username))

        if user_info == ',':
            print("Nothing was entered")
            self.toplevel.user_info.configure(text="Nothing entered!",
                                              foreground="red")
            return False

        elif Check.in_user_data(Check.all_user_data(user_info)):
            print("User '{}' Exists!".format(username))
            if self.toplevel.setting == "Name":
                new_name_label = ttk.Label(self.toplevel, font=MEDIUM_FONT,
                                           text=" New Username:")
                new_name_label.grid(row=4, column=0, sticky="W", pady=5,
                                    padx=7)
                new_name = ttk.Entry(self.toplevel)
                new_name.grid(row=5, column=0)
                self.toplevel.submit = ttk.Button(self.toplevel, text="Change",
                                                  command=change_name)
                self.toplevel.submit.grid(row=6, column=0, sticky="W", pady=5,
                                          padx=3)

            elif self.toplevel.setting == "Password":
                new_password_label = ttk.Label(self.toplevel,
                                               text="New Password:",
                                               font=MEDIUM_FONT)
                new_password_label.grid(row=4, column=0, sticky="W", pady=5,
                                        padx=12)
                new_password = ttk.Entry(self.toplevel)
                new_password.grid(row=5, column=0)
                self.toplevel.submit = ttk.Button(self.toplevel, text="Change",
                                                  command=change_pwd)
                self.toplevel.submit.grid(row=6, column=0, sticky="W", pady=5,
                                          padx=3)

            elif self.toplevel.setting == "Age":
                new_age_label = ttk.Label(self.toplevel, text="New Age:",
                                          font=MEDIUM_FONT)
                new_age_label.grid(row=4, column=0, sticky="W", pady=5,
                                   padx=12)
                self.toplevel.new_age = ttk.Entry(self.toplevel)
                self.toplevel.new_age.grid(row=5, column=0)
                self.toplevel.submit = ttk.Button(self.toplevel, text="Change",
                                                  command=change_age)
                self.toplevel.submit.grid(row=6, column=0, sticky="W", pady=5,
                                          padx=3)

            elif self.toplevel.setting == "Delete":
                delete_button = ttk.Button(self.toplevel, text="Delete User",
                                           command=del_user)
                delete_button.grid(row=6, column=0, sticky="W", pady=5, padx=3)

            else:
                raise NameError("Setting name is invalid!")

        else:
            print("User does not exist!")
            return False

    def change_name(self, new_name):
        """ Check name and either change or reject name """
        if Check.username(new_name):
            success_label = ttk.Label(self.toplevel, text="Username Accepted!",
                                      foreground="green")
            success_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

            print("Changing username...")
            old_name = self.toplevel.username.get()
            User.name_change(old_name, new_name)

            success_label.after(2500, lambda: self.remove_window())

        else:
            failure_label = ttk.Label(self.toplevel, text="Username Declined!",
                                      foreground="red")
            failure_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

    def change_password(self, new_password):
        """ Check password and either change or reject password """
        if Check.password(new_password):
            success_label = ttk.Label(self.toplevel, text="Password Accepted!",
                                      foreground="green")
            success_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

            print("Changing password...")
            username = self.toplevel.username.get()
            User.password_change(username, new_password)

            success_label.after(2500, lambda: self.remove_window())

        else:
            failure_label = ttk.Label(self.toplevel, text="Password Declined!",
                                      foreground="red")
            failure_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

    def change_age(self, new_age):
        """ Check age and either change or reject age """
        if Check.age(new_age):
            success_label = ttk.Label(self.toplevel, text="Age Accepted!",
                                      foreground="green")
            success_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

            print("Changing age...")
            username = self.toplevel.username.get()
            User.age_change(username, new_age)

            success_label.after(2500, lambda: self.remove_window())

        else:
            failure_label = ttk.Label(self.toplevel, text="Age Declined!",
                                      foreground="red")
            failure_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

    def delete_user(self, username):
        """ Delete the user """
        success_label = ttk.Label(self.toplevel, text="Deleting user...",
                                  foreground="green")
        success_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

        print("Deleting user...")
        User.delete(username)
        del_window = (lambda: self.remove_window_del(self.controller))
        success_label.after(2500, del_window)

    def remove_window_del(self, controller):
        """ Destroy the window and sign out the current user """
        self.toplevel.destroy()
        self.toplevel = None
        controller.show_frame(LoginPage)


class ShopPage(tk.Frame):

    def __init__(self, parent, controller):
        """ Display a list of shops the user can visit """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header Image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.shop_page_logo = tk.Label(self, image=self.Logo)
        self.shop_page_logo.grid(row=0, rowspan=12, column=0, columnspan=16)

        # Header
        shops_label = ttk.Label(self, text="Shops", font=LARGE_FONT)
        shops_label.grid(row=14, rowspan=2, column=1, columnspan=11, pady=15)

        # Buttons
        coffee_img = tk.PhotoImage(file="img/shops/coffee/coffee_button.gif")
        coffee_button = tk.Button(self, relief="flat", width=180, height=40,
                                  image=coffee_img,
                                  command=lambda: self.shop_coffee())
        coffee_button.grid(row=18, column=1, columnspan=12)
        coffee_button.image = coffee_img

        # tech shop image
        tech_img = tk.PhotoImage(file="img/shops/coffee/coffee_button.gif")
        tech_button = tk.Button(self, relief="flat", width=180, height=40,
                                image=tech_img)
        #                       command= lambda: shop_tech(self, ShopPage))
        tech_button.grid(row=19, column=1, columnspan=12)
        tech_button.image = tech_img

        # pizza shop image
        pizza_img = tk.PhotoImage(file="img/shops/coffee/coffee_button.gif")
        pizza_button = tk.Button(self, relief="flat", width=180, height=40,
                                 image=pizza_img)
        #                        command= lambda: shop_pizza(self, ShopPage))
        pizza_button.grid(row=20, column=1, columnspan=12)
        pizza_button.image = pizza_img

        VirtualWorld.menu_bar(self, controller)

    def back_button(self):
        self.controller.show_frame(UserPage)

    def shop_coffee(self):
        self.controller.show_frame(CoffeeShopPage)

    # def shop_tech(self):
    #     self.controller.show_frame(TechShopPage)
    #
    # def shop_pizza(self):
    #     self.controller.show_frame(PizzaShopPage)

    def balance_button(self):
        # To be finished
        # print("Balance: ${:.2f}".format(user.balance))
        pass


class CoffeeShopPage(tk.Frame):
    cappu_cost = 3.50
    espre_cost = 3.00
    flatw_cost = 2.50
    latte_cost = 4.50
    mocha_cost = 3.50

    def __init__(self, parent, controller):
        """ Coffee Shop where the user can buy different coffees """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header Image
        self.Logo = tk.PhotoImage(file="img/shops/coffee/coffee_cup.gif",
                                  height="120")
        self.coffee_logo = tk.Label(self, image=self.Logo)
        self.coffee_logo.grid(row=0, rowspan=5, column=0, columnspan=16)

        # Header
        menu_label = ttk.Label(self, text="Menu", font=LARGE_FONT)
        menu_label.grid(row=6, rowspan=2, column=0, columnspan=16, pady=15)

        # Sub-headers
        type_label = ttk.Label(self, text="Type", font=MEDIUM_FONT)
        type_label.grid(row=8, column=1, pady=10, sticky="W")
        price_label = ttk.Label(self, text="Price", font=MEDIUM_FONT)
        price_label.grid(row=8, column=4, columnspan=3, pady=10)
        amount_label = ttk.Label(self, text="Amount", font=MEDIUM_FONT)
        amount_label.grid(row=8, column=8, columnspan=6, pady=10)

        VirtualWorld.menu_bar(self, controller)

        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=22, column=10, columnspan=5, sticky="E")
        back_button.image = back_img

        # Coffee type labels, prices and entries

        # Cappuccino label, price and amount entry
        self.cappuccino_label = ttk.Label(self, text="Cappuccino",
                                          font=MEDIUM_FONT)
        self.cappuccino_label.grid(row=14, column=1, columnspan=5, pady=10,
                                   sticky="W")
        self.cappuccino_price = ttk.Label(self, font=MEDIUM_FONT,
                                          text="${:.2f}"
                                          .format(self.cappu_cost))
        self.cappuccino_price.grid(row=14, column=4, columnspan=3, pady=10)
        cappuccino_vcmd = (self.register(self.confirm), '%P', '%S',
                           'cappuccino')
        self.cappuccino_amount = ttk.Entry(self, validate="key",
                                           justify="center",
                                           validatecommand=cappuccino_vcmd)
        self.cappuccino_amount.grid(row=14, column=10, columnspan=2, pady=10)

        # Espresso label, price and amount entry
        self.espresso_label = ttk.Label(self, text="Espresso",
                                        font=MEDIUM_FONT)
        self.espresso_label.grid(row=15, column=1, columnspan=5, pady=10,
                                 sticky="W")
        self.espresso_price = ttk.Label(self, font=MEDIUM_FONT,
                                        text="${:.2f}".format(self.espre_cost))
        self.espresso_price.grid(row=15, column=4, columnspan=3, pady=10)
        espresso_vcmd = (self.register(self.confirm), '%P', '%S', 'espresso')
        self.espresso_amount = ttk.Entry(self, validate="key",
                                         justify="center",
                                         validatecommand=espresso_vcmd)
        self.espresso_amount.grid(row=15, column=10, columnspan=2, pady=10)

        # Flat white label, price and amount entry
        self.flat_w_label = ttk.Label(self, text="Flat White",
                                      font=MEDIUM_FONT)
        self.flat_w_label.grid(row=16, column=1, columnspan=5, pady=10,
                               sticky="W")
        self.flat_w_price = ttk.Label(self, font=MEDIUM_FONT,
                                      text="${:.2f}".format(self.flatw_cost))
        self.flat_w_price.grid(row=16, column=4, columnspan=3, pady=10)
        flat_w_vcmd = (self.register(self.confirm), '%P', '%S', 'flat_white')
        self.flat_w_amount = ttk.Entry(self, validate="key", justify="center",
                                       validatecommand=flat_w_vcmd)
        self.flat_w_amount.grid(row=16, column=10, columnspan=2, pady=10)

        # Latte label, price and amount entry
        self.latte_label = ttk.Label(self, text="Latte", font=MEDIUM_FONT)
        self.latte_label.grid(row=17, column=1, columnspan=5, pady=10,
                              sticky="W")
        self.latte_price = ttk.Label(self, font=MEDIUM_FONT,
                                     text="${:.2f}".format(self.latte_cost))
        self.latte_price.grid(row=17, column=4, columnspan=3, pady=10)
        latte_vcmd = (self.register(self.confirm), '%P', '%S', 'latte')
        self.latte_amount = ttk.Entry(self, validate="key", justify="center",
                                      validatecommand=latte_vcmd)
        self.latte_amount.grid(row=17, column=10, columnspan=2, pady=10)

        # Mocha label, price and amount entry
        self.mocha_label = ttk.Label(self, text="Mocha", font=MEDIUM_FONT)
        self.mocha_label.grid(row=18, column=1, columnspan=5, pady=10,
                              sticky="W")
        self.mocha_price = ttk.Label(self, font=MEDIUM_FONT,
                                     text="${:.2f}".format(self.mocha_cost))
        self.mocha_price.grid(row=18, column=4, columnspan=3, pady=10)
        mocha_vcmd = (self.register(self.confirm), '%P', '%S', 'mocha')
        self.mocha_amount = ttk.Entry(self, validate="key", justify="center",
                                      validatecommand=mocha_vcmd)
        self.mocha_amount.grid(row=18, column=10, columnspan=2, pady=10)

        # Maximum number of coffees
        self.amount_label = ttk.Label(self, font=SMALL_FONT, foreground="red",
                                      text="Maximum of 9 of each coffee type.")
        self.amount_label.grid(row=19, column=1, columnspan=9)

        # Total
        total_label = ttk.Label(self, text="Total:", font=MEDIUM_FONT)
        total_label.grid(row=20, column=1, sticky="W")
        self.total_cost_label = ttk.Label(self, font=MEDIUM_FONT,
                                          text="$0.00")
        self.total_cost_label.grid(row=20, column=1, columnspan=6,
                                   padx=10, sticky="E")

        self.toplevel = None

        # Buttons

        # Erase button
        self.erase_button = ttk.Button(self, text="Erase all",
                                       command=lambda: self.erase())
        self.erase_button.grid(row=19, column=9, columnspan=4, pady=5)

        # Purchase Button
        self.buy_img = tk.PhotoImage(file="img/shops/purchase_button.gif")
        buy_window = (lambda: self.order())
        self.buy_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                    width=80, height=40, image=self.buy_img,
                                    command=buy_window, state='disabled')
        self.buy_button.grid(row=20, column=7, columnspan=6, sticky="E",
                             pady=5)
        self.buy_button.image = self.buy_img

        CoffeeShopPage.reset_order_data()

    def erase(self):
        """
        Removes all data from the entries.
        """
        for amount in (self.cappuccino_amount, self.espresso_amount,
                       self.flat_w_amount, self.latte_amount,
                       self.mocha_amount):
            amount.delete(0, 1)
            amount.insert(0, "")

    def confirm(self, P, S, _type):
        """
        Only allow a 1 digit integer and if the total of all the entries
        is greater than one, enable the cart button.

        :param P: allowed value (%P)
        :param S: text being inserted (%S)
        :param _type: the coffee type (str)
        :return: True or False
        """
        allowed_value = P  # So the values of P and S are understandable
        inserted_value = S  # But are set as param so that %P and %S are used.

        if len(allowed_value) == 0:
            inserted_value = 0
            allowed_value = "0"
        else:
            try:
                inserted_value = int(inserted_value)
            except ValueError:
                print("Input is not an integer!")
        if isinstance(inserted_value, int) and 0 < len(allowed_value) == 1:
            with open(COFFEE_DATA_F, 'r') as file:
                current_data = [line.strip() for line in file]
            data = {}
            with open(COFFEE_DATA_F, 'r') as file:
                for line in file:
                    option, value = line.strip().split(':')
                    data[option] = value
            if data[_type] == str(allowed_value):
                print("No changes to be made to {}".format(COFFEE_DATA_F))
            else:
                current_data.remove('{}:{}'.format(_type, data[_type]))
                current_data.remove('{}:{}'.format('total', data['total']))
                data[_type] = int(allowed_value)
                data['total'] = 0
                total = 0
                for item in current_data:
                    item = item.split(':')
                    item.pop(0)
                    total += int(item[0])
                data['total'] = total + data[_type]
                current_data.append('{}:{}'.format(_type, data[_type]))
                current_data.append('{}:{}'.format('total', data['total']))

                cappuccino_total = 0
                espresso_total = 0
                flat_w_total = 0
                latte_total = 0
                mocha_total = 0
                for item in current_data:
                    item = item.split(':')
                    if item[0] == 'cappuccino' and int(item[1]) > 0:
                        cappuccino_total = int(item[1]) * self.cappu_cost
                    elif item[0] == 'espresso' and int(item[1]) > 0:
                        espresso_total = int(item[1]) * self.espre_cost
                    elif item[0] == 'flat_white' and int(item[1]) > 0:
                        flat_w_total = int(item[1]) * self.flatw_cost
                    elif item[0] == 'latte' and int(item[1]) > 0:
                        latte_total = int(item[1]) * self.latte_cost
                    elif item[0] == 'mocha' and int(item[1]) > 0:
                        mocha_total = int(item[1]) * self.mocha_cost
                new_total = cappuccino_total + espresso_total + \
                    flat_w_total + latte_total + mocha_total

            if int(data['total']) > 0:
                self.total_cost_label.configure(text="${:.2f}"
                                                .format(new_total))
                self.buy_button.configure(state='normal')
            else:
                self.total_cost_label.configure(text="$0.00")
                self.buy_button.configure(state='disabled')
            with open(COFFEE_DATA_F, 'w') as file:
                print("Writing new data to {}".format(COFFEE_DATA_F))
                file.write('\n'.join(current_data))
            return True
        else:
            self.bell()
            return False

    def back_button(self):
        """ Go back to the Login page """
        self.controller.show_frame(ShopPage)

    def submit_button(self):
        try:
            username = self.toplevel.username.get()
            password = self.toplevel.password.get()
        except AttributeError:
            username = "Guest"
            password = "None"

        name_and_pass = username + ',' + password
        amount = float(self.total_cost_label.cget("text").strip('$'))
        if name_and_pass == ',':
            print("Nothing was entered!")
            self.toplevel.user_info.configure(text="Nothing entered!",
                                              foreground="red")
            return False
        elif Check.in_user_data(Check.all_user_data(name_and_pass)):
            print("User '{}' Exists!".format(username))
            self.toplevel.user_info.configure(text="")
            purchase = (lambda: self.purchase(username, amount))
            self.toplevel.submit = ttk.Button(self.toplevel, text="Confirm",
                                              command=purchase)
            self.toplevel.submit.grid(row=13, column=6, columnspan=10, pady=5)
        else:
            self.toplevel.error_label = ttk.Label(
                self.toplevel, text="Incorrect username/password",
                foreground="red")
            self.toplevel.error_label.grid(row=14, column=9, columnspan=20)
            return False

    def purchase(self, username, amount):
        if username == 'Guest':
            self.toplevel.user_info.configure(text="Transaction successful",
                                              foreground="green")
            CoffeeShopPage.reset_order_data()
        elif User.withdraw(username, amount) is True:
            self.toplevel.user_info.configure(text="Transaction successful",
                                              foreground="green")
            CoffeeShopPage.reset_order_data()
        elif User.withdraw(username, amount) == "insufficient_funds":
            self.toplevel.user_info.configure(text="Insufficient funds",
                                              foreground="red")
        else:
            self.toplevel.user_info.configure(text="Transaction failed",
                                              foreground="red")
        self.toplevel.user_info.after(2500, lambda: self.remove_window())

    @staticmethod
    def reset_order_data():
        """ Resets the COFFEE_DATA_F file. """
        order_data = ['cappuccino', 'espresso', 'flat_white', 'latte', 'mocha',
                      'total']
        new_data = []
        with open(COFFEE_DATA_F, 'w') as file:
            for data in order_data:
                new_data.append('{}:0'.format(data))
            file.write('\n'.join(new_data))

    def order(self):
        if self.toplevel is None:
            self.toplevel = tk.Toplevel(self)
            self.toplevel.protocol('WM_DELETE_WINDOW',
                                   lambda: self.remove_window())
            self.toplevel.focus_set()
            self.toplevel.resizable(width=False, height=False)
            self.toplevel.title('Order')

            order_label = ttk.Label(self.toplevel, text="Here is your order:",
                                    font=MEDIUM_FONT)
            order_label.grid(row=0, column=0, columnspan=20, padx=5, pady=5)
            type_label = ttk.Label(self.toplevel, text="Type", font=SMALL_FONT)
            type_label.grid(row=2, column=0, columnspan=10, pady=10, padx=5)
            price_label = ttk.Label(self.toplevel, text="Amount",
                                    font=SMALL_FONT)
            price_label.grid(row=2, column=10, columnspan=9, pady=10)
            amount_label = ttk.Label(self.toplevel, text="Price",
                                     font=SMALL_FONT)
            amount_label.grid(row=2, column=20, pady=10)

            data = {}
            with open(COFFEE_DATA_F, 'r') as file:
                count = 2
                for line in file:
                    option, value = line.strip().split(':')
                    data[option] = value
                    if int(data[option]) > 0:
                        if option == 'flat_white':
                            coffee_type = 'Flat White'
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.flatw_cost)
                        elif option == 'cappuccino':
                            coffee_type = option.title()
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.cappu_cost)
                        elif option == 'espresso':
                            coffee_type = option.title()
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.espre_cost)
                        elif option == 'latte':
                            coffee_type = option.title()
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.latte_cost)
                        elif option == 'mocha':
                            coffee_type = option.title()
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.mocha_cost)
                        elif option == 'total':
                            coffee_type = option.title()
                            price = self.total_cost_label.cget("text")
                        else:
                            coffee_type = option
                            price = ""

                        count += 1
                        ttk.Label(self.toplevel, text=coffee_type)\
                            .grid(row=count, column=0, columnspan=10)
                        ttk.Label(self.toplevel, text=data[option])\
                            .grid(row=count, column=10, columnspan=9)
                        ttk.Label(self.toplevel, text=price)\
                            .grid(row=count, column=20)

            with open(current_user_file, 'r') as file:
                if 'Guest,None,50,1000000' not in file:
                    # Entries
                    username_label = ttk.Label(self.toplevel, text="Username:",
                                               font=SMALL_FONT)
                    username_label.grid(row=9, column=7, columnspan=11, pady=5)
                    self.toplevel.username = ttk.Entry(self.toplevel)
                    self.toplevel.username.grid(row=10, sticky='W', padx=20,
                                                column=9, columnspan=12)

                    password_label = ttk.Label(self.toplevel, text="Password:",
                                               font=SMALL_FONT)
                    password_label.grid(row=11, column=7, columnspan=11,
                                        pady=5)
                    self.toplevel.password = ttk.Entry(self.toplevel, show="*")
                    self.toplevel.password.grid(row=12, sticky="E", padx=20,
                                                column=9, columnspan=12)

            submit_command = (lambda: self.submit_button())
            cancel_command = (lambda: self.remove_window())

            # Buttons
            self.toplevel.submit = ttk.Button(self.toplevel, text="Submit",
                                              command=submit_command)
            self.toplevel.submit.grid(row=13, column=6, columnspan=10, pady=5)

            self.toplevel.cancel = ttk.Button(self.toplevel, text="Cancel",
                                              command=cancel_command)
            self.toplevel.cancel.grid(row=13, column=16, columnspan=6, pady=5)

            # ERROR Labels
            self.toplevel.user_info = ttk.Label(self.toplevel, text="",
                                                font=SMALL_FONT)
            self.toplevel.user_info.grid(row=14, column=8, columnspan=20)

            w = 250  # width for toplevel
            h = 335  # height for toplevel

            # get screen width and height
            ws = self.toplevel.winfo_screenwidth()  # width of the screen
            hs = self.toplevel.winfo_screenheight()  # height of the screen

            # calculate x and y coordinates for the Tk root window
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            # set the dimensions of the screen and where it is placed
            self.toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y - 30))
            self.toplevel.mainloop()

    def remove_window(self):
        """ Removes Username and Password window """
        self.toplevel.destroy()
        self.toplevel = None


class Check:

    @staticmethod
    def file():
        """ 
        Check files exist and returns data within them:

        'user_names' - for user_names.txt
        'user_data' - for user_data.txt
        'current_user' - for current_user.txt
        'options' - for options.txt
        """

        def options():
            """ 
            Check options.txt exists and it is created if it does not exist.
            """
            while True:
                try:
                    with open(options_file, 'r') as file:
                        print("Opening the options file '{}'.".format(
                              options_file))
                        option_data = [line.strip() for line in file]
                    return option_data
                except FileNotFoundError:
                    print("Failed to open the 'options.txt' file")
                    with open(options_file, 'w') as file:
                        print("Creating options.txt...")
                        file.write("running:False\ntimes_opened:0")

        def user_names():
            """ 
            Check user_names.txt exists and it is created if it does not exist. 
            Returns name_data as list.
            """
            while True:
                try:
                    with open(user_names_file, 'r') as file:
                        print("Opening the user_names_file '{}'.".format(
                              user_names_file))
                        name_data = [line.strip() for line in file]
                    return name_data
                except FileNotFoundError:
                    print("Failed to open '{}'.".format(user_names_file))
                    with open(user_names_file, 'w') as file:
                        print("Creating '{}'...".format(user_names_file))
                        file.write("Guest")

        def user_data():
            """ 
            Check user_data.txt exists and it is created if it does not exist.
            """
            while True:
                try:
                    with open(user_data_file, 'r') as file:
                        print("Opening the user_data_file '{}'.".format(
                              user_data_file))
                        _all_data = [line.strip() for line in file]
                    return _all_data
                except FileNotFoundError:
                    print("Failed to open '{}'.".format(user_data_file))
                    with open(user_data_file, 'w') as file:
                        print("Creating '{}'...".format(user_data_file))
                        file.write("Guest,None,50,1000000")

        def current_user():
            """ 
            Check current_user.txt exists and it is created if it 
            does not exist.
            """
            while True:
                try:
                    with open(current_user_file, 'r') as file:
                        print("Opening the current_user_file '{}'.".format(
                              current_user_file))
                        current_user_data = [line.strip() for line in file]
                    return current_user_data
                except FileNotFoundError:
                    print("Failed to open '{}'".format(current_user_file))
                    with open(current_user_file, 'w') as file:
                        print("Creating '{}'...".format(current_user_file))
                        file.write("Guest,None,50,1000000")

        return {"options": options(), "user_names": user_names(),
                "user_data": user_data(), "current_user": current_user()}

    @staticmethod
    def in_user_data(user):
        """
        Check if user's info is in user_data.txt
        """
        with open(user_data_file, 'r') as file:
            if user is None:
                return False
            elif re.search(user, file.read()):
                return True
            else:
                return False

    @staticmethod
    def all_user_data(user_info):
        """
        Gets all user data from the username and password.
        :param user_info: str
        :return: str
        """
        username, password = user_info.split(',')
        try:
            age = User.get_data(username)['age']
            balance = User.get_data(username)['balance']
            return user_info + ',' + age + ',' + balance
        except KeyError:
            return None

    @staticmethod
    def username(name):
        if name in Check.file()["user_names"]:
            print("You cannot use that name as it is already taken.")
            return False
        elif name == '':
            print("You must enter something for your username.")
            return False
        elif re.match('^[\w\d_-]*$', name):
            print("Username Accepted.")
            return True
        else:
            print("Your username may only contain letters, numbers, ",
                  "or underscores.")
            return False

    @staticmethod
    def password(pwd):
        if re.match('^[\w\d_-]*$', pwd):
            print("Password Accepted.")
            return True
        else:
            print("Your password may only contain letters, numbers, ",
                  "or underscores.")
            return False

    @staticmethod
    def age(years_old):
        if not(re.match('^[\d]{2,3}$', years_old)):
            print("You must enter a two or three digit integer!")
            return False
        else:
            print("Age accepted")
            return True


class User:

    @staticmethod
    def new(username, password, age):
        """ Appending the user_data.txt with new user information"""
        balance = User.create_balance(age)
        user_data = Check.file()['user_data']
        str_age = str(age)
        str_bal = str(balance)
        new_user = username + ',' + password + ',' + str_age + ',' + str_bal
        user_data.append(new_user)

        with open(user_data_file, 'w') as f:
            f.write('\n'.join(user_data))
        with open(user_names_file, 'r') as u:
            user_names = [line.strip() for line in u]
        user_names.append(username)
        with open(user_names_file, 'w') as f:
            f.write('\n'.join(user_names))
        print("\nUser {} created!\n".format(username))

    @staticmethod
    def get_data(username=None):
        data = {}
        with open(user_data_file, 'r') as file:
            for line in file:
                _user, _pwd, _years, _money = line.strip().split(',')
                data[_user] = [_pwd, _years, _money]
        password = data[username][0]
        age = data[username][1]
        balance = data[username][2]
        return {"username": username, "password": password,
                "age": age, "balance": balance}

    @staticmethod
    def get_current():
        with open(current_user_file, 'r') as file:
            user, pwd, age, balance = file.readline().split(',')
        return {"username": user, "password": pwd,
                "age": age, "balance": balance}

    @staticmethod
    def create_balance(age):
        """ Create a balance for a new user based on their age """
        age = int(age)
        if age > 80:         # Over 80
            return 100000
        elif 80 > age > 60:  # 60 to 80 years
            return 75000
        elif 60 > age > 40:  # 40 to 60 years
            return 50000
        elif 40 > age > 20:  # 20 to 40 years
            return 25000
        elif 20 > age > 15:  # 15 to 20 years
            return 15000
        elif age < 15:		 # Under 15
            return 2000
        else:
            return 5000

    @staticmethod
    def name_change(old_name, new_name):
        """ Change the user's name and appends it to the text files
            user_data.txt and user_names.txt
        """
        user_data = list(Check.file()['user_data'])
        password = User.get_data(old_name)['password']
        age = User.get_data(old_name)['age']
        balance = User.get_data(old_name)['balance']

        del_user = old_name + ',' + password + ',' + age + ',' + balance
        user_data.remove(del_user)
        new_user = new_name + ',' + password + ',' + age + ',' + balance
        user_data.append(new_user)

        with open(user_data_file, 'w') as f:
            f.write('\n'.join(user_data))

        with open(user_names_file, 'r') as r:
            user_names = [line.strip() for line in r]
        user_names.remove(old_name)
        user_names.append(new_name)

        with open(user_names_file, 'w') as f:
            f.write('\n'.join(user_names))

        with open(current_user_file, 'w') as f:
            f.write(new_user)

        print("Your username is now '{}'.".format(new_name))

    @staticmethod
    def password_change(username, new_password):
        """ Change the user's password and appends it to user_data.txt """
        user_data = list(Check.file()['user_data'])
        old_password = User.get_data(username)['password']
        age = User.get_data(username)['age']
        balance = User.get_data(username)['balance']

        del_user = username + ',' + old_password + ',' + age + ',' + balance
        user_data.remove(del_user)
        new_user = username + ',' + new_password + ',' + age + ',' + balance
        user_data.append(new_user)

        with open(user_data_file, 'w') as f:
            f.write('\n'.join(user_data))

        print("Your password is now '{}'.".format(new_password))

    @staticmethod
    def age_change(username, new_age):
        """ Change the user's age and appends it to user_data.txt """
        user_data = list(Check.file()['user_data'])
        password = User.get_data(username)['password']
        old_age = User.get_data(username)['age']
        balance = User.get_data(username)['balance']

        del_user = username + ',' + password + ',' + old_age + ',' + balance
        user_data.remove(del_user)
        new_user = username + ',' + password + ',' + new_age + ',' + balance
        user_data.append(new_user)

        with open(user_data_file, 'w') as f:
            f.write('\n'.join(user_data))

        print("You are now {:d} years old.".format(int(new_age)))

    @staticmethod
    def delete(username):
        """
        Delete a user from the user data.

        :param username: str
        :return: None
        """
        user_data = list(Check.file()['user_data'])
        password = User.get_data(username)['password']
        age = User.get_data(username)['age']
        balance = User.get_data(username)['balance']

        del_user = username + ',' + password + ',' + age + ',' + balance
        user_data.remove(del_user)

        with open(user_data_file, 'w') as f:
            f.write('\n'.join(user_data))

        with open(user_names_file, 'r') as u:
            user_names = [line.strip() for line in u]

        user_names.remove(username)
        with open(user_names_file, 'w') as f:
            f.write('\n'.join(user_names))

    @staticmethod
    def withdraw(username, amount):
        """ Withdraws money from the user's current balance. """
        user_balance = User.get_data(username)['balance']
        if float(user_balance) >= amount:
            user_data = list(Check.file()['user_data'])
            password = User.get_data(username)['password']
            age = User.get_data(username)['age']
            print("Withdrawing {} from {}".format(amount, username))
            del_user = username + ',' + password + ',' + age + ',' + \
                user_balance
            user_data.remove(del_user)

            new_balance = str(float(user_balance) - amount)

            new_user = username + ',' + password + ',' + age + ',' + \
                new_balance
            user_data.append(new_user)

            with open(user_data_file, 'w') as f:
                f.write('\n'.join(user_data))
            return True
        elif int(user_balance) < amount:
            return "insufficient_funds"
        else:
            return False

    @staticmethod
    def deposit(username, amount):
        """ Withdraws money from the user's current balance. """
        user_balance = User.get_data(username)['balance']
        user_data = list(Check.file()['user_data'])
        password = User.get_data(username)['password']
        age = User.get_data(username)['age']
        print("Depositing {} from {}".format(amount, username))
        del_user = username + ',' + password + ',' + age + ',' + \
            user_balance
        user_data.remove(del_user)

        new_balance = str(float(user_balance) + amount)

        new_user = username + ',' + password + ',' + age + ',' + \
            new_balance
        user_data.append(new_user)

        with open(user_data_file, 'w') as f:
            f.write('\n'.join(user_data))


class Options:

    def __init__(self):
        """ Setting up default options """
        self.options = Options.get()
        if self.options['running'] is 'True':
            sys.exit()
        else:
            self.options['running'] = 'True'
            self.options['times_opened'] = int(self.options['times_opened']) + 1
            new_data = self.options
            Options.update(new_data)

    @staticmethod
    def get():
        """ Return all options. """
        data = {}
        with open(options_file, 'r') as file:
            for line in file:
                option, value = line.strip().split(':')
                data[option] = value
        return data

    @staticmethod
    def update(new_data):
        """ Change the old option data to the new data. """
        option_data = []
        for option in new_data:
            option_data.append("{}:{}".format(option, new_data[option]))

        with open(options_file, 'w') as file:
            file.write('\n'.join(option_data))

    def exit(self):
        with open(options_file, 'r') as file:
            if "running:False" in file:
                sys.exit()
            else:
                self.options['running'] = "False"
                new_data = self.options
                Options.update(new_data)

    @staticmethod
    def print():
        for option in Options.get():
            print("{}:{}".format(option, Options.get()[option]))


def main():
    # import options_write  # overwrites the options file with default values
    Check.file()
    app = VirtualWorld()

    w = 500  # width for the Tk root
    h = 600  # height for the Tk root

    # get screen width and height
    ws = app.winfo_screenwidth()  # width of the screen
    hs = app.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen
    # and where it is placed
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))
    app.resizable(width=False, height=False)
    app_options = Options()
    app.mainloop()  # starts the mainloop
    app_options.exit()

if __name__ == "__main__":
    main()
