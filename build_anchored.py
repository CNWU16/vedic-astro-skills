#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
桥接脚本：从 skill 源仓库生成带锚点的抽取副本（SK-14b 替代方案）。
本体一字不动；产物只读，任何修改回源头重跑本脚本。

规格来源：D:\\jhora0520-product\\SKILL_FIX_HANDOFF.md 第七节（产品侧答复 2026-07-02）
  - 产物：build/anchored/<file>.anchored.md + build/anchored/rule_index.json
  - 锚三级：L1 章节(##/###)；L2 规则块(⚠️块/编号规则清单/代码块模板)；L3 条目(编号+加粗铁律行)
  - 锚 ID：A-{file缩写}-{块首行文本sha1前8}，不按行号；文本改动=新ID=同步信号
  - category 与 IO 剥离由产品侧做，本脚本只做锚点化+索引

跑法（本脚本住开源仓根，路径从自身位置推导，Mac/Windows 通用）：
  python build_anchored.py                    # 开源 + Pro 两仓库（Pro 缺席则只跑开源并明说）
  python build_anchored.py --repo <仓库根>    # 只跑指定仓库
  python build_anchored.py --pro <路径>       # Pro 仓不在同级时指定
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# 本脚本住开源仓根，路径从自身位置推导（Mac 也要能跑），不再硬编码机器路径。
# 内容中性——只有路径与文件清单，无 Pro 规则正文，放公开仓无碍。
# consistency_lint.py 相反：它的 BLACKLIST_PRO / VARGA_COPIES['Pro'] 写着 Pro 的
# 产物清单与 Step 编号，因此住 Pro 私有仓。
OPEN = Path(__file__).resolve().parent
PRO = OPEN.parent / 'vedic-astro-skills-pro'   # 可用 --pro 覆盖
SKILL_REL = Path('skills/vedic-core')
# 覆盖范围（第七节第1条；report_rules 产品不消费，略）
# prediction_rules 是 Pro 独有（开源版无此文件，build 时会打一行 [WARN] missing，属预期）。
# 补入原因：本清单当初按开源版的文件构成列，Pro 复用同一份 FILES，导致 Pro 最核心的增量
# ——Step 5 动态预测的全部判定细则——从未进过锚定管道。SKILL.md:1007 明写"均以该文件为准"，
# 即 SKILL.md 里只有指针、细则全在这 184 行（BAV过运校准/双过运窗口/Rahu-Ketu轴线/
# 格局激活验证/三轴结算/事件簇审计）。产品若以 Pro 为源却不锚它，拿到的是"8步流程的壳
# + 6步版本的预测能力"。2026-09-03 补。
FILES = {
    'SKILL.md': 'SK',
    'resources/p1_p12.md': 'P12',
    'resources/yogas.md': 'YG',
    'resources/house_framework.md': 'HF',
    'resources/qa_rules.md': 'QA',
    'resources/prediction_rules.md': 'PR',
    'resources/synthesis.md': 'SY',
}

RE_HEADING = re.compile(r'^(#{2,3})\s+(.+)$')
RE_WARN = re.compile(r'^\s*[>\-\*\s]*⚠️')
RE_L3 = re.compile(r'^\s*\d+\.\s+\*\*')          # 编号+加粗 = 铁律条目
RE_NUMLIST = re.compile(r'^\s*1\.\s+\S')          # 编号清单起点（非加粗的也算 L2 清单）


def anchor_id(abbr: str, first_line: str) -> str:
    h = hashlib.sha1(first_line.strip().encode('utf-8')).hexdigest()[:8]
    return f'A-{abbr}-{h}'


def clean_title(line: str, maxlen: int = 80) -> str:
    t = re.sub(r'^[#>\s\-\*]+', '', line).strip().strip('`*')
    return t[:maxlen]


def parse_file(text: str, abbr: str, relname: str):
    """逐行扫描，产出 (anchored_lines, anchors[])。"""
    lines = text.split('\n')
    out, anchors = [], []
    i, n = 0, len(lines)
    in_code = False

    def emit(level: str, first_line: str, block_lines: list):
        aid = anchor_id(abbr, first_line)
        anchors.append({
            'id': aid, 'file': relname, 'level': level,
            'title': clean_title(first_line),
            'text': '\n'.join(block_lines).strip(),
        })
        out.append(f'<!-- ANCHOR: {aid} {level} -->')

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # 代码块（L2：模板整块一锚，块内不再打锚）
        if stripped.startswith('```') and not in_code:
            j = i + 1
            while j < n and not lines[j].strip().startswith('```'):
                j += 1
            block = lines[i:min(j + 1, n)]
            first = next((l for l in block[1:] if l.strip()), block[0])
            emit('L2', first, block)
            out.extend(block)
            i = j + 1
            continue

        m = RE_HEADING.match(line)
        if m:  # L1 章节
            emit('L1', m.group(2), [line])
            out.append(line)
            i += 1
            continue

        if RE_WARN.match(line):  # L2 ⚠️ 块：到空行为止
            j = i
            while j < n and lines[j].strip():
                j += 1
            emit('L2', line, lines[i:j])
            out.extend(lines[i:j])
            i = j
            continue

        if RE_L3.match(line):  # L3 铁律条目：本条到下一条编号/空行
            j = i + 1
            while j < n and lines[j].strip() and not RE_L3.match(lines[j]) \
                    and not RE_HEADING.match(lines[j]) and not lines[j].strip().startswith('```'):
                j += 1
            emit('L3', line, lines[i:j])
            out.extend(lines[i:j])
            i = j
            continue

        if RE_NUMLIST.match(line) and not RE_L3.match(line):  # L2 普通编号清单：整个清单一锚
            j = i
            while j < n and lines[j].strip() and not RE_HEADING.match(lines[j]) \
                    and not lines[j].strip().startswith('```'):
                j += 1
            emit('L2', line, lines[i:j])
            out.extend(lines[i:j])
            i = j
            continue

        if stripped.startswith('>'):  # L2 blockquote 规则块：连续 > 行整块一锚
            # SQ-01 修复：> 形态的规则块（如分盘视角分离铁律）此前只被复制、不锚点化，
            # 锚 diff 看不见其改动。现纳入 L2，> 里的规则改动能进变更清单。
            j = i
            while j < n and lines[j].strip().startswith('>'):
                j += 1
            emit('L2', line, lines[i:j])
            out.extend(lines[i:j])
            i = j
            continue

        out.append(line)
        i += 1

    return '\n'.join(out), anchors


def compute_sections(text: str, abbr: str, relname: str):
    """SQ-04：按标题(##/###)切节，每节算全节内容哈希，堵住"节内散行编辑锚点看不见"的盲区。
    锚只给标题/⚠️/清单/代码块/blockquote 发，节内普通文字行不归任何锚管；section_hash
    覆盖整节正文，节内任何一行变了该节哈希即变，diff 立刻定位到"哪一节动了"再读原文即可。"""
    lines = text.split('\n')
    sections = []
    in_code = False
    cur = None  # {'heading', 'lines': []}

    def flush():
        if cur is not None:
            body = '\n'.join(cur['lines'])
            sections.append({
                'anchor': anchor_id(abbr, cur['heading']),
                'file': relname,
                'title': clean_title(cur['heading']),
                'section_hash': hashlib.sha1(body.encode('utf-8')).hexdigest()[:12],
                'n_lines': len(cur['lines']),
            })

    for line in lines:
        if line.strip().startswith('```'):
            in_code = not in_code
        m = RE_HEADING.match(line) if not in_code else None
        if m:
            flush()
            cur = {'heading': m.group(2), 'lines': [line]}
        elif cur is not None:
            cur['lines'].append(line)
    flush()
    return sections


def git_commit(repo: Path) -> str:
    """产物自报的 source_commit = 最后一次改动被锚文件的提交，**不是 HEAD**。

    2026-09-03 修：原实现取 `rev-parse HEAD`，而收尾链是
    「改规则 → commit 规则 → 重跑本脚本 → commit 锚产物」——提交锚产物本身会推进
    HEAD，此后任何一次重跑都会把 source_commit 写成那个**产物提交**，指向的不再是
    规则内容。实测复现过：开源 6d9054d→4884937、Pro 62483b5→0eaa75f，锚数与其余
    字段全同 = 纯指纹漂移。产品侧 vendor build/anchored/ 时正是读这个字段锁版本，
    漂了就锁错。改为只看 SKILL_REL 子树的最后一次提交，指纹跟规则内容走。

    ⚠️ pathspec 必须精确到 FILES 里那 6 个被锚文件，**不能只给 SKILL_REL 子树**。
    子树里还有 scripts/、__pycache__/ 等非规则内容：A2 那批在 Pro 仓 untrack 了
    vedic-core/scripts/__pycache__/*.pyc，用子树 pathspec 立刻把指纹顶成那个提交
    （实测 62483b5 → ffd112f）。指纹要跟的是"产品消费的规则正文"，不是目录活动。

    副作用（已知且可接受）：本脚本自身、scripts/、其他 skill 的改动不再 bump 指纹
    ——本来也不该 bump，那些改动对被锚规则内容零影响。
    """
    rel = str(SKILL_REL).replace('\\', '/')
    pathspec = [f'{rel}/{f}' for f in FILES]   # 开源仓无 prediction_rules.md，不匹配即忽略
    try:
        r = subprocess.run(
            ['git', '-C', str(repo), 'log', '-1', '--format=%H', '--', *pathspec],
            capture_output=True, text=True)
        out = r.stdout.strip()[:12]
        if out:
            return out
        # 子树无提交历史（新仓/浅克隆）——回落 HEAD 但明确标注，别让它冒充干净指纹
        head = subprocess.run(['git', '-C', str(repo), 'rev-parse', 'HEAD'],
                              capture_output=True, text=True).stdout.strip()[:12]
        return f'{head}-HEAD-fallback' if head else 'unknown'
    except Exception:
        return 'unknown'


def build(repo: Path) -> dict:
    src_dir = repo / SKILL_REL
    out_dir = repo / 'build' / 'anchored'
    out_dir.mkdir(parents=True, exist_ok=True)
    all_anchors = []
    all_sections = []
    file_hashes = {}
    for rel, abbr in FILES.items():
        p = src_dir / rel
        if not p.exists():
            print(f'  [WARN] missing {p}')
            continue
        text = p.read_text(encoding='utf-8')
        anchored, anchors = parse_file(text, abbr, rel)
        (out_dir / (Path(rel).name + '.anchored.md')).write_text(anchored, encoding='utf-8')
        all_anchors.extend(anchors)
        all_sections.extend(compute_sections(text, abbr, rel))          # SQ-04
        file_hashes[rel] = hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]  # SQ-04 整文件兜底
    index = {
        'source_commit': git_commit(repo),
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'repo': repo.name,
        'anchor_count': len(all_anchors),
        'section_count': len(all_sections),   # SQ-04
        'file_hashes': file_hashes,           # SQ-04：整文件级兜底哈希
        'anchors': all_anchors,
        'sections': all_sections,             # SQ-04：节级内容哈希，堵散行编辑盲区
    }
    (out_dir / 'rule_index.json').write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
    by = {}
    for a in all_anchors:
        by[a['level']] = by.get(a['level'], 0) + 1
    print(f'  {repo.name}: {len(all_anchors)} anchors '
          f'(L1={by.get("L1",0)} L2={by.get("L2",0)} L3={by.get("L3",0)}) '
          f'+ {len(all_sections)} sections(hash) -> {out_dir}')
    return index


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', help='只跑指定仓库根路径')
    ap.add_argument('--pro', help='Pro 仓路径（默认 <开源仓>/../vedic-astro-skills-pro）')
    args = ap.parse_args()
    if args.repo:
        targets = [Path(args.repo)]
    else:
        pro = Path(args.pro) if args.pro else PRO
        targets = [OPEN]
        if pro.exists():
            targets.append(pro)
        else:
            # 只克隆了开源仓的机器（Pro 是私有仓）——说清楚只跑了一个，
            # 别让人以为两仓的锚产物都刷新了。
            print(f'[SKIP] Pro 仓不存在，本次只重建开源仓锚产物: {pro}')
    for r in targets:
        if not r.exists():
            sys.exit(f'[FATAL] repo not found: {r}')
        build(r)
    print('done. 铁律：build/anchored/ 产物只读，改内容回源头 SKILL.md 重跑本脚本。')
