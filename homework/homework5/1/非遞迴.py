def hanoi_iterative(n, source='A', target='C', auxiliary='B'):
    """非遞迴版河內塔（顯式堆疊模擬）"""
    stack = [('SOLVE', n, source, target, auxiliary)]
  
    while stack:
        action, num, src, tgt, aux = stack.pop()
        
        if action == 'MOVE':
            print(f"將盤子 {num} 從 {src} 移動到 {tgt}")
        else:
            if num == 1:
                print(f"將盤子 1 從 {src} 移動到 {tgt}")
            else:
                stack.append(('SOLVE', num - 1, aux, tgt, src))
                stack.append(('MOVE', num, src, tgt, aux))
                stack.append(('SOLVE', num - 1, src, aux, tgt))
print("--- 非遞迴版河內塔 ---")
hanoi_iterative(3)
