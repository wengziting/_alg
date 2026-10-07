def sym_diff(expr, var='x'):

    if isinstance(expr, (int, float)):
        return 0

    if isinstance(expr, str):
        return 1 if expr == var else 0

    op = expr[0]

    if op == '+':
        return ('+', sym_diff(expr[1], var), sym_diff(expr[2], var))

    elif op == '-':
        return ('-', sym_diff(expr[1], var), sym_diff(expr[2], var))
        

    elif op == '*':
        u, v = expr[1], expr[2]
        return ('+', ('*', sym_diff(u, var), v), ('*', u, sym_diff(v, var)))
        

    elif op == '/':
        u, v = expr[1], expr[2]
        num = ('-', ('*', sym_diff(u, var), v), ('*', u, sym_diff(v, var)))
        den = ('^', v, 2)
        return ('/', num, den)
        
    elif op == '^':
        base, exp = expr[1], expr[2]
        if isinstance(exp, (int, float)):
            new_exp = ('^', base, exp - 1) if exp - 1 != 1 else base
            return ('*', ('*', exp, new_exp), sym_diff(base, var))
            
    elif op == 'sin':
        u = expr[1]
        return ('*', ('cos', u), sym_diff(u, var))
        
    elif op == 'cos':
        u = expr[1]
        return ('*', ('-', 0, ('sin', u)), sym_diff(u, var))

    raise ValueError(f"未知的運算符: {op}")

expr = ('+', ('^', 'x', 3), ('*', ('sin', 'x'), 'x'))
d_expr = sym_diff(expr, 'x')

print("原表達式 AST:", expr)
print("微分結果 AST:", d_expr)
