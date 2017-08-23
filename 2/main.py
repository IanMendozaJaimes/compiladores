from analizador import Analizador

class Main(object):

    def iniciar(self):
        expresion = input("Ingresa una expresion: ")
        analizador = Analizador()

        analizador.analizar(expresion)
        print(analizador.lista)

        analizador.automata.crearTablaEstados()
        while True:
            cadena = input('Ingresa una cadena a evaluar:')
            print(analizador.automata.evaluarCadena(cadena))
            if input('Quieres otra? s/n   ') != 's':
                break


main = Main()
main.iniciar()
