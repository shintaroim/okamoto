# -*- coding: utf-8 -*-
import subprocess
import os
import pymupdf

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORK_DIR = r"C:\AI Workspace\1_Projects\おかもっちゃん"
HTML = os.path.join(WORK_DIR, "prototype_showcase_temp.html")
PDF_TEST = os.path.join(WORK_DIR, "test_no_header.pdf")
TEST_PNG = os.path.join(WORK_DIR, "test_no_header_p1.png")

cmd = [
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_TEST}",
    HTML
]
res = subprocess.run(cmd, capture_output=True)
print("Returncode:", res.returncode)
print("PDF exists:", os.path.exists(PDF_TEST))

if os.path.exists(PDF_TEST):
    doc = pymupdf.open(PDF_TEST)
    pix = doc[0].get_pixmap(dpi=150)
    pix.save(TEST_PNG)
    print("Saved test png")
