# ===================================
# Filename: main.py
# Purpose: To setup and start the virtual-world program.
#
#
# virtual-world
# Copyright (C) 2017  Joshua Peter Booth
#
# This file is part of virtual-world.
#
# virtual-world is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# virtual-world is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with virtual-world (see LICENSE.md).
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact me:
# Email: joshb00th@icloud.com
# ===================================

from __init__ import *

logger.disabled = True


class VirtualWorld(tk.Tk):

    def __init__(self, *args, **kwargs):
        """ Setup of the Virtual World Game """
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="img/virtualworld_logo.ico")
        tk.Tk.wm_title(self, "Virtual World")
        container = ttk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for file in (UserPage, LoginPage, SignupPage, SettingsPage, ShopPage,
                     CoffeeShopPage, TechShopPage, PizzaShopPage):
            frame = file(container, self)
            self.frames[file] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)
        self.init_window()

    def init_window(self):
        """ Create the upper Menu bar (for all frames). """
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
        """ Bring frame to the user's view. """
        frame = self.frames[cont]
        frame.tkraise()

    def hide_frame(self, cont):
        """ Send frame away from the user's view. """
        frame = self.frames[cont]
        frame.lower()

    def menu_bar(self, controller):
        """ Create the lower Menu bar (for most frames). """
        self.balance = User.get_current()['balance']

        hidden = True
        balance_formatted = 'Balance: $' + self.balance
        balance_label = ttk.Label(self, text=balance_formatted,
                                  font=MEDIUM_FONT)

        def current_user():
            """
            Get the current user's name and balance.

            :returns: a dict with 'username' and 'balance' as keys.
            """
            username = User.get_current()['username']
            newest_balance = User.get_current()['balance']

            return {"username": username, "balance": newest_balance}

        def toggle_entry():
            """
            Toggle balance button.

            :raise: ValueError: Balance not valid!
            """
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
        """ Raise the UserPage frame to the user's view. """
        self.controller.show_frame(UserPage)

    def logout(self):
        """ Append current_user_file with a guest user then show LoginPage. """
        user = "Guest" + ',' + "None" + ',' + "50" + ',' + "1000000"
        with open(current_user_file, 'w') as f:
            f.write(user)
        self.show_frame(LoginPage)


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        """ Login frame of Virtual World. """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.login_page_logo = tk.Label(self, image=self.Logo)
        self.login_page_logo.grid(row=0, rowspan=12, column=0, columnspan=16)

        # Header
        login_label = ttk.Label(self, text="Login", font=LARGE_FONT)
        login_label.grid(row=14, rowspan=2, column=5, columnspan=6, pady=15)

        # Sign in labels and entries

        # Username label and entry
        username_label = ttk.Label(self, text="Username:", font=MEDIUM_FONT)
        username_label.grid(row=16, column=5, columnspan=5, sticky="W")
        self.username = ttk.Entry(self)
        self.username.grid(row=16, column=9, sticky="e")

        # Password label and entry
        password_label = ttk.Label(self, text="Password:", font=MEDIUM_FONT)
        password_label.grid(row=17, column=5, columnspan=5, sticky="W")
        self.password = ttk.Entry(self, show="*")
        self.password.grid(row=17, column=9, sticky="e")

        # Error labels
        self.error_label = ttk.Label(self, text="")
        self.error_label.grid(row=16, column=10, columnspan=3)
        self.error_label_2 = ttk.Label(self, text="")
        self.error_label_2.grid(row=17, column=10, columnspan=6, padx=10,
                                sticky="W")

        # Buttons

        # Sign up button
        self.signup_img = tk.PhotoImage(file="img/menu/signup_button.gif")
        signup_command = (lambda: controller.show_frame(SignupPage))
        self.signup_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                       width=80, height=40,
                                       image=self.signup_img,
                                       command=signup_command)
        self.signup_button.grid(row=18, column=5, columnspan=4, sticky="W",
                                pady=5)
        self.signup_button.image = self.signup_img

        # Sign in button
        sign_in_img = tk.PhotoImage(file="img/menu/submit_button.gif")
        sign_in_command = (lambda: self.sign_in_button())
        sign_in_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                   width=80, height=40, image=sign_in_img,
                                   command=sign_in_command)
        sign_in_button.grid(row=18, column=6, columnspan=5, sticky="E",
                            padx=20, pady=5)
        sign_in_button.image = sign_in_img

        # Guest user button
        guest_img = tk.PhotoImage(file="img/menu/guest_button.gif")
        guest_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                 width=150, height=40, image=guest_img,
                                 command=lambda: self.guest_button())
        guest_button.grid(row=19, column=2, columnspan=8, sticky="E", padx=35,
                          pady=5)
        guest_button.image = guest_img

    def sign_in_button(self):
        """
        Check user's info and sign them in.

        :return: False - If user does not exist.
        """
        username = self.username.get()
        password = self.password.get()
        name_and_pass = username + ',' + password
        full_user_data = Check.all_user_data(name_and_pass)
        # Attempt to get all of the user's data if user in the user_data_file
        if username == "":
            if username == "" and password == "":
                logger.info("Entering nothing will not work.")
            else:
                logger.info("You must enter a username.")
            self.error_label.configure(text="Incorrect", foreground="red")
            self.error_label_2.configure(text="Username/Password",
                                         foreground="red")
            return False
        elif Check.in_user_data(full_user_data):
            with open(current_user_file, 'w') as f:
                f.write(full_user_data)
            self.error_label.configure(text="User", foreground="green")
            self.error_label_2.configure(text="Accepted!", foreground="green")
            success_command = (lambda: self.controller.show_frame(UserPage))
            self.error_label_2.after(1250, success_command)
            logger.info("User '{}' Exists!".format(self.username.get()))
        else:
            logger.info("Incorrect Username/Password")
            self.error_label.configure(text="Incorrect", foreground="red")
            self.error_label_2.configure(text="Username/Password",
                                         foreground="red")
            return False

    def guest_button(self):
        """" Take the user (without a login) to the user homepage. """
        with open(current_user_file, 'w') as f:
            f.write('Guest,None,50,1000000')
        self.controller.show_frame(UserPage)


class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        """ Signup frame of Virtual World. """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.sign_in_logo = tk.Label(self, image=self.Logo)
        self.sign_in_logo.grid(row=0, rowspan=12, column=0, columnspan=16)

        # Header
        signup_title = ttk.Label(self, text="Sign Up", font=LARGE_FONT)
        signup_title.grid(row=14, rowspan=2, column=5, columnspan=6, pady=15)

        # Sign up labels and entries

        # Username label and entry
        username_label = ttk.Label(self, text="Username:", font=MEDIUM_FONT)
        username_label.grid(row=17, column=5, columnspan=5, sticky="W")
        self.username = ttk.Entry(self)
        self.username.grid(row=17, column=9, sticky="e")

        # Password label and entry
        password_label = ttk.Label(self, text="Password:", font=MEDIUM_FONT)
        password_label.grid(row=18, column=5, columnspan=5, sticky="W")
        self.password = ttk.Entry(self)
        self.password.grid(row=18, column=9, sticky="e")

        # Age label and entry
        age_label = ttk.Label(self, text="Age:", font=MEDIUM_FONT)
        age_label.grid(row=19, column=5, columnspan=5, sticky="W")
        self.age = ttk.Entry(self)
        self.age.grid(row=19, column=9, sticky="e")

        # Error labels
        self.name_error_label = ttk.Label(self, text="", foreground="red")
        self.name_error_label.grid(row=17, column=11, columnspan=4)

        self.pwd_error_label = ttk.Label(self, text="", foreground="red")
        self.pwd_error_label.grid(row=18, column=11, columnspan=4)

        self.age_error_label = tk.Label(self, text="", foreground="red")
        self.age_error_label.grid(row=19, column=11, columnspan=4)

        # Buttons

        # Back button
        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=21, column=5, columnspan=4, sticky="W", pady=5)
        back_button.image = back_img

        # Submit button
        submit_img = tk.PhotoImage(file="img/menu/submit_button.gif")
        submit_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                  width=80, height=40, image=submit_img,
                                  command=lambda: self.submit_button())
        submit_button.grid(row=21, column=6, columnspan=5, sticky="E",
                           padx=20, pady=5)
        submit_button.image = submit_img

    def back_button(self):
        """ Raise the LoginPage frame to the user's view. """
        self.controller.show_frame(LoginPage)

    def create_user(self, username, password, age):
        """
        Adds the user to the text file, shows a success message, then returns
        the user back to the LoginPage frame.
        """
        User.new(username, password, age)
        self.name_error_label.configure(text="")  # ttk label
        self.pwd_error_label.configure(text="", )  # ttk label
        self.age_error_label.configure(text="User Created!", fg="green")  # tk
        self.age_error_label.after(2500, self.back_button)

    def submit_button(self):
        """ Check user input then output a success/fail message. """
        # TODO: Fix this so that it is a validatecommand.
        if Check.username(self.username.get()):
            username = self.username.get()
            if Check.password(self.password.get()):
                password = self.password.get()
                if Check.age(self.age.get()):
                    age = self.age.get()
                    self.create_user(username, password, age)
                else:
                    logger.info("Age Failed")
                    self.name_error_label.configure(text="")
                    self.pwd_error_label.configure(text="")
                    self.age_error_label.configure(text="Invalid age",
                                                   foreground="red")
            else:
                logger.info("Password Failed")
                self.name_error_label.configure(text="")
                self.pwd_error_label.configure(text="Invalid password",
                                               foreground="red")
        else:
            logger.info("Username Failed.")
            self.name_error_label.configure(text="Invalid username",
                                            foreground="red")


