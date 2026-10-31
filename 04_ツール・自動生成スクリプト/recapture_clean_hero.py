# -*- coding: utf-8 -*-
"""
キャプチャサイズ最適化＆再撮影
"""
import subprocess
import os

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORK_DIR = r"C:\AI Workspace\1_Projects\おかもっちゃん"
PROTO_DIR = os.path.join(WORK_DIR, "prototype")
CAP_DIR = os.path.join(WORK_DIR, "proto_captures")

targets = [
    {"name": "b_lp_hero", "file": "index.html", "w": 1200, "h": 780},
    {"name": "a_portal_hero", "file": "portal.html", "w": 1200, "h": 780},
    {"name": "c_academy_hero", "file": "academy.html", "w": 1200, "h": 780},
    {"name": "d_shop_hero", "file": "shop.html", "w": 1200, "h": 780},
]

for t in targets:
    out_png = os.path.join(CAP_DIR, f"{t['name']}.png")
    html_file = os.path.join(PROTO_DIR, t["file"])
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={t['w']},{t['h']}",
        f"--screenshot={out_png}",
        html_file
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"Captured {t['name']}.png (1200x780)")

print("Re-captured clean hero images.")
