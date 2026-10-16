# Lambda Calculus Evaluator

## 專案簡介

本專案使用 Python 實作簡易的 Lambda Calculus（λ 演算）求值器，能夠建立 Lambda 表達式、計算自由變數、執行變數代換，並逐步進行 Beta 歸約。

## 功能介紹

- **Var**：表示變數。
- **Abs**：表示 Lambda 抽象。
- **App**：表示函數應用。
- **free_vars()**：計算表達式中的自由變數。
- **substitute()**：執行變數代換，並處理變數遮蔽與變數捕捉。
- **reduce_step()**：執行單步 Beta 歸約。
- **evaluate()**：顯示每一步的化簡結果，直到無法繼續化簡或達到最大步數。


## 使用範例

```python
expr = App(
    Abs("x", Var("x")),
    Var("y")
)

evaluate(expr)
```

輸出結果：

```text
初始: ((λx.x) y)
步驟 1: y
=> 已達 Normal Form (無法再化簡)
```

## 核心概念

Lambda Calculus 使用 Beta 歸約進行函數化簡：

`(λx.M) N → M[x := N]`

程式透過變數代換完成化簡，並使用 Alpha 轉換避免變數捕捉，讓表達式能正確地進行求值。
