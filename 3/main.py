from afnd import Afn
from convertir import Convertidor

class Main:
    def iniciar(self):
        convertidor = Convertidor()
        automata = Afn()

        automata.anadirEstado()
        automata.anadirEstado()
        automata.anadirEstado()
        automata.anadirEstado()
        automata.anadirEstado()
        automata.anadirEstado()

        automata.anadirTransicion(1,2,['+', '-'])
        automata.anadirTransicion(1,2)
        automata.anadirTransicion(2,2,['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        automata.anadirTransicion(2,3,['.'])
        automata.anadirTransicion(3,4,['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        automata.anadirTransicion(4,4,['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        automata.anadirTransicion(4,5)
        automata.anadirTransicion(2,6,['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        automata.anadirTransicion(6,4, ['.'])

        automata.anadirFinal(5)

        automata.crearTablaEstados()

        convertidor.iniciarAfnAuxiliar(automata)
        nuevoAfn = convertidor.eliminarTransicionesEpsilon()

        nuevoAfn.crearTablaEstados()
        for estado in nuevoAfn.tablaEstados:
            print(estado)

        #nuevoAfn.dibujarAutomata()
        print(nuevoAfn.evaluarCadena(input('Ingresa una cadena: ')))

main = Main()
main.iniciar()
