# -*- coding: utf-8 -*-
with open("generate_pdfs.py", "r", encoding="utf-8") as f:
    text = f.read()

for line in text.splitlines():
    if "chrome" in line.lower() or "print" in line.lower():
        print(line)
