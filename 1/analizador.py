class Arbol(object):
    pass

class Analizador(object):
    def __init__(self):
        self.arbol = Arbol()
        self.pila = []
        self.lista = []

    def analizar(self, cadena):
        if not self.validarCadena(cadena):
            return -1

        for caracter in cadena:
            if caracter == '(' or caracter == '.':
                self.pila.append(caracter)

            if caracter == '+':
                if self.pila


    def pilaVacia(self):
        if len(self.pila) == 0:
            return True
        else:
            return False

    def pilaTope(self):
        if not self.pilaVacia():
            return self.pila[len()]


    def validarCadena(self, cadena):
        if type(cadena) is not str:
            return False

        if len(cadena) == 0:
            return False

        return True