class UserPage(tk.Frame):

    def __init__(self, parent, controller):
        """ User's homepage frame of Virtual World. """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.user_page_logo = tk.Label(self, image=self.Logo)
        self.user_page_logo.grid(row=0, rowspan=12, column=0, columnspan=16)

        # Header
        welcome_label = ttk.Label(self, text="Welcome", font=LARGE_FONT)
        welcome_label.grid(row=14, rowspan=2, column=1, columnspan=11, pady=15)

        # Buttons

        # Shops button
        shop_img = tk.PhotoImage(file="img/shops/shop_button.gif")
        shop_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=shop_img,
                                command=lambda: self.shops_button())
        shop_button.grid(row=18, column=1, columnspan=11)
        shop_button.image = shop_img

        # Games button
        game_img = tk.PhotoImage(file="img/games/game_button.gif")
        game_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=game_img,
                                command=lambda: self.games_button())
        game_button.grid(row=19, column=1, columnspan=11)
        game_button.image = game_img

        # Tasks button
        task_img = tk.PhotoImage(file="img/tasks/task_button.gif")
        task_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=task_img,
                                command=lambda: self.tasks_button())
        task_button.grid(row=20, column=1, columnspan=11)
        task_button.image = task_img

        # Back button
        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=22, column=10, columnspan=5, sticky="E")
        back_button.image = back_img

        VirtualWorld.menu_bar(self, controller)

    def shops_button(self):
        """ Raise the ShopPage frame to the user's view. """
        self.controller.show_frame(ShopPage)

    def games_button(self):
        """ Raise the GamePage frame to the user's view. """
        pass

    def tasks_button(self):
        """ Raise the TaskPage frame to the user's view. """
        pass

    def back_button(self):
        """ Append current_user_file with a guest user then show LoginPage. """
        user = "Guest,None,50,1000000"
        with open(current_user_file, 'w') as f:
            f.write(user)
        self.controller.show_frame(LoginPage)


class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        """ Settings frame of Virtual World. """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.settings_page_logo = tk.Label(self, image=self.Logo)
        self.settings_page_logo.grid(row=0, rowspan=12, column=0,
                                     columnspan=16)

        # Header
        shops_label = ttk.Label(self, text="Settings", font=LARGE_FONT)
        shops_label.grid(row=14, rowspan=2, column=1, columnspan=11, pady=12)

        # Buttons

        # Name change button
        name_change_link = "img/settings/change_name.gif"
        name_change_img = tk.PhotoImage(file=name_change_link)
        name_window = (lambda: self.open_window("Name"))
        name_change_button = tk.Button(self, relief="flat", width=120,
                                       height=30, image=name_change_img,
                                       command=name_window)
        name_change_button.grid(row=18, column=1, columnspan=11)
        name_change_button.image = name_change_img

        # Password change button
        pwd_change_link = "img/settings/change_password.gif"
        pwd_change_img = tk.PhotoImage(file=pwd_change_link)
        pwd_window = (lambda: self.open_window("Password"))
        pwd_change_button = tk.Button(self, relief="flat", width=120,
                                      height=30, image=pwd_change_img,
                                      command=pwd_window)
        pwd_change_button.grid(row=19, column=1, columnspan=11)
        pwd_change_button.image = pwd_change_img

        # Age change button
        age_change_link = "img/settings/change_age.gif"
        age_change_img = tk.PhotoImage(file=age_change_link)
        age_window = (lambda: self.open_window("Age"))
        age_change_button = tk.Button(self, relief="flat", width=120,
                                      height=30, image=age_change_img,
                                      command=age_window)
        age_change_button.grid(row=20, column=1, columnspan=11)
        age_change_button.image = age_change_img

        # Delete button
        del_user_link = "img/settings/delete_user.gif"
        del_user_img = tk.PhotoImage(file=del_user_link)
        del_window = (lambda: self.open_window("Delete"))
        del_user_button = tk.Button(self, relief="flat", width=120, height=30,
                                    image=del_user_img, command=del_window)
        del_user_button.grid(row=21, column=1, columnspan=11)
        del_user_button.image = del_user_img

        # Back button
        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=22, column=10, columnspan=5, sticky="E")
        back_button.image = back_img

        VirtualWorld.menu_bar(self, controller)

        self.toplevel = None

    def open_window(self, setting):
        """
        Create a Username and Password window for verifying user information
        for changing settings, and provide a Toplevel for entries to be added.

        :return: False - If current user is a guest.
        """
        if self.toplevel is None:
            current_user = Check.file()['current_user']
            if 'Guest,None,50,1000000' in list(current_user):
                logger.info('Guest users cannot change their information!')
                return False

            self.toplevel = tk.Toplevel(self)
            self.toplevel.protocol('WM_DELETE_WINDOW',
                                   lambda: self.remove_window())
            self.toplevel.focus_set()
            self.toplevel.resizable(width=False, height=False)
            self.toplevel.setting = setting
            self.toplevel.title(setting)

            # Username and password labels and entries

            # Username label and entry
            username_label = ttk.Label(self.toplevel, text="Username:",
                                       font=MEDIUM_FONT)
            username_label.grid(row=0, column=0, sticky="W", pady=5, padx=12)
            self.toplevel.username = ttk.Entry(self.toplevel)
            self.toplevel.username.grid(row=1, column=0, padx=15)

            # Password label and entry
            password_label = ttk.Label(self.toplevel, text="Password:",
                                       font=MEDIUM_FONT)
            password_label.grid(row=2, column=0, sticky="W", pady=5, padx=12)
            self.toplevel.password = ttk.Entry(self.toplevel, show="*")
            self.toplevel.password.grid(row=3, column=0, padx=15)

            # Buttons

            # Submit button
            submit_command = (lambda: self.submit_button())
            self.toplevel.submit = ttk.Button(self.toplevel, text="Submit",
                                              command=submit_command)
            self.toplevel.submit.grid(row=6, column=0, sticky="W", pady=5,
                                      padx=3)

            # Cancel button
            cancel_command = (lambda: self.remove_window())
            self.toplevel.cancel = ttk.Button(self.toplevel, text="Cancel",
                                              command=cancel_command)
            self.toplevel.cancel.grid(row=6, column=0, sticky="E", pady=5)

            # Error label
            self.toplevel.user_info = ttk.Label(self.toplevel, text="",
                                                font=MEDIUM_FONT)
            self.toplevel.user_info.grid(row=8, column=0)

            # Toplevel position
            w = 157  # Width for toplevel
            h = 220  # Height for toplevel

            ws = self.toplevel.winfo_screenwidth()  # Width of the screen
            hs = self.toplevel.winfo_screenheight()  # Height of the screen

            # Calculate x and y coordinates for the Tk root window
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            # Set the dimensions of the screen and where it is placed
            self.toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y - 30))
            self.toplevel.mainloop()

    def remove_window(self):
        """ Remove the toplevel (username and password) window. """
        self.toplevel.destroy()
        self.toplevel = None

    def back_button(self):
        """ Remove the SettingsPage frame from the user's view. """
        self.controller.hide_frame(SettingsPage)

    def submit_button(self):
        """
        Check user input and change the setting window for the specified
        setting.

        :return: False - If user data is incorrect or if there is no data.
        :raise: NameError: Setting name is invalid!
        """
        username = self.toplevel.username.get()
        password = self.toplevel.password.get()
        user_info = username + ',' + password

        change_name = (lambda: self.change_name(new_name.get()))
        change_pwd = (lambda: self.change_password(new_password.get()))
        change_age = (lambda: self.change_age(self.toplevel.new_age.get()))
        del_user = (lambda: self.delete_user(username))

        if user_info == ',':
            logger.info("Nothing was entered")
            self.toplevel.user_info.configure(text="Nothing entered!",
                                              foreground="red")
            return False

        elif Check.in_user_data(Check.all_user_data(user_info)):
            logger.info("User '{}' Exists!".format(username))
            if self.toplevel.setting == "Name":
                # New user label and entry
                new_name_label = ttk.Label(self.toplevel, font=MEDIUM_FONT,
                                           text=" New Username:")
                new_name_label.grid(row=4, column=0, sticky="W", pady=5,
                                    padx=7)
                new_name = ttk.Entry(self.toplevel)
                new_name.grid(row=5, column=0)
                # Change name button
                self.toplevel.submit = ttk.Button(self.toplevel, text="Change",
                                                  command=change_name)
                self.toplevel.submit.grid(row=6, column=0, sticky="W", pady=5,
                                          padx=3)
            elif self.toplevel.setting == "Password":
                # New password label and entry
                new_password_label = ttk.Label(self.toplevel,
                                               text="New Password:",
                                               font=MEDIUM_FONT)
                new_password_label.grid(row=4, column=0, sticky="W", pady=5,
                                        padx=12)
                new_password = ttk.Entry(self.toplevel)
                new_password.grid(row=5, column=0)
                # Change password button
                self.toplevel.submit = ttk.Button(self.toplevel, text="Change",
                                                  command=change_pwd)
                self.toplevel.submit.grid(row=6, column=0, sticky="W", pady=5,
                                          padx=3)
            elif self.toplevel.setting == "Age":
                # New age label and entry
                new_age_label = ttk.Label(self.toplevel, text="New Age:",
                                          font=MEDIUM_FONT)
                new_age_label.grid(row=4, column=0, sticky="W", pady=5,
                                   padx=12)
                self.toplevel.new_age = ttk.Entry(self.toplevel)
                self.toplevel.new_age.grid(row=5, column=0)
                # Change age button
                self.toplevel.submit = ttk.Button(self.toplevel, text="Change",
                                                  command=change_age)
                self.toplevel.submit.grid(row=6, column=0, sticky="W", pady=5,
                                          padx=3)
            elif self.toplevel.setting == "Delete":
                # Delete button
                delete_button = ttk.Button(self.toplevel, text="Delete User",
                                           command=del_user)
                delete_button.grid(row=6, column=0, sticky="W", pady=5, padx=3)
            else:
                raise NameError("Setting name is invalid!")
        else:
            logger.info("User does not exist!")
            return False

    def change_name(self, new_name):
        """
        Change the user's name if the new name is valid, decline the username
        if is taken.

        :param new_name: This is user's new name (str).
        """
        if Check.username(new_name):
            # Success label
            success_label = ttk.Label(self.toplevel, text="Username Accepted!",
                                      foreground="green")
            success_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

            old_name = self.toplevel.username.get()
            logger.info("Changing username...")
            User.name_change(old_name, new_name)
            success_label.after(2500, lambda: self.remove_window())
        else:
            # Failure label
            failure_label = ttk.Label(self.toplevel, text="Username Declined!",
                                      foreground="red")
            failure_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

    def change_password(self, new_password):
        """
        Change the user's password if the new password is valid, decline the
        password if it is invalid.

        :param new_password: This is user's new password (str).
        """
        if Check.password(new_password):
            # Success label
            success_label = ttk.Label(self.toplevel, text="Password Accepted!",
                                      foreground="green")
            success_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

            username = self.toplevel.username.get()
            logger.info("Changing password...")
            User.password_change(username, new_password)
            success_label.after(2500, lambda: self.remove_window())
        else:
            # Failure label
            failure_label = ttk.Label(self.toplevel, text="Password Declined!",
                                      foreground="red")
            failure_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

    def change_age(self, new_age):
        """
        Change the user's age if the new age is valid, decline the
        age if it is below 10 and over 999.

        :param new_age: This is user's new age (str).
        """
        if Check.age(new_age):
            # Success label
            success_label = ttk.Label(self.toplevel, text="Age Accepted!",
                                      foreground="green")
            success_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

            username = self.toplevel.username.get()
            logger.info("Changing age...")
            User.age_change(username, new_age)
            success_label.after(2500, lambda: self.remove_window())
        else:
            # Failure label
            failure_label = ttk.Label(self.toplevel, text="Age Declined!",
                                      foreground="red")
            failure_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

    def delete_user(self, username):
        """
        Delete the given user.

        :param username: This is user's login name (str).
        """
        # Success label
        success_label = ttk.Label(self.toplevel, text="Deleting user...",
                                  foreground="green")
        success_label.grid(row=8, rowspan=2, column=0, pady=5, padx=12)

        logger.info("Deleting user...")
        User.delete(username)
        del_window = (lambda: self.remove_window_del())
        success_label.after(2500, del_window)

    def remove_window_del(self):
        """
        Destroy the window and bring the LoginPage frame to the user's view.
        """
        self.toplevel.destroy()
        self.toplevel = None
        self.controller.show_frame(LoginPage)


