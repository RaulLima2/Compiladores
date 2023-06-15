import re
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
    T.add_production('PROGRAM',['DECLS','STMTS','$'])
    T.add_production('DECLS',['DECLS2','DECLS'])
    T.add_production('DECLS2',['DECL'])
    T.add_production('DECLS2',[])
    T.add_production('DECL', ['int','id'])
    T.add_production('DECL', ['float','id'])
    T.add_production('STMTS', ['STMTS2', 'STMTS'])
    T.add_production('STMTS2', ['STMT'])
    T.add_production('STMT', ['ASSIGN'])
    T.add_production('STMT', ['LOOP'])
    T.add_production('STMT', ['IF'])
    T.add_production('STMT', ['PRINT'])
    T.add_production('ASSIGN', ['id','assign','EXPR'])
    T.add_production('PRINT',['print','id'])
    T.add_production('LOOP',['while', 'EXPR_C','do', 'STMT','STMTS','endWhile'])
    T.add_production('EXPR',['T','E2'])
    T.add_production('IF',['if','EXPR_C','then', 'STMT', 'STMTS', 'IF2'])
    T.add_production('IF2',['endif'])
    T.add_production('IF2',['else','STMT','STMTS','endif'])
    T.add_production('E2',['plus','T','E2'])
    T.add_production('E2',['minus','T','E2'])
    T.add_production('E2',[])
    T.add_production('T',['F','T2'])
    T.add_production('T2',['mul','F','T2'])
    T.add_production('T2',['div','F','T2'])
    T.add_production('T2',[])
    T.add_production('F',['int_num'])
    T.add_production('F',['float_num'])
    T.add_production('F',['id'])
    T.add_production('F',['(','EXPR',')'])
    T.add_production('EXPR_C',['EXPR','COMPARATOR','EXPR'])
    T.add_production('COMPARATOR',['equal','not_equal','less_than','greater_than','less_equal','greater_equal'])
    return T

def create_produtction_table()->dict:
    regex_table:dict = {
        r'^float$': 'float',
        r'^int$': 'int',
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
        r'^\$': 'break_line',
        r'^if$': 'if',
        r'^endif$':'endif',
        r'^else$': 'else'
    }
    return regex_table



if __name__ in '__main__':
    gra:Grammar = create_gramar()
    L = guided_ll1_parser(gra)
