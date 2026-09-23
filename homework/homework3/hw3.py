import itertools

def solve_sat_truth_table(variables, formula):
    """
    使用真值表列舉法解決 SAT 問題
    :param variables: 變數名稱清單，例如 ['A', 'B', 'C']
    :param formula: 邏輯表達式字串，例如 "(A or B) and (not A or C)"
    """
    n_vars = len(variables)
    satisfiable = False
    solutions = []
    
    # 建立真值表表頭
    header = " | ".join(variables) + " || Result"
    separator = "-" * len(header)
    
    print(f"表達式: {formula}")
    print(separator)
    print(header)
    print(separator)
    
    # 產生所有 2^n 種 True/False 組合
    # repeat=n 會產生如 (False, False), (False, True)... 的所有排列
    for values in itertools.product([False, True], repeat=n_vars):
        # 將變數名稱與對應的布林值綁定成字典，例如 {'A': False, 'B': True}
        env = dict(zip(variables, values))
        
        # 使用 eval() 帶入變數值並計算表達式結果
        try:
            result = eval(formula, {}, env)
        except Exception as e:
            print(f"解析表達式時發生錯誤: {e}")
            return
        
        # 將 True/False 轉換為 1/0 方便閱讀 (T/F 也可以)
        row = " | ".join(str(int(v)) for v in values) + f" || {int(result)}"
        print(row)
        
        # 如果結果為 True，記錄這組解
        if result:
            satisfiable = True
            solutions.append(env)
            
    print(separator)
    
    # 輸出最終結論
    if satisfiable:
        print("\n結論: SATISFIABLE (可滿足)")
        print(f"共有 {len(solutions)} 組解:")
        for idx, sol in enumerate(solutions, 1):
            # 格式化輸出解
            sol_str = ", ".join(f"{k}={v}" for k, v in sol.items())
            print(f"  解 {idx}: {sol_str}")
    else:
        print("\n結論: UNSATISFIABLE (不可滿足)")

# ==========================================
# 測試範例
# ==========================================
if __name__ == "__main__":
    # 範例 1：可滿足的表達式
    # (A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ ¬C)
    print("【範例 1】")
    vars_1 = ['A', 'B', 'C']
    expr_1 = "(A or B) and (not A or C) and (not B or not C)"
    solve_sat_truth_table(vars_1, expr_1)
    
    print("\n" + "="*40 + "\n")
    
    # 範例 2：不可滿足的表達式（矛盾式）
    # (P ∨ Q) ∧ (¬P) ∧ (¬Q)
    print("【範例 2】")
    vars_2 = ['P', 'Q']
    expr_2 = "(P or Q) and (not P) and (not Q)"
    solve_sat_truth_table(vars_2, expr_2)
