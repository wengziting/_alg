使用[gemini](https://share.gemini.google/zM4rZBfW0vQL)
## 1. 程式介紹
程式會把所有變數組合全部列出，在計算每一組的結果是否可以滿足結果。如果只要有一組為True就代表這個表達式是 SATISFIABLE
如果都不是就代表是 UNSATISFIABLE
## 2.使用方法
使用 itertools 產生所有 True / False 的組合
## 3.測試結果
範例 1
(A or B) and (not A or C) and (not B or not C)
有為 True 的組合，判定為 SATISFIABLE

範例 2
(P or Q) and (not P) and (not Q)
因為 P 和 Q 不符合條件，都為 False，判定為UNSATISFIABLE