class ShopPage(tk.Frame):

    def __init__(self, parent, controller):
        """ Shops frame of Virtual World. """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header image
        self.Logo = tk.PhotoImage(file="img/logo.gif")
        self.shop_page_logo = tk.Label(self, image=self.Logo)
        self.shop_page_logo.grid(row=0, rowspan=12, column=0, columnspan=16)

        # Header
        shops_label = ttk.Label(self, text="Shops", font=LARGE_FONT)
        shops_label.grid(row=14, rowspan=2, column=1, columnspan=11, pady=15)

        # Buttons                   TODO Fix image sizes!

        # Coffee Shop button
        coffee_img = tk.PhotoImage(file="img/shops/coffee/coffee_button.gif")
        coffee_button = tk.Button(self, relief="flat", width=180, height=40,
                                  image=coffee_img,
                                  command=lambda: self.shop_coffee())
        coffee_button.grid(row=18, column=1, columnspan=12)
        coffee_button.image = coffee_img

        # Tech Shop button
        tech_img = tk.PhotoImage(file="img/shops/tech/tech_button.gif")
        tech_button = tk.Button(self, relief="flat", width=180, height=40,
                                image=tech_img,
                                command=lambda: self.shop_tech())
        tech_button.grid(row=19, column=1, columnspan=12)
        tech_button.image = tech_img

        # Pizza Shop button
        pizza_img = tk.PhotoImage(file="img/shops/pizza/pizza_button.gif")
        pizza_button = tk.Button(self, relief="flat", width=180, height=40,
                                 image=pizza_img,
                                 command=lambda: self.shop_pizza())
        pizza_button.grid(row=20, column=1, columnspan=13, padx=10)
        pizza_button.image = pizza_img

        VirtualWorld.menu_bar(self, controller)

    def back_button(self):
        """ Raise the UserPage frame to the user's view. """
        self.controller.show_frame(UserPage)

    def shop_coffee(self):
        """ Raise the CoffeeShopPage frame to the user's view. """
        self.controller.show_frame(CoffeeShopPage)

    def shop_tech(self):
        """ Raise the TechShopPage frame to the user's view. """
        self.controller.show_frame(TechShopPage)

    def shop_pizza(self):
        """ Raise the PizzaShopPage frame to the user's view. """
        self.controller.show_frame(PizzaShopPage)

    def balance_button(self):
        # TODO: Fix this.
        # print("Balance: ${:.2f}".format(user.balance))
        pass


