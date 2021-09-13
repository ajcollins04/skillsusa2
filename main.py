from tkinter import *
import tkinter.font as tkFont
import tkinter.messagebox as tkMessage
import tkinter.filedialog

root = Tk()
root.geometry("600x500")
root.configure(bg="black")
root.title("SkillUSA Programs")

font = tkFont.Font(size=20)


def clear_frame():
    global frame
    frame.destroy()
    frame = Frame(bg="black")
    frame.place(relx=.5, rely=.5, anchor="c")


def start_screen():
    clear_frame()

    check_app = Button(frame, text="Checking App",
                       font=font, command=start_checking)
    check_app.grid(row=0, column=0)

    camp_app = Button(frame, text="Summer Camp App",
                      font=font, command=start_camp_app)
    camp_app.grid(row=0, column=1)
    frame.place(relx=.5, rely=.5, anchor="c")


def start_checking():
    clear_frame()

    balance_input_frame = Frame(frame, bg="black")
    balance_input_frame.grid(row=0, column=0)

    start_balance_label = Label(
        balance_input_frame, text="Starting Balance", font=font, bg="black", fg="white")
    start_balance_label.grid(row=0, column=0)

    start_balance_entry = Entry(
        balance_input_frame, textvariable=start_balance, font=font)
    start_balance_entry.grid(row=0, column=1)

    write_checks_button = Button(
        frame, text="Write a Check", command=start_writing_checks, font=tkFont.Font(size=15))
    write_checks_button.grid(row=1, column=0)

    frame.place(relx=.5, rely=.5, anchor="c")


def start_writing_checks():
    try:
        int(start_balance.get())
        clear_frame()

        checks.append(Check())

    except Exception as e:
        start_balance.set("")
        tkMessage.showwarning(
            "Oops!", f"Your balance value didn't work. Check to make sure it is a number (e.g. 1000). {e}")


class CreateInput:
    def __init__(self, master, row, label_text):
        self.input_var = StringVar()

        self.label = Label(master, text=label_text, bg='black',
                           fg="white", font=tkFont.Font(size=15))
        self.label.grid(row=row, column=0)

        self.input = Entry(master, textvariable=self.input_var, font=font)
        self.input.grid(row=row, column=1)


class Check:
    def __init__(self):
        self.check_input_frame = Frame(frame, bg="black")
        self.check_input_frame.grid(row=0, column=0)

        self.check_number_input = CreateInput(
            self.check_input_frame, 0, "Check Number")
        self.check_payee_input = CreateInput(
            self.check_input_frame, 1, "Payee")
        self.check_amount_input = CreateInput(
            self.check_input_frame, 2, "Check Amount")

        self.cleared = IntVar()

        self.check_cleared_label = Label(
            self.check_input_frame, text="Check Cleared", bg="black", fg="white", font=tkFont.Font(size=15))
        self.check_cleared_label.grid(row=3, column=0)

        self.check_cleared_button = Checkbutton(
            self.check_input_frame, variable=self.cleared, onvalue=1, offvalue=0, bg="black")
        self.check_cleared_button.grid(row=3, column=1, sticky="w")

        self.check_buttons = Button(frame, bg="black")
        self.check_buttons.grid(row=1, column=0)

        self.buttons_font = tkFont.Font(size=15)

        self.save_check = Button(self.check_buttons, text="Save Check",
                                 font=self.buttons_font, command=lambda: save_check(self))
        self.save_check.grid(row=1, column=0)

        self.check_balance = Button(self.check_buttons, text="Balance",
                                    font=self.buttons_font, command=lambda: check_balance(self))
        self.check_balance.grid(row=1, column=1)

        self.new_check = Button(self.check_buttons, text="New Check",
                                font=self.buttons_font, command=lambda: new_check(self))
        self.new_check.grid(row=1, column=2)

        


