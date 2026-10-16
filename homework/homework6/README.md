# 深入淺出：Lambda Calculus 解譯器 (The Ultimate Lambda Calculus Interpreter)

本專案是一個基於純 Python 實作的**無型別 Lambda Calculus (Untyped Lambda Calculus)** 逐步解譯器。

Lambda Calculus 是由阿隆佐·邱奇（Alonzo Church）在 1930 年代提出的形式系統，它證明了「只要有變數、函數宣告與函數呼叫」，就能夠計算出任何圖靈機可以計算的問題。本專案透過物件導向的方式建構抽象語法樹（AST），並精準實作了**Alpha 轉換（Alpha-conversion）**與**Beta 歸約（Beta-reduction）**，完整暴露出計算的每一道軌跡。

---



## 1. 完整解譯器原始碼 (Source Code)

無需安裝任何套件，請將以下程式碼全選並儲存為 `lambda_calc.py` 即可執行。這段程式碼包含了核心解譯器與幾組經典的測試案例。

```python
# lambda_calc.py

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

class Abs(Expr): # Lambda 抽象 (e.g., \x. M)
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

# 產生不重複的新變數名稱 (Alpha 轉換使用)
var_counter = 0
def fresh_var(base_name):
    global var_counter
    var_counter += 1
    return f"{base_name}{var_counter}"

# 實作代換: M[x := N] (把 M 裡面的 x 換成 N)
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
            return expr # 變數被遮蔽 (Shadowing)
        
        # 避免變數捕捉 (Variable Capture): 
        # 如果 Lambda 的參數出現在 replacement 的自由變數中，需進行 Alpha 轉換
        if expr.param in replacement.free_vars():
            new_param = fresh_var(expr.param)
            new_body = substitute(expr.body, expr.param, Var(new_param))
            return Abs(new_param, substitute(new_body, var_name, replacement))
        
        return Abs(expr.param, substitute(expr.body, var_name, replacement))

# 執行單步 Beta 歸約 (Normal Order: 最左最外優先)
def reduce_step(expr):
    if isinstance(expr, App):
        # 找到 Redex: (\x. M) N -> M[x := N]
        if isinstance(expr.func, Abs):
            return substitute(expr.func.body, expr.func.param, expr.arg), True
        
        # 嘗試化簡左半部
        new_func, reduced = reduce_step(expr.func)
        if reduced:
            return App(new_func, expr.arg), True
            
        # 嘗試化簡右半部
        new_arg, reduced = reduce_step(expr.arg)
        if reduced:
            return App(expr.func, new_arg), True
            
        return expr, False

    elif isinstance(expr, Abs):
        # 化簡 Lambda 內部
        new_body, reduced = reduce_step(expr.body)
        return Abs(expr.param, new_body), reduced

    elif isinstance(expr, Var):
        return expr, False

# 執行並印出完整過程
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


# ==========================================
# 測試區塊 (執行腳本時會自動輸出結果)
# ==========================================
if __name__ == "__main__":
    x, y, z, f = Var('x'), Var('y'), Var('z'), Var('f')
    
    # 測試 1: Identity 函數 (λx.x) 應用於 y
    print("=== 測試 1: Identity 函數 ===")
    evaluate(App(Abs('x', x), y))

    # 測試 2: Church Booleans AND TRUE FALSE -> FALSE
    TRUE_val = Abs('x', Abs('y', x))
    FALSE_val = Abs('x', Abs('y', y))
    AND_op = Abs('p', Abs('q', App(App(Var('p'), Var('q')), Var('p'))))
    print("=== 測試 2: 布林邏輯 AND TRUE FALSE ===")
    evaluate(App(App(AND_op, TRUE_val), FALSE_val))

    # 測試 3: Alpha 轉換 (避免變數捕捉)
    print("=== 測試 3: Alpha 轉換測試 ===")
    evaluate(App(Abs('x', Abs('y', App(x, y))), y))

    # 測試 4: Omega 組合子 (無限迴圈限制)
    print("=== 測試 4: Omega 組合子 (無窮迴圈測試，限制 3 步) ===")
    omega_inner = Abs('x', App(x, x))
    evaluate(App(omega_inner, omega_inner), max_steps=3)
