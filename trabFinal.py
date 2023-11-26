from ply.lex import lex
from ply.yacc import yacc
import sys
import yaml
print("Parser de lingugem inventada")
def printLinha():
    print("-"*80)

# Palavras reservadas
reservadas = {
    'if': 'IF',
    'while': 'WHILE'
}
#Definição dos tokens
tokens = ['FINAL', 'IGUAL','ADD', 'SUB', 'MUL', 'DIV', 'LPAR', 'RPAR', 'NUM', 'ID', 'MAIOR', 'MENOR', 'MAIORIG', 'MENORIG', 'DIF',
             'IGUAL2', 'DOISPONTOS', 'FUNCTION'
         ] + list(reservadas.values())

t_ignore = ' \t'
t_FINAL = r';'
t_IGUAL = r'='
t_ADD = r'\+'
t_SUB = r'-'
t_LPAR = r'\('
t_RPAR = r'\)'
t_IGUAL2 = r'=='
t_DIF = r'!='
t_MENOR = r'<'
t_MENORIG = r'<='
t_MAIOR = r'>'
t_MAIORIG = r'>='
t_DOISPONTOS =r':'
t_MUL = r'\*'
t_DIV = r'\/'

def t_FUNCTION(t):
    r'FUNCTION'
    return t

# Criação da tabela de símbolos
tabela_simbolo = {}
class InternalError(Exception):
    def __init__(self, msg):
        super().__init__(f"Internal error: {msg}")

def add_symbol(symbol, sym_type, lineno, **kwargs):
    kwargs["name"] = symbol
    kwargs["type"] = sym_type
    kwargs["lineno"] = lineno
    tabela_simbolo[symbol] = kwargs
    return tabela_simbolo[symbol]

def set_symbol(symbol, **kwargs):
    obj = get_symbol(symbol)
    if obj is None:
        raise InternalError(f"Symbol not defined: {symbol}")
    if "name" in kwargs:
        raise InternalError(
            f"Cannot modify symbol '{symbol}' attribute 'name'."
        )
    if "lineno" in kwargs:
        raise InternalError(f"Cannot modify symbol {symbol} attribute 'line'.")
    obj.update(kwargs)


def get_symbol(symbol):
    return tabela_simbolo.get(symbol)

#Definição do token ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t
#Definição do token Numero
def t_NUM(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    # Se houver um caracter inválido retorna essa informação, senão sai do programa.
    if t is not None:
        print("Erro léxico: Caracter inválido: '{}'".format(t.value[0]))
        t.lexer.skip(1)
        sys.exit()

class Programa:
    def __init__(self, program):
        self.program = program

    def __repr__(self):
        return repr(self.program)


class Bloco:
    def __init__(self, other_expression):
        self.other_expression = other_expression

    def __repr__(self):
        result = repr(self.other_expression[0])
        for st in self.other_expression[1:]:
            result += '; ' + repr(st)
        return result


class If:
    def __init__(self, condition, then):
        self.condition = condition
        self.then = then

    def __repr__(self):
        return 'if ' + '('+ repr(self.condition) + ':' + \
               repr(self.then) + ')'+ 'FINAL'


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'while ' + repr(self.condition) + ':' + \
               repr(self.body) + ' FINAL'


class Atribuicao:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return repr(self.identifier) + '=' + repr(self.expression)

class Comparacao:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return repr(self.left) + self.op + repr(self.right)


class Expressao:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return '(' + repr(self.left) + self.op + repr(self.right) + ')'

class Numero:
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return self.number

class Identificador:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return self.identifier

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV')
)

def p_program(p):
    """program : expression other_expression"""
    node = new_node("program")
    append_node(node, p[1])
    if p[2]:
        append_node(node, p[2])
    p[0] = node

def p_other_statement(p):
    """
    other_expression : expression other_expression
        | empty
    """
    if p[1]:
        node = new_node("other_expression")
        append_node(node, p[1])
        if p[2]:
            append_node(node, p[2])
        p[0] = node


def p_expression(p):  # noqa: D205, D400, D403, D415
    """
    expression : value_expr
        | assignment_expression
        | Statement
        | function
    """
    node = new_node("expression")
    append_node(node, p[1])
    p[0] = node

def p_assignment_expression(p):  # noqa: D205, D400, D403, D415
    """assignment_expression : ID IGUAL value_expr"""
    add_symbol(p[1], "VAR", p.lineno(1), value=p[3])
    node = new_node("assignment_expression")
    append_node(node, new_leaf("ID", value=p[1]))
    append_node(node, new_leaf(p.slice[2].type, value=p[2]))
    append_node(node, p[3])
    p[0] = node

