import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""xy 状态只读校验。

三条禁令：不写文件、不调用模型、不重启步骤。
用法：
    python check_state.py [项目根目录]
"""

import hashlib
import json
import os
import sys

_CACHE = {}


def sha16(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()[:16]


def dir_sha16(path):
    """目录哈希：排序后的 (相对路径, 内容哈希) 再哈希，避免遍历顺序影响。"""
    parts = []
    for root, dirs, files in os.walk(path):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(root, name)
            rel = os.path.relpath(full, path).replace('\\', '/')
            parts.append(rel + ':' + sha16(full))
    return hashlib.sha256('\n'.join(parts).encode('utf-8')).hexdigest()[:16]


def current_hash(root, rel):
    """内容哈希；不存在返回 None。带缓存，同一个文件只读一次。"""
    key = (root, rel)
    if key in _CACHE:
        return _CACHE[key]
    full = os.path.join(root, rel.replace('/', os.sep))
    if os.path.isdir(full):
        val = dir_sha16(full)
    elif os.path.isfile(full):
        val = sha16(full)
    else:
        val = None
    _CACHE[key] = val
    return val


def input_path(spec):
    """'RESULTS.md@sha256:9f3c' -> 'RESULTS.md'"""
    return spec.split('@sha256:')[0]


def input_hash(spec):
    parts = spec.split('@sha256:')
    return parts[1] if len(parts) > 1 else None


def stale_cascade(artifacts, changed):
    """changed 中的产物变更后，声明依赖它的产物传递失效。"""
    stale, queue = set(), list(changed)
    seen = set(changed)
    while queue:
        cur = queue.pop()
        for a in artifacts:
            deps = [input_path(i) for i in a.get('inputs', [])]
            if cur in deps and a['path'] not in stale:
                stale.add(a['path'])
                if a['path'] not in seen:
                    seen.add(a['path'])
                    queue.append(a['path'])
    return stale


def load_state(root):
    path = os.path.join(root, '.xy', 'STATE.json')
    if not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def report(root):
    state = load_state(root)
    if state is None:
        print('未找到 .xy/STATE.json —— 该项目尚未启用 xiangyu-workflow')
        return 0

    runs = state.get('runs', [])
    artifacts = state.get('artifacts', [])
    decisions = state.get('decisions', [])

    print('项目：%s' % state.get('project', '(未命名)'))
    print('工作流：%s   模式：%s' % (state.get('workflow', '?'), state.get('mode', '?')))
    print('更新：%s' % state.get('updated', '?'))
    print()

    done = [r for r in runs if r.get('status') == 'done']
    failed = [r for r in runs if r.get('status') == 'failed']
    running = [r for r in runs if r.get('status') == 'running']

    print('=== 进度 ===')
    print('已完成 %d 步' % len(done))
    for r in done:
        tag = {'full': '整步', 'focused': '局部', 'skipped': '跳过'}.get(r.get('scope', 'full'), '整步')
        outs = ', '.join(r.get('outputs', [])) or '(无记录)'
        print('  [%s] 步骤%s %s → %s' % (tag, r.get('step', 0), r.get('skill', '?'), outs))

    if failed:
        print('失败 %d 步' % len(failed))
        for r in failed:
            print('  x 步骤%s %s —— %s' % (r.get('step', 0), r.get('skill', '?'),
                                            r.get('reason', '未记录原因')))
    if running:
        print('运行中 %d 步（若已中断需恢复）' % len(running))
        for r in running:
            print('  ~ 步骤%s %s' % (r.get('step', 0), r.get('skill', '?')))

    print()
    print('=== 产物失效检查 ===')
    absent, changed = set(), set()

    for a in artifacts:
        rel = a['path']
        cur = current_hash(root, rel)
        if cur is None:
            absent.add(rel)
            continue
        if cur != a.get('sha256'):
            changed.add(rel)

    for a in artifacts:
        if a['path'] in absent:
            continue
        for spec in a.get('inputs', []):
            upstream = input_path(spec)
            want = input_hash(spec)
            got = current_hash(root, upstream)
            if got is None:
                continue
            if want and got != want:
                changed.add(a['path'])

    stale = (stale_cascade(artifacts, changed) - changed) if changed else set()

    if absent:
        print('丢失 %d 个产物：' % len(absent))
        for p in sorted(absent):
            print('  ! %s' % p)
    if changed:
        print('内容已变更 %d 个产物：' % len(changed))
        for p in sorted(changed):
            print('  ~ %s' % p)
    if stale:
        print('因传递依赖失效 %d 个（需重跑，本工具不重跑）：' % len(stale))
        for p in sorted(stale):
            print('  ! %s' % p)
    if not (absent or changed or stale):
        print('全部产物与记录一致')

    print()
    print('=== 已确认的决定 ===')
    if not decisions:
        print('（无）')
    for d in decisions:
        rejected = d.get('rejected', [])
        tail = '，已否决：%s' % '、'.join(rejected) if rejected else ''
        print('  * %s → %s%s' % (d.get('topic', '?'), d.get('choice') or '(仅否决)', tail))

    flags = state.get('flags', {})
    pending = flags.get('pending_gates', [])
    print()
    print('=== 待处理闸门 ===')
    if not pending:
        print('（无）')
    for g in pending:
        print('  > 步骤%s %s —— %s' % (g.get('step', '?'), g.get('skill', '?'), g.get('reason', '?')))

    print()
    print('（本工具只读，未写入任何文件、未调用模型、未改动任何步骤）')
    return 0


def main():
    global _CACHE
    _CACHE = {}
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    return report(root)


if __name__ == '__main__':
    sys.exit(main())
