#!/usr/bin/env python3
# 短剧创作者中心 剧本格式与体量检查脚本 v1.1（依据规则卡库 v1.1）
# 用法：python3 check_script.py 剧本.txt --mode zr|qianbu|mj [--title 剧名]
# 只做可机检的项目；内容判断由诊断 skill 人工完成。
import re, sys, argparse

CN = '零一二三四五六七八九十百千'
LIMITS = {'zr': (600, 800, 1200), 'qianbu': (375, 500, None), 'mj': (None, None, None)}
# 明确的非剧本标注：出现即必改
BAN_MARK = ['付费卡点', '投流素材', '本集创作复盘', '创作复盘', '情绪峰值', '节奏分析', '【BGM', 'BGM：', 'BGM:', '【音效',
            '【本集结束】', '本集结束', '本集终', '未完待续', '【黑屏', '镜头缓缓', '画面定格', 'To be continued', '修改记录', '版本号', '批注', '▋黑屏▋']
# 可能是标注、也可能是台词里的普通词：只有出现在【】里或作为"xx："标签时才算必改，否则交人工判断
SOFT_MARK = ['名场面', '视觉奇观', '爽点', '钩子', '景别', '运镜', '机位', '分镜', '特写镜头']
AI_WORDS = ['不禁', '不由得', '难以名状', '涌起一股', '深邃的', '意味深长', '五味杂陈', '仿佛', '眸子', '一抹']
RED_HINT = {'极端侮辱': ['狗链', '狗笼', '骨灰盒', '排泄物', '钻胯'], '肢体羞辱(控量)': ['下跪', '跪下', '磕头', '耳光', '扇了', '巴掌'],
            '暴力复仇': ['灭门', '灭族', '屠杀', '满门'], '迷信玄学': ['算命', '风水', '符箓', '阵法', '命格', '转世', '附身', '阴曹'],
            '金钱观': ['借贷', '放贷', '逃债', '高利贷'], '血腥': ['断肢', '血肉模糊', '挖眼', '剖腹'], '低俗': ['床戏', '上床', '脱衣', '裸体', '裸露']}
MKT = ['热播', '爆款', '强推', '误传', '测试', '废弃']

