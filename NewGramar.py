import re
from token_sequence import token_sequence
from predict import predict_algorithm
from grammar import Grammar
from ll1_check import is_ll1

# Create Grammar T
def create_gramar()->Grammar:
    T:Grammar = Grammar()
    terminal:list[str] = ['int','float','id','assign', 'print','while','do', 'endWhile', 'if', 'then', 'endif', 'else', 'plus', 'minus', 'mul', 'div', 'int_num', 'float_num', '(',')','equal','not_equal','less_than','greater_than','less_equal','greater_equal','$']
    non_terminal:list[str] = ['PROGRAM', 'STMTS','STMT', 'DECLS', 'DECL', 'PRINT', 'LOOP', 'EXPR', 'ASSIGN', 'IF', 'IF2', 'E2', 'T', 'T2', 'F', 'EXPR_C', 'COMPARATOR']
    for item in terminal:
        T.add_terminal(item)
    for item in non_terminal:
        T.add_nonterminal(item)
    # add production
    T.add_production('PROGRAM',['DECLS', 'STMTS','$']) # 44
    T.add_production('DECLS',['DECL','DECLS']) # 45
    T.add_production('DECLS',[]) # 46
    T.add_production('DECL', ['int','id']) # 49
    T.add_production('DECL', ['float','id']) # 50
    T.add_production('STMTS', ['STMT', 'STMTS']) # 51
    T.add_production('STMTS', []) # 52
    T.add_production('STMT', ['ASSIGN']) # 53
    T.add_production('STMT', ['LOOP']) # 54
    T.add_production('STMT', ['IF']) # 55
    T.add_production('STMT', ['PRINT']) # 56
    T.add_production('ASSIGN', ['id','assign','EXPR']) # 57
    T.add_production('PRINT',['print','id']) # 58
    T.add_production('LOOP',['while', 'EXPR_C','do', 'STMT','STMTS','endWhile']) # 59
    T.add_production('EXPR',['T','E2']) # 60
    T.add_production('IF',['if','EXPR_C','then', 'STMT','STMTS', 'IF2']) # 61
    T.add_production('IF2',['endif']) # 62
    T.add_production('IF2',['else','STMT','STMTS','endif']) # 63
    T.add_production('E2',['plus','T','E2']) # 64
    T.add_production('E2',['minus','T','E2']) # 65
    T.add_production('E2',[]) # 66
    T.add_production('T',['F','T2']) # 67
    T.add_production('T2',['mul','F','T2']) # 68
    T.add_production('T2',['div','F','T2']) # 69
    # T.add_production('T2',['$'])
    T.add_production('T2',[]) # 70
    T.add_production('F',['int_num']) # 71
    T.add_production('F',['float_num']) # 72
    T.add_production('F',['id']) # 73
    T.add_production('F',['(','EXPR',')'])  # 74
    T.add_production('EXPR_C',['EXPR','COMPARATOR','EXPR']) # 75
    T.add_production('COMPARATOR',['equal']) # 76
    T.add_production('COMPARATOR',['not_equal']) # 77
    T.add_production('COMPARATOR',['less_than']) # 78
    T.add_production('COMPARATOR',['greater_than']) # 78
    T.add_production('COMPARATOR',['less_equal']) # 79
    T.add_production('COMPARATOR',['greater_equal']) # 80
    return T

