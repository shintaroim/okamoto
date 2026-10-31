# -*- coding: utf-8 -*-
import os, subprocess, pymupdf

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cur_dir = os.path.abspath(".")

html_path = os.path.join(cur_dir, "05_作業中間データ・プレビュー", "prototype_showcase_temp.html")
out_pdf = os.path.join(cur_dir, "01_完成成果物_PDF", "岡本武司_Webプロトタイプ画面集.pdf")
preview_dir = os.path.join(cur_dir, "05_作業中間データ・プレビュー", "pdf_preview_showcase")

# 再生成
cmd = [
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=6000",
    "--no-pdf-header-footer",
    f"--print-to-pdf={out_pdf}",
    html_path
]
res = subprocess.run(cmd, capture_output=True)
print("Returncode:", res.returncode)

doc = pymupdf.open(out_pdf)
print(f"Pages: {len(doc)}")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    p = os.path.join(preview_dir, f"showcase_page_{i+1}.png")
    pix.save(p)
    text = page.get_text()
    has_date = "2026/10/31" in text
    print(f"Page {i+1}: has_date = {has_date}")
