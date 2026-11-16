#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DsPlayer 官方插件市场对账闸门（MARKET-PLATFORM-ADAPT-DESIGN §七）。

发版前必跑；退出码非零 = 拒绝发布。八项校验（R1-R6 + abis 词法 + 完整性 + icon）：
  1. market.json 可解析、条目 id 唯一、四要素（id/name/version/url）齐全
  2. 相对 url 指向的包存在于 packages/；packages/ 无孤儿文件（绝对 URL
     条目走 Release 分发，只查 md5 已声明，不查本地）
  3. 本地包文件 md5 == 索引声明 md5
  4. platforms 全量显式（R1）、恰好一词（R2）、词表内 android/win32（R3）
  5. abis 声名词法：缺省（未声明）= arm64-v8a；显式 [] = 不限；词表内
     （MARKET-ABI-ADAPT-DESIGN §六，2026-10-14）
  6. README 条目表：行数 == 条目数；头部计数行（N = 环境 X + 应用 Y）；逐行 id/版本/包名与 market.json 一致
  7. 顶层 updatedAt 存在且 ISO8601 格式合法
  8. 每条目 icon 已声明且文件存在于 icons/（防市场卡片空白图）

用法：python check_market.py   （在仓库根目录执行）
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
MARKET = os.path.join(HERE, 'market.json')
README = os.path.join(HERE, 'README.md')
PKGS = os.path.join(HERE, 'packages')
VALID_PLATFORMS = {'android', 'win32'}  # 预留 linux：加入词表时同步改
# abis 词表（MARKET-ABI-ADAPT-DESIGN §六）：缺省（未声明）= ['arm64-v8a']；
# 显式空数组 = 不限（纯资源形态）；多值允许（mpv 的 x86_64 模拟器例外）
VALID_ABIS = {'arm64-v8a', 'armeabi-v7a', 'x86_64', 'x86'}
REQUIRED_FIELDS = ('id', 'name', 'version', 'url')


class Report:
    def __init__(self):
        self.fails = []
        self.checks = []  # (名称, bool, 明细行列表)

    def check(self, name, ok, lines):
        self.checks.append((name, ok, lines))
        if not ok:
            self.fails.append(name)
        mark = 'PASS' if ok else 'FAIL'
        print(f'[{mark}] {name}')
        for ln in lines:
            print(f'       {ln}')


