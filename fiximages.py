# -*- coding: utf-8 -*-
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MATKONOT_DIR = os.path.join(ROOT, "source", "matkonot")
MAX_MATKONOT = 50


def folder_for(num):
    return "images" if num == 1 else "images%d" % num


def rename_images(num):
    folder = folder_for(num)
    img_dir = os.path.join(MATKONOT_DIR, folder)
    if not os.path.isdir(img_dir):
        return 0
    renamed = 0
    for name in sorted(os.listdir(img_dir)):
        path = os.path.join(img_dir, name)
        if not os.path.isfile(path):
            continue
        base, ext = os.path.splitext(name)
        base = base.replace(" ", "")
        ext = ext.lower()
        if base.startswith("m%d_" % num):
            continue
        m = re.match(r"^question(\d+)$", base, re.IGNORECASE)
        if not m:
            print("    [?] skipped: %s" % name)
            continue
        new_name = "m%d_question%s%s" % (num, m.group(1), ext)
        new_path = os.path.join(img_dir, new_name)
        if os.path.exists(new_path) and new_path.lower() != path.lower():
            print("    [!] exists, skipped: %s" % new_name)
            continue
        tmp = os.path.join(img_dir, new_name + ".tmp_rename")
        os.rename(path, tmp)
        os.rename(tmp, new_path)
        print("    %s -> %s" % (name, new_name))
        renamed += 1
    return renamed


def fix_md(num):
    folder = folder_for(num)
    changed = 0
    for key in ("short", "series", "trig", "calculus"):
        path = os.path.join(MATKONOT_DIR, "m%d_%s.md" % (num, key))
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        pattern = r"(%s/)(?!m%d_)question(\d+)\.(png|PNG)" % (re.escape(folder), num)
        new_content = re.sub(
            pattern,
            lambda mm: "%sm%d_question%s.png" % (mm.group(1), num, mm.group(2)),
            content,
        )
        if new_content != content:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_content)
            print("    updated: m%d_%s.md" % (num, key))
            changed += 1
    return changed


def main():
    if not os.path.isdir(MATKONOT_DIR):
        print("[!] not found: %s" % MATKONOT_DIR)
        return 1
    print("\n=== fixing image names ===\n")
    total_img = 0
    total_md = 0
    for num in range(1, MAX_MATKONOT + 1):
        if not os.path.isdir(os.path.join(MATKONOT_DIR, folder_for(num))):
            continue
        print("  matkonet %d:" % num)
        r = rename_images(num)
        c = fix_md(num)
        if r == 0 and c == 0:
            print("    already ok")
        total_img += r
        total_md += c
        print("")
    print("=== done ===")
    print("  images renamed: %d" % total_img)
    print("  md files updated: %d" % total_md)
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())