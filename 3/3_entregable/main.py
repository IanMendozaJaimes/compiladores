from afnd import Afn
from analizador import Analizador
from convertir import Convertidor

class Main:
    def iniciar(self):
        convertidor = Convertidor()
        automata = Afn()

        expresion = input("Ingresa una expresion: ")
        analizador = Analizador()

        analizador.analizar(expresion)
        print(analizador.lista)

        analizador.automata.crearTablaEstados()
        for x in analizador.automata.tablaEstados:
            print(x)

        convertidor.iniciarAfnAuxiliar(analizador.automata)
        nuevoAfd = convertidor.convertir()
        nuevoAfd.crearTablaEstados()

        print("__________________________________")

        for estado in nuevoAfd.tablaEstados:
            print(estado)

        for estado in nuevoAfd.estados:
            print(estado.final)

        nuevoAfd.dibujarAutomata()
        #analizador.automata.dibujarAutomata()

        while True:
            cadena = input('Ingresa una cadena a evaluar:')
            print(nuevoAfd.evaluarCadena(cadena))
            if input('Quieres otra? s/n   ') != 's':
                break

main = Main()
main.iniciar()
