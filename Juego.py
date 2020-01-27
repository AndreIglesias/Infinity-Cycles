# ============================================================================================
# PROGRAMA   : Juego.py
# AUTOR      : QEDD
# COPYRIGHT  : ESTE PROGRAMA NO PUEDE SER MODIFICADO SIN LA AUTORIZACION ESCRITA DEL AUTOR
# FECHA      : 29/06/2017
# DESCRIPCION: Juego con una serpiente de fractales
# ============================================================================================

from tkinter import *
import random
from fractal import *

class Chocador(object):
	"""
	docstring for Chocador
	Objeto con el cual la serpiente puede chocar,
	a parte de su propio cuerpo.
	Obstaculo o punto
	"""
	def __init__(self, canvas, x, y, r, color, tag):
		'''
		:param canvas:
		:param x: coordenada en x de la figura
		:param y: coordenada en y de la figura
		:param r: Longitud del lado de al figura
		:param color: color de la figura
		:param tag: tag de la figura
		'''
		super(Chocador, self).__init__()
		self.canvas = canvas
		self.x = x
		self.y = y
		self.r = r
		self.color = color
		self.ID = self.canvas.create_rectangle(self.x, self.y, self.x+self.r, self.y+self.r, fill = self.color, tags = tag)

class Gusano(object):
	"""
	docstring for Gusano
	Cabeza y cuerpo del gusano
	con sus metodos y atributos
	"""
	def __init__(self, canvas, tk, cantidad):
		'''
		:param canvas: canvas del juego
		:param tk: ventana del juego
		:param cantidad: cantidad de objetivos que hay
		'''
		super(Gusano, self).__init__()
		self.canvas = canvas
		self.tk = tk
		self.cantidad = cantidad # Cantidad de objetivos que hay
		self.cabeza = self.canvas.create_oval(int(canvas['width'])/2-20, int(canvas['height'])-40,int(canvas['width'])/2+20,int(canvas['height']), fill = 'spring green', tags = 'Gusano')
		x, y, a, b = self.canvas.coords(self.cabeza) # Coordenadas de la cabeza
		self.dibujar = Fractal(self.canvas)
		self.radio = 18
		self.fractalOval = self.dibujar.Fractal(self.radio, (x+a)/2, (y+b)/2, None, None, 1, 'fractal') # Fractal del cuerpo de la serpiente
		self.MOVIMIENTOS = [] # Direcciones de los movimientos hechos
		self.marcador = 0
		self.segundaCabeza = self.cabeza # Almacena la cabeza de la serpiente temporalente
		self.retrocesos = [] # Administra los retrocesos de la serpiente
		self.eliminado = [] # Objetivos eliminados 
		label = Label(self.canvas, text = 'Score: '+str(self.marcador), font = ('Arial', 15), bg = 'gray10', fg = 'white')
		label.place(x = 2, y = 2) # Puntaje
		self.fractalOval.append(self.cabeza)
		self.retrocesos.insert(0, self.fractalOval)
		self.RETROCEDIDO = False # Bandera para saber si se ha retrocedido
		self.STOP = False # Verifica si hay que detener el juego
		self.MAutomatico = False # Verifica si esta en modo automatico

	def borrarObjetivo(self, x, y, a, b): # Reacciona al choque de la serpiente con algo
		'''
		:param x: coordenada en x de la esquina superior izquierda de la serpiente
		:param y: coordenada en y de la esquina superior izquierda de la serpiente
		:param a: coordenada en x de la esquina inferior derecha de la serpiente
		:param b: coordenada en y de la esquina inferior derecha de la serpiente
		'''
		ides = self.canvas.find_overlapping(x, y, a, b) # Objetos que se superponen en las coordenadas pasadas como argumentos
		tags = [] # lista con los tags de los objetos de la tupla "ides"
		if len(ides) > 1:
			for i in ides:
				tagTuple = self.canvas.gettags(i)
				tags.append(tagTuple)
				try:
					if tagTuple[0] == 'Objetivo': # Eliminar los objetivos superpuestos a la serpiente
						self.eliminado.append(i)
						self.canvas.delete(i)
						self.marcador += 1
						label = Label(self.canvas, text = 'Score: '+str(self.marcador), font = ('Arial', 15), bg = 'gray10', fg = 'white')
						label.place(x = 2, y = 2)
						break
					elif (tagTuple[0] == 'Obstaculo') or (tags.count(('Cabeza', 'Gusano')) >= 2): # Verifica si la serpiente choco consigo misma o con un obstaculo
						self.Detener()
						if (tagTuple[0] != 'Obstaculo'):
							UltBurb = 'red'
						else:
							UltBurb = 'blue'
						for i in range(2):
							self.canvas.itemconfig(self.cabeza-i, fill = UltBurb)
						label = Label(self.canvas, text = 'Game Over', font = ('Arial', 15), bg = 'gray10', fg = 'white')
						label.place(x = int(canvas['width'])/2-50, y = int(canvas['height'])/2-20)
				except IndexError: pass

	def Condicional(self, x, y, a, b, sensibilidad, distancia, DIRECCION):
		'''
		:param x: coordenada en x de la esquina superior izquierda de la serpiente
		:param y: coordenada en y de la esquina superior izquierda de la serpiente
		:param a: coordenada en x de la esquina inferior derecha de la serpiente
		:param b: coordenada en y de la esquina inferior derecha de la serpiente
		:param sensibilidad: Area en la que se analiza
		:param distancia: Distancia en la que se analiza la presencia de algun objeto
		:param DIRECCION: Direccion de la serpiente
		'''
		try:
			serpiente = set(self.Analizando(x, y, a, b, sensibilidad, distancia, 'Gusano', True)) # if then serpiente = otra cosa
		except TypeError: serpiente = 'Comenzando el Juego'
		condicional = True
		if 'Arriba' in serpiente:
			condicional = DIRECCION != -2
		if 'Abajo' in serpiente:
			condicional = condicional and DIRECCION != 2
		if 'Derecha' in serpiente:
			condicional = condicional and DIRECCION != 1
		if 'Izquierda' in serpiente:
			condicional = condicional and DIRECCION != -1
		return condicional

	def eventos(self, grosor, altura, DIRECCION, sensibilidad = 1, distancia = 25): # Direccion: 1 Derecha, -1 Izquierda, -2 Arriba, 2 Abajo
		'''
		:param grosor: distancia en x a moverse (la serpiente)
		:param altura: distancia en y a moverse
		:param DIRECCION: direccion a moverse
		:param sensibilidad: Area en la que se analiza
		:param distancia: Distancia en la que se analiza la presencia de algun objeto
		'''
		try:
			if self.RETROCEDIDO: # Al terminar de retroceder cualquier cantidad de veces se vuelve a inicializar los retrocesos
				self.retrocesos = []
				#self.fractalOval.append(self.cabeza)
				#self.retrocesos.insert(0, self.fractalOval)
				self.RETROCEDIDO = False

			x, y, a, b = self.canvas.coords(self.cabeza)
			self.canvas.addtag_withtag('Gusano', self.cabeza) # Para diferenciar el cuerpo de la serpiente de la cabeza, se le anade otro tag
			self.segundaCabeza = self.cabeza
			condicional = True
			if self.MAutomatico:
				condicional = self.Condicional(x, y, a, b, sensibilidad, distancia, DIRECCION)
				print('Modo Automatico')

			if  ((self.MOVIMIENTOS == []) or not (-1*DIRECCION == self.MOVIMIENTOS[-1])) and (not self.STOP) and (condicional): # Se verifica si los movimientos no son opuestos o es el primer movimiento

				self.MOVIMIENTOS.append(DIRECCION) # las primeras cuatro condiciones se cumplen si la serpiente se sale de la pantalla, por lo que aparece al otro lado
				if a < -10: # la serpiente salio por la izquierda
					self.cabeza = self.canvas.create_oval(int(canvas['width'])-40, y+altura, int(canvas['width']), b+altura, fill = 'spring green', tags = 'Cabeza')
				elif a > int(canvas['width']) + 10: # la serpiente salio por la derecha
					self.cabeza = self.canvas.create_oval(0, y+altura, 40, b+altura, fill = 'spring green', tags = 'Cabeza')
				elif b < -10: # la serpiente salio por arriba
					self.cabeza = self.canvas.create_oval(x+grosor, int(canvas['height'])-40, a+grosor, int(canvas['height']), fill = 'spring green', tags = 'Cabeza')
				elif b > int(canvas['height']) + 10: # la serpiente salio por abajo
					self.cabeza = self.canvas.create_oval(x+grosor, 0, a+grosor, 40, fill = 'spring green', tags = 'Cabeza')
				else: # la serpiente no salio del canvas
					self.cabeza = self.canvas.create_oval(x+grosor, y+altura, a+grosor, b+altura, fill = 'spring green', tags = 'Cabeza')

				self.fractalOval = self.dibujar.Fractal(self.radio, (x+a)/2, (y+b)/2, None, None, 1, 'fractal') # Genera el fractal en la serpiente
				self.fractalOval.append(self.cabeza)
				self.retrocesos.insert(0, self.fractalOval)
				self.borrarObjetivo(x, y, a, b)
				self.canvas.after(2)
			else:
				if not self.STOP and condicional: # Se verifica que no haya terminado el juego
					if abs(DIRECCION) == 1:
						self.eventos(0,-45, -2) # Si se quiere ir hacia una direccion contraria a la anterior horizontalmente, la serpiente va hacia arriba
					else:
						self.eventos(45, 0, 1) # Si pasa lo mismo pero en verticalmente, la serpiente va hacia la derecha
					if self.MAutomatico:	
						if abs(DIRECCION) == 1:
							self.eventos(0, 45, 2)
						else:
							self.eventos(-45, 0, -1)
		except ValueError: pass

	def enclosedWithTag(self, x, y, a, b, tag): # Busca un objeto con un tag en especifico inscrito en un area dada
		'''
		:param x: coordenada en x de la esquina superior izquierda del area a analizar
		:param y: coordenada en y de la esquina superior izquierda del area a analizar
		:param a: coordenada en x de la esquina inferior derecha del area a analizar
		:param b: coordenada en y de la esquina inferior derecha del area a analizar
		:param tag: tag buscado
		'''
		enclosed = self.canvas.find_enclosed(x, y, a, b) # verifica todos los que esten inscritos en un rectangulo con las dimensiones de los argumentos 
		for i in enclosed:
			if tag in set(self.canvas.gettags(i)): # Si entre los objetos inscritos existe aquel con el tag buscado, la funcion devuelve True
				return True
		return False

	def findOverTag(self, x, y, a, b, tag): # La misma mecanica que con la funcion "enclosedWithTag"
		overtag = self.canvas.find_overlapping(x, y, a, b)
		for i in overtag:
			if tag in set(self.canvas.gettags(i)):
				return True
		return False

	def Analizando(self, x, y, a, b, sensibilidad, distancia, tag, enLista = False, lista = []):
		'''
		:param x: coordenada en x de la esquina superior izquierda del area a analizar
		:param y: coordenada en y de la esquina superior izquierda del area a analizar
		:param a: coordenada en x de la esquina inferior derecha del area a analizar
		:param b: coordenada en y de la esquina inferior derecha del area a analizar
		:param sensibilidad: Area en la que se analiza
		:param distancia: Distancia en la que se analiza la presencia de algun objeto
		:param tag: tag buscado
		:param enLista: Verifica si hay que devolver el resultado en una lista
		:param lista: acumula en la lista las direcciones
		'''
		lista = []
		if self.enclosedWithTag(x-sensibilidad, y-sensibilidad, a+sensibilidad, b+sensibilidad, tag):
			y -= distancia
			b -= distancia
			if self.findOverTag(x, y-sensibilidad, a, y, tag):
				#self.canvas.create_rectangle(x, y-sensibilidad, a, y, outline = 'red')
				if not enLista: return 'Arriba'
				else: lista.append('Arriba')
			y += distancia
			b += distancia
			x += distancia
			a += distancia
			if self.findOverTag(a, y, a+sensibilidad, b, tag):
				#self.canvas.create_rectangle(a, y, a+sensibilidad, b, outline = 'red')
				if not enLista: return 'Derecha'
				else: lista.append('Derecha')
			x -= 2*(distancia)
			a -= 2*(distancia)
			if self.findOverTag(x-sensibilidad, y, x, b, tag):
				#self.canvas.create_rectangle(x-sensibilidad, y, x, b, outline = 'red')
				if not enLista: return 'Izquierda'
				else: lista.append('Izquierda')
			y += distancia
			b += distancia
			if self.findOverTag(x, b, a, b+sensibilidad, tag):
				#self.canvas.create_rectangle(x, b, a, b-sensibilidad, outline = 'red')
				if not enLista: return 'Abajo'
				else: lista.append('Abajo')
			return lista



	def Boverlapping(self, sensibilidad = 85, distancia = 25):
		'''
		:param sensibilidad: Area en la que se analiza
		:param distancia: Distancia en la que se analiza la presencia de algun objeto
		:return: direccion en donde esta el obstaculo
		'''
		global controller
		x, y, a, b = self.canvas.coords(self.cabeza)
		self.borrarObjetivo(x, y, a, b)
		if self.marcador == self.cantidad:
			label = Label(self.canvas, text = 'YOU WIN ', font = ('Arial', 15), bg = 'gray10', fg = 'white')
			label.place(x = int(canvas['width'])/2-50, y = int(canvas['height'])/2-20)
			self.Detener()
		return self.Analizando(x, y, a, b, sensibilidad, distancia, 'Obstaculo') #, self.Analizando(x, y, a, b, sensibilidad, distancia, 'Gusano'))

	def Delante(self, event = None): # Flecha arriba
		self.eventos(0,-45, -2)
		self.Boverlapping()
		self.MAutomatico = False # Al utilizar una tecla, el modo automatico se pierde

	def Abajo(self, event = None): # Flecha abajo
		self.eventos(0, 45, 2)
		self.Boverlapping()
		self.MAutomatico = False

	def Izquierda(self, event = None): # Flecha izquierda
		self.eventos(-45, 0, -1)
		self.Boverlapping()
		self.MAutomatico = False

	def Derecha(self, event = None): # Flecha derecha
		self.eventos(45, 0, 1)
		self.Boverlapping()
		self.MAutomatico = False

	def Detener(self): # Se detiene el juego
		self.tk.unbind('<Up>')
		self.tk.unbind('<Left>')
		self.tk.unbind('<Right>')
		self.tk.unbind('<Down>')
		self.tk.unbind('<Return>')
		self.tk.unbind('<Delete>')
		self.STOP = True

