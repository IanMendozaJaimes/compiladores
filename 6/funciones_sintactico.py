
class Manejador_sintactico():

    def __init__(self):
        self.producciones = list()
        self.productores = dict()
        self.producidos = dict()
        self.inicial = ''
        self.siguientes_calculados = dict()
        self.visitados = None

    def primero(self, simbolo):
        if simbolo[0] not in self.productores:
            return {simbolo}

        primeros = set()
        for s in simbolo:
            for x in self.productores[s]:
                aux = set()
                if '%' in primeros:
                    primeros.remove('%')
                p = self.producciones[x][1]
                for caracter in p:
                    aux = aux.union(self.primero(caracter))
                    if '%' not in aux:
                        break
                primeros = primeros.union(aux)
            if '%' not in primeros:
                break
        return primeros

    def siguiente(self, simbolo):
        self.visitados = dict()
        self.visitados[simbolo] = 1
        return self.auxiliar_siguiente(simbolo)


    def auxiliar_siguiente(self, simbolo):
        siguientes = set()
        print('========')
        print(self.visitados)
        print('========')

        if simbolo == self.inicial:
            siguientes.add('$')

        for x in self.producidos[simbolo]:
            produccion = self.producciones[x][1]
            i = 0
            aux = set()
            while i < len(produccion):
                if produccion[i] == simbolo:
                    if (i + 1) < len(produccion):
                        print('primero de: ', produccion[i+1:])
                        aux = self.primero(produccion[i+1:])
                        if '%' in aux:
                            if self.producciones[x][0] not in self.visitados:
                                self.visitados[self.producciones[x][0]] = 1
                                aux = aux.union(self.auxiliar_siguiente(self.producciones[x][0]))
                        break
                    else:
                        if self.producciones[x][0] not in self.visitados:
                            self.visitados[self.producciones[x][0]] = 1
                            aux = self.auxiliar_siguiente(self.producciones[x][0])
                        break
                i += 1
            siguientes = siguientes.union(aux)
        return siguientes

    def cargar_gramaticas(self, nombre_archivo):
        archivo = open(nombre_archivo, 'r')
        contador = 0

        l = archivo.readline()
        contador2 = True
        for x in l.split(' '):
            aux = x.replace('\n','')
            if contador2:
                self.inicial = aux
                contador2 = False
            self.productores[aux] = list()
            self.producidos[aux] = list()

        for linea in archivo.readlines():
            s = ''
            p = ''
            i = 0

            while linea[i] != ' ':
                s += linea[i]
                i += 1
            i += 4

            while i < len(linea) and linea[i] != '\n':
                p += linea[i]
                if linea[i] in self.productores:
                    self.producidos[linea[i]].append(contador)
                i += 1
            p = p.replace('\\E', '%')
            self.productores[s].append(contador)
            self.producciones.append([s,p])
            contador += 1
