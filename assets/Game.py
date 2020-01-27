#Se importan todas las librerías de Tkinter.
from tkinter import *
import random
import time
from fractal import *
import winsound
from DataHandling import *

class Juego():

    def __init__(self, controller):
        #---------------------------------------------
        #***Configuraciones de la ventana y Tkinter***
        #---------------------------------------------

        #Se designa una variable self.master para inicializar la ventana principal del juego.
        self.master = Tk()

        #Se designa un widget de Canvas para el juego y otro para el HUD.
        self.master.geometry("1100x700")
        self.master.configure(bg="black")
        self.master.iconbitmap("assets/favicon.ico")
        self.w = Canvas(self.master, width=1100, height=650, bg="white", highlightbackground="black")
        self.hud = Canvas(self.master, width=1100, height=50, bg="#e8e8e8", highlightbackground="black")
        self.dibujar = Fractal(self.w)
        r = lambda: random.randint(0,300)
        self.dibujar.Fractal(None, r(), r(), '#c1c1c1', 1, 3)

        self.controller = controller
        self.settings = DataHandling("settings.json").load_data()

        #Título de la ventana.
        self.master.title("Juego")
        #Se restringe el tamaño de la ventana al especificado en el widget.
        self.master.resizable(width=0, height=0)

        '''
        La función verificarCoordenadas se usar para evitar que se creen elementos del juego sobre otros elementos ya creados.
        '''
        def verificarCoordenadas(rango):
            #Este bucle infinito se usa para establecer coordenadas que no estén ocupadas por otros objetivos.
            while(True):
                x1 = random.randint(100, 1000)
                y1 = random.randint(50, 400)
                disponible = self.w.find_overlapping(x1-rango, y1-rango, x1+rango, y1+rango)
                if(len(disponible) == 0):
                    return x1, y1
        '''
        La función generarObjetivos crea una lista en la que almacenará listas con las coordenadas, el color
        y los puntos de los objetivos, para asignar colores se hace uso de una tupla con los
        códigos hexadecimales y se utiliza un número aleatorio para seleccionar. Las coordenadas se
        generan con valores aleatorios en un rango específico y los puntajes se definen sumando 4
        al número aleatorio del color y multiplicando el resultado por el valor que tenga el multiplicador
        dependiendo de la dificultad establecida.
        Se retorna una matriz con todos los self.objetivos representados por una fila.
        '''
        def generarObjetivos(cantidad):
            objetivos = []
            colores = ("#f48c42", "#bbf441", "#41d0f4", "#f441dc")
            for i in range(0,cantidad):
                x1, y1 = verificarCoordenadas(15)
                valor = random.randint(0,100)
                if (valor >= 0 and valor < 50):
                    color = 0
                elif (valor >=50 and valor < 75):
                    color = 1
                elif (valor >= 75 and valor < 90):
                    color = 2
                elif (valor >= 90):
                    color = 3
                puntos = (color+4)*self.mult
                objetivos.append([self.w.create_oval(x1, y1, x1+30, y1+30,fill=colores[color], tags = 'target'),puntos])
            return objetivos

        '''
        La función generarObstaculos funciona de manera similar a generarObjetivos, con la diferencia que cada
        coordenada tiene un valor diferente para que varíe su forma, se verifica que los obstáculos no estén encima de otros
        obstáculos u objetivos.
        '''
        def generarObstaculos(cantidad):
            obstaculos = []
            for i in range(0,cantidad):
                while(True):
                    x1 = random.randint(100, 1000)
                    y1 = random.randint(50, 400)
                    xa = x1-random.randint(10, 50)
                    ya = y1-random.randint(10, 50)
                    xb = x1+random.randint(10, 50)
                    yb = y1+random.randint(10, 50)
                    disponible = self.w.find_overlapping(xa, ya, xb, yb)
                    if(len(disponible) == 0):
                        break
                obstaculos.append(self.w.create_rectangle(xa, ya, xb, yb, fill="black", tags = 'obstacle'))
            return obstaculos


        '''
        La función generarPowerUps genera los objetivos que suman tiempo y generará un power up aleatorio
        '''
        def generarPowerUps(cantidad):
            powerUps = []
            tipos = (("#f4e000", "#00bc4e", "timer"),()) #(Relleno, borde, tag)
            for i in range(0,cantidad):
                x1, y1 = verificarCoordenadas(30)
                powerUps.append(self.w.create_oval(x1, y1, x1+30, y1+30, fill=tipos[0][0], outline=tipos[0][1], width=3, tags=tipos[0][2]))
            return powerUps

        #Se crea un limitador de retrocesos, un multiplicador de puntos y la cantidad de obstáculos dependiendo de la dificultad del juego.
        self.dif = self.settings["difficulty"]["value"]
        if(self.dif == 1):
            self.retrocesosMax = 5
            self.cantidadObstaculos = 5
            self.mult = 11
            self.cantidadPowerUps = 8
        elif(self.dif == 2):
            self.retrocesosMax = 3
            self.cantidadObstaculos = 8
            self.mult = 13
            self.cantidadPowerUps = 4
        elif(self.dif == 3):
            self.retrocesosMax = 1
            self.cantidadObstaculos = 12
            self.mult = 15
            self.cantidadPowerUps = 2
        else:
            self.retrocesosMax = 0
            self.cantidadObstaculos = 14
            self.mult = 18
            self.cantidadPowerUps = 0

        #Se define la cantidad de objetivos a generar.
        self.cantidadObjetivos = 6
        #Se crean los objetivos usando la cantidad especificada anteriormente.
        self.objetivos = generarObjetivos(self.cantidadObjetivos)
        #Se generan los obstáculos del juego.
        self.obstaculos = generarObstaculos(self.cantidadObstaculos)
        #Se generan los power ups.
        self.powerUps = generarPowerUps(self.cantidadPowerUps)
        #Se asigna el tiempo que tendrá el jugador para alcanzar todos los objetivos.
        self.tiempo = 20
        self.tipoT = 0

        #Se define el .puntaje máximo para terminar el juego al alcanzarlo.
        self.puntajeMax = 0
        for valor in self.objetivos:
            self.puntajeMax += valor[1]

        self.w.pack()
        self.hud.pack()


        #Se define el puntaje con valor inicial de cero y el contador del turno.
        self.puntaje = 0
        self.movimiento = 0
        #Se muestran tanto el puntaje como el número del movimiento y el temporizador en el HUD.
        self.marcadorP = self.hud.create_text(30, 22, text="Puntaje: 000"+str(self.puntaje), anchor="w", font=("", "12", "bold"))
        self.hud.create_line(161, 0 , 161, 50 , width=3)

        self.hud.create_line(922, 0 , 922, 50 , width=3)
        self.marcadorM = self.hud.create_text(951, 22, text="Movimiento #00"+str(self.movimiento+1), anchor="w", font=("", "12", "bold"))

        self.timer = self.hud.create_text((406, 22), text="Texto", font=("", "12", "bold"), fill="#0048b5")
        self.hud.create_line(451, 0 , 451, 50 , width=3)

        #Rango máximo y mínimo para generar un fractal nuevo.
        self.minimo=25
        self.maximo=40

        self.retrocesos = 0
        #Se muestra la cantidad de retrocesos en el HUD.
        self.marcadorR = self.hud.create_text(195, 22, text="Retrocesos: "+str(self.retrocesos)+"/"+str(self.retrocesosMax), anchor="w", font=("", "12", "bold"))
        self.hud.create_line(350, 0 , 350, 50 , width=3)

        #Se definen los puntos de inicio de la hitbox.
        self.xInicial, self.yInicial = 550, 610
        #Se crea una lista que almacenará las acciones realizadas en cada turno.
        self.circulos = [[self.w.create_line(550, 650, 550, 610), self.xInicial, self.yInicial, self.w.create_oval(self.xInicial-2, self.yInicial-2, self.xInicial+2, self.yInicial+2, fill="black"), self.movimiento, []]]
        #Se reproduce la música de fondo.
        if(self.settings["sounds"]["value"] == 1):
            winsound.PlaySound("assets/sound.wav", winsound.SND_ASYNC)

    #-------------------------
    #***Funciones del juego***
    #-------------------------

    '''
    La función timer crea la cuenta atrás que determina el tiempo que el jugador tiene para agarrar el mayor número
    de objetivos posible.
    '''
    def detener(self):
        self.w.unbind("<Motion>")
        self.w.unbind("<Button-1>")
        self.w.unbind("<Button-3>")
        self.hud.itemconfig(self.timer,fill="#dd0000")
        self.tiempo = 0
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.controller.deiconify()
        self.controller.endgame(self.puntaje)
        self.master.destroy()

    '''
    Las dos fuciones siguientes trabajan en conjunto para operar el timer y mostrarlo, así
    como cambia los colores dependiendo del tiempo restante.
    La función mostrar tiempo se utiliza al tocar los objetivos para incrementar tiempo
    y por eso tiene un if interno que altera lo que se mostrará en el timer.
    '''
    def mostrarTiempo(self):
        #divmod realiza la división y el módulo entre los dos valores dados, mins equivale a / y secs a %
        mins, secs = divmod(self.tiempo, 60)
        #se le da formato, el 2 significa la cantidad de dígitos que hay a cada lado de los : y la "d" decimal integer
        #.format() le da el formato específicado a los valores dados.
        timeformat = "{:02d}:{:02d}".format(mins, secs)

        if(self.tipoT >= 1 and self.tipoT <=2):
            extra = "+5"
            self.tipoT += 1
        else:
            extra = ""
            self.tipoT = 0
        self.hud.itemconfig(self.timer,text=timeformat+extra)

    def countdown(self):
        self.mostrarTiempo()
        if(self.tiempo>0):
            #Esta serie de condicionales cambia el color del temporizador dependiendo del tiempo restante.
            if (self.tiempo > 30):
                self.hud.itemconfig(self.timer,fill="#0048b5")
            elif (self.tiempo >= 20):
                self.hud.itemconfig(self.timer,fill="#05a000")
            elif (self.tiempo >= 10):
                self.hud.itemconfig(self.timer,fill="#efbb00")
            elif (self.tiempo >= 5):
                self.hud.itemconfig(self.timer,fill="#dd0000")

            #after() manda a llamar a la función indicada después de que pase el tiempo indicado (en milisegundos).
            self.tiempo -= 1
            self.master.after(1000,self.countdown)
        else:
            self.detener()


    '''
    La función mostrarMovimiento imprime los movimientos asignando un formato adecuado al número de movimientos actuales.
    '''
    def mostrarMovimiento(self):
        if (self.movimiento < 9):
            self.hud.itemconfig(self.marcadorM, text="Movimiento #00"+str(self.movimiento+1))
        elif (self.movimiento < 99):
            self.hud.itemconfig(self.marcadorM, text="Movimiento #0"+str(self.movimiento+1))
        else:
            self.hud.itemconfig(self.marcadorM, text="Movimiento #"+str(self.movimiento+1))


    '''
    La función vista previa crea una simulación del siguiente movimiento.
    '''
    def vistaPrevia(self, event):
        x = event.x
        y = event.y
        self.xInicial
        self.yInicial
        a = self.xInicial-x
        b = self.yInicial-y
        c = ((a**2)+(b**2))**(1/2)
        if(c >= self.minimo and c <= self.maximo):
            try:
                self.w.delete(self.previo)
                self.w.delete(self.puntoP)
                self.previo = self.w.create_oval(self.xInicial-c, self.yInicial+c, self.xInicial+c, self.yInicial-c, fill="#d8d8d8", outline="#878787")
                self.puntoP = self.w.create_oval(x-2, y-2, x+2, y+2, fill="#878787", outline="#878787")
            except AttributeError:
                self.previo = self.w.create_oval(self.xInicial-c, self.yInicial+c, self.xInicial+c, self.yInicial-c, fill="#d8d8d8", outline="#878787")
                self.puntoP = self.w.create_oval(x-2, y-2, x+2, y+2, fill="#878787", outline="#878787")
        else:
            try:
                self.w.delete(self.previo)
                self.w.delete(self.puntoP)
            except AttributeError:
                pass

    '''
    La función crear obtiene los valores de "x" y "y" al dar click y valida que el puntero no se encuentre
    muy lejos ni muy cerca del punto de inicio para realizar el movimiento. La función también verifica
    si la hitbox está tocando algún objetivo o al fractal para decidir si sumar puntos, terminar la ejecución
    o simplemente no hacer nada.
    '''
    def crear(self, event):
        x = event.x
        y = event.y
        self.xInicial
        self.yInicial
        a = self.xInicial-x
        b = self.yInicial-y
        c = ((a**2)+(b**2))**(1/2)

        if(c >= self.minimo and c <= self.maximo):
            self.movimiento
            self.retrocesos
            self.retrocesosMax
            try:
                self.w.delete(self.previo)
                self.w.delete(self.puntoP)
            except AttributeError:
                pass
            #Se cambia el color del fractal anterior para diferenciar del fractal actual.
            self.w.itemconfig(self.circulos[self.movimiento][0], fill='#545454')
            #Se sombrean los círculos a los cuales ya no se puede retroceder.
            if(len(self.circulos) > self.retrocesosMax):
                self.w.itemconfig(self.circulos[self.movimiento-self.retrocesosMax][0], fill='black')
            #Se crea un nuevo fractal desde el centro del anterior.
            self.oval = self.w.create_oval(self.xInicial-c, self.yInicial+c, self.xInicial+c, self.yInicial-c, fill="#999999")
            self.fractalOval = self.dibujar.Fractal(c-4, self.xInicial, self.yInicial, None, None, 1, 'fractal')
            #Se cambian los puntos de inicio.
            self.xInicial = x
            self.yInicial = y
            #Se crea una nueva hitbox.
            self.punto = self.w.create_oval(self.xInicial-2, self.yInicial-2, self.xInicial+2, self.yInicial+2, fill="black")
            #Se define una variable que almacenará una tupla con los elementos que estén tocando la posición
            #actual de la hitbox.
            colision = self.w.find_overlapping(self.xInicial-2, self.yInicial-2, self.xInicial+2, self.yInicial+2) ######################################################

            lista = []
            for i in colision:
                if self.w.gettags(i) != ():
                    #print(i, self.w.gettags(i))
                    if self.w.gettags(i)[0] == 'target' or self.w.gettags(i)[0] == 'timer':
                        index = colision.index(i)
                    lista.append(self.w.gettags(i)[0])
            if lista.count('target') >= 1:
                #print(colision)

                for i in self.objetivos:
                    if i[0] == colision[index]:
                        self.puntaje += i[1]

                if(self.puntaje < 100):
                    self.hud.itemconfig(self.marcadorP, text="Puntaje: 00"+str(self.puntaje))
                elif(self.puntaje < 1000):
                    self.hud.itemconfig(self.marcadorP, text="Puntaje: 0"+str(self.puntaje))
                else:
                    self.hud.itemconfig(self.marcadorP, text="Puntaje: "+str(self.puntaje))

                if(self.puntaje >= self.puntajeMax):
                    print("Felicidades! Has ganado!")
                    self.detener()
                for i in self.objetivos:
                    if i[0] == colision[index]:
                        self.w.delete(i[0])
                        i = []

            if lista.count('timer') >= 1:
                self.tiempo += 5
                self.tipoT = 1
                self.mostrarTiempo()
                for i in self.powerUps:
                    if i == colision[index]:
                        self.w.delete(i)
                #winsound.PlaySound("timerUp.wav", winsound.SND_ASYNC)

            if lista.count('fractal') >= 1 or lista.count('obstacle') >= 1:
                    print("Ups! has chocado!")
                    self.detener()

            self.movimiento += 1
            self.mostrarMovimiento()
            self.circulos.append([self.oval, self.xInicial, self.yInicial, self.punto, self.movimiento, self.fractalOval])
            #Si la cantidad de retrocesos es menor a la cantidad máxima entonces se agrega un retroceso al contador.
            if(self.retrocesos < self.retrocesosMax):
                self.retrocesos += 1
                self.hud.itemconfig(self.marcadorR, text="Retrocesos: "+str(self.retrocesos)+"/"+str(self.retrocesosMax))
            #Si la tupla de colisión posee más de 2 valores significa que en esa posición existe un elemento
            #adicional a la hitboxr y el fractal.
            self.puntaje


    '''
    Esta función borra los elementos del turno actual y ubica el puntero en los puntos iniciales anteriores.
    Tabién se resta 1 al contador de retrocesos, solo se puede retroceder si se tienen más de cero retrocesos.
    '''
    def regresar(self, event):
        self.movimiento
        self.retrocesos
        if(self.retrocesos > 0):
            self.w.delete(self.circulos[self.movimiento][0])
            self.w.delete(self.circulos[self.movimiento][3])
            for i in self.circulos[self.movimiento][5]:
                self.w.delete(i)
            self.circulos.pop(self.movimiento)
            self.xInicial
            self.yInicial
            self.movimiento -= 1
            self.xInicial = self.circulos[self.movimiento][1]
            self.yInicial = self.circulos[self.movimiento][2]
            if(self.movimiento != 0):
                self.w.itemconfig(self.circulos[self.movimiento][0], fill='#999999')
            self.retrocesos -= 1
            try:
                self.w.delete(self.previo)
                self.w.delete(self.puntoP)
            except AttributeError:
                pass
        else:
            def reestablecerColor():
                 self.hud.itemconfig(self.marcadorR, fill="black")

            self.hud.itemconfig(self.marcadorR, fill="red")
            self.master.after(200, reestablecerColor)

        self.mostrarMovimiento()
        self.hud.itemconfig(self.marcadorR, text="Retrocesos: "+str(self.retrocesos)+"/"+str(self.retrocesosMax))


    '''
    La función Jugar es la que maneja rodo lo que está pasando en pantalla haciendo uso de eventos por medio de bindings.
    '''
    def Jugar(self):
        #Se manda a llamar la función que crea la cuenta regresiva.
        self.countdown()
        #Se crea una vista previa del siguiente self.movimiento.
        self.w.bind("<Motion>", self.vistaPrevia)
        #Al recibir el evento click izquierdo se realiza la función retornar.
        self.w.bind("<Button-1>", self.crear)
        #Al recibir el evento click derecho se regresará un movimiento atrás.
        self.w.bind("<Button-3>", self.regresar)
        #se asigna la cantidad de tiempo en segundos que tendrá el jugador.

        self.w.pack()



        #Se retorna al main loop
        self.master.mainloop()
if __name__ == '__main__':
    juego = Juego()
    juego.Jugar()
