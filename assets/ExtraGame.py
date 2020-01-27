from tkinter import *
import random
from fractal import *


class Chocador(object):
	"""docstring for Chocador"""
	def __init__(self, canvas, x, y, r, color, tag):
		super(Chocador, self).__init__()
		self.canvas = canvas
		self.x = x
		self.y = y
		self.r = r
		self.color = color
		self.ID = self.canvas.create_rectangle(self.x, self.y, self.x+self.r, self.y+self.r, fill = self.color, tags = tag)

class Gusano(object):
	"""docstring for Gusano"""
	def __init__(self, canvas, tk, cantidad):
		super(Gusano, self).__init__()
		self.canvas = canvas
		self.tk = tk
		self.cantidad = cantidad
		self.cabeza = self.canvas.create_oval(int(self.canvas['width'])/2-20, int(self.canvas['height'])-40,int(self.canvas['width'])/2+20,int(self.canvas['height']), fill = 'spring green', tags = 'Gusano')
		x, y, a, b = self.canvas.coords(self.cabeza)
		self.dibujar = Fractal(self.canvas)
		self.radio = 18
		self.fractalOval = self.dibujar.Fractal(self.radio, (x+a)/2, (y+b)/2, None, None, 1, 'fractal')
		#print(self.canvas.find_closest((x+a)/2, (y+b)/2))
		self.MOVIMIENTOS = []
		self.marcador = 0
		self.segundaCabeza = self.cabeza
		self.retrocesos = []
		self.eliminado = []
		label = Label(self.canvas, text = 'Score: '+str(self.marcador), font = ('Arial', 15), bg = 'gray10', fg = 'white')
		label.place(x = 2, y = 2)
		self.fractalOval.append(self.cabeza)
		self.retrocesos.insert(0, self.fractalOval)
		self.RETROCEDIDO = False

	def borrarObjetivo(self, x, y, a, b):
		ides = self.canvas.find_overlapping(x, y, a, b)
		tags = []
		if self.marcador == self.cantidad:
			label = Label(self.canvas, text = 'You win!', font = ('Arial', 15), bg = 'gray10', fg = 'white')
			label.place(x = int(self.canvas['width'])/2-50, y = int(self.canvas['height'])/2-20)
			self.Detener()
		if len(ides) > 1:
			for i in ides:
				tagTuple = self.canvas.gettags(i)
				tags.append(tagTuple)
				#print(tagTuple)
				try:
					if tagTuple[0] == 'Objetivo':
						self.eliminado.append(i)
						self.canvas.delete(i)
						self.marcador += 1
						label = Label(self.canvas, text = 'Score: '+str(self.marcador), font = ('Arial', 15), bg = 'gray10', fg = 'white')
						label.place(x = 2, y = 2)
						break
					elif (tagTuple[0] == 'Obstaculo') or (tags.count(('Cabeza', 'Gusano')) >= 2):
						#self.canvas.delete("all")
						self.Detener()
						if (tagTuple[0] != 'Obstaculo'):
							UltBurb = 'red'
						else:
							UltBurb = 'blue'

						for i in range(2):
							self.canvas.itemconfig(self.cabeza-i, fill = UltBurb)
						label = Label(self.canvas, text = 'Game Over', font = ('Arial', 15), bg = 'gray10', fg = 'white')
						label.place(x = int(self.canvas['width'])/2-50, y = int(self.canvas['height'])/2-20)
				except IndexError: pass

	def eventos(self, grosor, altura, DIRECCION): # Direccion: 1 Derecha, -1 Izquierda, -2 Arriba, 2 Abajo
		try:

			if self.RETROCEDIDO:
				self.retrocesos = []
				self.fractalOval.append(self.cabeza)
				self.retrocesos.insert(0, self.fractalOval)
				self.RETROCEDIDO = False

			x, y, a, b = self.canvas.coords(self.cabeza)
			#print(self.canvas.find_closest(x, y))
			self.canvas.addtag_withtag('Gusano', self.cabeza)
			self.segundaCabeza = self.cabeza
			if  (self.MOVIMIENTOS == []) or not (-1*DIRECCION == self.MOVIMIENTOS[-1]):

				self.MOVIMIENTOS.append(DIRECCION)
				if a < -10:
					self.cabeza = self.canvas.create_oval(int(self.canvas['width'])-40, y+altura, int(self.canvas['width']), b+altura, fill = 'spring green', tags = 'Cabeza')
				elif a > int(self.canvas['width']) + 10:
					self.cabeza = self.canvas.create_oval(0, y+altura, 40, b+altura, fill = 'spring green', tags = 'Cabeza')
				elif b < -10:
					self.cabeza = self.canvas.create_oval(x+grosor, int(self.canvas['height'])-40, a+grosor, int(self.canvas['height']), fill = 'spring green', tags = 'Cabeza')
					#print('entre')
				elif b > int(self.canvas['height']) + 10:
					self.cabeza = self.canvas.create_oval(x+grosor, 0, a+grosor, 40, fill = 'spring green', tags = 'Cabeza')
				else:
					self.cabeza = self.canvas.create_oval(x+grosor, y+altura, a+grosor, b+altura, fill = 'spring green', tags = 'Cabeza')

				self.fractalOval = self.dibujar.Fractal(self.radio, (x+a)/2, (y+b)/2, None, None, 1, 'fractal')
				self.fractalOval.append(self.cabeza)
				self.retrocesos.insert(0, self.fractalOval)
				self.borrarObjetivo(x, y, a, b)
				self.canvas.after(2)
		except ValueError: pass

	def Delante(self, event = None):
		self.eventos(0,-45, -2)

	def Abajo(self, event = None):
		self.eventos(0, 45, 2)

	def Izquierda(self, event = None):
		self.eventos(-45, 0, -1)

	def Derecha(self, event = None):
		self.eventos(45, 0, 1)

	def Detener(self):
		self.tk.unbind('<Up>')
		self.tk.unbind('<Left>')
		self.tk.unbind('<Right>')
		self.tk.unbind('<Down>')
		self.tk.unbind('<Return>')
		self.tk.unbind('<Delete>')

