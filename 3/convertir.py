from afnd import Afn, Afd

class Convertidor:
    def __init__(self):
        self.afnAuxiliar = None
        self.afdAuxiliar = None
        self.nuevosEstados = None


    def eliminarTransicionesEpsilon(self):
        if self.afnAuxiliar == None:
            return None

        self.obtenerNuevosEstados()

        nuevoAfn = Afn()
        for nuevo in range(0, len(self.nuevosEstados)):
            nuevoAfn.anadirEstado()

        contador = 1
        for nuevo in  self.nuevosEstados:
            for elemento in nuevo:
                if self.afnAuxiliar.estados[elemento-1].final:
                    if not nuevoAfn.estados[contador-1].final:
                        nuevoAfn.anadirFinal(contador)
                for transicion in self.afnAuxiliar.estados[elemento-1].transiciones:
                    if len(transicion.condiciones) > 0:
                        for siguiente in self.obtenerEstado(transicion.siguiente):
                            nuevoAfn.anadirTransicion(contador, siguiente, transicion.condiciones)
            contador += 1

        return nuevoAfn


    def obtenerEstado(self, estado):
        nuevo = {estado}
        contador = 1
        for nuevoEstado in self.nuevosEstados:
            if nuevo == nuevoEstado:
                return [contador]
            contador += 1

        contador = 1
        auxiliar = list()
        for nuevoEstado in self.nuevosEstados:
            if nuevo <= nuevoEstado:
                auxiliar.append(contador)
            contador += 1

        return auxiliar


    def obtenerNuevosEstados(self):
        self.nuevosEstados = list()
        for estado in self.afnAuxiliar.estados:
            self.nuevosEstados.append(self.cerraduraEpsilon(estado.nombre))


    def cerraduraEpsilon(self, estado):
        auxiliar = set()
        arreglo = list()
        auxiliar.add(estado)

        for transicion in self.afnAuxiliar.estados[estado-1].transiciones:
            if len(transicion.condiciones) == 0:
                arreglo += self.cerraduraAuxiliar(transicion.siguiente)

        for elemento in arreglo:
            auxiliar.add(elemento)

        return auxiliar


    def cerraduraAuxiliar(self, estado):
        aux = [estado]
        for transicion in self.afnAuxiliar.estados[estado-1].transiciones:
            for condicion in transicion.condiciones:
                if len(condicion) == 0:
                    aux += self.cerraduraAuxiliar(transicion.siguiente)

        return aux


    def convertir(self):
        pass


    def iniciarAfnAuxiliar(self, automata):
        if type(automata) is not Afn:
            return None

        self.afnAuxiliar = automata
        return 0


    def iniciarAfdAuxiliar(self, automata):
        if type(automata) is not Afd:
            return None

        self.afdAuxiliar = automata
        return 0
