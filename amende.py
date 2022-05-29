import requests
import tkinter as tk
from tkinter import ttk
import json
from tqdm import tqdm

####INFO TO CHANGE#####
your_username = "YOURUSERNAME"
your_pass = "YOURPASS"
amende_food = 49844
####INFO TO CHANGE#####


class App:

    bar = ""

    def __init__(self, root):
        self.parent = root
        self.parent.title("Welcome")
        self.parent.minsize(300,100)
        self.label = tk.Label(start_window, text ="Bienvenue au distributeur d'amendes ! Entrez un bar :")
        self.label.grid(column = 0, row = 0)
        self.entry = tk.StringVar()
        self.entry = ttk.Entry(self.parent, width = 15, textvariable = self.entry)
        self.entry.insert(tk.END, 'volleyrouje')
        self.entry.grid(column = 0, row = 1)
        self.button = ttk.Button(start_window, text = "Valider", command = self.button_action)
        self.button.grid(column = 0, row = 2)
    def button_action(self):
        App.bar = self.entry.get()
        self.parent.destroy()


def get_session(): #Create session
    return requests.Session()


def get_token(s): #Create token
    global your_username, your_pass
    s.get("https://api.chocapix.binets.fr/api-token-auth/")
    login = {'username' : your_username, "password" : your_pass}
    result = s.post("https://api.chocapix.binets.fr/api-token-auth/", data = login, allow_redirects = True )
    return result.text.split('"')[3]


def get_user_to_id_dict(s, token):

    global url_account
    list_user = s.get('https://api.chocapix.binets.fr/user/', headers = { "Authorization": "JWT "+ token} )
    all_users = json.loads(list_user.text)

    users = {}
    list_account = s.get(url_account, headers = { "Authorization": "JWT "+ token} )
    all_accounts = json.loads(list_account.text)
    cur_account, cur_user = 0,0

    while (cur_account < len(all_accounts) ) :
        while (all_users[cur_user]["id"] != all_accounts[cur_account]["owner"]):
            cur_user += 1
        users[all_users[cur_user]["lastname"] + " " + all_users[cur_user]["firstname"]] = all_accounts[cur_account]["id"]

        cur_account += 1


    return users



def give_amende(s,token,account_dict) :
    ###Window creation
    window = tk.Tk()
    window.title("Distributeur d'amendes")
    window.minsize(300,100)

    def clickMe(): ##Click function
        global s, amende_food
        payload = {"items":[{"qty":int(qty.get()),"sellitem":amende_food}],"accounts":[{"account":account_dict[criminel.get()],"ratio":1,"amount":3}],"name":"Amende","type":"meal"}
        result = s.post(url_transaction, json = payload, headers = {"Authorization": "JWT "+ token} )
        if "Amende" in result.text :
            new_string = "Amende donnée avec succès ! Merci pour votre contribution face aux menaces criminels de ce BE."
        else :
            new_string = "Oups ! Y'a eu un p'tit problème technique. Réessayez..."
        label.configure(text= new_string)



    label2 = ttk.Label(window, text = "C'est qui ce batard ?")
    label2.grid(column = 0, row = 0)

    choices = [person for person in account_dict.keys()]
    criminel = tk.StringVar(window)
    criminel.set('Barré Théo')

    w = ttk.Combobox(window, textvariable = criminel, values = choices)
    w.grid(column = 0, row = 1);


    label = ttk.Label(window, text = "Combien d'euros d'amende voulez-vous mettre à ce chenapan?")
    label.grid(column = 0, row = 2)

    qty = tk.StringVar()
    qty = ttk.Entry(window, width = 15, textvariable = qty)
    qty.grid(column = 0, row = 3)


    button = ttk.Button(window, text = "Exterminer la menace", command = clickMe)
    button.grid(column= 0, row = 4)

    window.mainloop()




if __name__ == "__main__":

    s = get_session()
    token = get_token(s)
    account_dict = {}


    ###Start window creation
    start_window = tk.Tk()
    app = App(start_window)
    start_window.mainloop()


    url_transaction = "https://api.chocapix.binets.fr/transaction/?bar=" + App.bar
    url_account = "https://api.chocapix.binets.fr/account/?bar=" + App.bar

    account_dict = get_user_to_id_dict(s, token)
    give_amende(s,token,account_dict)