def obj(cantObj, cantObs, canvas, radio = None):
	global objetivos

	def GenerarFigura(radio, cantidad, tag, color = None):
		if radio == None:
			radio = lambda: random.randint(50, 60)
		else:
			radio = lambda: radio
		x = lambda: random.randint(150, int(canvas['width'])-150)
		y = lambda: random.randint(150, int(canvas['height'])-150)
		arreglo = list(range(cantidad))
		colores = ['red', 'green', 'orange', 'yellow', 'cyan']
		centinela = False
		if color is None: centinela = True
		for i in arreglo:
			if centinela: color = colores[i]
			X = x()
			Y = y()
			R = radio()
			if (len(canvas.find_overlapping(X, Y, X+R, Y+R)) == 0):
				c = Chocador(canvas, X, Y, R, color, tag)
				#print('si se pudo', X, Y)
				if centinela:
					objetivos.append(c.ID)
				#print('no')
			else:
				arreglo.append(1)
		print('longitud',len(arreglo))

	GenerarFigura(radio, cantObj, 'Objetivo')
	GenerarFigura(radio, cantObs, 'Obstaculo', 'black')

def MinDicciones(diccionario):
	minx = {}
	miny = {}
	my, mx = None, None
	for key in diccionario:
		miny[key] = diccionario[key][1]
		if my == None: my = miny[key]
		if my < miny[key]: my = miny[key]

	for key in diccionario:
		if diccionario[key][1] == my:
			mx = diccionario[key][0]
			break
	return mx, my