class CoffeeShopPage(tk.Frame):
    cappu_cost = 3.50
    espre_cost = 3.00
    flatw_cost = 2.50
    latte_cost = 4.50
    mocha_cost = 3.50

    def __init__(self, parent, controller):
        """ Coffee shop frame of Virtual World. """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header image
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

        # Coffee type labels, prices and entries

        # Cappuccino and price label and amount entry
        # Cappuccino label
        self.cappuccino_label = ttk.Label(self, text="Cappuccino",
                                          font=MEDIUM_FONT)
        self.cappuccino_label.grid(row=14, column=1, columnspan=5, pady=10,
                                   sticky="W")
        # Cappuccino price label
        self.cappuccino_price = ttk.Label(self, font=MEDIUM_FONT,
                                          text="${:.2f}"
                                          .format(self.cappu_cost))
        self.cappuccino_price.grid(row=14, column=4, columnspan=3, pady=10)
        # Cappuccino amount entry
        cappuccino_vcmd = (self.register(self.confirm), '%P', '%S',
                           'cappuccino')
        self.cappuccino_amount = ttk.Entry(self, validate="key",
                                           justify="center",
                                           validatecommand=cappuccino_vcmd)
        self.cappuccino_amount.grid(row=14, column=10, columnspan=2, pady=10)

        # Espresso label, price and amount entry
        # Espresso label
        self.espresso_label = ttk.Label(self, text="Espresso",
                                        font=MEDIUM_FONT)
        self.espresso_label.grid(row=15, column=1, columnspan=5, pady=10,
                                 sticky="W")
        # Espresso price label
        self.espresso_price = ttk.Label(self, font=MEDIUM_FONT,
                                        text="${:.2f}".format(self.espre_cost))
        self.espresso_price.grid(row=15, column=4, columnspan=3, pady=10)
        # Espresso amount entry
        espresso_vcmd = (self.register(self.confirm), '%P', '%S', 'espresso')
        self.espresso_amount = ttk.Entry(self, validate="key",
                                         justify="center",
                                         validatecommand=espresso_vcmd)
        self.espresso_amount.grid(row=15, column=10, columnspan=2, pady=10)

        # Flat white label, price and amount entry
        # Flat white label
        self.flat_w_label = ttk.Label(self, text="Flat White",
                                      font=MEDIUM_FONT)
        self.flat_w_label.grid(row=16, column=1, columnspan=5, pady=10,
                               sticky="W")
        # Flat white price label
        self.flat_w_price = ttk.Label(self, font=MEDIUM_FONT,
                                      text="${:.2f}".format(self.flatw_cost))
        self.flat_w_price.grid(row=16, column=4, columnspan=3, pady=10)
        # Flat white amount entry
        flat_w_vcmd = (self.register(self.confirm), '%P', '%S', 'flat_white')
        self.flat_w_amount = ttk.Entry(self, validate="key", justify="center",
                                       validatecommand=flat_w_vcmd)
        self.flat_w_amount.grid(row=16, column=10, columnspan=2, pady=10)

        # Latte label, price and amount entry
        # Latte label
        self.latte_label = ttk.Label(self, text="Latte", font=MEDIUM_FONT)
        self.latte_label.grid(row=17, column=1, columnspan=5, pady=10,
                              sticky="W")
        # Latte price label
        self.latte_price = ttk.Label(self, font=MEDIUM_FONT,
                                     text="${:.2f}".format(self.latte_cost))
        self.latte_price.grid(row=17, column=4, columnspan=3, pady=10)
        # Latte amount entry
        latte_vcmd = (self.register(self.confirm), '%P', '%S', 'latte')
        self.latte_amount = ttk.Entry(self, validate="key", justify="center",
                                      validatecommand=latte_vcmd)
        self.latte_amount.grid(row=17, column=10, columnspan=2, pady=10)

        # Mocha label, price and amount entry
        # Mocha label
        self.mocha_label = ttk.Label(self, text="Mocha", font=MEDIUM_FONT)
        self.mocha_label.grid(row=18, column=1, columnspan=5, pady=10,
                              sticky="W")
        # Mocha price label
        self.mocha_price = ttk.Label(self, font=MEDIUM_FONT,
                                     text="${:.2f}".format(self.mocha_cost))
        self.mocha_price.grid(row=18, column=4, columnspan=3, pady=10)
        # Mocha amount entry
        mocha_vcmd = (self.register(self.confirm), '%P', '%S', 'mocha')
        self.mocha_amount = ttk.Entry(self, validate="key", justify="center",
                                      validatecommand=mocha_vcmd)
        self.mocha_amount.grid(row=18, column=10, columnspan=2, pady=10)

        # Maximum number of coffees
        self.amount_label = ttk.Label(self, font=SMALL_FONT, foreground="red",
                                      text="Maximum of 9 of each coffee type.")
        self.amount_label.grid(row=19, column=1, columnspan=9)

        # Total label and total amount label
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

        # Back button
        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=22, column=10, columnspan=5, sticky="E")
        back_button.image = back_img

        VirtualWorld.menu_bar(self, controller)

        CoffeeShopPage.reset_order_data()

    def erase(self):
        """ Remove all data from the order entries. """
        for amount in (self.cappuccino_amount, self.espresso_amount,
                       self.flat_w_amount, self.latte_amount,
                       self.mocha_amount):
            amount.delete(0, 1)
            amount.insert(0, "")

    def confirm(self, P, S, _type):
        """
        Only allow a 1 digit integer and if the total of all the entries
        is greater than one, enable the cart button.

        :param P: allowed value (%P).
        :param S: text being inserted (%S).
        :param _type: the coffee type (str).
        :returns: True - If value is valid.
                 False - If input is invalid.
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
                logger.error("Input is not an integer!")
        if isinstance(inserted_value, int) and 0 < len(allowed_value) == 1:
            with open(COFFEE_DATA_F, 'r') as file:
                current_data = [line.strip() for line in file]
            data = {}
            with open(COFFEE_DATA_F, 'r') as file:
                for line in file:
                    option, value = line.strip().split(':')
                    data[option] = value
            if data[_type] == str(allowed_value):
                logger.debug("No changes to be made to {}".format(COFFEE_DATA_F))
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
                logger.debug("Writing new data to {}".format(COFFEE_DATA_F))
                file.write('\n'.join(current_data))
            return True
        else:
            self.bell()
            return False

    def back_button(self):
        """ Raise the ShopPage frame to the user's view. """
        self.controller.show_frame(ShopPage)

    def submit_button(self):
        """
        Check user input and change the order window for the specified
        user, where guests do not pay but all other users do.

        :return: False - If user data is incorrect or if there is no data.
        """
        try:
            username = self.toplevel.username.get()
            password = self.toplevel.password.get()
        except AttributeError:
            username = "Guest"
            password = "None"

        name_and_pass = username + ',' + password
        full_user_data = Check.all_user_data(name_and_pass)
        # Attempt to get all of the user's data if user in the user_data_file
        amount = float(self.total_cost_label.cget("text").strip('$'))
        if name_and_pass == ',':
            logger.info("Nothing was entered!")
            self.toplevel.user_info.configure(text="Nothing entered!",
                                              foreground="red")
            return False
        elif Check.in_user_data(full_user_data):
            logger.info("User '{}' Exists!".format(username))
            self.toplevel.user_info.configure(text="")
            # Confirm button
            purchase = (lambda: self.purchase(username, amount))
            self.toplevel.submit = ttk.Button(self.toplevel, text="Confirm",
                                              command=purchase)
            self.toplevel.submit.grid(row=13, column=6, columnspan=10, pady=5)
        else:
            # Error label
            self.toplevel.error_label = ttk.Label(
                self.toplevel, text="Incorrect username/password",
                foreground="red")
            self.toplevel.error_label.grid(row=14, column=9, columnspan=20)
            return False

    def purchase(self, username, amount):
        """
        Check the user is not a guest and then withdraw the amount from the
        user's account. Reset the order_data_file if the transaction is
        successful.
        """
        if username == 'Guest':
            self.toplevel.user_info.configure(text="Transaction successful",
                                              foreground="green")
            CoffeeShopPage.reset_order_data()
        elif User.withdraw(username, amount) is True:
            self.toplevel.user_info.configure(text="Transaction successful",
                                              foreground="green")
            CoffeeShopPage.reset_order_data()
        elif User.withdraw(username, amount) == "inadequate_funds":
            self.toplevel.user_info.configure(text="Inadequate funds",
                                              foreground="red")
        else:
            self.toplevel.user_info.configure(text="Transaction failed",
                                              foreground="red")
        self.toplevel.user_info.after(2500, lambda: self.remove_window())

    @staticmethod
    def reset_order_data():
        """ Reset the COFFEE_DATA_F file. """
        order_data = ['cappuccino', 'espresso', 'flat_white', 'latte', 'mocha',
                      'total']
        new_data = []
        with open(COFFEE_DATA_F, 'w') as file:
            for data in order_data:
                new_data.append('{}:0'.format(data))
            file.write('\n'.join(new_data))

    def order(self):
        """
        Create the order window (which displays the user's order) and display
        the correct amounts and totals for the user's order.
        """
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
                row_num = 2
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

                        row_num += 1
                        ttk.Label(self.toplevel, text=coffee_type)\
                            .grid(row=row_num, column=0, columnspan=10)
                        ttk.Label(self.toplevel, text=data[option])\
                            .grid(row=row_num, column=10, columnspan=9)
                        ttk.Label(self.toplevel, text=price)\
                            .grid(row=row_num, column=20)

            with open(current_user_file, 'r') as file:
                if 'Guest,None,50,1000000' not in file:
                    # Username and password labels and entries
                    # Username label
                    username_label = ttk.Label(self.toplevel, text="Username:",
                                               font=SMALL_FONT)
                    username_label.grid(row=9, column=7, columnspan=11, pady=5)
                    # Username entry
                    self.toplevel.username = ttk.Entry(self.toplevel)
                    self.toplevel.username.grid(row=10, sticky='W', padx=20,
                                                column=9, columnspan=12)
                    # Password label
                    password_label = ttk.Label(self.toplevel, text="Password:",
                                               font=SMALL_FONT)
                    password_label.grid(row=11, column=7, columnspan=11,
                                        pady=5)
                    # Password entry
                    self.toplevel.password = ttk.Entry(self.toplevel, show="*")
                    self.toplevel.password.grid(row=12, sticky="E", padx=20,
                                                column=9, columnspan=12)
            # Buttons

            # Submit button
            submit_command = (lambda: self.submit_button())
            self.toplevel.submit = ttk.Button(self.toplevel, text="Submit",
                                              command=submit_command)
            self.toplevel.submit.grid(row=13, column=6, columnspan=10, pady=5)

            # Cancel button
            cancel_command = (lambda: self.remove_window())
            self.toplevel.cancel = ttk.Button(self.toplevel, text="Cancel",
                                              command=cancel_command)
            self.toplevel.cancel.grid(row=13, column=16, columnspan=6, pady=5)

            # Error label
            self.toplevel.user_info = ttk.Label(self.toplevel, text="",
                                                font=SMALL_FONT)
            self.toplevel.user_info.grid(row=14, column=8, columnspan=20)

            # Toplevel position
            w = 250  # Width for toplevel
            h = 335  # Height for toplevel

            ws = self.toplevel.winfo_screenwidth()  # Width of the screen
            hs = self.toplevel.winfo_screenheight()  # Height of the screen

            # Calculate x and y coordinates for the toplevel window
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            # Set the dimensions of the screen and where it is placed
            self.toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y - 30))
            self.toplevel.mainloop()

    def remove_window(self):
        """ Remove the toplevel (order) window. """
        self.toplevel.destroy()
        self.toplevel = None