def save_check(current_check):
    try:
        int(current_check.check_number_input.input_var.get())
        int(current_check.check_amount_input.input_var.get())

        check_spent = 0
        for check in checks:
            if int(check.check_number_input.input_var.get()) == int(current_check.check_number_input.input_var.get())\
                    and check != current_check:
                tkMessage.showwarning(
                    "Oops!", "You've already used that check number.")
                return
            check_spent += int(check.check_amount_input.input_var.get())

        if check_spent > int(start_balance.get()):
            tkMessage.showwarning(
                "Oops!", "That would spend more money than you have.")
            return

        directory = tkinter.filedialog.asksaveasfilename(
            filetypes=[("Text file", "*.txt")])
        if directory[-4:] != ".txt":
            directory += ".txt"

        file = open(directory, "w")
        file.write(f"Check Number: {int(check.check_number_input.input_var.get())}\n"
                   f"Check Payee: {check.check_payee_input.input_var.get()}\n"
                   f"Check Amount: {int(check.check_amount_input.input_var.get())}")
        file.close()
    except:
        tkMessage.showwarning(
            "Oops!", "Saving didn't work. Check your inputs.")


def new_check(current_check):
    try:
        int(current_check.check_number_input.input_var.get())
        int(current_check.check_amount_input.input_var.get())

        check_spent = 0
        for check in checks:
            if int(check.check_number_input.input_var.get()) == int(current_check.check_number_input.input_var.get())\
                    and check != current_check:
                tkMessage.showwarning(
                    "Oops!", "You've already used that check number.")
                return

            check_spent += int(check.check_amount_input.input_var.get())

        if check_spent > int(start_balance.get()):
            tkMessage.showwarning(
                "Oops!", "That would spend more money than you have.")
            return

        start_writing_checks()
    except:
        tkMessage.showwarning(
            "Oops!", "Something went wrong. Check your inputs.")


def check_balance(current_check):
    try:
        int(current_check.check_number_input.input_var.get())
        int(current_check.check_amount_input.input_var.get())

        amount_spent = 0
        for check in checks:
            if int(check.check_number_input.input_var.get()) == int(current_check.check_number_input.input_var.get())\
                    and check != current_check:
                tkMessage.showwarning(
                    "Oops!", "You've already used that check number.")
                return
            if check.cleared.get() == 1:
                amount_spent += int(check.check_amount_input.input_var.get())

        if amount_spent > int(start_balance.get()):
            tkMessage.showwarning(
                "Oops!", "That would spend more money than you have.")
            return

        clear_frame()

        balance_frame = Frame(frame, bg="black")
        balance_frame.grid(row=0, column=0)

        balance_label = Label(
            balance_frame, text="Current Balance:", bg="black", fg="white", font=font)
        balance_label.grid(row=0, column=0)

        current_balance = Label(
            balance_frame, text=f"{int(start_balance.get()) - amount_spent}", bg="black", fg="white", font=font)
        current_balance.grid(row=0, column=1)

        balance_buttons = Frame(frame, bg="black")
        balance_buttons.grid(row=1, column=0)

        new_check = Button(balance_buttons, text="New Check", font=tkFont.Font(
            size=15), command=start_writing_checks)
        new_check.grid(row=0, column=0)

        exit_button = Button(balance_buttons, text="Exit Program",
                             font=tkFont.Font(size=15), command=exit)
        exit_button.grid(row=0, column=1)

    except:
        tkMessage.showwarning(
            "Oops!", "Something went wrong. Check your inputs.")


def start_camp_app():
    global clicked
    clear_frame()

    clicked = StringVar()


    camp_inputs = CampInputs()

    camp_buttons = Frame(frame, bg="black")
    camp_buttons.grid(row=1, column=0)

    calculate_total_button = Button(camp_buttons, text="Calculate Total", command=lambda: calculate_total(
        camp_inputs), font=tkFont.Font(size=15))
    calculate_total_button.grid(row=0, column=0)

    clear_button = Button(camp_buttons, text="Clear Inputs",
                          command=start_camp_app, font=tkFont.Font(size=15))
    clear_button.grid(row=0, column=1)

    exit_program = Button(camp_buttons, text="Exit Program",
                          font=tkFont.Font(size=15), command=exit)
    exit_program.grid(row=0, column=2)


