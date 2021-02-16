from tkinter import *
from tkinter import ttk
import os
from functools import partial
from typing import Container
import gameplay as gp
from PIL import ImageTk, Image

class GameApp(Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
        
        # __init__ function for class Tk 
        Tk.__init__(self, *args, **kwargs) 
        self.title("Quantum Poker")
        self.container = ttk.Frame(self, padding="3 3 12 12")   
        self.container.grid_configure(padx=5, pady=5)

        self.game = gp.Game()
   
        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (HomePage, InstructionPage): 
   
            frame = F(self.container, self) 
   
            # initializing frame of that object from 
            # startpage, page1, page2 respectively with  
            # for loop 
            self.frames[F] = frame  
            frame.grid(row = 0, column = 0, sticky ="nsew") 

        for i in range(3):
            start_page = StartPage(self.container, self, self.game.players[i])
            player_page = PlayerPage(self.container, self, self.game.players[i])
            
            self.frames[f"Start Page {i+1}"] = start_page
            self.frames[f"Player {i+1}"] = player_page

            player_page.grid(row = 0, column = 0, sticky ="nsew")
            start_page.grid(row = 0, column = 0, sticky ="nsew")
   
        self.show_frame(HomePage) 
   
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise()

    def show_place_selector(self, card, player):
        print(card.get())
        frame = PlaceSelector(self.container, self, card.get(), player)
        frame.grid(row = 0, column = 0, sticky ="nsew") 
        frame.tkraise()

    def show_player_page(self, player):
        frame = PlayerPage(self.container, self, player)
        frame.grid(row = 0, column = 0, sticky ="nsew") 
        frame.tkraise()

    def show_start_page(self, player):
        if player.number == 3:
            next_player = 1
        else:
            next_player = player.number + 1
        frame = StartPage(self.container, self, self.game.players[next_player-1])
        frame.grid(row = 0, column = 0, sticky ="nsew") 
        frame.tkraise()

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent) 

        home_title = ttk.Label(self, text="Welcome to Quantum Poker!")
        
        
        image1 = Image.open(os.path.join(os.getcwd(), "figures", "initial_circuit.png"))
        test = ImageTk.PhotoImage(image1)
        home_image = ttk.Label(self, image=test)
        # home_image = ttk.Label(self, text="sup")
        home_image.image = test

        # imgobj = PhotoImage(file=)
        # home_image['image'] = imgobj
        button_newgame = ttk.Button(self, text='New Game', command=lambda : controller.show_frame("Start Page 1"))
        button_instructions = ttk.Button(self, text='Instructions', command=lambda : controller.show_frame(InstructionPage))

        home_title.grid(column=0, row=0)
        home_image.grid(column=0, row=home_title.grid_info()["row"]+1)
        button_newgame.grid(column=0, row=home_image.grid_info()["row"]+1)
        button_instructions.grid(column=0, row=button_newgame.grid_info()["row"]+1)

        for child in self.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        button_newgame.focus()

class StartPage(ttk.Frame):
    def __init__(self, parent, controller, player):
        ttk.Frame.__init__(self, parent)
        self.player_number = player.number

        start_title = ttk.Label(self, text="Do you have what it takes to win it?")

        player_button = ttk.Button(self, text=f'Player {self.player_number}', command=partial(controller.show_player_page, player))

        home_button = ttk.Button(self, text='Return to Home', command=lambda : controller.show_frame(HomePage))

        start_title.grid(column=0, row=0)
        player_button.grid(column=0, row=1)

        for child in self.winfo_children(): 
            child.grid_configure(padx=5, pady=5)


class InstructionPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent) 
        instructions = Message(self, text="Some Instructions Here. I am")
        # instructions.insert("1.0", "Some Instructions Here.")
        button_homepage = ttk.Button(self, text='Return to Home', command=lambda : controller.show_frame(HomePage))
        
        instructions.grid(column=0, row=0)
        button_homepage.grid(column=0, row=1)
        
        for child in self.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

class PlayerPage(ttk.Frame):
    def __init__(self, parent, controller, player):
        self.controller = controller
        ttk.Frame.__init__(self, parent)
        self.player_number = player.number

        header = Label(self, text=f"Player {self.player_number}")
        # instructions.insert("1.0", "Some Instructions Here.")
        img = ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "figures", "initial_circuit.png")))
        circuit_image = ttk.Label(self, image=img)
        circuit_image.image=img

        cards = CardChoice(self, controller, player)

        
        header.grid(column=0, row=0)
        circuit_image.grid(columnspan=1, row=header.grid_info()["row"]+1)
        cards.grid(column=0, row=circuit_image.grid_info()["row"]+1)
        
        for child in self.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
    

class CardChoice(ttk.Frame):
    def __init__(self, parent, controller, player):
        ttk.Frame.__init__(self, parent)
        self.card_options = list(set(player.cards))

        self.selected_card = StringVar(controller)
        radiobuttons = [ttk.Radiobutton(self, text=card, variable=self.selected_card, value=card) for card in self.card_options]        
        button_confirm = ttk.Button(self, text='Confirm', command=partial(controller.show_place_selector, self.selected_card, player))


        for i in range(len(radiobuttons)):
            radiobuttons[i].grid(column=i, row=0)        

        button_confirm.grid(columnspan=len(self.card_options), row=radiobuttons[0].grid_info()["row"]+1)

        
        for child in self.winfo_children(): 
            child.grid_configure(padx=5, pady=5)


class PlaceSelector(ttk.Frame):
    def __init__(self, parent, controller, card, player):
        ttk.Frame.__init__(self, parent)

        if card == "Toffoli":
            self.place_options = ["Control 1", "Control 2", "Target"]
        elif card == "CNOT":
            self.place_options = ["Control", "Target"]
        elif card == "SWAP":
            self.place_options = ["Target 1", "Target 2"]
        else:
            self.place_options = ["Target"]


        choices = [1, 2, 3]

        img = ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), "figures", "initial_circuit.png")))
        circuit_image = ttk.Label(self, image=img)
        circuit_image.image=img

        options = [ttk.Label(self, text=place_option) for place_option in self.place_options]
        places = [StringVar() for i in range(len(self.place_options))]
        radiobuttons = [[ttk.Radiobutton(self, text=choices[i], variable=place, value=choices[i]) for i in range(len(choices))] for place in self.place_options]        
        button_confirm = ttk.Button(self, text='Confirm', command=partial(controller.show_start_page, player))

        circuit_image.grid(columnspan=len(self.place_options), row=0)

        for i in range(len(options)):
            options[i].grid(column=i, row=circuit_image.grid_info()["row"]+1)

        for i in range(len(radiobuttons)):
            radiobutton = radiobuttons[i]
            for j in range(len(radiobutton)):
                radiobutton[j].grid(column=i, row=j+options[0].grid_info()["row"]+1)
        
        button_confirm.grid(columnspan=len(self.place_options), row=radiobuttons[0][2].grid_info()["row"]+1)
        
        
        for child in self.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

