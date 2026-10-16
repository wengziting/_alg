class Expr:
    def free_vars(self):
        pass

class Var(Expr):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def free_vars(self):
        return {self.name}

class Abs(Expr):
    def __init__(self, param, body):
        self.param = param
        self.body = body
    def __str__(self):
        return f"(λ{self.param}.{self.body})"
    def free_vars(self):
        return self.body.free_vars() - {self.param}

class App(Expr): # 函數應用 (e.g., M N)
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg
    def __str__(self):
        return f"({self.func} {self.arg})"
    def free_vars(self):
        return self.func.free_vars() | self.arg.free_vars()

var_counter = 0
def fresh_var(base_name):
    global var_counter
    var_counter += 1
    return f"{base_name}{var_counter}"

def substitute(expr, var_name, replacement):
    if isinstance(expr, Var):
        if expr.name == var_name:
            return replacement
        return expr
    elif isinstance(expr, App):
        return App(substitute(expr.func, var_name, replacement),
                   substitute(expr.arg, var_name, replacement))
    elif isinstance(expr, Abs):
        if expr.param == var_name:
            return expr 

        if expr.param in replacement.free_vars():
            new_param = fresh_var(expr.param)
            new_body = substitute(expr.body, expr.param, Var(new_param))
            return Abs(new_param, substitute(new_body, var_name, replacement))
        
        return Abs(expr.param, substitute(expr.body, var_name, replacement))

def reduce_step(expr):
    if isinstance(expr, App):
        # 找到 Redex: (\x. M) N -> M[x := N]
        if isinstance(expr.func, Abs):
            return substitute(expr.func.body, expr.func.param, expr.arg), True

        new_func, reduced = reduce_step(expr.func)
        if reduced:
            return App(new_func, expr.arg), True

        new_arg, reduced = reduce_step(expr.arg)
        if reduced:
            return App(expr.func, new_arg), True
            
        return expr, False

    elif isinstance(expr, Abs):

        new_body, reduced = reduce_step(expr.body)
        return Abs(expr.param, new_body), reduced

    elif isinstance(expr, Var):
        return expr, False

def evaluate(expr, max_steps=100):
    print(f"初始: {expr}")
    step = 1
    current_expr = expr
    while step <= max_steps:
        next_expr, reduced = reduce_step(current_expr)
        if not reduced:
            print("=> 已達 Normal Form (無法再化簡)\n")
            break
        print(f"步驟 {step}: {next_expr}")
        current_expr = next_expr
        step += 1
    if step > max_steps:
        print("=> 達到最大步數限制 (可能無限迴圈)\n")
