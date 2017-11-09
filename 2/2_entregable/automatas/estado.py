class Transicion(object):
    def __init__(self, siguiente, condiciones=[]):
        self.condiciones = condiciones
        self.siguiente = siguiente


class Estado(object):
    def __init__(self, nombre, inicial=False, final=False):
        self.nombre = nombre
        self.inicial = inicial
        self.final = final
        self.transiciones = []

    def anadirTransicion(self, transicion):
        self.transiciones.append(transicion)
        return 0;

    def obtenerNumEpsilons(self):
        cont = []
        for t in self.transiciones:
            if len(t.condiciones) == 0:
                cont.append(t.siguiente)
        return cont

    def volverFinal(self):
        self.final = not self.final
        return 0;

    def volverInicial(self):
        self.inicial = not self.inicial
        return 0;