def obj(cantObj, cantObs, lado = None):
	'''
	:param cantObj: cantidad de objetivos
	:param cantObs: cantidad de obstaculos
	:param lado: largo del lado del objeto
	'''
	def GenerarFigura(lado, cantidad, tag, color = None):
		if lado == None:
			lado = lambda: random.randint(38, 38) # Coordenadas random modificables para el lado de las figuras
		else:
			lado = lambda: lado
		x = lambda: random.randint(150, int(canvas['width'])-150) # coordenadas random dentro del canvas
		y = lambda: random.randint(150, int(canvas['height'])-150) # coordenadas random dentro del canvas
		arreglo = list(range(cantidad)) # Controla las iteraciones del bucle
		centinela = False
		if color is None:
			centinela = True
			lado = lambda: random.randint(40, 60)
			ro = lambda: random.randint(50, 255)
		for i in arreglo:
			if centinela: color = '#%02X%02X%02X' % (ro(),ro(),ro()) # Color al azar para los objetivos
			X = x()
			Y = y()
			R = lado()
			if (len(canvas.find_overlapping(X, Y, X+R, Y+R)) == 0)and (X%40 == 0) and (Y%40 == 0):
				c = Chocador(canvas, X, Y, R, color, tag)
				if centinela:
					objetivos.append(c.ID)
			else:
				arreglo.append(1) # Coloca un elemento mas a recorrer en el bucle
		print('longitud',len(arreglo))

	GenerarFigura(lado, cantObj, 'Objetivo') # Se crean los objetivos con el tag "Objetivo"
	GenerarFigura(lado, cantObs, 'Obstaculo', 'black') # Se crean los obstaculos con el tag "Obstaculo"

