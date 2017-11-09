from automatas.estado import Estado, Transicion
import networkx as nx
import matplotlib.pyplot as plt

class Afn(object):

    def __init__(self):
        self.estados = []
        self.tablaEstados = []
        self.contadorEstados = 0
        self.inicial = 0
        self.historialCondiciones = set()
        self.err = 0

    def anadirEstado(self):
        self.contadorEstados += 1

        if self.inicial == 0:
            self.estados.append(Estado(self.contadorEstados, True))
            self.inicial = self.contadorEstados
        else:
            self.estados.append(Estado(self.contadorEstados, False))

        return self.contadorEstados

    def anadirTransicion(self, estado, siguiente, condiciones=[]):
        if estado > self.contadorEstados or estado < 1:
            return -1

        if siguiente > self.contadorEstados or estado < 1:
            return -1

        for x in condiciones:
            self.historialCondiciones.add(x)

        if len(condiciones) > 0:
            transicion = Transicion(siguiente, condiciones)
            self.estados[estado-1].anadirTransicion(transicion)
            for condicion in condiciones:
                self.historialCondiciones.add(condicion)
        else:
            transicion = Transicion(siguiente)
            self.estados[estado-1].anadirTransicion(transicion)

        return 0

    def anadirFinal(self, estado):
        if estado > self.contadorEstados or estado < 1:
            return -1

        self.estados[estado-1].volverFinal()
        return 0

    def cambiarInicial(self, estado):
        if estado > self.contadorEstados or estado < 1:
            return -1

        self.estados[self.inicial-1].volverInicial()
        self.estados[estado-1].volverInicial()
        self.inicial = estado
        return 0

    def dibujarAutomata(self):
        G = nx.DiGraph()
        etiqueta = {}
        for estado in self.estados:
            if estado.inicial:
                print('SOY EL INICIAL:', estado.nombre)
            if estado.final:
                print('SOY EL FINAL:', estado.nombre)
            for transicion in estado.transiciones:
                G.add_edge(estado.nombre, transicion.siguiente)
                etiqueta[estado.nombre, transicion.siguiente] = transicion.condiciones

        pos=nx.spring_layout(G)

        nx.draw_networkx_nodes(G, pos, node_size=500, node_color="blue")
        nx.draw_networkx_edges(G, pos,width=2, alpha=0.5, edge_color='black')
        nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif')

        nx.draw_networkx_edge_labels(G, pos, etiqueta, label_pos=0.3, with_labels = True)

        plt.show();

    def manejarEpsilon(self, nombreEstado):
        epsilons = self.estados[nombreEstado - 1].obtenerNumEpsilons()
        aux = [nombreEstado]

        if len(epsilons) == len(self.estados[nombreEstado - 1].transiciones) and len(self.estados[nombreEstado - 1].transiciones) > 0:
            aux.pop()
        if len(epsilons) == 0:
            return aux

        for e in epsilons:
            aux += self.manejarEpsilon(e)

        return aux


    def obtenerTransiciones(self, nombreEstado):
        aux = dict()
        aux[' '] = []
        for transicion in self.estados[nombreEstado - 1].transiciones:
            for condicion in transicion.condiciones:
                if condicion not in aux:
                    aux[condicion] = []

                aux[condicion].append(transicion.siguiente)

            if len(transicion.condiciones) == 0:
                aux[' '] += self.manejarEpsilon(transicion.siguiente)

        return aux


    def crearTablaEstados(self):
        if len(self.estados) == 0:
            return -1

        aux = []
        cont = 0
        for estado in self.estados:
            aux.append([])
            for condicion, etds in self.obtenerTransiciones(estado.nombre).items():
                if len(etds) > 0:
                    aux[cont].append([condicion, etds])
            cont += 1

        self.tablaEstados = aux
        return self.tablaEstados


    def validarCadena(self, cadena):
        if type(cadena) is not str:
            return False
        if len(self.tablaEstados) == 0:
            print(cadena)
        if type(self.inicial) is not int:
            return False

        return True


    def evaluarEpsilon(self, estados, caracter):
        temp = []
        for e in estados:
            for x in self.tablaEstados[e-1]:
                if x[0] == caracter:
                    temp += x[1]
                if x[0] == ' ':
                    temp += self.evaluarEpsilon(x[1], caracter)
        return temp


    def validacionFinal(self, estados):
        temp = []
        for e in estados:
            epsilons = self.estados[e-1].obtenerNumEpsilons()
            if len(epsilons) == 0:
                temp += [e]
            else:
                temp += self.validacionFinal(epsilons)
        return temp


    def evaluarCadena(self, cadena):
        if not self.validarCadena(cadena):
            return False

        if len(cadena) == 0:
            cadena = ' '

        estds = [self.inicial]
        temp = []
        temp2 = []

        for caracter in cadena:
            temp = []
            for e in estds:
                for x in self.tablaEstados[e-1]:
                    if x[0] == caracter:
                        temp += x[1]
                    if x[0] == ' ':
                        temp += self.evaluarEpsilon(x[1], caracter)
            estds = temp

        estds = self.validacionFinal(estds)

        for e in estds:
            if self.estados[e-1].final:
                return True

        return False


class Afd(Afn):

    def anadirTransicion(self, estado, siguiente, condiciones=[]):
        if len(condiciones) > 1:
            return -1

        if estado > self.contadorEstados or estado < 1:
            return -1

        if siguiente > self.contadorEstados or estado < 1:
            return -1

        if len(condiciones) > 0:
            transicion = Transicion(siguiente, condiciones)
            self.estados[estado-1].anadirTransicion(transicion)
        else:
            transicion = Transicion(siguiente)
            self.estados[estado-1].anadirTransicion(transicion)

        return 0
