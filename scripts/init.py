#!/usr/bin/env python3
"""my/ 뼈대를 만든다. my.example/ 를 그대로 복사한다.

    python3 scripts/init.py

질문(점수·목표·약점)은 여기서 하지 않는다 — 조수가 채팅으로 묻고 my/profile.md 에 적는다.
my/ 가 이미 있으면 아무것도 건드리지 않는다. 남의 기록을 덮어쓰는 일은 없어야 한다.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def copy_example(root):
    """my.example/ → my/. 이미 있으면 False."""
    src, dst = root / "my.example", root / "my"
    if dst.exists():
        return False
    shutil.copytree(src, dst)
    return True


def main():
    if copy_example(ROOT):
        print("[+] my/ 를 만들었다. 이제 조수가 점수·목표·약점을 묻는다 (/toeic init).")
    else:
        print("my/ 가 이미 있다. 건드리지 않았다.", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
