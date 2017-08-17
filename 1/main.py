from afnd import Afn, Afd

class Main(object):

    def iniciar(self):
        automata = Afn()

        automata.anadirEstado()
        automata.anadirEstado()
        automata.anadirEstado()
        automata.anadirEstado()
        automata.anadirEstado()
        automata.anadirEstado()

        automata.anadirFinal(6)

        automata.anadirTransicion(1, 2, ['1'])
        automata.anadirTransicion(2, 1, ['1'])
        automata.anadirTransicion(2, 3, ['0'])
        automata.anadirTransicion(3, 2, ['0'])
        automata.anadirTransicion(3, 4, ['1'])
        automata.anadirTransicion(4, 3, ['1'])
        automata.anadirTransicion(4, 1, ['0'])
        automata.anadirTransicion(1, 4, ['0'])
        automata.anadirTransicion(4, 5)
        automata.anadirTransicion(5, 6, ['j'])

        for x in automata.crearTablaEstados():
            print(x)

        automata.dibujarAutomata()
        print('====')
        while True:
            print(automata.evaluarCadena(input("Ingresa una cadena: ")))
            if input("Quieres ingresar otra?: s/n    ") != 's':
                break


main = Main()
main.iniciar()
