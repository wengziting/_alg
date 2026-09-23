# SAT Solver - Truth Table

## 1. 程式介紹

本程式使用 Python 實作一個簡單的 **SAT Solver（Boolean Satisfiability Solver，布林可滿足性求解器）**。

程式會將輸入的布林邏輯表示式解析後，利用 **Truth Table（真值表）** 列舉所有可能的變數組合，判斷是否存在至少一組變數設定可以讓整個邏輯表示式的結果為 `True`。

如果存在至少一組符合條件的變數賦值，則判定為：

```text
SAT (Satisfiable / 可滿足)
```

如果所有可能的變數組合都無法讓表示式成立，則判定為：

```text
UNSAT (Unsatisfiable / 不可滿足)
```

---

## 2. 使用到的 Python 套件

本程式主要使用以下 Python 標準函式庫：

### `ast`

用來解析 Python 風格的布林邏輯表示式，例如：

```python
(A or B) and (not A or C)
```

程式會將表示式轉換成 AST（Abstract Syntax Tree，抽象語法樹），再進行驗證與計算。

### `itertools`

使用：

```python
itertools.product()
```

產生所有可能的布林變數組合。

例如有 A、B 兩個變數時：

```text
A = T, B = T
A = T, B = F
A = F, B = T
A = F, B = F
```

### `re`

使用正規表示式從輸入的邏輯表示式中找出變數名稱。

例如：

```text
(A or B) and (not A or C)
```

會找出：

```text
A, B, C
```

---

## 3. 程式主要功能

本程式主要由以下幾個函式組成。

### `extract_variables(expr_str)`

負責從邏輯表示式中找出所有變數。

例如：

```python
extract_variables("(A or B) and (not A or C)")
```

會取得：

```text
['A', 'B', 'C']
```

並排除：

```text
and
or
not
True
False
```

等關鍵字。

---

### `evaluate_ast(node, env)`

負責計算 AST 中的邏輯表示式。

支援：

* `and`
* `or`
* `not`
* `True`
* `False`
* 一般布林變數

例如：

```text
A = True
B = False
```

計算：

```python
A and not B
```

結果為：

```text
True
```

---

### `validate_ast(node)`

負責檢查輸入的表示式是否使用了程式允許的語法。

本程式只允許：

```text
and
or
not
True
False
變數
```

例如以下表示式可以使用：

```python
A and B
```

```python
(A or B) and not C
```

但不支援其他 Python 運算，例如：

```python
A + B
A > B
A == B
```

這樣可以避免使用者輸入不支援的運算。

---

### `solve_sat_by_truth_table(expr_str)`

這是整個 SAT Solver 的主要函式。

執行流程如下：

```text
輸入邏輯表示式
        ↓
檢查是否為空白
        ↓
使用 AST 解析
        ↓
驗證表示式是否合法
        ↓
找出所有變數
        ↓
產生所有可能的變數組合
        ↓
逐組計算邏輯表示式
        ↓
建立真值表
        ↓
找出 SAT Models
        ↓
判斷 SAT / UNSAT
        ↓
輸出統計資訊
```

---

## 4. SAT 與 UNSAT

### SAT

如果至少存在一組變數設定，使邏輯表示式為 `True`，就是 SAT。

例如：

```python
A or B
```

只要：

```text
A = True
```

或：

```text
B = True
```

表示式就成立。

因此：

```text
SAT
```

---

### UNSAT

如果所有可能的變數設定都無法使表示式成立，就是 UNSAT。

例如：

```python
A and not A
```

當：

```text
A = True
```

時：

```text
True and False = False
```

當：

```text
A = False
```

時：

```text
False and True = False
```

因此沒有任何一組設定可以讓結果為 `True`。

所以：

```text
UNSAT
```

---

## 5. 範例

程式中提供兩個測試案例。

### 範例 1：SAT

```python
solve_sat_by_truth_table(
    "(A or B) and (not A or C) and (not B or not C)"
)
```

程式會列出 A、B、C 的所有可能組合，並計算每一組的結果。