def MinDicciones(diccionario): # En un diccionario de tuplas, encuentra la tupla con menor numero en la posicion 1
	'''
	:param diccionario: Diccionario de tuplas
	:return: elementos de la tupla con segundo elemento mayor
	'''
	minx = {}
	miny = {}
	my, mx = None, None
	for key in diccionario: # Encuentra el mayor numero en la posicion 1 de las tuplas del diccionario
		miny[key] = diccionario[key][1]
		if my == None: my = miny[key]
		if my < miny[key]: my = miny[key]

	for key in diccionario: # Encuentra la pareja faltante de la tupla
		if diccionario[key][1] == my:
			mx = diccionario[key][0]
			break
	return mx, my # retorna los elementos de la tupla

def movimiento(a,b, m, atributo):
	'''
	:param a: cantidad en x a moverse
	:param b: cantidad en y a moverse
	:param m: posicion a moverse (puede ser en y o x)
	:param atributo: atributo del canvas
	:return: centinela
	'''
	def Condicion(a, b, coord, sensibilidad): # se verifica la relacion entre la distancia objetivo y la actual
		'''
		:param a: cantidad en x a moverse
		:param b: cantidad en y a moverse
		:param coord: coordenada del objeto
		:param sensibilidad: distancia permisible en el que analiza la condicion
		:return: si se cumple la condicion (True o False)
		'''
		centinela = 0
		if (a > 0) or (b > 0): 
			condicion = m > coord + sensibilidad # segun el rango de sensibilidad determina la cercania permisible
		elif (a <= 0) or (b <= 0):
			condicion = m < coord - sensibilidad
		return condicion

	if b is 0: index = 0 # Se busca alcanzar la coordenada en 'x' o en 'y'
	else: index = 1

	coord = canvas.coords(Gusano.cabeza)[index]
	i = 0
	centinela = False
	if a is not 0:
		signo = abs(a)/a
	else:
		signo = abs(b)/b
	sensibilidad = 45
	condicion = Condicion(a, b, coord, sensibilidad)

	while (condicion) and (coord > 0) and (coord < int(canvas[atributo])) and (i < 15):
		i += 1
		try:
			obsta = Gusano.Boverlapping()
			if obsta == 'Arriba': # Mandar derecha
				Gusano.eventos(45, 0, 1)
				#print('Arriba-------------------------------')
				continue
			elif obsta == 'Derecha': # Mandar arriba
				Gusano.eventos(0,-45, -2)
				#print('Derecha-------------------------------')
				continue
			elif obsta == 'Izquierda': # Mandar arriba
				Gusano.eventos(0,-45, -2)
				#print('Izquierda-------------------------------')
				continue
			elif obsta == 'Abajo': #  Mandar arriba
				Gusano.eventos(45, 0, 1)
				#print('Abajo-------------------------------')
				continue
		except ValueError: pass

		condicion = Condicion(a, b, coord, sensibilidad)
		Gusano.eventos(a, b, (index + 1)*signo) # Mueve el gusano para una direccion
		coord = canvas.coords(Gusano.cabeza)[index]
		centinela = True
	return centinela


