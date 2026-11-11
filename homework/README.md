rows = [
    (1, "查表法",            "是", "", "", ""),
    (2, "複雜度",            "是", "", "", ""),
    (3, "列舉＋暴力",        "是", "", "", ""),
    (4, "迭代法",            "否", "是", ("證明", "#"), ""),
    (5, "遞迴，函數式編程",  "是", "", "", ("week5-fp-lambda", "#")),
    (6, "Lambda Calculus",   "是", "", "", ""),
    (7, "動態規劃與文字算法", "是", "", "", ""),
    (8, "優化算法",          "是", "", "", ""),
    (9, "搜尋算法",          "是", "", "", ""),
]
headers = ["第幾週", "習題內容", "有上課且準時繳交", "補交", "附上請假證明", "作業連結"]


def cell(v):
    # 如果是 (文字, 網址) 就做成連結
    if isinstance(v, tuple):
        return f'<a href="{v[1]}">{v[0]}</a>'
    return str(v)


# ---------- 1. 產生 HTML ----------
html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>每週檢驗表格</title>
<style>
  body {{ font-family: "Microsoft JhengHei", sans-serif; margin: 24px; color: #1f2328; }}
  table {{ border-collapse: collapse; margin-top: 16px; }}
  th, td {{ border: 1px solid #d0d7de; padding: 12px 16px; }}
  th {{ font-weight: 600; text-align: center; }}
  td {{ text-align: left; }}
  td:first-child {{ text-align: left; }}
  tr:nth-child(even) td {{ background: #f6f8fa; }}
  a {{ color: #0969da; }}
</style>
</head>
<body>
<div>每週檢驗表格</div>
<table>
  <thead><tr>{''.join(f'<th>{h}</th>' for h in headers)}</tr></thead>
  <tbody>
{''.join('    <tr>' + ''.join(f'<td>{cell(c)}</td>' for c in r) + '</tr>' + chr(10) for r in rows)}  </tbody>
</table>
</body>
</html>"""

with open("table.html", "w", encoding="utf-8") as f:
    f.write(html)


# ---------- 2. 產生 Markdown ----------
def md_cell(v):
    if isinstance(v, tuple):
        return f"[{v[0]}]({v[1]})"
    return str(v)

md = "每週檢驗表格\n\n"
md += "| " + " | ".join(headers) + " |\n"
md += "|" + "|".join([":---:"] * len(headers)) + "|\n"
for r in rows:
    md += "| " + " | ".join(md_cell(c) for c in r) + " |\n"

with open("table.md", "w", encoding="utf-8") as f:
    f.write(md)

print(md)
print("已產生 table.html 與 table.md")
