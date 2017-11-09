from afnd import Afn

automata = Afn()

automata.anadirEstado()
automata.anadirEstado()
automata.anadirEstado()
automata.anadirEstado()

automata.anadirTransicion(1,2)
automata.anadirTransicion(2,3)
automata.anadirTransicion(3,4)

automata.anadirFinal(4)