def movimiento(a,b, m, atributo, canvas):
	def Condicion(a, b, coord, sensibilidad):
		centinela = 0
		if (a > 0) or (b > 0):
			condicion = m > coord + sensibilidad
			#print('a > 0', condicion)
			#print(m, '>', coord)
		elif (a <= 0) or (b <= 0):
			condicion = m < coord - sensibilidad
			#print('a <= 0', condicion)
			#print(m, '<', coord)
		return condicion

	if b is 0: index = 0
	else: index = 1
	coord = canvas.coords(Gusano.cabeza)[index]
	i = 0
	centinela = False
	if a is not 0:
		signo = abs(a)/a
	else:
		signo = abs(b)/b
	condicion = Condicion(a, b, coord, 60)

	while (condicion) and (coord > 0) and (coord < int(canvas[atributo])) and (i < 20):
		condicion = Condicion(a, b, coord, 60)
		Gusano.eventos(a, b, (index + 1)*signo)
		coord = canvas.coords(Gusano.cabeza)[index]
		i += 1
		centinela = True
	return centinela


def amoverY(my):
	centinela = movimiento(0, -45, my, 'height', canvas)

	if not centinela:
		centinela = movimiento(0, 45, my, 'height', canvas)

def amoverX(mx, my, canvas):
	for i in range(3):
		centinela = movimiento(-45, 0, mx, 'width')

		if not centinela:
			movimiento(45, 0, mx, 'width')

		amoverY(my, canvas)

	# IR AL PUNTO MAS BAJO

def automatico(canvas):
	global objetivos
	coordenadas = {}
	try:
		for i in Gusano.eliminado:
			objetivos.pop(objetivos.index(i))
			Gusano.eliminado.pop(Gusano.eliminado.index(i))
	except ValueError: pass

	try:
		x, y, a, b = Gusano.canvas.coords(Gusano.cabeza)
		Gusano.borrarObjetivo(x, y, a, b)
	except ValueError: pass
	try:
		for i in objetivos:
			x, y, a, b = self.canvas.coords(i)
			coordenadas[i] = ((x+a)/2,(y+b)/2)
	except ValueError: pass
	#print(coordenadas)
	mx, my = MinDicciones(coordenadas)
	#print(mx, my)
	try:
		amoverX(mx, my, canvas)
	except TypeError: pass

def CaptMouse(event = None):
	global label
	label['text'] = 'x, y = ('+str(event.x)+','+str(event.y)+')'

def borrarfractal(canvas):
	if len(Gusano.retrocesos) > 1:
		canvas.delete(Gusano.cabeza)
		for i in Gusano.retrocesos[0]:
			canvas.delete(i)
		Gusano.retrocesos.pop(0)
		Gusano.cabeza = Gusano.cabeza - len(Gusano.fractalOval)
		print(Gusano.cabeza)
		try:
			x, y, a, b = Gusano.canvas.coords(Gusano.cabeza)
			Gusano.borrarObjetivo(x, y, a, b)
		except ValueError: pass
		Gusano.RETROCEDIDO = True

# ==================================================================================================================================
# MAIN =============================================================================================================================
# ==================================================================================================================================
objetivos = []
tk = Tk()
canvas = Canvas(tk, width = 1100, height = 700, bg = 'white')
canvas.pack()
cantidad = 5
Gusano = Gusano(canvas, tk, cantidad)

class ExtraGame:

	def __init__(controller):
		dibujar = Fractal(canvas)
		r = lambda: random.randint(200,300)
		dibujar.Fractal(None, r(), r(), 'white', 1, 4)
		obj(cantidad, 3, canvas)

		#label = Label(canvas, text = 'x, y = (None, None)', font = ('Arial', 15), bg ='gray10', fg = 'white')
		#label.place(x = 920, y = 10)
		tk.bind('<Up>', Gusano.Delante)
		tk.bind('<Left>', Gusano.Izquierda)
		tk.bind('<Right>', Gusano.Derecha)
		tk.bind('<Down>', Gusano.Abajo)
		tk.bind('<Escape>', quit)
		tk.bind('<Return>', automatico)
		#tk.bind('<Motion>', CaptMouse)
		tk.bind('<Delete>', lambda : borrarfractal(canvas))
		controller.deiconify()
		tk.destroy()
		mainloop()