最後會顯示：

```text
【判定結果】：SAT (Satisfiable / 可滿足)
```

並列出可以讓表示式成立的 Model。

例如：

```text
Model 1: A=F, B=T, C=F
Model 2: A=T, B=F, C=T
```

實際 Model 數量則由程式執行結果決定。

---

### 範例 2：UNSAT

```python
solve_sat_by_truth_table(
    "A and not A"
)
```

可能的情況只有：

```text
A = T
A = F
```

兩種結果都為 `False`，因此：

```text
【判定結果】：UNSAT (Unsatisfiable / 不可滿足)
```

---

## 6. 輸出資訊

程式執行後會顯示：

### 邏輯表示式

```text
邏輯表示式：(A or B) and ...
```

### 變數資訊

例如：

```text
變數個數：3
變數列表：A, B, C
```

### 真值表總列數

如果有 `n` 個變數，總共有：

```text
2^n
```

種可能。

例如有 3 個變數：

```text
2^3 = 8
```

所以需要測試 8 組變數組合。

### SAT / UNSAT 結果

最後判斷：

```text
SAT
```

或：

```text
UNSAT
```

### 統計資訊

程式也會統計：

```text
總測試數
SAT 組數
UNSAT 組數
可滿足比例
```

---

## 7. 時間複雜度

本程式採用 **Truth Table（真值表）暴力列舉法**。

假設有 `n` 個變數，每個變數只有：

```text
True / False
```

兩種可能。

因此所有可能的組合共有：

```text
2^n
```

組。

所以程式至少需要檢查：

```text
2^n
```

種情況。

其時間複雜度會呈現：

```text
O(2^n)
```

其中 `n` 是變數數量。

---

## 8. 效率分析

當變數數量很少時，真值表方法非常容易理解，也能快速得到答案。

例如：

| 變數數量 |         真值表列數 |
| ---: | ------------: |
|    1 |             2 |
|    2 |             4 |
|    3 |             8 |
|    4 |            16 |
|    5 |            32 |
|   10 |         1,024 |
|   20 |     1,048,576 |
|   30 | 1,073,741,824 |

可以看出，變數數量增加時，所需要檢查的組合會快速增加。

因此這種方法適合：

* 小型 SAT 問題
* 教學與學習
* 驗證布林邏輯
* 產生真值表
* 觀察 SAT / UNSAT 的概念

但如果變數數量非常大，使用真值表逐一列舉會變得非常沒有效率。

---

## 9. 程式特色

本程式具有以下特色：

1. **自動找出邏輯表示式中的變數**
2. **使用 AST 安全解析表示式**
3. **檢查不支援的運算**
4. **自動產生完整真值表**
5. **列出所有 SAT Models**
6. **自動判斷 SAT 或 UNSAT**
7. **統計 SAT / UNSAT 數量**
8. **計算可滿足比例**
9. **支援 `and`、`or`、`not` 邏輯運算**

---

## 10. 如何執行

將程式儲存為：

```text
sat_solver.py
```

然後在終端機執行：

```bash
python sat_solver.py
```

程式會自動執行內建的兩個範例：

```text
範例 1：可滿足 (SAT)
範例 2：不可滿足 (UNSAT)
```

---

## 11. 限制

目前程式使用真值表方式求解，因此最大的限制是：

```text
變數數量增加 → 組合數量以 2^n 增加
```

此外，目前只支援：

```text
and
or
not
True
False
```

不支援：

```text
XOR
NAND
NOR
```

等其他邏輯運算。

---

## 12. 結論

本程式透過 Python 的 `ast`、`itertools` 和 `re` 模組，實作了一個基於真值表的 SAT Solver。

程式會自動解析布林邏輯表示式，找出變數，列舉所有可能的布林值組合，並判斷是否存在能讓表示式成立的 Model。

雖然 Truth Table 方法的時間複雜度為 **O(2^n)**，當變數數量增加時效率會快速下降，但它的優點是演算法概念簡單、容易理解，非常適合作為 SAT 問題與布林邏輯的基礎實作。