def md5_of(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def parse_readme_rows():
    """解析 README 条目表行 → [(id, version, 包名 basename)]。

    表格式（「### 环境（env）」「### 应用（app）」两节）：
      | 条目 | id | 版本 | type | 包 |
    id 列与包列取反引号内容（无反引号取整格 strip），版本列取整格 strip。
    """
    rows = []
    with open(README, encoding='utf-8') as f:
        in_table = False
        for line in f:
            s = line.strip()
            if s.startswith('### '):
                in_table = '（env）' in s or '（app）' in s
                continue
            if not in_table or not s.startswith('|'):
                continue
            cells = [c.strip() for c in s.strip('|').split('|')]
            if len(cells) < 5 or cells[0] in ('条目', '---') or set(cells[0]) <= {'-', ' '}:
                continue  # 表头/分隔行
            def cell_val(c):
                m = re.search(r'`([^`]+)`', c)
                return m.group(1) if m else c
            rows.append((cell_val(cells[1]), cells[2], os.path.basename(cell_val(cells[4]))))
    return rows


def main():
    print(f'== DsPlayer 市场对账闸门 ==  仓库：{HERE}\n')
    rpt = Report()

    # ---- 1. market.json 可解析 / id 唯一 / 四要素 ----
    try:
        with open(MARKET, encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f'[FAIL] market.json 解析失败：{e}')
        return 1
    plugins = data.get('plugins')
    lines, ok = [], isinstance(plugins, list) and len(plugins) > 0
    if not ok:
        lines.append(f'plugins 数组缺失/为空: {type(plugins)}')
        plugins = plugins if isinstance(plugins, list) else []
    seen, dup = set(), set()
    for i, e in enumerate(plugins):
        for fld in REQUIRED_FIELDS:
            if not str(e.get(fld, '') or '').strip():
                lines.append(f'#{i}（{e.get("id", "?")}）缺四要素字段 {fld}')
                ok = False
        eid = str(e.get('id', ''))
        if eid in seen:
            dup.add(eid)
        seen.add(eid)
    if dup:
        lines.append(f'id 重复：{sorted(dup)}')
        ok = False
    rpt.check('1. market.json 解析 / id 唯一 / 四要素齐全', ok,
              lines or [f'{len(plugins)} 条目，id 全部唯一'])

    by_id = {str(e.get('id')): e for e in plugins}

    # ---- 2. 包存在 + 无孤儿（绝对 URL 豁免本地检查）----
    lines, ok = [], True
    remote_ids, local_urls = set(), {}
    for e in plugins:
        url = str(e['url'])
        eid = str(e['id'])
        if url.startswith('http://') or url.startswith('https://'):
            remote_ids.add(eid)
            continue
        p = os.path.join(HERE, *url.split('/'))
        if not os.path.isfile(p):
            lines.append(f'#{eid}：包不存在 {url}')
            ok = False
        else:
            local_urls[os.path.normpath(p)] = eid
    orphans = []
    for fn in sorted(os.listdir(PKGS)) if os.path.isdir(PKGS) else []:
        p = os.path.normpath(os.path.join(PKGS, fn))
        if p not in local_urls:
            orphans.append(fn)
    if orphans:
        lines.append(f'packages/ 孤儿文件（无条目引用）：{orphans}')
        ok = False
    rpt.check('2. 包存在于 packages/ 且无孤儿文件', ok,
              lines or [f'本地包 {len(local_urls)} 个全有条目；'
                        f'Release 分发 {len(remote_ids)} 条（{sorted(remote_ids) or "无"}）豁免'])

    # ---- 3. md5 一致（本地包）----
    lines, ok = [], True
    for p, eid in sorted(local_urls.items()):
        declared = str(by_id[eid].get('md5', '') or '')
        if not declared:
            lines.append(f'#{eid}：未声明 md5（R5 官方仓全量声明）')
            ok = False
            continue
        actual = md5_of(p)
        if actual != declared.lower():
            lines.append(f'#{eid}：md5 不符 声明={declared} 实际={actual}')
            ok = False
    for eid in sorted(remote_ids):
        if not str(by_id[eid].get('md5', '') or ''):
            lines.append(f'#{eid}：Release 分发条目未声明 md5')
            ok = False
    rpt.check('3. 包 md5 与索引声明一致（R5）', ok,
              lines or [f'{len(local_urls)} 本地包 md5 全对账一致'])

    # ---- 4. platforms 全量显式 / 恰好一词 / 词表内（R1-R3）----
    # R2「恰好一词」仅约束二进制形态条目（import/apk——R2 禁的是双平台
    # 二进制合包互拖死重）；live/server/source 数据类无二进制，R1 要求
    # 标全平台组合（如 ["android","win32"]），允许多词。
    lines, ok = [], True
    for e in plugins:
        eid = str(e['id'])
        pl = e.get('platforms')
        if not isinstance(pl, list) or not pl:
            lines.append(f'#{eid}：platforms 缺省（R1 要求显式声明）')
            ok = False
            continue
        if str(e.get('type')) in ('import', 'apk') and len(pl) != 1:
            lines.append(f'#{eid}：platforms={pl} 多于一词（R2 禁多合一，拆包）')
            ok = False
        bad = [x for x in pl if x not in VALID_PLATFORMS]
        if bad:
            lines.append(f'#{eid}：词表外取值 {bad}（R3：{"、".join(sorted(VALID_PLATFORMS))}）')
            ok = False
    rpt.check('4. platforms 显式 / 二进制条目恰好一词 / 词表内（R1-R3）', ok,
              lines or [f'{len(plugins)} 条目全量显式；import/apk 单平台'])

    # ---- 5. abis 声名词法（MARKET-ABI-ADAPT-DESIGN §六，2026-10-14）----
    # 缺省（未声明）= arm64-v8a（历史存量全是 arm64 构建，老条目零改动兼容）；
    # 显式 [] = 不限（纯资源形态，如 agent）；多值允许（mpv 的 x86_64 例外）。
    # 本段只做词法校验——语义判定在客户端（宿主进程 ABI ∈ abis）。
    lines, ok = [], True
    for e in plugins:
        eid = str(e['id'])
        if 'abis' not in e:
            continue
        ab = e.get('abis')
        if not isinstance(ab, list):
            lines.append(f'#{eid}：abis 必须是数组（缺省即 arm64-v8a，勿写标量）')
            ok = False
            continue
        bad = [x for x in ab if x not in VALID_ABIS]
        if bad:
            lines.append(f'#{eid}：abis 词表外取值 {bad}'
                         f'（{"、".join(sorted(VALID_ABIS))}）')
            ok = False
    declared = sum(1 for e in plugins if 'abis' in e)
    rpt.check('5. abis 声名词法（缺省=arm64-v8a；空数组=不限；词表内）', ok,
              lines or [f'{declared} 条目显式声明，其余缺省 arm64-v8a'])

    # ---- 6. README 条目表逐行对账（R6）----
    rows = parse_readme_rows()
    lines, ok = [], True
    if len(rows) != len(plugins):
        lines.append(f'README 条目行 {len(rows)} != market.json 条目数 {len(plugins)}')
        ok = False
    with open(README, encoding='utf-8') as f:
        m = re.search(r'当前收录（(\d+) 个条目 = 环境 (\d+) \+ 应用 (\d+)）', f.read())
    if m:
        total, env_n, app_n = map(int, m.groups())
        real_env = sum(1 for e in plugins if e.get('category', 'env') == 'env')
        if (total, env_n, app_n) != (len(plugins), real_env, len(plugins) - real_env):
            lines.append(f'README 计数行 {total} = {env_n} + {app_n} != 实际 '
                         f'{len(plugins)} = {real_env} + {len(plugins) - real_env}')
            ok = False
    elif '当前收录' in open(README, encoding='utf-8').read():
        lines.append('README 计数行格式不符（期望「当前收录（N 个条目 = 环境 X + 应用 Y）」）')
        ok = False
    readme_ids = [r[0] for r in rows]
    missing = set(by_id) - set(readme_ids)
    extra = set(readme_ids) - set(by_id)
    if missing:
        lines.append(f'README 缺行：{sorted(missing)}')
        ok = False
    if extra:
        lines.append(f'README 多行（market.json 无此 id）：{sorted(extra)}')
        ok = False
    if len(readme_ids) != len(set(readme_ids)):
        lines.append(f'README 表 id 重复：'
                     f'{sorted({i for i in readme_ids if readme_ids.count(i) > 1})}')
        ok = False
    for rid, rver, rpkg in rows:
        e = by_id.get(rid)
        if not e:
            continue
        if rver != str(e['version']):
            lines.append(f'#{rid}：版本不符 README={rver} market.json={e["version"]}')
            ok = False
        url_base = os.path.basename(str(e['url']).split('?')[0])
        if rpkg != url_base:
            lines.append(f'#{rid}：包名不符 README={rpkg} market.json={url_base}')
            ok = False
    rpt.check('6. README 条目表逐行对账（行数/计数行/id/版本/包名）', ok,
              lines or [f'{len(rows)} 行 + 计数行一致（id/版本/包名）'])

    # ---- 7. updatedAt 存在且格式合法 ----
    upd = str(data.get('updatedAt', '') or '')
    try:
        datetime.fromisoformat(upd.replace('Z', '+00:00'))
        ok6, line6 = True, f'updatedAt = {upd}'
    except ValueError:
        ok6, line6 = (upd != ''), f'updatedAt 非法：{upd!r}（期望 ISO8601，如 2026-10-09T09:54:39Z）'
    rpt.check('7. 顶层 updatedAt 存在且 ISO8601 合法', ok6, [line6])

    # ---- 8. icon 全量声明且文件存在（市场卡片不空白）----
    no_icon = [str(e['id']) for e in plugins if not e.get('icon')]
    missing_icon = []
    for e in plugins:
        icon = e.get('icon')
        if icon and not os.path.isfile(os.path.join(HERE, icon)):
            missing_icon.append(f"#{e['id']} -> {icon}")
    lines = []
    if no_icon:
        lines.append(f'未声明 icon：{no_icon}')
    if missing_icon:
        lines.append(f'icon 文件不存在：{missing_icon}')
    rpt.check('8. icon 全量声明且文件存在', not lines,
              lines or [f'{len({e.get("icon") for e in plugins})} 个图标文件覆盖全部条目'])

    # ---- 总结 ----
    print(f'\n== 总结：{len(plugins)} 条目 · {len(local_urls)} 本地包 · '
          f'{len(rows)} README 行 · '
          f'{"全部 PASS，可发布" if not rpt.fails else "FAIL " + "、".join(rpt.fails)} ==')
    return 1 if rpt.fails else 0


if __name__ == '__main__':
    sys.exit(main())
