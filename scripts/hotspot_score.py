#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""热点四维打分：从候选里挑出最适合做氧舱内容的 10 条。

用法：
    python hotspot_score.py candidates.json
    python hotspot_score.py candidates.csv
    cat candidates.json | python hotspot_score.py -

输入字段（JSON 数组或 CSV 表头）：
    title      热点标题
    scope      local | national      本地 / 全国
    age_days   距今天数（整数）
    relevance  相关性 1-5（能不能一句话挂到氧舱上）
    safety     安全性 1-5（5=完全安全；<4 直接淘汰）
    bridge     一句挂桥（可选，输出里带出来）

评分：相关 0.40 / 本地 0.25 / 时效 0.20 / 安全 0.15
安全性 < 4 一票否决（灾难、医疗事故、明星、对立、涉政）。

零依赖，Python 3.8+。
"""
import sys
import json
import csv
import io

W = {"relevance": 0.40, "local": 0.25, "timeliness": 0.20, "safety": 0.15}


def load(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    raw = raw.strip()
    if not raw:
        sys.exit("输入为空")
    if raw[0] in "[{":
        data = json.loads(raw)
        return data if isinstance(data, list) else data.get("items", [])
    return list(csv.DictReader(io.StringIO(raw)))


def num(row, key, default=0.0):
    try:
        return float(row.get(key, default) or default)
    except (TypeError, ValueError):
        return default


def local_score(scope):
    s = str(scope or "").lower()
    if s.startswith("local") or "本" in s or "同城" in s:
        return 5.0
    if s.startswith("national") or "全国" in s:
        return 2.5
    return 3.0


def time_score(age_days):
    d = num({"x": age_days}, "x", 999)
    if d <= 2:
        return 5.0
    if d <= 7:
        return 4.0
    if d <= 14:
        return 3.0
    return 0.0


def score(row):
    rel = num(row, "relevance", 3)
    saf = num(row, "safety", 5)
    loc = local_score(row.get("scope"))
    tim = time_score(row.get("age_days", 999))
    total = W["relevance"] * rel + W["local"] * loc + W["timeliness"] * tim + W["safety"] * saf
    return total, rel, loc, tim, saf


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    rows = load(sys.argv[1])
    kept, dropped = [], []
    for r in rows:
        total, rel, loc, tim, saf = score(r)
        if saf < 4:
            dropped.append((r.get("title", "?"), "安全性否决"))
        elif tim == 0:
            dropped.append((r.get("title", "?"), "超过 14 天"))
        else:
            kept.append((total, rel, loc, tim, saf, r))

    kept.sort(key=lambda x: -x[0])
    print("=" * 66)
    print("热点打分（取前 10）")
    print("=" * 66)
    print(f"{'#':>2}  {'总分':>5} {'相关':>4} {'本地':>4} {'时效':>4} {'安全':>4}  标题")
    for i, (total, rel, loc, tim, saf, r) in enumerate(kept[:10], 1):
        print(f"{i:>2}  {total:5.2f} {rel:>4.0f} {loc:>4.1f} {tim:>4.1f} {saf:>4.0f}  {r.get('title','')}")
        if r.get("bridge"):
            print(f"     └ 挂桥：{r['bridge']}")

    if len(kept) > 10:
        print(f"\n落选 {len(kept) - 10} 条（分数不够），未列出。")
    if dropped:
        print("\n一票否决 / 过期：")
        for t, why in dropped:
            print(f"  - {t}（{why}）")
    if len(kept) < 10:
        print(f"\n注意：合格热点只有 {len(kept)} 条，不足 10 条。")
        print("按 references/10-hotspot-engine.md 的规则，可补季节常青选题，但必须标注“非热点”。")


if __name__ == "__main__":
    main()