class TechShopPage(tk.Frame):
    camera_cost = 300.00
    phone_cost = 500.00
    tv_cost = 1200.00
    pc_cost = 1000.00
    tablet_cost = 800.00

    def __init__(self, parent, controller):
        """ Tech shop frame of Virtual World. """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header image
        self.Logo = tk.PhotoImage(file="img/shops/tech/tech_logo.gif",
                                  height="120")
        self.tech_logo = tk.Label(self, image=self.Logo)
        self.tech_logo.grid(row=0, rowspan=5, column=0, columnspan=16, padx=20)

        # Header
        menu_label = ttk.Label(self, text="Catalogue", font=LARGE_FONT)
        menu_label.grid(row=6, rowspan=2, column=0, columnspan=16, pady=15)

        # Sub-headers
        type_label = ttk.Label(self, text="Type", font=MEDIUM_FONT)
        type_label.grid(row=8, column=1, pady=10, sticky="W")
        price_label = ttk.Label(self, text="Price", font=MEDIUM_FONT)
        price_label.grid(row=8, column=4, columnspan=3, pady=10)
        amount_label = ttk.Label(self, text="Amount", font=MEDIUM_FONT)
        amount_label.grid(row=8, column=8, columnspan=6, pady=10)

        # Tech type labels, prices and entries

        # Camera label, price and amount entry
        self.camera_label = ttk.Label(self, text="Camera", font=MEDIUM_FONT)
        self.camera_label.grid(row=14, column=1, columnspan=5, pady=10,
                               sticky="W")
        self.camera_price = ttk.Label(self, font=MEDIUM_FONT, text="${:.2f}"
                                      .format(self.camera_cost))
        self.camera_price.grid(row=14, column=4, columnspan=3, pady=10)
        camera_vcmd = (self.register(self.confirm), '%P', '%S', 'camera')
        self.camera_amount = ttk.Entry(self, validate="key", justify="center",
                                       validatecommand=camera_vcmd)
        self.camera_amount.grid(row=14, column=10, columnspan=2, pady=10)

        # Phone label, price and amount entry
        self.phone_label = ttk.Label(self, text="Phone", font=MEDIUM_FONT)
        self.phone_label.grid(row=15, column=1, columnspan=5, pady=10,
                              sticky="W")
        self.phone_price = ttk.Label(self, font=MEDIUM_FONT,
                                     text="${:.2f}".format(self.phone_cost))
        self.phone_price.grid(row=15, column=4, columnspan=3, pady=10)
        phone_vcmd = (self.register(self.confirm), '%P', '%S', 'phone')
        self.phone_amount = ttk.Entry(self, validate="key", justify="center",
                                      validatecommand=phone_vcmd)
        self.phone_amount.grid(row=15, column=10, columnspan=2, pady=10)

        # T.V. label, price and amount entry
        self.tv_label = ttk.Label(self, text="Television", font=MEDIUM_FONT)
        self.tv_label.grid(row=16, column=1, columnspan=5, pady=10, sticky="W")
        self.tv_price = ttk.Label(self, font=MEDIUM_FONT,
                                  text="${:.2f}".format(self.tv_cost))
        self.tv_price.grid(row=16, column=4, columnspan=3, pady=10)
        tv_vcmd = (self.register(self.confirm), '%P', '%S', 'tv')
        self.tv_amount = ttk.Entry(self, validate="key", justify="center",
                                   validatecommand=tv_vcmd)
        self.tv_amount.grid(row=16, column=10, columnspan=2, pady=10)

        # P.C. label, price and amount entry
        self.pc_label = ttk.Label(self, text="Computer", font=MEDIUM_FONT)
        self.pc_label.grid(row=17, column=1, columnspan=5, pady=10,
                           sticky="W")
        self.pc_price = ttk.Label(self, font=MEDIUM_FONT,
                                  text="${:.2f}".format(self.pc_cost))
        self.pc_price.grid(row=17, column=4, columnspan=3, pady=10)
        pc_vcmd = (self.register(self.confirm), '%P', '%S', 'pc')
        self.pc_amount = ttk.Entry(self, validate="key", justify="center",
                                   validatecommand=pc_vcmd)
        self.pc_amount.grid(row=17, column=10, columnspan=2, pady=10)

        # Tablet label, price and amount entry
        self.tablet_label = ttk.Label(self, text="Tablet", font=MEDIUM_FONT)
        self.tablet_label.grid(row=18, column=1, columnspan=5, pady=10,
                               sticky="W")
        self.tablet_price = ttk.Label(self, font=MEDIUM_FONT,
                                      text="${:.2f}".format(self.tablet_cost))
        self.tablet_price.grid(row=18, column=4, columnspan=3, pady=10)
        tablet_vcmd = (self.register(self.confirm), '%P', '%S', 'tablet')
        self.tablet_amount = ttk.Entry(self, validate="key", justify="center",
                                       validatecommand=tablet_vcmd)
        self.tablet_amount.grid(row=18, column=10, columnspan=2, pady=10)

        # Maximum number of tech
        self.amount_label = ttk.Label(self, font=SMALL_FONT, foreground="red",
                                      text="Maximum of 9 of each tech type.")
        self.amount_label.grid(row=19, column=1, columnspan=9)

        # Total label and total amount label
        total_label = ttk.Label(self, text="Total:", font=MEDIUM_FONT)
        total_label.grid(row=20, column=1, sticky="W")
        self.total_cost_label = ttk.Label(self, font=MEDIUM_FONT,
                                          text="$0.00")
        self.total_cost_label.grid(row=20, column=1, columnspan=6,
                                   padx=10, sticky="E")

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

        # Back button
        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=22, column=10, columnspan=5, sticky="E")
        back_button.image = back_img

        VirtualWorld.menu_bar(self, controller)
        self.toplevel = None

        TechShopPage.reset_order_data()

    def erase(self):
        """ Remove all data from the order entries. """
        for amount in (self.camera_amount, self.phone_amount,
                       self.tv_amount, self.pc_amount,
                       self.tablet_amount):
            amount.delete(0, 1)
            amount.insert(0, "")

    def confirm(self, P, S, _type):
        """
        Only allow a 1 digit integer and if the total of all the entries
        is greater than one, enable the cart button.

        :param P: allowed value (%P).
        :param S: text being inserted (%S).
        :param _type: the tech type (str).
        :returns: True - If value is valid.
                 False - If input is invalid.
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
                logger.error("Input is not an integer!")
        if isinstance(inserted_value, int) and 0 < len(allowed_value) == 1:
            with open(TECH_DATA_F, 'r') as file:
                current_data = [line.strip() for line in file]
            data = {}
            with open(TECH_DATA_F, 'r') as file:
                for line in file:
                    option, value = line.strip().split(':')
                    data[option] = value
            if data[_type] == str(allowed_value):
                logger.debug("No changes to be made to {}".format(TECH_DATA_F))
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

                camera_total = 0
                phone_total = 0
                tv_total = 0
                pc_total = 0
                tablet_total = 0

                for item in current_data:
                    item = item.split(':')
                    if item[0] == 'camera' and int(item[1]) > 0:
                        camera_total = int(item[1]) * self.camera_cost
                    elif item[0] == 'phone' and int(item[1]) > 0:
                        phone_total = int(item[1]) * self.phone_cost
                    elif item[0] == 'tv' and int(item[1]) > 0:
                        tv_total = int(item[1]) * self.tv_cost
                    elif item[0] == 'pc' and int(item[1]) > 0:
                        pc_total = int(item[1]) * self.pc_cost
                    elif item[0] == 'tablet' and int(item[1]) > 0:
                        tablet_total = int(item[1]) * self.tablet_cost
                new_total = camera_total + phone_total + \
                    tv_total + pc_total + tablet_total

            if int(data['total']) > 0:
                self.total_cost_label.configure(text="${:.2f}"
                                                .format(new_total))
                self.buy_button.configure(state='normal')
            else:
                self.total_cost_label.configure(text="$0.00")
                self.buy_button.configure(state='disabled')
            with open(TECH_DATA_F, 'w') as file:
                logger.debug("Writing new data to {}".format(TECH_DATA_F))
                file.write('\n'.join(current_data))
            return True
        else:
            self.bell()
            return False

    def back_button(self):
        """ Raise the ShopPage frame to the user's view. """
        self.controller.show_frame(ShopPage)

    def submit_button(self):
        """
        Check user input and change the order window for the specified
        user, where guests do not pay but all other users do.

        :return: False - If user data is incorrect or if there is no data.
        """
        try:
            username = self.toplevel.username.get()
            password = self.toplevel.password.get()
        except AttributeError:
            username = "Guest"
            password = "None"

        name_and_pass = username + ',' + password
        full_user_data = Check.all_user_data(name_and_pass)
        # Attempt to get all of the user's data if user in the user_data_file
        amount = float(self.total_cost_label.cget("text").strip('$'))
        if name_and_pass == ',':
            logger.info("Nothing was entered!")
            self.toplevel.user_info.configure(text="Nothing entered!",
                                              foreground="red")
            return False
        elif Check.in_user_data(full_user_data):
            logger.info("User '{}' Exists!".format(username))
            self.toplevel.user_info.configure(text="")
            # Confirm button
            purchase = (lambda: self.purchase(username, amount))
            self.toplevel.submit = ttk.Button(self.toplevel, text="Confirm",
                                              command=purchase)
            self.toplevel.submit.grid(row=13, column=6, columnspan=10, pady=5)
        else:
            # Error label
            self.toplevel.error_label = ttk.Label(
                self.toplevel, text="Incorrect username/password",
                foreground="red")
            self.toplevel.error_label.grid(row=14, column=9, columnspan=20)
            return False

    def purchase(self, username, amount):
        """
        Check the user is not a guest and then withdraw the amount from the
        user's account. Reset the order_data_file if the transaction is
        successful.
        """
        if username == 'Guest':
            self.toplevel.user_info.configure(text="Transaction successful",
                                              foreground="green")
            TechShopPage.reset_order_data()
        elif User.withdraw(username, amount) is True:
            self.toplevel.user_info.configure(text="Transaction successful",
                                              foreground="green")
            TechShopPage.reset_order_data()
        elif User.withdraw(username, amount) == "inadequate_funds":
            self.toplevel.user_info.configure(text="Inadequate funds",
                                              foreground="red")
        else:
            self.toplevel.user_info.configure(text="Transaction failed",
                                              foreground="red")
        self.toplevel.user_info.after(2500, lambda: self.remove_window())

    @staticmethod
    def reset_order_data():
        """ Reset the TECH_DATA_F file. """
        order_data = ['camera', 'phone', 'tv', 'pc', 'tablet', 'total']
        new_data = []
        with open(TECH_DATA_F, 'w') as file:
            for data in order_data:
                new_data.append('{}:0'.format(data))
            file.write('\n'.join(new_data))

    def order(self):
        """
        Create the order window (which displays the user's order) and display
        the correct amounts and totals for the user's order.
        """
        if self.toplevel is None:
            self.toplevel = tk.Toplevel(self)
            self.toplevel.protocol('WM_DELETE_WINDOW',
                                   lambda: self.remove_window())
            self.toplevel.focus_set()
            self.toplevel.resizable(width=False, height=False)
            self.toplevel.title('Order')

            # Order label
            order_label = ttk.Label(self.toplevel, text="Here is your order:",
                                    font=MEDIUM_FONT)
            order_label.grid(row=0, column=0, columnspan=20, padx=5, pady=5)
            # Tech type label
            type_label = ttk.Label(self.toplevel, text="Type", font=SMALL_FONT)
            type_label.grid(row=2, column=0, columnspan=10, pady=10, padx=5)
            # Price label
            price_label = ttk.Label(self.toplevel, text="Amount",
                                    font=SMALL_FONT)
            price_label.grid(row=2, column=10, columnspan=9, pady=10)
            # Amount label
            amount_label = ttk.Label(self.toplevel, text="Price",
                                     font=SMALL_FONT)
            amount_label.grid(row=2, column=20, pady=10)

            data = {}
            with open(TECH_DATA_F, 'r') as file:
                row_num = 2
                for line in file:
                    option, value = line.strip().split(':')
                    data[option] = value
                    if int(data[option]) > 0:
                        if option == 'tv':
                            tech_type = "Television"
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.tv_cost)
                        elif option == 'camera':
                            tech_type = option.title()
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.camera_cost)
                        elif option == 'phone':
                            tech_type = option.title()
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.phone_cost)
                        elif option == 'pc':
                            tech_type = "Computer"
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.pc_cost)
                        elif option == 'tablet':
                            tech_type = option.title()
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.tablet_cost)
                        elif option == 'total':
                            tech_type = option.title()
                            price = self.total_cost_label.cget("text")
                        else:
                            tech_type = option
                            price = ""

                        row_num += 1
                        ttk.Label(self.toplevel, text=tech_type)\
                            .grid(row=row_num, column=0, columnspan=10)
                        ttk.Label(self.toplevel, text=data[option])\
                            .grid(row=row_num, column=10, columnspan=9)
                        ttk.Label(self.toplevel, text=price)\
                            .grid(row=row_num, column=20)

            with open(current_user_file, 'r') as file:
                if 'Guest,None,50,1000000' not in file:
                    # Username and password labels and entries
                    # Username label
                    username_label = ttk.Label(self.toplevel, text="Username:",
                                               font=SMALL_FONT)
                    username_label.grid(row=9, column=7, columnspan=11, pady=5)
                    # Username entry
                    self.toplevel.username = ttk.Entry(self.toplevel)
                    self.toplevel.username.grid(row=10, sticky='W', padx=20,
                                                column=9, columnspan=12)
                    # Password label
                    password_label = ttk.Label(self.toplevel, text="Password:",
                                               font=SMALL_FONT)
                    password_label.grid(row=11, column=7, columnspan=11,
                                        pady=5)
                    # Password entry
                    self.toplevel.password = ttk.Entry(self.toplevel, show="*")
                    self.toplevel.password.grid(row=12, sticky="E", padx=20,
                                                column=9, columnspan=12)
            # Buttons

            # Submit button
            submit_command = (lambda: self.submit_button())
            self.toplevel.submit = ttk.Button(self.toplevel, text="Submit",
                                              command=submit_command)
            self.toplevel.submit.grid(row=13, column=6, columnspan=10, pady=5)

            # Cancel button
            cancel_command = (lambda: self.remove_window())
            self.toplevel.cancel = ttk.Button(self.toplevel, text="Cancel",
                                              command=cancel_command)
            self.toplevel.cancel.grid(row=13, column=16, columnspan=6, pady=5)

            # Error label
            self.toplevel.user_info = ttk.Label(self.toplevel, text="",
                                                font=SMALL_FONT)
            self.toplevel.user_info.grid(row=14, column=8, columnspan=20)

            # Toplevel position
            w = 250  # Width for toplevel
            h = 335  # Height for toplevel

            ws = self.toplevel.winfo_screenwidth()  # Width of the screen
            hs = self.toplevel.winfo_screenheight()  # Height of the screen

            # Calculate x and y coordinates for the Tk root window
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            # Set the dimensions of the screen and where it is placed
            self.toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y - 30))
            self.toplevel.mainloop()

    def remove_window(self):
        """ Remove the toplevel (order) window. """
        self.toplevel.destroy()
        self.toplevel = None


