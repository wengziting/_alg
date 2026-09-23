```python
import ast
import itertools
import re


def extract_variables(expr_str: str) -> list[str]:
    keywords = {
        "and", "or", "not",
        "true", "false",
        "True", "False"
    }

    tokens = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', expr_str)

    vars_set = {
        token
        for token in tokens
        if token not in keywords
    }

    return sorted(vars_set)


def evaluate_ast(node, env: dict[str, bool]) -> bool:
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]

        if node.id == "True":
            return True

        if node.id == "False":
            return False

        raise ValueError(f"未知變數：{node.id}")

    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            return node.value

        raise ValueError(
            f"只允許布林常數 True / False，不允許：{node.value!r}"
        )

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not evaluate_ast(node.operand, env)

    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And):
        return all(evaluate_ast(value, env) for value in node.values)

    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
        return any(evaluate_ast(value, env) for value in node.values)

    raise ValueError(
        f"不支援的運算：{type(node).__name__}"
    )


def validate_ast(node):
    if isinstance(node, ast.Expression):
        validate_ast(node.body)
        return

    if isinstance(node, ast.Name):
        return

    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            return

        raise ValueError(
            f"只允許 True / False，不允許常數：{node.value!r}"
        )

    if isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, ast.Not):
            raise ValueError("只允許使用 not 運算")

        validate_ast(node.operand)
        return

    if isinstance(node, ast.BoolOp):
        if not isinstance(node.op, (ast.And, ast.Or)):
            raise ValueError("只允許使用 and / or")

        for value in node.values:
            validate_ast(value)

        return

    raise ValueError(
        f"發現不支援的語法：{type(node).__name__}"
    )


def solve_sat_by_truth_table(expr_str: str):
    if not expr_str or not expr_str.strip():
        print("錯誤：邏輯表示式不可為空白。")
        return None

    expr_str = expr_str.strip()

    try:
        tree = ast.parse(expr_str, mode="eval")
        validate_ast(tree)

    except SyntaxError as e:
        print("錯誤：邏輯表示式語法錯誤。")
        print(f"詳細資訊：{e}")
        return None

    except ValueError as e:
        print(f"錯誤：{e}")
        return None

    vars_list = extract_variables(expr_str)
    n = len(vars_list)

    print("=" * 65)
    print("SAT Solver - Truth Table")
    print("=" * 65)

    print(f"邏輯表示式：{expr_str}")

    if vars_list:
        print(f"變數個數：{n}")
        print(f"變數列表：{', '.join(vars_list)}")
    else:
        print("變數個數：0（純布林常數表示式）")

    total_rows = 2 ** n
    print(f"真值表總列數：2^{n} = {total_rows}")
    print()

    if vars_list:
        header_vars = " | ".join(
            f"{var:^5}" for var in vars_list
        )
        header = f"| {header_vars} | Result |"
    else:
        header = "| Result |"

    divider = "-" * len(header)

    print(divider)
    print(header)
    print(divider)

    satisfying_models = []

    for combination in itertools.product([True, False], repeat=n):
        env = dict(zip(vars_list, combination))

        try:
            result = evaluate_ast(tree.body, env)

        except Exception as e:
            print(f"\n計算錯誤：{e}")
            return None

        if vars_list:
            row_vars = " | ".join(
                f"{'T' if env[var] else 'F':^5}"
                for var in vars_list
            )

            print(
                f"| {row_vars} | "
                f"{'T' if result else 'F':^6} |"
            )
        else:
            print(
                f"| {'T' if result else 'F':^7} |"
            )

        if result:
            satisfying_models.append(env.copy())

    print(divider)

    if satisfying_models:
        status = "SAT"
        status_description = "Satisfiable / 可滿足"

        print(f"\n【判定結果】：{status} ({status_description})")
        print(
            f"共找到 {len(satisfying_models)} 組可滿足賦值 "
            f"(Model)："
        )

        for idx, model in enumerate(satisfying_models, start=1):
            if model:
                model_fmt = ", ".join(
                    f"{key}={'T' if value else 'F'}"
                    for key, value in model.items()
                )
            else:
                model_fmt = "(無變數)"

            print(f"  Model {idx}: {model_fmt}")

    else:
        status = "UNSAT"
        status_description = "Unsatisfiable / 不可滿足"

        print(f"\n【判定結果】：{status} ({status_description})")
        print("不存在任何變數賦值能使該表示式為 True。")

    sat_count = len(satisfying_models)
    unsat_count = total_rows - sat_count

    print("\n【統計資訊】")
    print(f"總測試數：{total_rows}")
    print(f"SAT 組數：{sat_count}")
    print(f"UNSAT 組數：{unsat_count}")

    if total_rows > 0:
        percentage = sat_count / total_rows * 100
        print(f"可滿足比例：{percentage:.2f}%")

    print("=" * 65)

    return {
        "expression": expr_str,
        "variables": vars_list,
        "variable_count": n,
        "total_rows": total_rows,
        "status": status,
        "satisfying_models": satisfying_models,
        "sat_count": sat_count,
        "unsat_count": unsat_count
    }


if __name__ == "__main__":

    print("=== 範例 1：可滿足 (SAT) ===")

    result1 = solve_sat_by_truth_table(
        "(A or B) and (not A or C) and (not B or not C)"
    )

    print("\n" + "\n")

    print("=== 範例 2：不可滿足 (UNSAT) ===")

    result2 = solve_sat_by_truth_table(
        "A and not A"
    )
```