def create_produtction_table()->dict:
    regex_table:dict = {
        r'^int$': 'int',
        r'^float$': 'float',
        r'^print$': 'print',
        r'^[a-zA-Z]$' : 'id',
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
        r'^\\$': 'div',
        r'^[0-9]+$': 'int_num',
        r'^[0-9]+\.[0-9]+$': 'float_num',
        r'^\($': '(',
        r'^\)$': ')',
        r'^if$': 'if',
        r'^then$': 'then',
        r'^endif$':'endif',
        r'^else$': 'else',
        r'^while$':'while',
        r'^do$':'do',
        r'^endWhile$': 'endWhile'
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
    print(token_sequence)
    return token_sequence

def Program(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(44):
        Decls(ts, p)
        #Stmt(ts, p)
        Stmts(ts, p)
        ts.match('$')
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def Decls(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(45):
        Decl(ts, p)
        Decls(ts, p)
    #elif ts.peek() in p.predict(48):
        #ts.match('$')
    elif ts.peek() in p.predict(46):
        return
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def Decl(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(47):
        ts.match('int')
        ts.match('id')
    elif ts.peek() in p.predict(48):
        ts.match('float')
        ts.match('id')
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def Stmts(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(49):
        Stmt(ts, p)
        Stmts(ts, p)
    elif ts.peek() in p.predict(50):
        return
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def Stmt(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(51):
        Assign(ts, p)
    elif ts.peek() in p.predict(52):
        Loop(ts, p)
    elif ts.peek() in p.predict(53):
        If(ts, p)
    elif ts.peek() in p.predict(54):
        Print(ts, p)
    else:
        print('Lexical error: ',ts.peek())
        exit(0)
        
    
def Assign(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(55):
        ts.match('id')
        ts.match('assign')
        Expr(ts, p)
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def Print(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(56):
        ts.match('print')
        ts.match('id')
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def Loop(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(57):
        ts.match('while')
        Expr_c(ts, p)
        ts.match('do')
        Stmt(ts, p)
        Stmts(ts, p)
        ts.match('endWhile')
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def Expr(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(58):
        T(ts, p)
        E2(ts, p)
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def If(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(59):
        ts.match('if')
        Expr_c(ts, p)
        ts.match('then')
        Stmt(ts, p)
        Stmts(ts, p)
        If2(ts, p)
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def If2(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(60):
        ts.match('endif')
    elif ts.peek() in p.predict(61):
        ts.match('else')
        Stmt(ts, p)
        Stmts(ts, p)
        ts.match('endif')
    else:
        print('Lexical error: ',ts.peek())
        exit(0)
        
def E2(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(62):
        ts.match('plus')
        T(ts, p)
        E2(ts, p)
    elif ts.peek() in p.predict(63):
        ts.match('minus')
        T(ts, p)
        E2(ts, p)
    elif ts.peek() in p.predict(64):
        return
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def T(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(65):
        F(ts, p)
        T2(ts, p)
    else:
        print('Lexical error: ',ts.peek())
        exit(0) 

def T2(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(66):
        ts.match('mul')
        F(ts, p)
        T2(ts, p)
    elif ts.peek() in p.predict(67):
        ts.match('div')
        F(ts, p)
        T2(ts, p)
    elif ts.peek() in p.predict(68):
        return
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def F(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(69):
        ts.match('int_num')
    elif ts.peek() in p.predict(70):
        ts.match('float_num')
    elif ts.peek() in p.predict(71):
        ts.match('id')
    elif ts.peek() in p.predict(72):
        ts.match('(')
        Expr(ts, p)
        ts.match(')')
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def Expr_c(ts:token_sequence, p:predict_algorithm):
    if  ts.peek() in p.predict(73):
        Expr(ts, p)
        Comparator(ts, p)
        Expr(ts, p)
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

def Comparator(ts:token_sequence, p:predict_algorithm):
    if ts.peek() in p.predict(74):
        ts.match('equal')
    elif ts.peek() in p.predict(75):
        ts.match('not_equal')
    elif ts.peek() in p.predict(76):
        ts.match('less_than')
    elif ts.peek() in p.predict(77):
        ts.match('greather_than')
    elif ts.peek() in p.predict(78):
        ts.match('less_equal')
    elif ts.peek() in p.predict(79):
        ts.match('greater_equal')
    else:
        print('Lexical error: ',ts.peek())
        exit(0)

if __name__ in '__main__':
    filename:str = 'teste.t'
    gra:Grammar = create_gramar()
    tokens = lexical_analyser(filename)
    p_algorithm = predict_algorithm(gra)
    ts = token_sequence(tokens)
    print(is_ll1(gra, p_algorithm))
    Program(ts, p_algorithm)
