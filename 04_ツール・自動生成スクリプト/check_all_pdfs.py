# -*- coding: utf-8 -*-
import os, pymupdf

pdf_dir = "01_完成成果物_PDF"
for fn in os.listdir(pdf_dir):
    if fn.endswith(".pdf"):
        doc = pymupdf.open(os.path.join(pdf_dir, fn))
        text = doc[0].get_text()
        has_date = "2026/10/31" in text
        print(f"{fn}: has_date = {has_date}")
        if has_date:
            for line in text.splitlines():
                if "2026/10/31" in line or "http" in line or "file:///" in line:
                    print("   Found line:", line)
