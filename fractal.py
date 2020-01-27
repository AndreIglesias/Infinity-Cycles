import random, string, math, cmath
from cmath import *

class circulo(object):
    '''
    Circulo: centro y radio
    '''
    def __init__(self, mx, my, r):
        '''
        :param mx: Coordenada real del centro del circulo
        :param my: Coordenada imaginaria del centro del circulo
        :param r:  Radio del circulo
        '''
        self.r = r
        self.m = mx + my * 1j

    def curvatura(self): return 1 / self.r

class Fractal:
	def __init__(self, w):
		self.w = w
		self.resultado = []

	def circuloTan1(self, c1,c2,c3):
	    '''
	    :param c1: Circulo tangente 1 con sus caracterisitcas
	    :param c2: Circulo tangente 2 con sus caracteristicas
	    :param c3: Circulo tangente 3 con sus caracteristicas
	    :type c1: L{Circle}
	    :type c2: L{Circle}
	    :type c3: L{Circle}
	    :return: The enclosing circle
	    :rtype: L{Circle}
	    :return: Circulo 4 con sus caracteristicas, circunscribe los otros circulos
	    '''

	    cur1 = c1.curvatura()
	    cur2 = c2.curvatura()
	    cur3 = c3.curvatura()
	    m1 = c1.m
	    m2 = c2.m
	    m3 = c3.m

	    curva = (-2 * sqrt(cur1*cur2 + cur2*cur3 + cur1 * cur3) + cur1 + cur2 + cur3).real
	    centro = (-2 * sqrt(cur1*m1*cur2*m2 + cur2*m2*cur3*m3 + cur1*m1*cur3*m3) + cur1*m1 + cur2*m2 + cur3*m3) / curva
	    return circulo(centro.real, centro.imag, 1/curva)

	def circuloTan2(self, fijo, c1, c2, c3):
	    '''
	    :param fijo: Uno de los circulos tangente a los otros 3
	    :param c1, c2, c3: Circulos a los que el nuevo y el fijo son tangentes
	    :return: Segundo circulo tangente
	    '''
	    curvaturaFija = fijo.curvatura()
	    curvatura1 = c1.curvatura()
	    curvatura2 = c2.curvatura()
	    curvatura3 = c3.curvatura()

	    curvatu = 2*(curvatura1+curvatura2+curvatura3) - curvaturaFija
	    coor = (2*(curvatura1*c1.m + curvatura2*c2.m + curvatura3*c3.m) - curvaturaFija*fijo.m) / curvatu
	    return circulo(coor.real, coor.imag, 1/curvatu)

	def CirculosTangentes(self, radio1, radio2, radio3):
	    '''
	    Genera los primeros cuatro circulos a partir de los radios dados
	    :param radio2: Radio del circulo 2
	    :param radio3: Radio del circulo 3
	    :param radio4: Radio del circulo 4
	    :return: Primeros cuatro circulos
	    :type radio2: int or float
	    :type radio3: int or float
	    :type radio4: int or float
	    :rtype: L{circulo}, L{circulo}, L{circulo}, L{circulo}
	    '''
	    circulo1 = circulo(0, 0, radio1)
	    circulo2 = circulo(radio1 + radio2, 0, radio2)
	    coor0x = (radio1*(radio1+radio3+radio2) - (radio2*radio3)) / (radio1 + radio2)
	    coor0y = sqrt((radio1 + radio3)**2 - coor0x**2)
	    circulo3 = circulo(coor0x, coor0y, radio3)
	    circulo0 = self.circuloTan1(circulo1, circulo2, circulo3)
	    return (circulo0, circulo1, circulo2, circulo3)

	#----------------------------------------------------------------------------------------

	def Fractal(self, Rd, clickx, clicky, color, fd, nivel, tag = None):
	    '''
	    :param c1, c2, c3: Curvatura de los circulos internos
	    :type c1: int or float
	    :type c2: int or float
	    :type c3: int or float
	    '''
	    
	    self.resultado = []

	    if tag is None:
	    	self.tag = 'Nada'
	    else:
	    	self.tag = tag

	    if fd is None: rad1 = rad2 = rad3 = abs(Rd*(-2*sqrt(3)+3).real)
	    else:
	        r = lambda: random.randint(200, 500)
	        rad1 = r()
	        rad2 = r()
	        rad3 = r()
	    clicky = clicky.real
	    clickx = clickx.real

	    self.color = color
	    #print('rad1: {}\nrad2: {}\nrad3: {}'.format(rad1, rad2, rad3))


	    self.start = self.CirculosTangentes(rad1, rad2, rad3)

	    self.genCircles = list(self.start)

	    self.radio1 = radio1 = rad1
	    self.radio2 = radio2 = rad2
	    self.radio3 = radio3 = rad3
	    self.radio4 = radio4 = self.start[0].r
	    self.centradox = centradox = clickx - rad1
	    self.centradoy = centradoy = clicky - rad1 * (1/sqrt(3))

	    r = lambda: random.randint(20,60) # 0 min, 255 max -- color = None para circulo vacio con orilla blanca
	    self.circu(centradox+(self.start[0].m).real - radio4, centradoy+(self.start[0].m).imag - radio4, radio4, self.color, self.w)
	    #print(radio4, self.start[0].m)
	    self.circu(centradox+(self.start[1].m).real - radio1, centradoy+(self.start[1].m).imag - radio1, radio1, self.color, self.w)
	    self.circu(centradox+(self.start[2].m).real - radio2, centradoy+(self.start[2].m).imag - radio2, radio2, self.color, self.w)
	    self.circu(centradox+(self.start[3].m).real - radio3, centradoy+(self.start[3].m).imag - radio3, radio3, self.color, self.w)

	    self.generate(nivel, self.w)
	    return self.resultado

	def circu(self, x, y, r, color, w):
	    x = x.real
	    y = y.real
	    r = r.real
	    if color is None:
	        ro = lambda: random.randint(60, 120)
	        self.resultado.append(self.w.create_oval(x, y, x + 2 * r, y + 2 * r, width = 1, fill = '#%02X%02X%02X' % (ro(),ro(),ro()), tags = self.tag))
	    else:
	        self.resultado.append(self.w.create_oval(x, y, x + 2 * r, y + 2 * r, width = 1, outline = self.color, dash = 1, tags = self.tag))

	def recurse(self, circles, depth, maxDepth, c):
	    '''
	    De manera recursiva, se calcula el circulo mas pequeno del fractal
	    hasta la profundidad preestablecida (2*3**(n+1) cicrulos para una profundidad "n")
	    :param maxDepth: Maxima profundidad
	    :type maxDepth: int
	    :param circles: Tupla de circulos
	    :type circles: (L{Circle}, L{Circle}, L{Circle}, L{Circle})
	    :param depth: Profundidad actual
	    :type depth: int
	    '''
	    if(depth == maxDepth):
	    	return
	    (c1, c2, c3, c4) = circles

	    if(depth == 0):
	        # Unica vez que se necesita calcular los 4 circulos
	        del self.genCircles[4:]
	        cspecial = self.circuloTan2(c1, c2, c3, c4)
	        #print(cspecial.m, cspecial.r)
	        csradio = cspecial.r
	        r = lambda: random.randint(20,60)
	        self.circu(self.centradox+(cspecial.m).real - csradio, self.centradoy+(cspecial.m).imag - csradio, csradio, '#%02X%02X%02X' % (r(),r(),r()), c)
	        self.genCircles.append(cspecial)
	        self.recurse((cspecial, c2, c3, c4), 1, maxDepth, c)

	    cn2 = self.circuloTan2(c2, c1, c3, c4)
	    self.genCircles.append(cn2)
	    cn3 = self.circuloTan2(c3, c1, c2, c4)
	    self.genCircles.append(cn3)
	    cn4 = self.circuloTan2(c4, c1, c2, c3)
	    self.genCircles.append(cn4)

	    r = lambda: random.randint(20,60)
	    self.circu(self.centradox + (cn2.m).real - cn2.r, self.centradoy + (cn2.m).imag - cn2.r, cn2.r, self.color, c)
	    r = lambda: random.randint(20,60)
	    self.circu(self.centradox + (cn3.m).real - cn3.r, self.centradoy + (cn3.m).imag - cn3.r, cn3.r, self.color, c)
	    r = lambda: random.randint(20,60)
	    self.circu(self.centradox + (cn4.m).real - cn4.r, self.centradoy + (cn4.m).imag - cn4.r, cn4.r, self.color, c)


	    self.recurse((cn2, c1, c3, c4), depth+1, maxDepth, c)
	    self.recurse((cn3, c1, c2, c4), depth+1, maxDepth, c)
	    self.recurse((cn4, c1, c2, c3), depth+1, maxDepth, c)

	def generate(self, depth, c):
	    '''
	    Genera con la funcion recursiva el fractal
	    :param depth: Recursion depth of the Gasket
	    :type depth: int
	    '''
	    self.recurse(self.start, 0, depth, c)

