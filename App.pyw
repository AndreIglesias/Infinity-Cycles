from tkinter import *
from Game import *
from Options import *
from DataHandling import *
import string

class App(Tk):

    username = ""
    password = ""

    def __init__(self):

        # Call to Tkinter.Tk as self
        Tk.__init__(self)

        # Window configuration
        self.geometry(WIDTH + "x" + HEIGHT)
        self.title("Infinity Cycles")
        self.resizable(width=False, height=False)
        #self.iconbitmap("./assets/favicon.ico")

        # Main Container
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Call to DataHandling
        # @params
        # filename = settings.json
        settings = DataHandling("settings.json")

        # If settings.json is empty, defaults values are saved
        if(not settings.load_data()):
            settings.save_data("sounds", ("value", 0))
            settings.save_data("difficulty", ("value", 1))

        self.frames = {}

        # Call to general Frames Classes with default values
        for F in (Login, Player, Settings, Ranking, Gameover, GameoverM):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the starting frame
        self.show_frame(Login)

    def show_frame(self, container):

        # Changes the frame at the front of the window
        if(container == Ranking):
            frame = Ranking(self.container, self)
            self.frames[Ranking] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[container]
        frame.tkraise()

    def endgame(self, score1):
        # Call to DataHandling
        # @params
        # filename = data.json
        data = DataHandling("data.json")

        # "Updates" user's score
        if(data.load_data()[self.username]["score"] < score1):
            data.save_data(self.username, ("password", self.password), ("score", score1))
        # "Updates" Gameover's widgets
        Gameover.update(score1, self)
        self.show_frame(Gameover)

    def endgameM(self, score1, score2, player):
        if(player == 1):
            Juego2 = Juego(self, True, score1, player + 1)
            Juego2.Jugar()
        else:
            self.deiconify()
            GameoverM.update(score2, score1, self)
            self.show_frame(GameoverM)

