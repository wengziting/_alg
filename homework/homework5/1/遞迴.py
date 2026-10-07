def hanoi_recursive(n, source='A', target='C', auxiliary='B'):
    """遞迴版河內塔"""
    if n == 1:
        print(f"將盤子 1 從 {source} 移動到 {target}")
        return  
    hanoi_recursive(n - 1, source, auxiliary, target)
    print(f"將盤子 {n} 從 {source} 移動到 {target}")
    hanoi_recursive(n - 1, auxiliary, target, source)
print("--- 遞迴版河內塔 ---")
hanoi_recursive(3)
