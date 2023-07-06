import re
from token_sequence import token_sequence
from predict import predict_algorithm
from grammar import Grammar
from guided_ll1 import guided_ll1_parser


# Create Grammar T
def create_gramar()->Grammar:
    T:Grammar = Grammar()
    terminal:list[str] = ['int','float','id','assign', 'print','while','do', 'endWhile', 'if', 'then', 'endif', 'else', 'plus', 'minus', 'mul', 'div', 'int_num', 'float_num', '(',')','equal','not_equal','less_than','greater_than','less_equal','greater_equal','$']
    non_terminal:list[str] = ['PROGRAM', 'STMTS','STMTS2', 'STMT', 'DECLS', 'DECLS2','DECL', 'PRINT', 'LOOP', 'EXPR', 'ASSIGN', 'IF', 'IF2', 'E2', 'T', 'T2', 'F', 'EXPR_C', 'COMPARATOR']
    for item in terminal:
        T.add_terminal(item)
    for item in non_terminal:
        T.add_nonterminal(item)
    # add production
    T.add_production('PROGRAM',['DECLS','STMTS','$']) #
    T.add_production('DECLS',['DECLS2','DECLS']) #
    T.add_production('DECLS2',['DECL']) #
    #T.add_production('DECLS2',[])
    T.add_production('DECL', ['int','id']) #
    T.add_production('DECL', ['float','id']) #
    T.add_production('STMTS', ['STMTS2', 'STMTS']) #
    T.add_production('STMTS2', ['STMT']) #
    T.add_production('STMT', ['ASSIGN']) #
    T.add_production('STMT', ['LOOP']) #
    T.add_production('STMT', ['IF']) #
    T.add_production('STMT', ['PRINT']) #
    T.add_production('ASSIGN', ['id','assign','EXPR']) #
    T.add_production('PRINT',['print','id']) #
    T.add_production('LOOP',['while', 'EXPR_C','do', 'STMT','STMTS','endWhile']) #
    T.add_production('EXPR',['T','E2']) #
    T.add_production('IF',['if','EXPR_C','then', 'STMT', 'STMTS', 'IF2']) #
    T.add_production('IF2',['endif']) #
    T.add_production('IF2',['else','STMT','STMTS','endif']) #
    T.add_production('E2',['plus','T','E2']) #
    T.add_production('E2',['minus','T','E2']) #
    T.add_production('E2',[]) #
    T.add_production('T',['F','T2']) #
    T.add_production('T2',['mul','F','T2']) #
    T.add_production('T2',['div','F','T2']) #
    T.add_production('T2',[]) #
    T.add_production('F',['int_num']) #
    T.add_production('F',['float_num']) #
    T.add_production('F',['id']) #
    T.add_production('F',['(','EXPR',')'])  #
    T.add_production('EXPR_C',['EXPR','COMPARATOR','EXPR']) #
    T.add_production('COMPARATOR',['equal'])
    T.add_production('COMPARATOR',['not_equal'])
    T.add_production('COMPARATOR',['less_than'])
    T.add_production('COMPARATOR',['greater_than'])
    T.add_production('COMPARATOR',['less_equal'])
    T.add_production('COMPARATOR',['greater_equal'])
    return T

def create_produtction_table()->dict:
    regex_table:dict = {
        r'^int$': 'int',
        r'^float$': 'float',
        r'^print$': 'print',
        r'^[abcdeghjlmnoqrstuvwxyz]$' : 'id',
        r'^:$':'assign',
        r'^=$':'equal',
        r'^!=$':'not_equal',
        r'^>$':'greater_than',
        r'^<$':'less_than',
        r'^<=$':'less_equal',
        r'^>=$':'greater_equal',
        r'^\+$': 'plus',
        r'^\-$': 'minus',
        r'^\*$': 'mul',
        r'^\/\$': 'div',
        r'^[0-9]+$': 'int_num',
        r'^[0-9]+\.[0-9]+$': 'float_num',
        r'^\($': '(',
        r'^\)$': ')',
        r'^\$': '',
        r'^if$': 'if',
        r'^endif$':'endif',
        r'^else$': 'else'
    }
    return regex_table