class Login(Frame):

    def __init__(self, parent, controller):

        # Call to Tkinter.Frame as self
        # @params
        # width = Options.WIDTH
        # height = Options.HEIGHT
        # bg = Options.BACKGROUND
        Frame.__init__(self, parent, width=WIDTH, height=HEIGHT, bg=BACKGROUND)

        # Call to DataHandling
        # @params
        # filename = data.json
        data = DataHandling("data.json")

        # Header
        header = Frame(self, width=WIDTH, bg=BACKGROUND)
        header.pack_propagate()
        header.pack()
        self.logo = PhotoImage(file ='assets/logo.png')
        Label(header, image = self.logo, bg=BACKGROUND).pack(pady=(100,0))

        # Form
        form = Frame(self, width=WIDTH, height=250, bg=BACKGROUND)
        form.pack()
        Label(form, text="Usuario:", font = FONT_TITLE, bg=BACKGROUND).pack(pady = 5)
        usernameWrapper = Frame(form, bg="#fff")
        txtusername = StringVar()
        txtusername.set("Usuario")
        self.username = Entry(usernameWrapper, textvariable = txtusername, width=30, bd=0, fg="#aaa", font=FONT_TEXT)
        self.username.bind("<FocusIn>", lambda event: checkUsername())
        self.username.bind("<FocusOut>", lambda event: checkUsername())
        self.username.pack(expand=True)
        usernameWrapper.pack(pady=10,ipady=10,ipadx=20)

        def checkUsername():
            text = self.username.get()
            if(text == "Usuario"):
                self.username.config(fg="#000")
                self.username.delete(0, "end")
            if(text == ""):
                self.username.config(textvariable=txtusername.set("Usuario"), fg="#aaa")

        Label(form, text="Contraseña:", font = FONT_TITLE, bg=BACKGROUND).pack(pady = 5)
        passwordWrapper = Frame(form, bg="#fff")
        txtpassword = StringVar()
        txtpassword.set("Password")
        self.password = Entry(passwordWrapper, textvariable = txtpassword, width=30, show="*", bd=0, fg="#aaa", font=FONT_TEXT)
        self.password.bind("<FocusIn>", lambda event: checkPassword())
        self.password.bind("<FocusOut>", lambda event: checkPassword())
        self.password.bind("<Return>", lambda event: signin(self.username.get(), self.password.get()))
        self.password.pack(expand=True)
        passwordWrapper.pack(pady=10,ipady=10,ipadx=20)

        def checkPassword():
            text = self.password.get()
            if(text == "Password"):
                self.password.config(fg="#000")
                self.password.delete(0, "end")
            if(text == ""):
                self.password.config(textvariable=txtpassword.set("Password"), fg="#aaa")

        # Footer
        footer = Frame(self, width=WIDTH, height=120, bg=BACKGROUND)
        footer.pack()
        login = Label(footer, text="Iniciar", fg="#fff", bg=GREEN, font=FONT_TITLE)
        login.bind("<Button-1>", lambda event: signin(self.username.get(), self.password.get()))
        login.pack(expand=True, ipady=10, ipadx=75, pady=(0,50))

        def signin(username, password):
            users = data.load_data()
            login.unbind("<Button-1>")
            try:
                if(username.isalnum() and (len(username) >= 5 and len(username) <=8)):
                    if(users[username]["password"] == password):
                        login.bind("<Button-1>", lambda event: signin(self.username.get(), self.password.get()))
                        controller.username = username
                        controller.password = password
                        controller.show_frame(Player)
                    else:
                        login.bind("<Button-1>", lambda event: signin(self.username.get(), self.password.get()))
                        self.message = Frame(self, width=300, height=300, bg="white")
                        self.message.place(x=490,y=160)
                        Label(self.message, text="Contraseña y/o Usuario \n incorrecto", fg="#000", bg="white", font=FONT_TITLE, width=25).place(x=50,y=100)
                        no = Label(self.message, text="Cerrar", fg="#000", bg=RED, font=FONT_TITLE, width=10, height=2)
                        no.bind("<Button-1>", lambda event: close())
                        no.place(x=100,y=200)
                        def close():
                            self.message.destroy()
                            login.bind("<Button-1>", lambda event: signin(self.username.get(), self.password.get()))
                else:
                    login.bind("<Button-1>", lambda event: signin(self.username.get(), self.password.get()))
                    self.message = Frame(self, width=300, height=300, bg="white")
                    self.message.place(x=490,y=160)
                    Label(self.message, text="Longitud de usuario debe \n estar entre 5 y 8 caracteres", fg="#000", bg="white", font=FONT_TITLE, width=25).place(x=50,y=100)
                    no = Label(self.message, text="Cerrar", fg="#000", bg=RED, font=FONT_TITLE, width=10, height=2)
                    no.bind("<Button-1>", lambda event: close())
                    no.place(x=100,y=200)
                    def close():
                        self.message.destroy()
                        login.bind("<Button-1>", lambda event: signin(self.username.get(), self.password.get()))
            except Exception as e:
                self.message = Frame(self, width=300, height=300, bg="white")
                self.message.place(x=490,y=160)
                Label(self.message, text="¿Desea crear el usuario: \n" + username + " ?", fg="#000", bg="white", font=FONT_TITLE, width=25).place(x=50,y=100)
                yes = Label(self.message, text="Si", fg="#000", bg=GREEN, font=FONT_TITLE, width=10, height=2)
                yes.bind("<Button-1>", lambda event: createUser())

                def createUser():
                    data.save_data(username, ("password", password), ("score", 0))
                    login.bind("<Button-1>", lambda event: signin(self.username.get(), self.password.get()))
                    controller.username = username
                    controller.password = password
                    controller.show_frame(Player)
                yes.place(x=60,y=200)
                no = Label(self.message, text="No", fg="#000", bg=GREEN, font=FONT_TITLE, width=10, height=2)
                no.bind("<Button-1>", lambda event: close())
                def close():
                    self.message.destroy()
                    login.bind("<Button-1>", lambda event: signin(self.username.get(), self.password.get()))
                no.place(x=160,y=200)

        header.pack(expand=True, fill=BOTH)
        form.pack(expand=True, fill=BOTH)
        footer.pack(expand=True, fill=BOTH)

