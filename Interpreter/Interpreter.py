class Interpreter():
    
    __sam_code:list[str] = []

    def __init__(self,ts,predict_algorithm):
        Program(ts, predict_algorithm)

    def Program(ts:token_sequence, p:predict_algorithm):
        if ts.peek() in p.predict(44):
            Decls(ts, p)
            #Stmt(ts, p)# adcionar a quebra de linha

            Stmts(ts, p)
            ts.match('$')
        else:
            print('Syntax Error: ',ts.peek())
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
            print('Syntax Error: ',ts.peek())
            exit(0)

    def Decl(ts:token_sequence, p:predict_algorithm):
        if ts.peek() in p.predict(47):
            ts.match('int')
            ts.match('id')
            __sam_code.append()
        elif ts.peek() in p.predict(48):
            ts.match('float')
            ts.match('id')
            __sam_code.append()
        else:
            print('Syntax Error: ',ts.peek())
            exit(0)

    def Stmts(ts:token_sequence, p:predict_algorithm):
        if ts.peek() in p.predict(49):
            Stmt(ts, p)
            Stmts(ts, p)
        elif ts.peek() in p.predict(50):
            return
        else:
            print('Syntax Error: ',ts.peek())
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
            print('Syntax Error: ',ts.peek())
            exit(0)
            
        
    def Assign(ts:token_sequence, p:predict_algorithm):
        if ts.peek() in p.predict(55):
            ts.match('id')
            ts.match('assign')
            Expr(ts, p)
        else:
            print('Syntax Error: ',ts.peek())
            exit(0)

    def Print(ts:token_sequence, p:predict_algorithm):
        if ts.peek() in p.predict(56):
            ts.match('print')
            ts.match('id')
        else:
            print('Syntax Error: ',ts.peek())
            exit(0)

    def Loop(ts:token_sequence, p:predict_algorithm):
        if ts.peek() in p.predict(57):
            ts.match('while')
            __sam_code.append('')
            Expr_c(ts, p)
            ts.match('do')
            Stmt(ts, p)
            Stmts(ts, p)
            ts.match('endWhile')
        else:
            print('Syntax Error: ',ts.peek())
            exit(0)

    def Expr(ts:token_sequence, p:predict_algorithm):
        if ts.peek() in p.predict(58):
            T(ts, p)
            E2(ts, p)
        else:
            print('Syntax Error: ',ts.peek())
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
            print('Syntax Error: ',ts.peek())
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
            print('Syntax Error: ',ts.peek())
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
            print('Syntax Error: ',ts.peek())
            exit(0)

    def T(ts:token_sequence, p:predict_algorithm):
        if ts.peek() in p.predict(65):
            F(ts, p)
            T2(ts, p)
        else:
            print('Syntax Error: ',ts.peek())
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
            print('Syntax Error: ',ts.peek())
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
            print('Syntax Error: ',ts.peek())
            exit(0)

    def Expr_c(ts:token_sequence, p:predict_algorithm):
        if  ts.peek() in p.predict(73):
            Expr(ts, p)
            Comparator(ts, p)
            Expr(ts, p)
        else:
            print('Syntax Error: ',ts.peek())
            exit(0)

    def Comparator(ts:token_sequence, p:predict_algorithm):
        if ts.peek() in p.predict(74):
            ts.match('equal')
        elif ts.peek() in p.predict(75):
            ts.match('not_equal')
        elif ts.peek() in p.predict(76):
            ts.match('less_than')
        elif ts.peek() in p.predict(77):
            ts.match('greater_than')
        elif ts.peek() in p.predict(78):
            ts.match('less_equal')
        elif ts.peek() in p.predict(79):
            ts.match('greater_equal')
        else:
            print('Syntax Error: ',ts.peek())
            exit(0)