class ExtraActivity:
    def __init__(self, master, text, row, value):
        self.var = IntVar()
        self.value = value
        check_button_label = Label(
            master, text=text, bg="black", fg="white", font=tkFont.Font(size=15))
        check_button_label.grid(row=row, column=0)

        check_button = Checkbutton(
            master, variable=self.var, onvalue=1, offvalue=0, bg="black")
        check_button.grid(row=row, column=1, sticky="w")


class CampInputs:
    def __init__(self):
        self.camp_inputs = Frame(frame, bg="black")
        self.camp_inputs.grid(row=0, column=0)

        self.camper_name = CreateInput(self.camp_inputs, 0, "Camper Name")
        self.address = CreateInput(self.camp_inputs, 1, "Full Address")
        self.emergency_contact_name = CreateInput(
            self.camp_inputs, 2, "Emergency Contact")
        self.emergency_contact_phone = CreateInput(
            self.camp_inputs, 3, "Emergency Contact Phone")
        self.options = ["Half Day", "Full Day"]

        self.drop_label = Label(self.camp_inputs, text="Half or Full Day",
                                bg="black", fg="white", font=tkFont.Font(size=15))
        self.drop_label.grid(row=4, column=0)

        self.drop = OptionMenu(self.camp_inputs, clicked, *self.options)
        self.drop.grid(row=4, column=1, sticky="w")

        self.days_staying = CreateInput(self.camp_inputs, 5, "Days Staying")

        self.swimming = ExtraActivity(self.camp_inputs, "Swimming", 6, 5)
        self.canoeing = ExtraActivity(self.camp_inputs, "Canoeing", 7, 7.5)
        self.horseback = ExtraActivity(
            self.camp_inputs, "Horseback Riding", 8, 8.75)
        self.crafts = ExtraActivity(self.camp_inputs, "Crafts", 9, 4)

        self.inputs = [self.camper_name, self.address, self.emergency_contact_name, self.emergency_contact_phone]
        self.checkboxes = [self.swimming, self.canoeing, self.horseback, self.crafts]


def calculate_total(inputs):
    for each_input in inputs.inputs:
        if each_input.input_var.get() == "":
            tkMessage.showwarning(
                    "Oops!", "You have an empty input.")
            return
        
        
    for each_input in inputs.emergency_contact_phone, inputs.days_staying:
        try: 
            int(each_input.input_var.get())
        except:
            tkMessage.showwarning(
                "Oops!", "One of your inputs needs to be a number.")  
            return

    if clicked.get() == "Half Day":
        total = int(inputs.days_staying.input_var.get()) * 25
    else:
        total = int(inputs.days_staying.input_var.get()) * 35


    for each_checkbox in inputs.checkboxes:
        if each_checkbox.var.get() == 1:
            total += int(inputs.days_staying.input_var.get()) * each_checkbox.value

    clear_frame()

    total_label = Label(frame, bg="black", fg="white", text=f"Total: {total}", font=font)
    total_label.grid(row=0, column=0)

    buttons_frame = Frame(frame, bg="black")
    buttons_frame.grid(row=1, column=0)

    new_camper = Button(buttons_frame, text="New Camper", command=start_camp_app, font=font)
    new_camper.grid()

    end_program = Button(buttons_frame, text="Quit Program", command=exit, font=font)
    end_program.grid(row=0, column=1)




start_balance = StringVar()
clicked = StringVar()

checks = []
activites = []

frame = Frame(bg="black")
frame.place(relx=.5, rely=.5, anchor="c")

start_screen()

root.mainloop()
