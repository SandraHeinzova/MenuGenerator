import pathlib
import random
import os
from tkinter import *
from tkinter import messagebox
from datetime import date
import smtplib
from email.message import EmailMessage
import requests
from googletrans import Translator


today = date.today()
menu_list = []
amount = 0
my_email = os.environ.get("MyEmail")
password = os.environ.get("PasswordEmail")
nw_entry_email = None
complete_menu = ""
p = pathlib.Path(__file__).resolve().parents[0]


# ------------- function body -------------
def printable(txt, sheet):
    global complete_menu
    file = p / f"{sheet}.txt"
    with file.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            for x in range(len(txt)):
                new_line = line.replace(f"food{x}", txt[x])
                if str(x) in line:
                    complete_menu += new_line + "\n"
                else:
                    continue

    print_menu = p / f"menu-{today}.txt"
    print_menu.write_text(complete_menu, encoding="utf-8")


def random_foods(amounts):
    global nw_entry_email
    global send_to
    global menu_list
    menu_text = ""
    with open("meals.txt", "r", encoding="utf-8") as meals:
        meal = list(meals)

    menu_list = random.sample(meal, amounts)

    for y in menu_list:
        menu_text += y

    new_window = Toplevel()
    new_window.geometry("270x300+500+400")
    new_window.title("Menu")
    new_window.config(padx=50, pady=25, bg="#3795BD")
    new_window.attributes('-topmost', True)

    nw_label = Label(new_window, text="Váš výběr:", font=("Arial", 10, "bold"))
    nw_label.grid(column=0, row=0)
    nw_label.config(bg="#3795BD", fg="#3A1078")

    nw_label2 = Label(new_window, text=f"{menu_text}", font=("Arial", 10, "bold"))
    nw_label2.grid(column=0, row=1)
    nw_label2.config(pady=25, bg="#3795BD", fg="#9f02ad")

    nw_entry_email = Entry(new_window, width=28)
    nw_entry_email.insert(0, "heinzova.sandra@gmail.com")
    nw_entry_email.grid(column=0, row=3)

    nw_button = Button(new_window, text="Pošli na mail", command=send)
    nw_button.grid(column=0, row=4)

    nw_label3 = Label(new_window, text=quote())
    nw_label3.grid(column=0, row=5)
    nw_label3.config(bg="#3795BD", fg="#3A1078", wraplength=300)


def send():
    send_to = nw_entry_email.get()
    if amount > 1:
        msg = EmailMessage()
        msg["From"] = my_email
        msg["Subject"] = "Menu"
        msg["To"] = send_to
        msg.set_content("Bon Appetite!")
        msg.add_attachment(open(f"menu-{today}.txt",
                                "r", encoding="utf-8").read(), filename="Menu.txt")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.send_message(msg=msg)

        messagebox.showinfo(title="Úspěšně posláno", message="Menu už letí do emailu!")
    else:
        messagebox.showwarning(title="Nelze poslat", message="Přece nechcete jedno jídlo na týden.")


def choose_one():
    global amount
    amount = int(generate1.cget("text"))
    random_foods(amount)
    menu_list.clear()


def choose_four():
    global amount
    amount = int(generate4.cget("text"))
    random_foods(amount)
    printable(menu_list, "menu_short")
    menu_list.clear()


def choose_seven():
    global amount
    amount = int(generate7.cget("text"))
    random_foods(amount)
    printable(menu_list, "menu")
    menu_list.clear()


def temporary(e):
    add_new.delete("1.0", END)


def add_new_meal():
    new_meal = add_new.get("1.0", END).capitalize()
    with open("meals.txt", "r", encoding="utf-8") as meals:
        meal = list(meals)
        if new_meal not in meal:
            with open("meals.txt", "a", encoding="utf-8") as a_meals:
                a_meals.write(new_meal.capitalize())
                messagebox.showinfo(title="Přidáno", message="Úspěšně přidáno!")
        else:
            messagebox.showinfo(title="Nepřidáno", message="Toto jídlo již v seznamu je!")


def quote():
    category = 'food'
    MY_API_KEY = "v4GWQ2IyOh6byNqbsSF5Qg==C8xMYYnONrksdAeW"
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': MY_API_KEY})
    if response.status_code == requests.codes.ok:
        data = response.json()
        quote = data[0]["quote"]
        author = data[0]["author"]
        translator = Translator()
        translated_quote = translator.translate(quote, dest="cs")
        return translated_quote.text
    else:
        print("Error:", response.status_code, response.text)


# ------------- ui body -------------

window = Tk()
window.title("Menu Generator")
window.geometry("375x425+450+250")
window.resizable(width=False, height=False)
window.config(pady=20, padx=20, bg="#3795BD")

#  labels
title_label = Label(text="Menu Generator", font=("Arial", 20))
title_label.grid(column=1, row=0, columnspan=2)
title_label.config(padx=60, pady=25, bg="#3795BD", fg="#3A1078")

add_new_label = Label(text="Přidej nové jídlo:", font=("Arial", 10, "bold"))
add_new_label.grid(column=1, row=4, columnspan=2, sticky=S)
add_new_label.config(pady=10, bg="#3795BD", fg="#3A1078")

one_meal = Label(text="Chci jedno jídlo", font=("Arial", 8, "bold"))
one_meal.config(padx=10, pady=10, bg="#3795BD", fg="#3A1078")
one_meal.grid(column=1, row=1, sticky=E)

four_meals = Label(text="Chci čtyři jídla", font=("Arial", 8, "bold"))
four_meals.config(padx=10, pady=10, bg="#3795BD", fg="#3A1078")
four_meals.grid(column=1, row=2, sticky=E)

seven_meals = Label(text="Chci sedm jídel", font=("Arial", 8, "bold"))
seven_meals.config(padx=10, pady=10, bg="#3795BD", fg="#3A1078")
seven_meals.grid(column=1, row=3, sticky=E)

# buttons
one = PhotoImage(file="one.png")
generate1 = Button(text="1", image=one, command=choose_one)
generate1.grid(column=2, row=1, sticky=W)

four = PhotoImage(file="four.png")
generate4 = Button(text="4", image=four, command=choose_four)
generate4.grid(column=2, row=2, sticky=W)

seven = PhotoImage(file="seven.png")
generate7 = Button(text="7", image=seven, command=choose_seven)
generate7.grid(column=2, row=3, sticky=W)

photo = PhotoImage(file="food.png")
add = Button(image=photo, command=add_new_meal)
add.config(pady=20, padx=10)
add.grid(column=1, row=6, columnspan=2)

# Entry large text
add_new = Text(height=4, width=20)
add_new.insert(END, "Piš sem..")
add_new.grid(column=1, row=5, columnspan=2)
add_new.bind("<FocusIn>", temporary)

window.mainloop()