class PizzaShopPage(tk.Frame):
    meat_cost = 5.00
    cheese_cost = 5.00
    pepperoni_cost = 5.00
    hawaiian_cost = 5.00
    seafood_cost = 5.00

    def __init__(self, parent, controller):
        """ Pizza shop frame of Virtual World. """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Header image
        self.Logo = tk.PhotoImage(file="img/shops/pizza/pizza_logo.gif",
                                  height="120")
        self.pizza_logo = tk.Label(self, image=self.Logo)
        self.pizza_logo.grid(row=0, rowspan=5, column=0, columnspan=16, padx=10)

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

        # Pizza type labels, prices and entries

        # Meat lovers label, price and amount entry
        self.meat_label = ttk.Label(self, text="Meat lovers", font=MEDIUM_FONT)
        self.meat_label.grid(row=14, column=1, columnspan=5, pady=10,
                             sticky="W")
        self.meat_price = ttk.Label(self, font=MEDIUM_FONT, text="${:.2f}"
                                    .format(self.meat_cost))
        self.meat_price.grid(row=14, column=4, columnspan=3, pady=10)
        meat_vcmd = (self.register(self.confirm), '%P', '%S', 'meat')
        self.meat_amount = ttk.Entry(self, validate="key", justify="center",
                                     validatecommand=meat_vcmd)
        self.meat_amount.grid(row=14, column=10, columnspan=2, pady=10)

        # Cheese label, price and amount entry
        self.cheese_label = ttk.Label(self, text="Cheese", font=MEDIUM_FONT)
        self.cheese_label.grid(row=15, column=1, columnspan=5, pady=10,
                               sticky="W")
        self.cheese_price = ttk.Label(self, font=MEDIUM_FONT,
                                      text="${:.2f}".format(self.cheese_cost))
        self.cheese_price.grid(row=15, column=4, columnspan=3, pady=10)
        cheese_vcmd = (self.register(self.confirm), '%P', '%S', 'cheese')
        self.cheese_amount = ttk.Entry(self, validate="key", justify="center",
                                       validatecommand=cheese_vcmd)
        self.cheese_amount.grid(row=15, column=10, columnspan=2, pady=10)

        # Pepperoni label, price and amount entry
        self.pepperoni_label = ttk.Label(self, text="Pepperoni",
                                         font=MEDIUM_FONT)
        self.pepperoni_label.grid(row=16, column=1, columnspan=5, pady=10,
                                  sticky="W")
        self.pepperoni_price = ttk.Label(self, font=MEDIUM_FONT,
                                         text="${:.2f}".format(
                                             self.pepperoni_cost))
        self.pepperoni_price.grid(row=16, column=4, columnspan=3, pady=10)
        pepperoni_vcmd = (self.register(self.confirm), '%P', '%S', 'pepperoni')
        self.pepperoni_amount = ttk.Entry(self, validate="key",
                                          justify="center",
                                          validatecommand=pepperoni_vcmd)
        self.pepperoni_amount.grid(row=16, column=10, columnspan=2, pady=10)

        # Hawaiian label, price and amount entry
        self.hawaii_label = ttk.Label(self, text="Hawaiian", font=MEDIUM_FONT)
        self.hawaii_label.grid(row=17, column=1, columnspan=5, pady=10,
                               sticky="W")
        self.hawaii_price = ttk.Label(self, font=MEDIUM_FONT,
                                      text="${:.2f}".format(
                                          self.hawaiian_cost))
        self.hawaii_price.grid(row=17, column=4, columnspan=3, pady=10)
        hawaii_vcmd = (self.register(self.confirm), '%P', '%S', 'hawaiian')
        self.hawaii_amount = ttk.Entry(self, validate="key", justify="center",
                                       validatecommand=hawaii_vcmd)
        self.hawaii_amount.grid(row=17, column=10, columnspan=2, pady=10)

        # Seafood label, price and amount entry
        self.seafood_label = ttk.Label(self, text="Seafood", font=MEDIUM_FONT)
        self.seafood_label.grid(row=18, column=1, columnspan=5, pady=10,
                                sticky="W")
        self.seafood_price = ttk.Label(self, font=MEDIUM_FONT,
                                       text="${:.2f}".format(self.seafood_cost))
        self.seafood_price.grid(row=18, column=4, columnspan=3, pady=10)
        seafood_vcmd = (self.register(self.confirm), '%P', '%S', 'seafood')
        self.seafood_amount = ttk.Entry(self, validate="key", justify="center",
                                        validatecommand=seafood_vcmd)
        self.seafood_amount.grid(row=18, column=10, columnspan=2, pady=10)

        # Maximum number of pizzas
        self.amount_label = ttk.Label(self, font=SMALL_FONT, foreground="red",
                                      text="Maximum of 9 of each pizza type.")
        self.amount_label.grid(row=19, column=1, columnspan=9)

        # Total label and total amount label
        total_label = ttk.Label(self, text="Total:", font=MEDIUM_FONT)
        total_label.grid(row=20, column=1, sticky="W")
        self.total_cost_label = ttk.Label(self, font=MEDIUM_FONT,
                                          text="$0.00")
        self.total_cost_label.grid(row=20, column=1, columnspan=6,
                                   padx=10, sticky="E")

        # Buttons

        # Erase button
        self.erase_button = ttk.Button(self, text="Erase all",
                                       command=lambda: self.erase())
        self.erase_button.grid(row=19, column=9, columnspan=4, pady=5)

        # Purchase button
        self.buy_img = tk.PhotoImage(file="img/shops/purchase_button.gif")
        buy_window = (lambda: self.order())
        self.buy_button = tk.Button(self, compound=tk.TOP, relief="flat",
                                    width=80, height=40, image=self.buy_img,
                                    command=buy_window, state='disabled')
        self.buy_button.grid(row=20, column=7, columnspan=6, sticky="E",
                             pady=5)
        self.buy_button.image = self.buy_img

        # Back button
        back_img = tk.PhotoImage(file="img/menu/back_button.gif")
        back_button = tk.Button(self, relief="flat", width=80, height=40,
                                image=back_img,
                                command=lambda: self.back_button())
        back_button.grid(row=22, column=10, columnspan=5, sticky="E")
        back_button.image = back_img

        VirtualWorld.menu_bar(self, controller)
        self.toplevel = None

        PizzaShopPage.reset_order_data()

    def erase(self):
        """ Remove all data from the order entries. """
        for amount in (self.meat_amount, self.cheese_amount,
                       self.pepperoni_amount, self.hawaii_amount,
                       self.seafood_amount):
            amount.delete(0, 1)
            amount.insert(0, "")

    def confirm(self, P, S, _type):
        """
        Only allow a 1 digit integer and if the total of all the entries
        is greater than one, enable the cart button.

        :param P: allowed value (%P).
        :param S: text being inserted (%S).
        :param _type: the pizza type (str).
        :returns: True - If value is valid.
                 False - If input is invalid.
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
                logger.error("Input is not an integer!")
        if isinstance(inserted_value, int) and 0 < len(allowed_value) == 1:
            with open(PIZZA_DATA_F, 'r') as file:
                current_data = [line.strip() for line in file]
            data = {}
            with open(PIZZA_DATA_F, 'r') as file:
                for line in file:
                    option, value = line.strip().split(':')
                    data[option] = value
            if data[_type] == str(allowed_value):
                logger.debug("No changes to be made to {}".format(PIZZA_DATA_F))
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

                meat_total = 0
                cheese_total = 0
                pepperoni_total = 0
                hawaiian_total = 0
                seafood_total = 0

                for item in current_data:
                    item = item.split(':')
                    if item[0] == 'meat' and int(item[1]) > 0:
                        meat_total = int(item[1]) * self.meat_cost
                    elif item[0] == 'cheese' and int(item[1]) > 0:
                        cheese_total = int(item[1]) * self.cheese_cost
                    elif item[0] == 'pepperoni' and int(item[1]) > 0:
                        pepperoni_total = int(item[1]) * self.pepperoni_cost
                    elif item[0] == 'hawaiian' and int(item[1]) > 0:
                        hawaiian_total = int(item[1]) * self.hawaiian_cost
                    elif item[0] == 'seafood' and int(item[1]) > 0:
                        seafood_total = int(item[1]) * self.seafood_cost
                new_total = meat_total + cheese_total + pepperoni_total + \
                    hawaiian_total + seafood_total

            if int(data['total']) > 0:
                self.total_cost_label.configure(text="${:.2f}"
                                                .format(new_total))
                self.buy_button.configure(state='normal')
            else:
                self.total_cost_label.configure(text="$0.00")
                self.buy_button.configure(state='disabled')
            with open(PIZZA_DATA_F, 'w') as file:
                logger.debug("Writing new data to {}".format(PIZZA_DATA_F))
                file.write('\n'.join(current_data))
            return True
        else:
            self.bell()
            return False

    def back_button(self):
        """ Raise the ShopPage frame to the user's view. """
        self.controller.show_frame(ShopPage)

    def submit_button(self):
        """
        Check user input and change the order window for the specified
        user, where guests do not pay but all other users do.

        :return: False - If user data is incorrect or if there is no data.
        """
        try:
            username = self.toplevel.username.get()
            password = self.toplevel.password.get()
        except AttributeError:
            username = "Guest"
            password = "None"

        name_and_pass = username + ',' + password
        full_user_data = Check.all_user_data(name_and_pass)
        # Attempt to get all of the user's data if user in the user_data_file
        amount = float(self.total_cost_label.cget("text").strip('$'))
        if name_and_pass == ',':
            logger.info("Nothing was entered!")
            self.toplevel.user_info.configure(text="Nothing entered!",
                                              foreground="red")
            return False
        elif Check.in_user_data(full_user_data):
            logger.info("User '{}' Exists!".format(username))
            self.toplevel.user_info.configure(text="")
            # Confirm button
            purchase = (lambda: self.purchase(username, amount))
            self.toplevel.submit = ttk.Button(self.toplevel, text="Confirm",
                                              command=purchase)
            self.toplevel.submit.grid(row=13, column=6, columnspan=10, pady=5)
        else:
            # Error label
            self.toplevel.error_label = ttk.Label(
                self.toplevel, text="Incorrect username/password",
                foreground="red")
            self.toplevel.error_label.grid(row=14, column=9, columnspan=20)
            return False

    def purchase(self, username, amount):
        """
        Check the user is not a guest and then withdraw the amount from the
        user's account. Reset the order_data_file if the transaction is
        successful.
        """
        if username == 'Guest':
            self.toplevel.user_info.configure(text="Transaction successful",
                                              foreground="green")
            PizzaShopPage.reset_order_data()
        elif User.withdraw(username, amount) is True:
            self.toplevel.user_info.configure(text="Transaction successful",
                                              foreground="green")
            PizzaShopPage.reset_order_data()
        elif User.withdraw(username, amount) == "inadequate_funds":
            self.toplevel.user_info.configure(text="Inadequate funds",
                                              foreground="red")
        else:
            self.toplevel.user_info.configure(text="Transaction failed",
                                              foreground="red")
        self.toplevel.user_info.after(2500, lambda: self.remove_window())

    @staticmethod
    def reset_order_data():
        """ Reset the PIZZA_DATA_F file. """
        order_data = ['meat', 'cheese', 'pepperoni', 'hawaiian', 'seafood',
                      'total']
        new_data = []
        with open(PIZZA_DATA_F, 'w') as file:
            for data in order_data:
                new_data.append('{}:0'.format(data))
            file.write('\n'.join(new_data))

    def order(self):
        """
        Create the order window (which displays the user's order) and display
        the correct amounts and totals for the user's order.
        """
        if self.toplevel is None:
            self.toplevel = tk.Toplevel(self)
            self.toplevel.protocol('WM_DELETE_WINDOW',
                                   lambda: self.remove_window())
            self.toplevel.focus_set()
            self.toplevel.resizable(width=False, height=False)
            self.toplevel.title('Order')

            # Order label
            order_label = ttk.Label(self.toplevel, text="Here is your order:",
                                    font=MEDIUM_FONT)
            order_label.grid(row=0, column=0, columnspan=20, padx=5, pady=5)
            # Pizza type label
            type_label = ttk.Label(self.toplevel, text="Type", font=SMALL_FONT)
            type_label.grid(row=2, column=0, columnspan=10, pady=10, padx=5)
            # Price label
            price_label = ttk.Label(self.toplevel, text="Amount",
                                    font=SMALL_FONT)
            price_label.grid(row=2, column=10, columnspan=9, pady=10)
            # Amount label
            amount_label = ttk.Label(self.toplevel, text="Price",
                                     font=SMALL_FONT)
            amount_label.grid(row=2, column=20, pady=10)

            data = {}
            with open(PIZZA_DATA_F, 'r') as file:
                row_num = 2
                for line in file:
                    option, value = line.strip().split(':')
                    data[option] = value
                    if int(data[option]) > 0:
                        if option == 'meat':
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.meat_cost)
                        elif option == 'cheese':
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.cheese_cost)
                        elif option == 'pepperoni':
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.pepperoni_cost)
                        elif option == 'hawaiian':
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.hawaiian_cost)
                        elif option == 'seafood':
                            price = "${:.2f}".format(int(data[option]) *
                                                     self.seafood_cost)
                        elif option == 'total':
                            price = self.total_cost_label.cget("text")
                        else:
                            price = ""
                        pizza_type = option.title()
                        row_num += 1
                        ttk.Label(self.toplevel, text=pizza_type)\
                            .grid(row=row_num, column=0, columnspan=10)
                        ttk.Label(self.toplevel, text=data[option])\
                            .grid(row=row_num, column=10, columnspan=9)
                        ttk.Label(self.toplevel, text=price)\
                            .grid(row=row_num, column=20)

            with open(current_user_file, 'r') as file:
                if 'Guest,None,50,1000000' not in file:
                    # Username and password labels and entries
                    # Username label
                    username_label = ttk.Label(self.toplevel, text="Username:",
                                               font=SMALL_FONT)
                    username_label.grid(row=9, column=7, columnspan=11, pady=5)
                    # Username entry
                    self.toplevel.username = ttk.Entry(self.toplevel)
                    self.toplevel.username.grid(row=10, sticky='W', padx=20,
                                                column=9, columnspan=12)
                    # Password label
                    password_label = ttk.Label(self.toplevel, text="Password:",
                                               font=SMALL_FONT)
                    password_label.grid(row=11, column=7, columnspan=11,
                                        pady=5)
                    # Password entry
                    self.toplevel.password = ttk.Entry(self.toplevel, show="*")
                    self.toplevel.password.grid(row=12, sticky="E", padx=20,
                                                column=9, columnspan=12)
            # Buttons

            # Submit button
            submit_command = (lambda: self.submit_button())
            self.toplevel.submit = ttk.Button(self.toplevel, text="Submit",
                                              command=submit_command)
            self.toplevel.submit.grid(row=13, column=6, columnspan=10, pady=5)

            # Cancel button
            cancel_command = (lambda: self.remove_window())
            self.toplevel.cancel = ttk.Button(self.toplevel, text="Cancel",
                                              command=cancel_command)
            self.toplevel.cancel.grid(row=13, column=16, columnspan=6, pady=5)

            # Error label
            self.toplevel.user_info = ttk.Label(self.toplevel, text="",
                                                font=SMALL_FONT)
            self.toplevel.user_info.grid(row=14, column=8, columnspan=20)

            # Toplevel position
            w = 250  # Width for toplevel
            h = 335  # Height for toplevel

            ws = self.toplevel.winfo_screenwidth()  # Width of the screen
            hs = self.toplevel.winfo_screenheight()  # Height of the screen

            # Calculate x and y coordinates for the Tk root window
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            # Set the dimensions of the screen and where it is placed
            self.toplevel.geometry('%dx%d+%d+%d' % (w, h, x, y - 30))
            self.toplevel.mainloop()

    def remove_window(self):
        """ Remove the toplevel (order) window. """
        self.toplevel.destroy()
        self.toplevel = None