def amoverY(my): # controla los movimientos verticales
	centinela = movimiento(0, -45, my, 'height')
	if not centinela:
		centinela = movimiento(0, 45, my, 'height')

def amoverX(mx, my): # controla los movimientos horizontales
	for i in range(5):
		centinela = movimiento(-45, 0, mx, 'width')
		if not centinela:
			movimiento(45, 0, mx, 'width')
		amoverY(my)

	# IR AL PUNTO MAS BAJO

def automatico(event = None): # comienza el proceso de busqueda automatica de las burbujas
	global objetivos
	Gusano.MAutomatico = True # Enciende el modo automatico
	coordenadas = {}
	try:
		print(Gusano.eliminado)
		for i in Gusano.eliminado: # busca los objetivos y los elimina de la lista "eliminado" de Gusano
			print(i)
			objetivos.pop(objetivos.index(i))
			Gusano.eliminado.pop(Gusano.eliminado.index(i))
	except ValueError: pass

	try:
		for i in objetivos: # Crea el diccionario de coordenadas de los objetivos
			x, y, a, b = canvas.coords(i)
			coordenadas[i] = (x, y) #((x+a)/2,(y+b)/2)
	except ValueError: pass
	#print(coordenadas)
	mx, my = MinDicciones(coordenadas) # Devuelve la tupla con la coordenada en y mas baja
	#print(mx, my)
	try:
		amoverX(mx, my)
	except TypeError: pass

	Gusano.Boverlapping()

