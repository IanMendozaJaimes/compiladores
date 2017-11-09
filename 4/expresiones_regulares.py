#http://www.dabeaz.com/ply/ply.html
tokens = [
    'COMENTARIO',
    'dje',
    'BOOLEANO',
    'IDENTIFICADOR',
    'CONSTANTE_FLOTANTE',
    'CONSTANTE_ENTERA',
    'INCREMENTO',
    'OPERADOR_ARITMETICO',
    'OPERADOR_LOGICO',
    'ASIGNACION',
    'SEPARACION',
    'MODIFICADOR'
]

reservado = {
   'si' : 'SI',
   'sino' : 'SINO',
   'otros' : 'OTROS',
   'para': 'PARA',
   'mientras': 'MIENTRAS',
   'tocar': 'TOCAR',
   'funcion': 'FUNCION',
   'do': 'DO',
   're': 'RE',
   'mi': 'MI',
   'fa': 'FA',
   'sol': 'SOL',
   'la': 'LA',
   'si': 'SI',
   'retorna': 'RETORNA',
   'piano': 'PIANO',
   'guitarra': 'GUITARRA',
   'flauta': 'FLAUTA',
}

states = (
    ('dje', 'exclusive'),
)

tokens += list(reservado.values());

#Las siguientes son las expresiones regulares de cada clase lexica, con el comportamiento por default de lex
def t_COMENTARIO(t):
    r'(/\*(.|\n)*\*/)|(//.*)'
    t.lineno += t.value.count('\n')
    t.lexer.lexliterals = [t.type]
    return t ##este esta solo para revisar, ya en produccion, esto se quita, no tiene caso que retornemos comentarios

def t_BOOLEANO(t):
    r'verdadero|falso'
    t.lexer.lexliterals = [t.type]
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_]\w*'
    t.lexer.lexliterals = [t.type]
    t.type = reservado.get(t.value,'IDENTIFICADOR')    # Check for reserved words
    return t

def t_CONSTANTE_FLOTANTE(t):
    r'[\d]*[.][\d]+'
    t.lexer.lexliterals = [t.type]
    t.value = float(t.value)
    return t

def t_CONSTANTE_ENTERA(t):
    r'\d+'
    t.lexer.lexliterals = [t.type]
    t.value = int(t.value)
    return t

def t_OPERADOR_ARITMETICO(t):
    r'[\*|\/]'
    t.lexer.lexliterals = [t.type]
    return t

def t_OPERADOR_LOGICO(t):
    r'[=][=]|[<][=]|[>][=]|[!][=]|[<>]'
    t.lexer.lexliterals = [t.type]
    return t

def t_ASIGNACION(t):
    r'[=]'
    t.lexer.lexliterals = [t.type]
    return t

def t_SEPARACION(t):
    r'\(|\)|\[|\]|\{|\}|\,'
    t.lexer.lexliterals = [t.type]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lexliterals = [t.type]
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

#Aqui comienzan las reglas que no usan las operaciones por default de lex
def t_dje(t):
    r'[-|+]'

    aux = t.lexer.lexdata[t.lexer.lexpos-1:t.lexer.lexpos+1]
    if aux == '--' or t.value == '++':
        t.type = 'INCREMENTO'
        t.value = aux
        t.lexer.lexpos = t.lexer.lexpos+1
        t.lexer.begin('INITIAL')
        return t

    if type(t.lexer.lexliterals) is str:
        t.lexer.lexliterals = ['NADA']

    t.lexer.code_start = t.lexer.lexpos
    t.lexer.lexliterals.append(t.value)
    t.lexer.begin('dje')

def t_dje_OPERADOR_ARITMETICO(t):
    r'[+|-]'
    t.value = t.lexer.lexliterals[1]
    t.type = 'OPERADOR_ARITMETICO'
    t.lexer.lexpos = t.lexer.code_start
    t.lexer.lexliterals = [t.type]
    t.lexer.begin('INITIAL')
    return t

def t_dje_CONSTANTE_FLOTANTE(t):
    r'[\d]*[.][\d]+'

    aux = t.lexer.lexliterals[0]
    if aux == 'CONSTANTE_ENTERA' or aux == 'CONSTANTE_FLOTANTE' or aux == 'IDENTIFICADOR' or aux == ')':
        t.type = 'OPERADOR_ARITMETICO'
        t.value = t.lexer.lexliterals[1]
        t.lexer.begin('INITIAL')
        t.lexer.lexpos = t.lexer.code_start
        return t

    t.type = 'CONSTANTE_FLOTANTE'
    t.value = float(t.lexer.lexliterals[1] + t.value)
    t.lexer.begin('INITIAL')
    return t

def t_dje_CONSTANTE_ENTERA(t):
    r'\d+'

    aux = t.lexer.lexliterals[0]
    if aux == 'CONSTANTE_ENTERA' or aux == 'CONSTANTE_FLOTANTE' or aux == 'IDENTIFICADOR' or aux == ')':
        t.type = 'OPERADOR_ARITMETICO'
        t.value = t.lexer.lexliterals[1]
        t.lexer.begin('INITIAL')
        t.lexer.lexpos = t.lexer.code_start
        return t

    t.type = 'CONSTANTE_ENTERA'
    t.value = int(t.lexer.lexliterals[1] + t.value)
    t.lexer.begin('INITIAL')
    return t

def t_dje_IDENTIFICADOR(t):
    r'[a-zA-Z_]\w*'
    t.type = 'OPERADOR_ARITMETICO'
    t.value = t.lexer.lexliterals[1]
    t.lexer.begin('INITIAL')
    t.lexer.lexpos = t.lexer.code_start
    return t

t_dje_ignore = " \t\n"


'''
    Estos metodos son invocados cuando el analizador lexico encuentra un error,
    no obstante el manejador de errores aun no esta programado, por lo que solo se imprime
    un caracter ilegal, mas adelante estos metodos mandaran a llamar al manejador de errores
'''

def t_error(t):
    print ("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

def t_dje_error(t):
    print ("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)
