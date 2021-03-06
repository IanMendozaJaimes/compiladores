from automatas.afnd import Afn

class Manejador_nodos(object):
    def __init__(self):
        self.inicio = None
        self.ultimo = None

class Analizador(object):
    def __init__(self):
        self.pila = []
        self.lista = []
        self.automata = None

    def analizar(self, cadena):
        if not self.validarCadena(cadena):
            return -1

        self.convertirPostorden(cadena)
        self.crearAutomata()


    def crearAutomata(self):
        self.automata = Afn()
        for elemento in self.lista:
            if elemento == '+':
                auxiliar1 = self.pila.pop()
                auxiliar2 = self.pila.pop()
                manejador_nodos = Manejador_nodos()
                manejador_nodos.inicio = self.automata.anadirEstado()
                manejador_nodos.final = self.automata.anadirEstado()
                self.automata.anadirTransicion(manejador_nodos.inicio, auxiliar1.inicio)
                self.automata.anadirTransicion(manejador_nodos.inicio, auxiliar2.inicio)
                self.automata.anadirTransicion(auxiliar1.final, manejador_nodos.final)
                self.automata.anadirTransicion(auxiliar2.final, manejador_nodos.final)
                self.pila.append(manejador_nodos)

            elif elemento == '.':
                auxiliar1 = self.pila.pop()
                auxiliar2 = self.pila.pop()
                manejador_nodos = Manejador_nodos()
                manejador_nodos.inicio = auxiliar2.inicio
                manejador_nodos.final = auxiliar1.final
                self.automata.anadirTransicion(auxiliar2.final, auxiliar1.inicio)
                self.pila.append(manejador_nodos)

            elif elemento == '^':
                auxiliar1 = self.pila.pop()
                auxiliar2 = self.pila.pop()
                manejador_nodos = Manejador_nodos()
                manejador_nodos.inicio = self.automata.anadirEstado()
                manejador_nodos.final = self.automata.anadirEstado()
                self.automata.anadirTransicion(manejador_nodos.inicio, auxiliar2.inicio)
                self.automata.anadirTransicion(auxiliar2.final, manejador_nodos.final)
                self.automata.anadirTransicion(auxiliar2.final, auxiliar2.inicio)
                if auxiliar1.inicio == -1:
                    self.automata.anadirTransicion(manejador_nodos.inicio, manejador_nodos.final)
                self.pila.append(manejador_nodos)

            elif elemento == '*':
                manejador_nodos = Manejador_nodos()
                manejador_nodos.inicio = -1
                manejador_nodos.final = -1
                self.pila.append(manejador_nodos)

            elif elemento == '++':
                manejador_nodos = Manejador_nodos()
                manejador_nodos.inicio = -2
                manejador_nodos.final = -2
                self.pila.append(manejador_nodos)

            elif elemento == 'E':
                manejador_nodos = Manejador_nodos()
                manejador_nodos.inicio = self.automata.anadirEstado()
                manejador_nodos.final = self.automata.anadirEstado()
                self.automata.anadirTransicion(manejador_nodos.inicio, manejador_nodos.final)
                self.pila.append(manejador_nodos)

            else:
                manejador_nodos = Manejador_nodos()
                manejador_nodos.inicio = self.automata.anadirEstado()
                manejador_nodos.final = self.automata.anadirEstado()
                self.automata.anadirTransicion(manejador_nodos.inicio, manejador_nodos.final, [elemento])
                self.pila.append(manejador_nodos)

        manejador_nodos = self.pila.pop()
        self.automata.cambiarInicial(manejador_nodos.inicio)
        self.automata.anadirFinal(manejador_nodos.final)


    def convertirPostorden(self, cadena):
        concatenacion = False
        for caracter in cadena:
            if caracter == '(':
                if concatenacion:
                    self.pila.append('.')
                concatenacion = False
                self.pila.append(caracter)
            elif caracter == '+':
                concatenacion = False
                if self.pilaTope() == '^':
                    self.lista.append(caracter+caracter)
                elif self.pilaTope() == '.':
                    while not self.pilaVacia():
                        if self.pilaTope() != '(':
                            self.lista.append(self.pila.pop())
                        else:
                            break
                    self.pila.append(caracter)
                else:
                    self.pila.append(caracter)
            elif caracter == '^':
                concatenacion = False
                self.pila.append(caracter)
            elif caracter ==')':
                concatenacion = True
                while True:
                    if self.pilaTope() == '(':
                        self.pila.pop()
                        break
                    if not self.pilaVacia():
                        self.lista.append(self.pila.pop())
                    else:
                        return None
            else:
                if concatenacion:
                    if self.pilaTope() == '^':
                        while not self.pilaVacia():
                            if self.pilaTope() != '(':
                                self.lista.append(self.pila.pop())
                            else:
                                break
                    self.pila.append('.')
                concatenacion = True
                self.lista.append(caracter)

        while not self.pilaVacia():
            if self.pilaTope() != '(':
                self.lista.append(self.pila.pop())
            else:
                return None



    def pilaVacia(self):
        if len(self.pila) == 0:
            return True
        else:
            return False

    def pilaTope(self):
        if not self.pilaVacia():
            return self.pila[len(self.pila)-1]
        return None

    def validarCadena(self, cadena):
        if type(cadena) is not str:
            return False

        if len(cadena) == 0:
            return False

        return True
