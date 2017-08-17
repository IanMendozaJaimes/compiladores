class Lenguaje(object):
    def __init__(self, elementos):
        self.elementos = set(elementos)

    def union(self, otroLenguaje):
        if type(otroLenguaje) is not Lenguaje:
            return -1

        self.elementos += otroLenguaje.elementos
        return 0

    def concatenacion(self, otroLenguaje):
        if type(otroLenguaje) is not Lenguaje:
            return -1

        temp = set()
        for elemento in self.elementos:
            for otro in otroLenguaje:
                temp.add(elemento + otro)