def p_statement(p):
    '''Statement : If
                 | While
                 | Assignment'''
    p[0] = p[1]


def p_if(p):
    '''If : IF LPAR Relation RPAR DOISPONTOS other_expression FINAL'''
    p[0] = If(p[2], p[4])


def p_while(p):
    '''While : WHILE Comparison DOISPONTOS other_expression FINAL'''
    p[0] = While(p[2], p[4])


def p_assignment(p):
    'Assignment : Id IGUAL Expression'
    p[0] = Atribuicao(p[1], p[3])


def p_comparison(p):
    '''Comparison : Expression Relation Expression
                | NUM Relation NUM
                | NUM Relation Expression
                | Expression Relation NUM'''
    p[0] = Comparacao(p[1], p[2], p[3])


def p_relation(p):
    '''Relation : MAIOR
                | MENOR
                | MAIORIG
                | MENORIG
                | IGUAL2
                | DIF '''
    p[0] = p[1]

def p_expression_binary(p):
    '''value_expr : value_expr ADD value_expr
                  | value_expr SUB value_expr
                  | value_expr MUL value_expr
                  | value_expr DIV value_expr
                  | value_expr ADD NUM
                  | value_expr SUB NUM
                  | value_expr MUL NUM
                  | value_expr DIV NUM
                  | NUM ADD value_expr
                  | NUM SUB value_expr
                  | NUM MUL value_expr
                  | NUM DIV value_expr
                  | NUM ADD NUM
                  | NUM SUB NUM
                  | NUM MUL NUM
                  | NUM DIV NUM
                  '''
    node = new_node("value_expr")
    append_node(node, p[1])
    append_node(node, new_leaf(p.slice[2].type, value=p[2]))
    append_node(node, p[3])
    p[0] = node


def p_expression_num(p):
    'Expression : NUM'
    p[0] = Numero(p[1])


def p_expression_id(p):
    'Expression : ID'
    p[0] = p[1]

def p_id(p):
    'Id : ID'
    p[0] = Identificador(p[1])

def p_value_expr_par(p):
    """value_expr : LPAR value_expr RPAR"""
    node = new_node("value_expr")
    append_node(node, new_leaf(p.slice[1].type, value=p[1]))
    append_node(node, p[2])
    append_node(node, new_leaf(p.slice[3].type, value=p[3]))
    p[0] = node


def p_value_expr_num(p):
    """value_expr : NUM"""
    node = new_node("value_expr")
    leaf = new_leaf("NUM", value=p[1])
    append_node(node, leaf)
    p[0] = node


def p_value_expr_id(p):
    """value_expr : ID"""
    sym = get_symbol(p[1])
    if sym is None:
        print("p",p[0],p)
        raise Exception(f"Undefined symbol: {p[1]}: {p.lineno(1)}")
    node = new_node("value_expr")
    leaf = new_leaf("ID", value=p[1])
    append_node(node, leaf)
    p[0] = node


def p_empty(p):
    """empty :"""
    p[0] = None

def p_function(p):
    '''function : FUNCTION ID LPAR RPAR DOISPONTOS other_expression FINAL'''
    add_symbol(p[2], "Função", p.lineno(2))
    node = new_node("function")
    leaf = new_leaf("ID", value=p[2])
    append_node(node, leaf)
    leaf = new_leaf("LPAR", value=p[3])
    append_node(node, leaf)
    leaf = new_leaf("RPAR", value=p[4])
    append_node(node, leaf)
    leaf = new_leaf("DOISPONTOS", value=p[5])
    append_node(node, leaf)
    leaf = new_leaf("other_expression", value=p[6])
    append_node(node, leaf)
    p[0] = node

def p_error(p):
    if p is not None:
        print("Erro de sintaxe: ", p)
        sys.exit()

# Criação da arvore de derivação
def new_node(name):
    return dict(name=name, children=[])

def append_node(node, new_node):
    assert isinstance(node, dict) and "children" in node
    node["children"].append(new_node)

def new_leaf(name, **kwargs):
    return dict(name=name, value=kwargs)

scanner = lex()
teste = scanner.input('''
c = 0
FUNCTION teste(): 
c = 5;
FUNCTION teste2():
c = 10;
''')
printLinha()
parser = yacc()
ast = parser.parse(teste, lexer=scanner)
print("Árvore de derivação:\n", yaml.dump(ast, indent=2, sort_keys=False))