class Player(Frame):

    def __init__(self, parent, controller):

        # Call to Tkinter.Frame as self
        # @params
        # width = Options.WIDTH
        # height = Options.HEIGHT
        # bg = Options.BACKGROUND
        Frame.__init__(self, parent, width=WIDTH, height=HEIGHT, bg=BACKGROUND)

        # Body
        body = Frame(self, width=WIDTH, height=720, bg=BACKGROUND)
        body.pack(expand=True, fill=BOTH)
        sologame = Label(body, text="1P", fg="#fff", bg=GREEN, font=FONT_TITLE, width=25, height=2)
        sologame.bind("<Button-1>", lambda event: play())
        sologame.place(x=540, y=150)

        # Call to Juego
        # @params
        # controller = controller
        def play():
            controller.withdraw()
            Juego1 = Juego(controller, False)
            Juego1.Jugar()

        multigame = Label(body, text="2P", fg="#fff", bg=GREEN, font=FONT_TITLE, width=25, height=2)
        multigame.bind("<Button-1>", lambda event: multplay())
        multigame.place(x=540, y=300)

        def multplay():
            controller.withdraw()
            Juego1 = Juego(controller, True)
            Juego1.Jugar()

        extra = Label(body, text="Extra", fg="#fff", bg=GREEN, font=FONT_TITLE, width=25, height=2)
        extra.bind("<Button-1>", lambda event: extraGame(controller))
        extra.place(x=540, y=450)

        def extraGame(controller):
            import Juego
            Juego.Play(controller)

        exit = Label(body, text="Salir", fg="#fff", bg=RED, font=FONT_TITLE, width=25, height=2)
        exit.bind("<Button-1>", lambda event: controller.show_frame(Login))
        exit.place(x=540, y=600)

        # Footer
        self.ranking = PhotoImage(file = "assets/ranking.png")
        ranking = Label(body, image = self.ranking, bg=BACKGROUND)
        ranking.place(x=100, y=550)
        ranking.bind("<Button-1>", lambda event: controller.show_frame(Ranking))
        self.settings = PhotoImage(file = "assets/settings.png")
        settings = Label(body, image = self.settings, bg=BACKGROUND)
        settings.place(x=1080,y=550)
        settings.bind("<Button-1>", lambda event: controller.show_frame(Settings))