def cn_num(s):
    return bool(s) and all(c in CN for c in s)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('file'); ap.add_argument('--mode', default='zr'); ap.add_argument('--title', default='')
    a = ap.parse_args()
    text = open(a.file, encoding='utf-8').read().replace('\r', '')
    lines = text.split('\n')
    issues = []  # (级别, 位置, 问题, 规则卡)
    def add(lv, pos, msg, card): issues.append((lv, pos, msg, card))

    # 剧名
    if a.title:
        t = a.title
        if len(t) > 20: add('必改', '剧名', f'剧名 {len(t)} 字符，超过 20', 'G2-04')
        if re.search(r'[《》<>\s]', t): add('必改', '剧名', '剧名含书名号、尖括号或空格', 'G2-04')
        bad = re.findall(r'[^\w，！：？“”,!:?"一-鿿]', t)
        if bad: add('必改', '剧名', '剧名含不允许的标点：' + ''.join(set(bad)), 'G2-05')
        for w in MKT:
            if w in t: add('必改', '剧名', f'剧名含营销或无关词：{w}', 'G2-07')

    # 切集
    eps = []  # [title, lineno, [lines]]
    for i, l in enumerate(lines, 1):
        s = re.sub(r'^#+\s*', '', l.strip())
        m = re.match(r'^第(.+?)集\s*$', s)
        m2 = re.match(r'^(EP\s*\d+|第\s*\d+\s*集|第\s*[零一二三四五六七八九十百千]+\s*集\s*\S)', s, re.I)
        if m2 and l.strip().startswith('#'):
            add('必改', f'第{i}行', '集标题前有 Markdown 标记"#"，集标题应单独成行写"第一集"', 'M3-01')
        if m2 and not (m and cn_num(m.group(1))):
            add('必改', f'第{i}行', f'集标题"{s}"不是中文数字格式，应写"第一集"', 'M3-01')
            eps.append([s, i, []]); continue
        if m and cn_num(m.group(1)):
            eps.append([s, i, []]); continue
        if eps: eps[-1][2].append((i, l))
    if not eps:
        add('必改', '全文', '未识别到任何集标题（第一集、第二集……）', 'M3-01')

    rows = []
    lo, hi, cap = LIMITS.get(a.mode, (None, None, None))
    for title, ln, body in eps:
        content = [s for _, s in body if s.strip()]
        chars = sum(len(re.sub(r'\s', '', s)) for s in content)
        scenes = 0; dash = 0; os_n = 0
        for j, (i, l) in enumerate(body):
            s = l.strip()
            if not s: continue
            if re.match(r'^\d+-\d+\s', s):
                scenes += 1
                parts = s.split()
                if len(parts) < 4 or not re.search(r'(日|夜|晨|昏|午|夕|傍晚|清晨|黄昏|凌晨|白天)', parts[-2] if len(parts) >= 2 else '') or parts[-1] not in ('内', '外', '内外', '内/外'):
                    add('必改', f'第{i}行', f'场次标题"{s}"应为"集号-场号 地点 时间 内外景"', 'M3-02')
                nxt = next((x.strip() for _, x in body[j+1:j+4] if x.strip()), '')
                if not nxt.startswith('出场人物'):
                    add('必改', f'第{i}行', '场次标题后缺"出场人物："行', 'M3-03')
                elif nxt.endswith('。') or (',' in nxt) or ('、' in nxt):
                    add('必改', f'第{i}行后', '出场人物行应用中文逗号分隔、末尾不加句号', 'M3-03')
            if re.match(r'^\[场景\]|^\d+-\d+\s+(日|夜)/', s) or re.match(r'^S\d+-\d+', s):
                add('必改', f'第{i}行', f'"{s[:20]}"是其他 skill 的场次格式，需改为平台投稿模板的场次格式', 'M3-02')
            if re.match(r'^【OS】', s) or re.match(r'^OS[:：]', s):
                add('必改', f'第{i}行', 'OS 未依附人物', 'M3-07')
            if s.startswith('【') and not re.match(r'^【(字幕|VO|画面|镜头|闪回|回忆|特写|黑屏)', s) and len(s) > 20:
                add('必改', f'第{i}行', '用【】写大段动作或环境描写；动作行应以△开头，【】只作技术标记', 'M3-04、M3-08')
            if re.match(r'^[^\s△【]{1,10}（VO', s):
                add('必改', f'第{i}行', 'VO 应写在行首："【VO】人物名（语气）：台词"', 'M3-07')
            if re.match(r'^(O\.S\.|V\.O\.)', s) or re.search(r'\s(O\.S\.|V\.O\.)\s*$', s):
                add('必改', f'第{i}行', 'O.S./V.O. 是好莱坞格式；应写"人物名（OS）："或"【VO】人物名："', 'M3-07')
            if re.match(r'^\s{4,}\S{1,8}\s*$', l) and not s.startswith(('△', '（', '(')):
                add('必改', f'第{i}行', '人物名单独居中成行是好莱坞对白格式；应写"人物名（提示）：台词"同一行', 'M3-06')
            if re.match(r'^人物[:：]', s):
                add('必改', f'第{i}行', '应写"出场人物："', 'M3-03')
            if re.match(r'^旁白', s) or '【旁白' in s:
                add('必改', f'第{i}行', '出现叙述旁白；对话剧不用上帝视角旁白', 'M4-13、M1-04')
            if 'OS' in s: os_n += 1
            dash += s.count('\u2014\u2014')
            hit = next((w for w in BAN_MARK if w in s), None)
            if hit: add('必改', f'第{i}行', f'正文含非纯剧本内容：{hit}', 'M2-08')
            else:
                for w in SOFT_MARK:
                    if re.search('【[^】]*' + w, s) or re.match(r'^[^\w]*' + w + r'\s*[:：]', s):
                        add('必改', f'第{i}行', f'正文含创作或拍摄标注：{w}', 'M2-08'); break
                    if w in s:
                        add('人工判断', f'第{i}行', f'出现"{w}"，若是标注需删除，若是台词内容可保留', 'M2-08'); break
            is_dialog = re.match(r'^[^\s（(【△：:]{1,10}(（[^）]*）)?[：:]', s) is not None
            if not s.startswith('△') and not is_dialog and len(s) > 40 and not s.startswith(('出场人物', '【', '第')) and not re.match(r'^\d+-\d+', s):
                add('建议改', f'第{i}行', '疑似未以△开头的动作描写或小说化段落', 'M3-04')
            for w in AI_WORDS:
                if w in s: add('建议改', f'第{i}行', f'AI 高频词或书面腔：{w}', 'M5-13')
            for k, ws in RED_HINT.items():
                for w in ws:
                    if w in s: add('人工判断', f'第{i}行', f'红线关键词"{w}"（{k}），需结合情节判断', 'G4')
        last = next((s.strip() for _, s in reversed(body) if s.strip() and not re.fullmatch(r'[━─=\-*_\s]+', s.strip())), '')
        if last != '（本集完）':
            add('必改', title, f'集尾应为"（本集完）"，当前为"{last[:15]}"', 'M3-12')
        if scenes == 0: add('必改', title, '本集未识别到场次标题', 'M3-02')
        if dash >= 6: add('建议改', title, f'破折号 {dash} 处，偏多（AI 痕迹）', 'M5-13')
        if lo and chars < lo: add('建议改', title, f'字数 {chars}，低于建议下限 {lo}', 'Z1-01' if a.mode == 'zr' else 'Z3-01')
        if hi and chars > hi and not (cap and chars > cap): add('建议改', title, f'字数 {chars}，高于建议上限 {hi}', 'Z1-01' if a.mode == 'zr' else 'Z3-01')
        if cap and chars > cap: add('必改', title, f'字数 {chars}，超过上限 {cap}', 'Z1-01')
        rows.append((title, chars, scenes, os_n, dash))

    total = sum(r[1] for r in rows)
    print('# 格式与体量机检报告\n')
    print(f'- 模式：{a.mode}；集数：{len(rows)}；总字数（去空白）：{total}')
    if a.mode == 'qianbu':
        print(f'- 千部计划要求 40 集、总字数 1.5 万到 2 万（Z3-01）：集数{"符合" if len(rows)==40 else "不符"}，总字数{"符合" if 15000<=total<=20000 else "不符"}')
    if a.mode == 'mj':
        print(f'- AI剧长篇要求超过 70 集且不低于 7 万字（M1-01）：集数{"符合" if len(rows)>70 else "未达"}，总字数{"符合" if total>=70000 else "未达"}（30 集投稿阶段可忽略）')
    print('\n| 集 | 字数 | 场次数 | OS 处数 | 破折号 |\n|---|---|---|---|---|')
    for r in rows: print(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |')
    order = {'必改': 0, '建议改': 1, '人工判断': 2}
    # 同类问题超过 3 处时合并成一行，避免报告被逐行问题淹没
    groups = {}
    for it in issues:
        key = (it[0], re.sub(r'"[^"]*"|：\S+$|\d+', '', it[2]), it[3])
        groups.setdefault(key, []).append(it)
    merged = []
    for key, its in groups.items():
        if len(its) > 3 and all(x[1].startswith('第') and x[1].endswith('行') for x in its):
            pos = '、'.join(x[1] for x in its[:3])
            msgs = list(dict.fromkeys(x[2] for x in its))
            msg = its[0][2]
            if len(msgs) > 1 and all('：' in m for m in msgs):
                msg = msgs[0].split('：')[0] + '：' + '、'.join(dict.fromkeys(m.split('：', 1)[1] for m in msgs))
            merged.append((its[0][0], f'全文 {len(its)} 处', msg + f'（如{pos}）', its[0][3]))
        else:
            merged.extend(its)
    issues = merged
    issues.sort(key=lambda x: order[x[0]])
    print(f'\n## 问题清单（必改 {sum(1 for x in issues if x[0]=="必改")}，建议改 {sum(1 for x in issues if x[0]=="建议改")}，人工判断 {sum(1 for x in issues if x[0]=="人工判断")}）\n')
    print('| 级别 | 位置 | 问题 | 规则卡 |\n|---|---|---|---|')
    for lv, pos, msg, card in issues: print(f'| {lv} | {pos} | {msg} | {card} |')
    print('\n说明：本报告只覆盖可机检项目；"人工判断"项是关键词提示，不等于违规。')

if __name__ == '__main__':
    main()
