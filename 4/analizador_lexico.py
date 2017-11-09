import expresiones_regulares
from ply.lex import lex


class AnalizadorLexico:

    def __init__(self):
        self.lexer = lex(module=expresiones_regulares)

    def analizar(self, cadena):
        self.lexer.input(cadena)
        token = self.lexer.token()

        while token is not None:
            print(token)
            token = self.lexer.token()
