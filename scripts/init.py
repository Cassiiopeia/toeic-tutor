#!/usr/bin/env python3
"""my/ 뼈대를 만든다. my.example/ 를 그대로 복사하고, .gitignore 를 보강한다.

    python3 scripts/init.py          (Windows: python scripts/init.py)

질문(점수·목표·약점)은 여기서 하지 않는다 — 조수가 채팅으로 묻고 my/profile.md 에 적는다.
my/ 가 이미 있으면 아무것도 건드리지 않는다. 남의 기록을 덮어쓰는 일은 없어야 한다.

.gitignore 보강은 my/ 존재 여부와 무관하게 매번 돌린다. 이 레포는 clone 해서 쓰는 공개 레포라,
성적표 PDF·점수 캡처 같은 개인 자료가 레포에 남으면 그대로 공개된다. 개인 자료가 들어갈 수 있는
경로를 미리 막아 둔다.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: 개인 자료가 커밋되면 안 되는 경로. init 이 .gitignore 에 없으면 채워 넣는다.
#: 루트 한정 패턴(/*.pdf 등)이라 docs/ 안의 문서용 이미지는 막지 않는다.
PRIVATE_PATTERNS = [
    ("/my/", "개인 기록 — 점수·오답·세션"),
    ("/private/", "성적표 PDF·점수 캡처 등 조수에게 준 개인 파일은 여기에"),
    ("/*.pdf", "루트에 떨어진 성적표·교재 PDF"),
    ("/*.png", "루트에 떨어진 점수 캡처"),
    ("/*.jpg", None),
    ("/*.jpeg", None),
    ("/*.webp", None),
]

HEADER = "# 개인 자료 — init.py 가 채운다. 이 레포는 공개라 개인 파일이 커밋되면 그대로 공개된다"


def ensure_gitignore(root):
    """.gitignore 에 PRIVATE_PATTERNS 를 보강한다. 추가한 패턴 목록을 돌려준다.

    이미 있는 줄은 건드리지 않는다. 두 번 돌려도 아무것도 더 붙지 않는다.
    """
    nl = chr(10)
    path = Path(root) / ".gitignore"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    present = {line.split("#")[0].strip() for line in text.splitlines()}

    missing = [(pat, note) for pat, note in PRIVATE_PATTERNS if pat not in present]
    if not missing:
        return []

    # gitignore 에서 '#' 는 줄 맨 앞에서만 주석이다. 패턴 뒤에 붙이면 패턴이 통째로 죽는다.
    block = ["", HEADER]
    for pat, note in missing:
        if note:
            block.append("# " + note)
        block.append(pat)

    if text and not text.endswith(nl):
        text += nl
    path.write_text(text + nl.join(block) + nl, encoding="utf-8")
    return [pat for pat, _ in missing]


def copy_example(root):
    """my.example/ → my/. 이미 있으면 False."""
    src, dst = Path(root) / "my.example", Path(root) / "my"
    if dst.exists():
        return False
    shutil.copytree(src, dst)
    return True


def main():
    added = ensure_gitignore(ROOT)
    if added:
        print("[+] .gitignore 보강: " + " ".join(added))

    if copy_example(ROOT):
        print("[+] my/ 를 만들었다. 이제 조수가 점수·목표·약점을 묻는다 (/toeic init).")
    else:
        print("my/ 가 이미 있다. 건드리지 않았다.", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