class Settings(Frame):

    def __init__(self, parent, controller):

        # Call to Tkinter.Frame as self
        # @params
        # width = Options.WIDTH
        # height = Options.HEIGHT
        # bg = Options.BACKGROUND
        Frame.__init__(self, parent, width=WIDTH, height=HEIGHT, bg=BACKGROUND)

        # Call to DataHandling
        # @params
        # filename = settings.json
        settings = DataHandling("settings.json")

        # Sounds
        Label(self, text="Opciones", font=FONT_MAX, fg="#000",width=10, bg=BACKGROUND).place(x=560,y=100)
        Label(self, text="Sonidos", font=FONT_TITLE_BIG, fg="#000",width=10, bg=BACKGROUND).place(x=350,y=250)

        def displaySound():
            if(settings.load_data()["sounds"]["value"] == 1):
                self.switch = PhotoImage(file ='assets/on_switch.png')
            else:
                self.switch = PhotoImage(file ='assets/off_switch.png')
        displaySound()
        sounds = Label(self, image = self.switch, bg=BACKGROUND)
        sounds.bind("<Button-1>", lambda event: changeSound())
        sounds.place(x=785,y=237)

        def changeSound():
            if(settings.load_data()["sounds"]["value"] == 0):
                value = 1
            else:
                value = 0
            settings.save_data("sounds", ("value", value))
            displaySound()
            sounds.configure(image=self.switch)

        # Difficulty
        Label(self, text="Dificultad", font=FONT_TITLE_BIG, fg="#000",width=10, bg=BACKGROUND).place(x=350,y=400)
        def displayDifficulty():
            self.difficulty = []
            for i in range(0, settings.load_data()["difficulty"]["value"]):
                self.difficulty.append(PhotoImage(file ='assets/difficulty.png'))
            for i in range(settings.load_data()["difficulty"]["value"],4):
                self.difficulty.append(PhotoImage(file ='assets/no_difficulty.png'))
        displayDifficulty()
        x = 0
        images = []
        for i,image in enumerate(self.difficulty):
            images.append(Label(self, image = image, bg=BACKGROUND, name=str(i+1)))
            images[i].bind("<Button-1>", lambda event: changeDifficulty(event))
            images[i].place(x=700 + x,y=387)
            x += 75

        def changeDifficulty(event):
            ids = int(str(event.widget).split(".")[-1])
            value = ids
            settings.save_data("difficulty", ("value", value))
            displayDifficulty()
            for i,image in enumerate(self.difficulty):
                images[i].configure(image=image)

        # Footer
        self.ranking = PhotoImage(file = "assets/ranking.png")
        ranking = Label(self, image = self.ranking, bg=BACKGROUND)
        ranking.place(x=100, y=570)
        ranking.bind("<Button-1>", lambda event: controller.show_frame(Ranking))
        self.game = PhotoImage(file = "assets/game.png")
        game = Label(self, image = self.game, bg=BACKGROUND)
        game.place(x=1080, y=570)
        game.bind("<Button-1>", lambda event: controller.show_frame(Player))

class Ranking(Frame):

    def __init__(self, parent, controller):

        # Call to Tkinter.Frame as self
        # @params
        # width = Options.WIDTH
        # height = Options.HEIGHT
        # bg = Options.BACKGROUND
        Frame.__init__(self, parent, width=WIDTH, height=HEIGHT, bg=BACKGROUND)

        data = DataHandling("data.json").load_data()
        rankings = []
        for key in data.keys():
            if len(rankings) <= 10:
                rankings.append([key, data[key]["score"]])
            else:
                break

        def isInList(element, _list):
            for item in _list:
                if(element in item):
                    return True
            return False

        for key in data.keys():
            if(not(isInList(key, rankings))):
                for i,ranking in enumerate(rankings):
                    if(data[key]["score"] > ranking[1]):
                        rankings[i] = [key, data[key]["score"]]
                        break
        rankings = sorted(rankings, reverse=True, key=lambda ranking: ranking[1])[:10]
        row = Frame(self, width=500, height=60, bg="#fff", bd=1)
        row.place(x=390, y=50)
        Label(row, width=10, text="#", height=4, font=FONT_TEXT).place(x=0,y=0)
        Label(row, width=30, bg="#bbb", text="Nombre", height=2, font=FONT_TITLE).place(x=85,y=0)
        Label(row, width=25, bg="#ccc", text="Puntaje", height=2, font=FONT_TITLE).place(x=320,y=0)
        posY = 100
        for i, ranking in enumerate(rankings):
            row = Frame(self, width=500, height=60, bg="#fff", bd=1)
            row.place(x=390, y=posY)
            Label(row, width=10, text="#" + str(i+1), height=4, font=FONT_TEXT).place(x=0,y=0)
            Label(row, width=30, bg="#bbb", text=ranking[0], height=4, font=FONT_TEXT).place(x=85,y=0)
            Label(row, width=25, bg="#ccc", text=ranking[1], height=4, font=FONT_TEXT).place(x=320,y=0)
            posY += 50

        self.game = PhotoImage(file = "assets/game.png")
        game = Label(self, image = self.game, bg=BACKGROUND)
        game.place(x=100, y=570)
        game.bind("<Button-1>", lambda event: controller.show_frame(Player))

        self.settings = PhotoImage(file = "assets/settings.png")
        settings = Label(self, image = self.settings, bg=BACKGROUND)
        settings.place(x=1080, y=570)
        settings.bind("<Button-1>", lambda event: controller.show_frame(Settings))



