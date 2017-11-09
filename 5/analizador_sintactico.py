class analizador():
    def __init__(self):
        self.cadena = 'aacbbb'
        self.contador = 0;

    def error(self):
        print('LA CADENA NO ES VALIDA.')
        exit()

    def consume(self,valor=''):
        if(self.contador == len(self.cadena)):
            self.error()
        if self.cadena[self.contador] == valor:
            print(self.cadena[self.contador])
            self.contador += 1
        else:
            self.error()

    def S(self):
        if self.cadena[self.contador] == 'a':
            self.consume('a')
            self.S()
            self.consume('b')
        elif self.cadena[self.contador] == 'c':
            self.consume('c')
        else:
            self.error()

a = analizador()
a.S()
if(a.contador == len(a.cadena)):
    print('LA CADENA ES VALIDA')
else:
    a.error()