class Check:

    @staticmethod
    def file():
        """
        Check files exist and returns data within them:

        :returns: a dict containing the keys:

                 'user_names'   - user_names.txt     (list)
                 'user_data'    - user_data.txt      (list)
                 'current_user' - current_user.txt   (list)
                 'options'      - options.txt        (list)
        """

        def options():
            """
            Check options.txt exists and it is created if it does not exist.

            :return: option_data (list).
            """
            while True:
                try:
                    with open(options_file, 'r') as file:
                        logger.debug("Opening the options file '{}'.".format(
                              options_file))
                        option_data = [line.strip() for line in file]
                    return option_data
                except FileNotFoundError:
                    logger.error("Failed to open the 'options.txt' file")
                    with open(options_file, 'w') as file:
                        logger.debug("Creating options.txt...")
                        file.write("running:False\ntimes_opened:0")

        def user_names():
            """
            Check user_names.txt exists and it is created if it does not exist.
            Returns name_data as list.

            :return: name_data (list).
            """
            while True:
                try:
                    with open(user_names_file, 'r') as file:
                        logger.debug("Opening the user_names_file '{}'.".format(
                              user_names_file))
                        name_data = [line.strip() for line in file]
                    return name_data
                except FileNotFoundError:
                    logger.error("Failed to open '{}'.".format(user_names_file))
                    with open(user_names_file, 'w') as file:
                        logger.debug("Creating '{}'...".format(user_names_file))
                        file.write("Guest")

        def user_data():
            """
            Check user_data.txt exists and it is created if it does not exist.

            :return: _all_data (list).
            """
            while True:
                try:
                    with open(user_data_file, 'r') as file:
                        logger.debug("Opening the user_data_file '{}'.".format(
                              user_data_file))
                        _all_data = [line.strip() for line in file]
                    return _all_data
                except FileNotFoundError:
                    logger.error("Failed to open '{}'.".format(user_data_file))
                    with open(user_data_file, 'w') as file:
                        logger.debug("Creating '{}'...".format(user_data_file))
                        file.write("Guest,None,50,1000000")

        def current_user():
            """
            Check current_user.txt exists and it is created if it does not
            exist.

            :return: current_user_data (list).
            """
            while True:
                try:
                    with open(current_user_file, 'r') as file:
                        logger.debug("Opening the current_user_file '{}'."
                                     .format(current_user_file))
                        current_user_data = [line.strip() for line in file]
                    return current_user_data
                except FileNotFoundError:
                    logger.error("Failed to open '{}'"
                                 .format(current_user_file))
                    with open(current_user_file, 'w') as file:
                        logger.debug("Creating '{}'..."
                                     .format(current_user_file))
                        file.write("Guest,None,50,1000000")

        return {"options": options(), "user_names": user_names(),
                "user_data": user_data(), "current_user": current_user()}

    @staticmethod
    def in_user_data(user):
        """
        Check if user's info is in the user_data_file.

        :param user: the user's info to search (str).
        :returns: True - If user is in the file (bool).
                  False - If user is None or not in file (bool).
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

        :param user_info: user's username and password (str).
        :return: (str) - If age and balance don't raise a KeyError.
                 None - If a KeyError is raised.
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
        """
        Check if the user's name is in the user_names file, or is '' or
        contains only alphabet characters or numbers.

        :param name: user's name (str).
        :return: True - If username matches the regular expression.
                 False - If username in the user_names file, '' or anything
                         else.
        """
        if name in Check.file()["user_names"]:
            logger.info("You cannot use that name as it is already taken.")
            return False
        elif name == '':
            logger.info("You must enter something for your username.")
            return False
        elif re.match('^[\w\d_-]*$', name):
            logger.info("Username Accepted.")
            return True
        else:
            logger.info("Your username may only contain letters, numbers, ",
                        "or underscores.")
            return False

    @staticmethod
    def password(pwd):
        """
        Check if the user's password contains only alphabet characters or
        numbers.

        :param pwd: user's password (str).
        :return: True - If password matches the regular expression.
                 False - If it is anything else.
        """
        if re.match('^[\w\d_-]*$', pwd):
            logger.info("Password Accepted.")
            return True
        else:
            logger.info("Your password may only contain letters, numbers, ",
                  "or underscores.")
            return False

    @staticmethod
    def age(years_old):
        """
        Check if the user's age is a two or three digit integer.

        :param years_old: user's age (int).
        :return: True - If age does not match the regular expression.
                 False - If does not match the regular expression.
        """
        if not(re.match('^[\d]{2,3}$', years_old)):
            logger.info("You must enter a two or three digit integer!")
            return False
        else:
            logger.info("Age accepted")
            return True


class User:

    @staticmethod
    def new(username, password, age):
        """
        Appending the user_data_file with the new user's information.

        :param username: user's login name (str).
        :param password: user's login password (str).
        :param age: user's age (str).
        """
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
        logger.info("\nUser {} created!\n".format(username))

    @staticmethod
    def get_data(username=None):
        """
        Open user_data_file and get the user data for the specified username.

        :param username: the user to get the data for (str).
        :returns: a dict containing the keys:

                 'username'  - (str)
                 'password'  - (str)
                 'age'       - (str)
                 'balance'   - (str)
        """
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
        """
        Open current_user_file and get the current user data.

        :returns: a dict containing the keys:

                 'username'  - (str)
                 'password'  - (str)
                 'age'       - (str)
                 'balance'   - (str)
        """
        with open(current_user_file, 'r') as file:
            user, pwd, age, balance = file.readline().split(',')
        return {"username": user, "password": pwd,
                "age": age, "balance": balance}

    @staticmethod
    def create_balance(age):
        """
        Create a balance for a new user based on their age.

        :param age: the user's age in years (str).
        :returns: 100000 - If over 80           (int)
                  75000  - If between 60 and 80 (int)
                  50000  - If between 40 and 60 (int)
                  25000  - If between 20 and 40 (int)
                  15000  - If between 15 and 20 (int)
                  2000   - If less than 15      (int)
                  5000   - If none of the above (int)
        """
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
        """
        Change the user's name and append it to the user_data_file and
        user_names_file.

        :param old_name: user's original name (str).
        :param new_name: user's new name(str).
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

        logger.info("Your username is now '{}'.".format(new_name))

    @staticmethod
    def password_change(username, new_password):
        """
        Change the user's password and append it to user_data_file.

        :param username: user's login name (str).
        :param new_password: user's new password (str).
        """
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

        logger.info("Your password is now '{}'.".format(new_password))

    @staticmethod
    def age_change(username, new_age):
        """
        Change the user's age and append it to user_data_file.

        :param username: user's login name (str).
        :param new_age: user's new age (str).
        """
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

        logger.info("You are now {:d} years old.".format(int(new_age)))

    @staticmethod
    def delete(username):
        """
        Delete the user from the user_data_file.

        :param username: user's login name (str).
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
        """
        Withdraw an amount from the user's current balance.

        :param username: user's login name (str).
        :param amount: amount of money to withdraw (float).
        :returns: True - If withdrawal is successful (bool).
                  inadequate_funds - If user balance is less than amount (str).
                  False - If any other case.
        """
        user_balance = User.get_data(username)['balance']
        if float(user_balance) >= amount:
            user_data = list(Check.file()['user_data'])
            password = User.get_data(username)['password']
            age = User.get_data(username)['age']
            logger.info("Withdrawing {} from {}".format(amount, username))
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
            return "inadequate_funds"
        else:
            return False

    @staticmethod
    def deposit(username, amount):
        """
        Deposit an amount to the user's current balance.

        :param username: user's login name (str).
        :param amount: amount of money to deposit (float).
        """
        user_balance = User.get_data(username)['balance']
        user_data = list(Check.file()['user_data'])
        password = User.get_data(username)['password']
        age = User.get_data(username)['age']
        logger.info("Depositing {} to {}".format(amount, username))
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
        """ Setup the default options. """
        self.options = Options.get()
        if self.options['running'] is 'True':
            sys.exit()
        else:
            self.options['running'] = 'True'
            self.options['times_opened'] = (int(self.options['times_opened']) +
                                            1)
            new_data = self.options
            Options.update(new_data)

    @staticmethod
    def get():
        """
        Get all the options and their values.

        :return: data (dict).
        """
        data = {}
        with open(options_file, 'r') as file:
            for line in file:
                option, value = line.strip().split(':')
                data[option] = value
        return data

    @staticmethod
    def update(new_data):
        """
        Change the old option data to the new data.

        :param new_data: all of the new option data (dict).
        """
        option_data = []
        for option in new_data:
            option_data.append("{}:{}".format(option, new_data[option]))

        with open(options_file, 'w') as file:
            file.write('\n'.join(option_data))

    def exit(self):
        """ Change the value of running to False in the options_file. """
        with open(options_file, 'r') as file:
            if "running:False" in file:
                sys.exit()
            else:
                self.options['running'] = "False"
                new_data = self.options
                Options.update(new_data)

    @staticmethod
    def print():
        """ Print the options and their values to the log file. """
        for option in Options.get():
            logger.debug("{}:{}".format(option, Options.get()[option]))


def main():
    """
    Check files, setup class instances, app dimensions and properties. Start
    of the Virtual World program, and calls for the exit cleanup.
    """
    # import options_write  # overwrites the options file with default values
    Check.file()
    app = VirtualWorld()

    w = 500  # Width for the Tk root
    h = 600  # Height for the Tk root

    # Root window position
    ws = app.winfo_screenwidth()  # Width of the screen
    hs = app.winfo_screenheight()  # Height of the screen

    # Calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # Set the dimensions of the screen
    # and where it is placed
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))
    app.resizable(width=False, height=False)
    app_options = Options()
    app.mainloop()  # starts the mainloop
    app_options.exit()

if __name__ == "__main__":
    main()