def lexical_analyser(filepath:str) -> list[str]:
    regex_table = create_produtction_table()
    with open(filepath,'r') as readline:
        token_sequence:list[str] = []
        tokens:list = []
        for line in readline:
            tokens = tokens + line.split(' ')
        for token in tokens:
            found:bool = False
            for regex,category in regex_table.items():
                if re.match(regex,token):
                    token_sequence.append(category)
                    found = True
            if not found:
                print('Lexical error: ',token)
                exit(0)
    token_sequence.append('$')
    return token_sequence

def Program(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(16):
        Dcls(ts, p)
        Stmts(ts, p)
        ts.match('$')

def Dcls(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(2):
        Decls()
        Decls2()

def Decls2(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(3):
        Decls()

def Decl(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(4):
        ts.metch('int')
        ts.metch('id')
    elif ts.peek() in p.predict(5):
        ts.metch('float')
        ts.metch('id')
    else:
        return

def Stmts(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(6):
        Stmts2(ts, p)
        Stmts(ts, p)

def Stmts2(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(7):
        Stmt(ts, p)

def Stmt(ts, p):
    if ts.peek() in p.predict(8):
        Assign(ts, p)
    elif ts.peek() in p.predict(9):
        Loop(ts, p)
    elif ts.peek() in p.predict(10):
        If(ts, p)
    elif ts.peek() in p.predict(11):
        Print(ts, p)
    
def Assign(ts, p):
    if ts.peek() in p.predict(12):
        ts.match('id')
        ts.match('assign')
        Expr(ts, p)

def Print(ts, p):
    if ts.peek() in p.predict(14):
        ts.match('print')
        ts.match('id')

def Loop(ts, p):
    if ts.peek() in p.predict(15):
        ts.metch('while')
        Expr_c(ts, p)
        ts.metch('do')
        Stmt(ts, p)
        Stmts(ts, p)
        ts.match('endWhile')

def Expr(ts, p):
    if ts.peek() in p.predict(16):
        T(ts, p)
        E2(ts, p)

def If(ts, p):
    if ts.peek() in p.predict(17):
        ts.metch('if')
        Expr_c(ts, p)
        ts.metch('then')
        Stmt(ts, p)
        Stmts(ts, p)
        If2(ts, p)

def If2(ts, p):
    if ts.peek() in p.predict(18):
        ts.metch('endif')
    elif ts.peek() in p.predict(19):
        ts.metch('else')
        Stmt(ts, p)
        Stmts(ts, p)
        ts.metch('endif')
        
def E2(ts, p):
    if ts.peek() in p.predict(20):
        ts.metch('plus')
        T(ts, p)
        E2(ts, p)
    elif ts.peek() in p.predict(21):
        ts.metch('minus')
        T(ts, p)
        E2(ts, p)

def T(ts, p):
    if ts.peek() in p.predict(22):
        F(ts, p)
        T2(TS, P)

def T2(ts, p):
    if ts.peek() in p.predict(23):
        ts.metch('mul')
        F(ts, p)
        T2(ts, p)
    elif ts.peek() in p.predict(24):
        ts.metch('div')
        F(ts, p)
        T2(ts, p)
    elif ts.peek() in p.predict(25):
        return

def f(ts, p):
    if ts.peek() in p.predict(26):
        ts.metch('int_num')
    elif ts.peek() in p.predict(27):
        ts.metch('float_num')
    elif ts.peek() in p.predict(28):
        ts.metch('id')
    elif ts.peek() in p.predict(29):
        ts.metch('(')
        Expr(ts, p)
        ts.metch(')')

def Expr_c(ts, p):
    if  ts.peek() in p.predict(30):
        Expr(ts, p)
        Comparator(ts, p)
        Expr(ts, p)

def Comparator(ts, p):
    if ts.peek() in p.predict(31):
        ts.metch('equal')
    elif ts.peek() in p.predict(32):
        ts.metch('not_equal')
    elif ts.peek() in p.predict(33):
        ts.metch('less_than')
    elif ts.peek() in p.predict(34):
        ts.metch('greather_than')
    elif ts.peek() in p.predict(35):
        ts.metch('less_equal')
    elif ts.peek() in p.predict(36):
        ts.metch('greater_equal')


if __name__ in '__main__':
    filename = 'teste.t'
    gra:Grammar = create_gramar()
    tokens = lexical_analyser(filename)
    ts = token_sequence(tokens)
    L = guided_ll1_parser(gra)
    L.parse(ts)