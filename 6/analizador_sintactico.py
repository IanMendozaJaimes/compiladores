from funciones_sintactico import Manejador_sintactico

class Main():

    def iniciar(self):
        archivo = 'gramaticas.txt'
        analizador = Manejador_sintactico()
        analizador.cargar_gramaticas(archivo)

        print('Producciones:', analizador.producciones)
        print('')
        print('Producidos:', analizador.producidos)
        print('')
        print('Productores', analizador.productores)

        print(analizador.siguiente(input()))


main = Main()
main.iniciar()
