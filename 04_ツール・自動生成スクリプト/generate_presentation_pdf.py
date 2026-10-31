# -*- coding: utf-8 -*-
"""
岡本武司（おかもっちゃん / 瑞司）全企画案 詳細説明資料 HTML & PDF 生成スクリプト
ヘッダー日時・ファイル名非表示（--no-pdf-header-footer）対応版
"""

import os
import subprocess
import pymupdf

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HTML_PATH = os.path.join("05_作業中間データ・プレビュー", "presentation_doc.html")
PDF_PATH = os.path.join("01_完成成果物_PDF", "岡本武司_全企画案_詳細説明資料.pdf")
PREVIEW_DIR = os.path.join("05_作業中間データ・プレビュー", "pdf_preview_presentation")

def build_presentation_html():
    # 既存のHTMLを読み込んで再利用するか、生成する
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    return html

def render_pdf():
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
    print(f"Generated PDF: {os.path.exists(PDF_PATH)} ({os.path.getsize(PDF_PATH)} bytes)")

def check_pdf_pages():
    doc = pymupdf.open(PDF_PATH)
    page_count = len(doc)
    print(f"Total PDF pages: {page_count}")
    
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    png_paths = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        png_path = os.path.join(PREVIEW_DIR, f"page_{i+1}.png")
        pix.save(png_path)
        png_paths.append(png_path)
        print(f"Saved {png_path} ({pix.width}x{pix.height})")
    return png_paths

if __name__ == "__main__":
    render_pdf()
    check_pdf_pages()
