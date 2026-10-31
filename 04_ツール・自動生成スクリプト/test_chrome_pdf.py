# -*- coding: utf-8 -*-
import subprocess
import os
import pymupdf

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cur_dir = os.path.abspath(".")
html_test = os.path.join(cur_dir, "test_header.html")
with open(html_test, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
<title>My Document Title</title>
<style>
@page {
    size: A4 portrait;
    margin: 15mm;
}
body { font-family: sans-serif; }
</style>
</head>
<body>
<h1>Hello World</h1>
</body>
</html>""")

flag_tests = [
    ["--no-pdf-header-footer"],
    ["--print-to-pdf-no-header"],
    [],
]

for i, flags in enumerate(flag_tests):
    out_pdf = os.path.join(cur_dir, f"test_out_{i}.pdf")
    if os.path.exists(out_pdf):
        os.remove(out_pdf)
    cmd = [CHROME, "--headless=new", "--disable-gpu", f"--print-to-pdf={out_pdf}"] + flags + [html_test]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(out_pdf):
        doc = pymupdf.open(out_pdf)
        text = doc[0].get_text()
        print(f"Test {i} ({flags}): text = {repr(text.strip())}")
    else:
        print(f"Test {i} ({flags}): FAILED. stderr: {res.stderr[:200]}")
