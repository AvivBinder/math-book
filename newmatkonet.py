# -*- coding: utf-8 -*-
import sys
import os
import re

SECTIONS = [
    ("short",    "שאלות קצרות",                 [1, 2, 3, 4]),
    ("series",   "סדרות והסתברות",              [5, 6]),
    ("trig",     "טריגונומטריה וגאומטריה",       [7, 8]),
    ("calculus", "חשבון דיפרנציאלי ואינטגרלי",  [9, 10, 11]),
]

ROOT = os.path.dirname(os.path.abspath(__file__))
MATKONOT_DIR = os.path.join(ROOT, "source", "matkonot")
INDEX_RST = os.path.join(ROOT, "source", "index.rst")


def fix_image_names(img_dir):
    if not os.path.isdir(img_dir):
        return 0
    fixed = 0
    for name in os.listdir(img_dir):
        old_path = os.path.join(img_dir, name)
        if not os.path.isfile(old_path):
            continue
        base, ext = os.path.splitext(name)
        new_name = base.replace(" ", "") + ext.lower()
        if new_name != name:
            tmp_path = os.path.join(img_dir, new_name + ".tmp_rename")
            os.rename(old_path, tmp_path)
            os.rename(tmp_path, os.path.join(img_dir, new_name))
            print("  shem tukan: %s -> %s" % (name, new_name))
            fixed += 1
    return fixed


def check_images(img_dir, expected=11):
    missing = []
    for i in range(1, expected + 1):
        if not os.path.isfile(os.path.join(img_dir, "question%d.png" % i)):
            missing.append(i)
    return missing


def write_file(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("  created: %s" % os.path.relpath(path, ROOT))


def build_section(title, questions, img_folder):
    lines = ["# %s" % title, ""]
    for q in questions:
        lines.append("```{image} %s/question%d.png" % (img_folder, q))
        lines.append(":width: 600px")
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def build_main(num):
    lines = ["# מתכונת %d" % num, "", "```{toctree}", ":maxdepth: 1", ""]
    for key, _t, _q in SECTIONS:
        lines.append("m%d_%s" % (num, key))
    lines += [
        "```",
        "",
        "## תשובות סופיות",
        "",
        "```{raw} html",
        '<iframe src="../_static/matkonet%d-answers.pdf" width="100%%" height="800px" style="border: 1px solid #ccc;"></iframe>' % num,
        '<p><a href="../_static/matkonet%d-answers.pdf" download>הורדת הקובץ</a></p>' % num,
        "```",
        "",
    ]
    return "\n".join(lines)


def update_index(num):
    entry = "matkonot/matkonet%d" % num
    if not os.path.isfile(INDEX_RST):
        print("  [!] index.rst not found - add manually: %s" % entry)
        return
    with open(INDEX_RST, "r", encoding="utf-8") as f:
        content = f.read()
    if entry in content:
        print("  index.rst: already there")
        return
    lines = content.split("\n")
    last_idx = None
    indent = "   "
    for i, line in enumerate(lines):
        if re.match(r"^\s+matkonot/matkonet\d+\s*$", line):
            last_idx = i
            indent = line[:len(line) - len(line.lstrip())]
    if last_idx is None:
        print("  [!] toctree not found - add manually: %s" % entry)
        return
    lines.insert(last_idx + 1, indent + entry)
    with open(INDEX_RST, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print("  index.rst: added %s" % entry)


def main():
    if len(sys.argv) < 2 or not sys.argv[1].isdigit():
        print("usage:  py newmatkonet.py <number>")
        return 1

    num = int(sys.argv[1])
    img_folder = "images" if num == 1 else "images%d" % num
    img_dir = os.path.join(MATKONOT_DIR, img_folder)

    print("\n=== matkonet %d ===" % num)
    os.makedirs(img_dir, exist_ok=True)

    print("\n[1] image names")
    if fix_image_names(img_dir) == 0:
        print("  nothing to fix")

    missing = check_images(img_dir)
    if missing:
        print("\n  [!] missing: %s" % ", ".join("question%d.png" % m for m in missing))
        print("  put them in: %s" % os.path.relpath(img_dir, ROOT))

    print("\n[2] creating files")
    for key, title, questions in SECTIONS:
        path = os.path.join(MATKONOT_DIR, "m%d_%s.md" % (num, key))
        if os.path.exists(path):
            print("  skipped (exists): m%d_%s.md" % (num, key))
            continue
        write_file(path, build_section(title, questions, img_folder))

    main_path = os.path.join(MATKONOT_DIR, "matkonet%d.md" % num)
    if os.path.exists(main_path):
        print("  skipped (exists): matkonet%d.md" % num)
    else:
        write_file(main_path, build_main(num))

    print("\n[3] index.rst")
    update_index(num)

    print("\n=== done ===")
    print("next:")
    print("  1. images -> source\\matkonot\\%s" % img_folder)
    print("  2. matkonet%d-answers.pdf -> source\\_static" % num)
    print("  3. py -m sphinx source build\\html")
    print("  4. git add .  /  git commit -m \"Add matkonet %d\"  /  git push" % num)
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())