def borrarfractal(event = None): # Se ocupa de los retrocesos
	print(len(Gusano.retrocesos))
	if len(Gusano.retrocesos) > 1:
		canvas.delete(Gusano.cabeza)
		for i in Gusano.retrocesos[0]: # Borra del canvas los elementos de la lista "retrocesos"
			canvas.delete(i)
		Gusano.retrocesos.pop(0)
		Gusano.cabeza = Gusano.cabeza - len(Gusano.fractalOval) # reasigna el id de la cabeza
		#print(Gusano.cabeza)
		try:
			x, y, a, b = Gusano.canvas.coords(Gusano.cabeza)
			Gusano.borrarObjetivo(x, y, a, b)
		except ValueError: pass
		Gusano.RETROCEDIDO = True

# ==================================================================================================================================
# MAIN =============================================================================================================================
# ==================================================================================================================================

tk = Tk()
canvas = Canvas(tk, width = 1100, height = 700, bg = 'gray10')
canvas.pack()
dibujar = Fractal(canvas)
r = lambda: random.randint(200,300)
dibujar.Fractal(None, r(), r(), 'white', 1, 4)
objetivos = []
cantidad = 5
obj(cantidad, 3)
Gusano = Gusano(canvas, tk, cantidad)

tk.bind('<Up>', Gusano.Delante) # Flecha arriba
tk.bind('<Left>', Gusano.Izquierda) # Flecha izquierda
tk.bind('<Right>', Gusano.Derecha) # Flecha derecha
tk.bind('<Down>', Gusano.Abajo) # Flecha abajo
tk.bind('<Escape>', quit) # Tecla ESC
tk.bind('<Return>', automatico) # Tecla Enter
tk.bind('<Delete>', borrarfractal) # Tecla Supr
def Play(_controller):
	global controller
	controller = _controller
mainloop()
