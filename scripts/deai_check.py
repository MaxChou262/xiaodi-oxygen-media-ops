#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""口播 AI 味自检：句长、禁用词、标点、连词、时长。

用法：
    python deai_check.py 口播.txt
    cat 口播.txt | python deai_check.py -

检查五件事：
    1 句长方差（全段等长 = 像机器）
    2 僵尸词 / 商业黑话命中
    3 「不是……而是……」出现次数
    4 显性连词密度、破折号/冒号密度
    5 按 4.7 字/秒估算时长

评分 0-100，越低越好。>40 建议重写。
零依赖，Python 3.8+。
"""
import sys
import re
import statistics

ZOMBIE = [
    "进行", "开展", "实施", "落实", "推进", "赋能", "助力", "打造", "构建",
    "闭环", "生态", "抓手", "链路", "全方位", "一站式", "精准", "深度",
    "高效", "值得注意的是", "不难发现", "众所周知", "综上", "总而言之",
    "致力于", "致力于为", "解决方案", "沉浸式", "显著", "有效改善",
]
CONNECTIVES = ["首先", "其次", "再次", "最后", "因此", "然而", "此外", "同时", "另外", "从而"]
SENT_END = "。！？!?\n"


def read(path):
    return sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()


def split_sentences(text):
    out, buf = [], ""
    for ch in text:
        if ch in SENT_END:
            if buf.strip():
                out.append(buf.strip())
            buf = ""
        else:
            buf += ch
    if buf.strip():
        out.append(buf.strip())
    return out


def cn_len(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    text = read(sys.argv[1]).strip()
    if not text:
        sys.exit("文本为空")

    chars = cn_len(text)
    sents = split_sentences(text)
    lens = [cn_len(s) for s in sents if cn_len(s) > 0]
    if not lens:
        sys.exit("没有中文句子")

    mean = statistics.mean(lens)
    var = statistics.pstdev(lens) if len(lens) > 1 else 0.0
    shortest = min(lens)

    hits = [(w, text.count(w)) for w in ZOMBIE if w in text]
    hit_n = sum(c for _, c in hits)
    conn = sum(text.count(w) for w in CONNECTIVES)
    dash = text.count("—") + text.count("——")
    colon = text.count("：") + text.count(":")
    nab = len(re.findall(r"不是[^。！？\n]{0,20}?而是", text))

    # 评分：各项超阈值计分
    score = 0
    issues = []
    if var < 5:
        score += 25
        issues.append(f"句长方差 {var:.1f} < 5：全段等长，像朗读稿")
    if shortest > 10:
        score += 15
        issues.append(f"最短句 {shortest} 字：缺短句，语流没有起伏")
    if hit_n:
        score += min(25, hit_n * 6)
        issues.append("僵尸词：" + "、".join(f"{w}×{c}" for w, c in hits))
    if nab > 1:
        score += 15
        issues.append(f"「不是…而是…」出现 {nab} 次：AI 第一特征，留一次就够")
    if conn >= 3:
        score += 10
        issues.append(f"显性连词 {conn} 个：删掉六成，用短句推进")
    if dash + colon >= 4:
        score += 5
        issues.append(f"破折号/冒号 {dash + colon} 处：偏多，念出来会卡")
    score = min(100, score)

    secs = chars / 4.7
    print("=" * 60)
    print("口播 AI 味自检")
    print("=" * 60)
    print(f"汉字数     {chars}")
    print(f"句子数     {len(lens)}")
    print(f"平均句长   {mean:.1f} 字")
    print(f"句长标准差 {var:.1f}   （建议 > 5）")
    print(f"最短句     {shortest} 字 （建议 ≤ 10）")
    print(f"预计时长   {secs:.1f} 秒  （4.7 字/秒）")
    print(f"AI 味评分  {score}/100  （越低越好，>40 建议重写）")

    if issues:
        print("\n问题：")
        for i in issues:
            print(f"  - {i}")
    else:
        print("\n未发现明显 AI 特征。仍建议念一遍——脚本测不出「念着别扭」。")

    if secs < 25:
        print("\n提示：时长偏短，30 秒档建议 140 字左右。")
    elif secs > 70:
        print("\n提示：时长偏长，单条超过 70 秒建议拆成两条。")


if __name__ == "__main__":
    main()
