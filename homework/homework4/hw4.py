import numpy as np

def generic_iterator(transition_func, is_converged, initial_state, max_iter=1000):
    state = initial_state
    for iteration in range(max_iter):
        next_state = transition_func(state)
        if is_converged(state, next_state, iteration):
            return next_state, iteration + 1
        state = next_state
    return state, max_iter

def demo_gradient_descent():
    print("--- 10. 梯度下降法 (Gradient Descent) ---")
    
    df = lambda x: 2.0 * x - 4.0
    learning_rate = 0.1
    transition = lambda x: x - learning_rate * df(x)
    converged = lambda old, new, i: abs(new - old) < 1e-6
    result, iters = generic_iterator(transition, converged, initial_state=0.0)
    
    print(f"結果: 最小值發生在 x = {result:.6f} (耗時 {iters} 次迭代)\n")

demo_gradient_descent()
