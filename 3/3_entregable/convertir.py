from afnd import Afn, Afd

class Convertidor:
    def __init__(self):
        self.afnAuxiliar = None
        self.afdAuxiliar = None
        self.nuevosEstados = None
        self.funcionTransicion = None


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
        if type(estado) == set:
            contador = 1
            for nuevoEstado in self.nuevosEstados:
                if estado == nuevoEstado:
                    return contador
                contador += 1
        else:
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


    def mover(self, estados, caracter):
        #print('mover',estados)
        conjunto = set()
        for estado in estados:
            auxiliar = set()

            for transicion in self.afnAuxiliar.estados[estado-1].transiciones:
                for condicion in transicion.condiciones:
                    if condicion == caracter:
                        auxiliar.add(transicion.siguiente)
                        break
            conjunto = conjunto.union(auxiliar)
        #print('mover-retorno',conjunto)
        return conjunto


    def obtenerNuevosEstados(self):
        self.nuevosEstados = list()
        for estado in self.afnAuxiliar.estados:
            self.nuevosEstados.append(self.cerraduraEpsilon(estado.nombre))


    def cerraduraEpsilon(self, estados):
        #print('epsilon',estados)
        conjunto = set()
        for estado in estados:
            auxiliar = set()
            arreglo = list()
            auxiliar.add(estado)

            for transicion in self.afnAuxiliar.estados[estado-1].transiciones:
                if len(transicion.condiciones) == 0:
                    #print('EL SIGUIENTE: ', transicion.siguiente)
                    auxiliar = auxiliar.union(self.cerraduraAuxiliar(transicion.siguiente))

            conjunto = conjunto.union(auxiliar)

        return conjunto


    def cerraduraAuxiliar(self, estado):
        aux = set()
        aux.add(estado)

        for transicion in self.afnAuxiliar.estados[estado-1].transiciones:
            if len(transicion.condiciones) == 0:
                #print('EL SIGUIENTE AUX: ', transicion.siguiente)
                aux = aux.union(self.cerraduraAuxiliar(transicion.siguiente))

        return aux

##=======================================================
## agarrate, esto se va a poner feo....
##=======================================================

    def convertir(self):
        self.estadosRevisados = dict()
        self.nuevosEstados = list()
        self.funcionTransicion = list()

        self.afdAuxiliar = Afd()

        #print('LEL:',self.cerraduraEpsilon({self.afnAuxiliar.inicial}))
        self.nuevosEstados.append(self.cerraduraEpsilon({self.afnAuxiliar.inicial}))
        self.afdAuxiliar.anadirEstado()

        con = 0
        for estado in self.nuevosEstados:
            con += 1
            for condicion in self.afnAuxiliar.historialCondiciones:
                #print('condicion', condicion)
                aux = self.cerraduraEpsilon(self.mover(estado, condicion))
                if len(aux) != 0:
                    e = self.agregar(aux)
                    self.afdAuxiliar.anadirTransicion(con, e, condicion)

        return self.afdAuxiliar


    def agregar(self, conjunto):
        con = 0
        for estado in self.nuevosEstados:
            con += 1
            if estado == conjunto:
                return con

        self.nuevosEstados.append(conjunto)
        e = self.afdAuxiliar.anadirEstado()

        con = 0
        for elemento in conjunto:
            if self.afnAuxiliar.estados[elemento-1].final:
                if con == 0:
                    self.afdAuxiliar.anadirFinal(e)
                    con += 1

        return e



    def llenarFuncionTransicion(self):
        i = 0
        conjuntoAuxiliar = set()
        while i < len(self.nuevosEstados):
            self.funcionTransicion.append({})
            for condicion in self.afnAuxiliar.historialCondiciones:
                for elemento in self.nuevosEstados[i]:
                    conjuntoAuxiliar = self.obtenerSiguiente(condicion, elemento)
                    if len(conjuntoAuxiliar) > 0:
                        if condicion in self.funcionTransicion[i]:
                            self.funcionTransicion[i][condicion].union(conjuntoAuxiliar)
                        else:
                            self.funcionTransicion[i][condicion] = conjuntoAuxiliar

                if condicion in self.funcionTransicion[i]:
                    incertar = True
                    for revisado in self.nuevosEstados:
                        if revisado == self.funcionTransicion[i][condicion]:
                            incertar = False
                            break
                    if incertar:
                        self.nuevosEstados.append(self.funcionTransicion[i][condicion])
            i+=1


    def obtenerSiguiente(self, condicion, estado):
        conjunto = set()
        for transicion in self.afnAuxiliar.estados[estado-1].transiciones:
            for c in transicion.condiciones:
                if condicion == c:
                    conjunto.add(transicion.siguiente)
        return conjunto


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