class Gameover(Frame):

    def __init__(self, parent, controller):

        # Call to Tkinter.Frame as self
        # @params
        # width = Options.WIDTH
        # height = Options.HEIGHT
        # bg = Options.BACKGROUND
        Frame.__init__(self, parent, width=WIDTH, height=HEIGHT, bg=BACKGROUND)

        # Call to DataHandling
        # @params
        # filename = data.json
        data = DataHandling("data.json").load_data()

        self.logo = PhotoImage(file ='assets/logo.png')
        Label(self, image = self.logo, bg=BACKGROUND).place(x=503, y=100)
        Label(self, text="Fin del Juego", bg=BACKGROUND, font=FONT_MAX, fg="#000", width=15).place(x=510, y=350)
        Label(self, text="Puntaje: ", bg=BACKGROUND, font=FONT_TITLE_BIG, fg="#000", width=15).place(x=460, y=450)
        record = Label(self, text=0, bg=BACKGROUND, font=FONT_TITLE_BIG, fg="#000", width=15, name="score")
        record.place(x=640, y=450)
        tryagain = Label(self, text="Intentar otra vez", fg="#fff", bg=GREEN, font=FONT_TITLE, width=30, height=2)
        tryagain.place(x=390, y=550)
        tryagain.bind("<Button-1>", lambda event: play())

        # Call to Juego
        # @params
        # controller = controller
        def play():
            controller.withdraw()
            Juego1 = Juego(controller)
            Juego1.Jugar()

        back = Label(self, text="Regresar", fg="#fff", bg=RED, font=FONT_TITLE, width=30, height=2)
        back.place(x=650, y=550)
        back.bind("<Button-1>", lambda event: controller.show_frame(Player))

    def update(score, controller):
        controller.nametowidget("!frame.!gameover.score").configure(text=score)

class GameoverM(Frame):

    def __init__(self, parent, controller):

        # Call to Tkinter.Frame as self
        # @params
        # width = Options.WIDTH
        # height = Options.HEIGHT
        # bg = Options.BACKGROUND
        Frame.__init__(self, parent, width=WIDTH, height=HEIGHT, bg=BACKGROUND)

        # Call to DataHandling
        # @params
        # filename = data.json
        data = DataHandling("data.json").load_data()

        self.logo = PhotoImage(file ='assets/logo.png')
        Label(self, image = self.logo, bg=BACKGROUND).place(x=503, y=100)
        Label(self, text="Fin del Juego", bg=BACKGROUND, font=FONT_MAX, fg="#000", width=15).place(x=510, y=350)
        record = Label(self, text=0, bg=BACKGROUND, font=FONT_TITLE_BIG, fg="#000", width=20, name="score")
        record.place(x=500, y=450)

        back = Label(self, text="Regresar", fg="#fff", bg=RED, font=FONT_TITLE, width=30, height=2)
        back.place(x=520, y=550)
        back.bind("<Button-1>", lambda event: controller.show_frame(Player))

    def update(score1, score2, controller):
        print(score1)
        print(score2)
        if(score1 > score2):
            controller.nametowidget("!frame.!gameoverm.score").configure(text="Ha ganado el jugador 1")
        elif(score2 > score1):
            controller.nametowidget("!frame.!gameoverm.score").configure(text="Ha ganado el jugador 2")
        else:
            controller.nametowidget("!frame.!gameoverm.score").configure(text="Empate")


App = App()
App.mainloop()
