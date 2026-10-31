# -*- coding: utf-8 -*-
"""
岡本武司（おかもっちゃん / 瑞司）Webプロトタイプ画面集 PDF生成スクリプト
ヘッダー日時・ファイル名非表示（--no-pdf-header-footer）対応版
"""

import os
import subprocess
import pymupdf

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HTML_PATH = os.path.join("05_作業中間データ・プレビュー", "prototype_showcase_temp.html")
PDF_PATH = os.path.join("01_完成成果物_PDF", "岡本武司_Webプロトタイプ画面集.pdf")
PREVIEW_DIR = os.path.join("05_作業中間データ・プレビュー", "pdf_preview_showcase")

def render_showcase_pdf():
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        f"--print-to-pdf={PDF_PATH}",
        "--no-pdf-header-footer",
        HTML_PATH
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Chrome exit code:", res.returncode)
    print(f"Generated Showcase PDF: {os.path.exists(PDF_PATH)} ({os.path.getsize(PDF_PATH)} bytes)")

def check_pdf():
    doc = pymupdf.open(PDF_PATH)
    print(f"Total Showcase PDF pages: {len(doc)}")
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        p = os.path.join(PREVIEW_DIR, f"showcase_page_{i+1}.png")
        pix.save(p)
        print(f"Saved {p}")

if __name__ == "__main__":
    render_showcase_pdf()
    check_pdf()
