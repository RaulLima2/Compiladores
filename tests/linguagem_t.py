import re
from language_t import table_symbol
from language_t.grammar import grammar
from language_t.token_sequence.token_sequence import token_sequence
from language_t.predict import predict_algorithm
from language_t.lexical_analyser import lexical_analyser
from language_t.syntax_analyser.syntax_analyser import Program
from language_t.guided_ll1.ll1_check import is_ll1
from language_t.guided_ll1.guided_ll1 import guided_ll1_parser

 # Create Grammar T
def create_gramar()->grammar.Grammar:
    T:Grammar = grammar.Grammar()
    terminal:list[str] = ['int','float','id','assign', 'print','while','do', 'end_while', 'if', 'then', 'endif', 'else', 'plus', 'minus', 'mul', 'div', 'int_num', 'float_num', '(',')','equal','not_equal','less_than','greater_than','less_equal','greater_equal','$']
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
    T.add_production('LOOP',['while', 'EXPR_C','do', 'STMT','STMTS','end_while']) # 59
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

if __name__ in '__main__':
    filename:str = 'data/teste.t'
    tbl_symbol = table_symbol.table_symbol(None, None)
    gra:grammar.Grammar = create_gramar()
    p_algorithm = predict_algorithm(gra)
    # print(is_ll1(gra, p_algorithm))
    tokens = lexical_analyser.lexical_analyser(filename, tbl_symbol)
    ts = token_sequence(tokens)
    # tbl_symbol.p()
    # p = guided_ll1_parser(gra)
    # p.parse(ts)
    Program(ts, p_algorithm)
