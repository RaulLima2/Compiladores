import re
from language_t.table_production.table_production import create_produtction_table

def lexical_analyser(filepath:str, tbl_symbol:dict) -> list[str]:
    regex_table = create_produtction_table()
    with open(filepath,'r') as readline:
        tokens:list = []
        n_line:list = []
        token_sequence:list[str] = []
        for line in readline:
            if '' in line.split(' '):
                n_line = [item for item in line.split(' ') if item != '']
                tokens = tokens + n_line
            else:
                n_line = line.split(' ')
                tokens = tokens + n_line
        for token in tokens:
            found:bool = False
            for regex,category in regex_table.items():
                if re.match(regex,token.replace('\n','')):
                    tbl_symbol.put(key=category,val=token.replace('\n',''))
                    token_sequence.append(category)
                    found = True
                    break
            if not found:
                print('Lexical Error: ',token)
                exit(0)
    token_sequence.append('$')
    print(token_sequence)
    return token_sequence
