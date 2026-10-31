# -*- coding: utf-8 -*-
"""
プロトタイプ各画面の高解像度キャプチャ生成スクリプト
"""

import subprocess
import os

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORK_DIR = r"C:\AI Workspace\1_Projects\おかもっちゃん"
PROTO_DIR = os.path.join(WORK_DIR, "prototype")
CAP_DIR = os.path.join(WORK_DIR, "proto_captures")
os.makedirs(CAP_DIR, exist_ok=True)

targets = [
    {"name": "b_lp_hero", "file": "index.html", "w": 1200, "h": 900},
    {"name": "b_lp_services", "file": "index.html", "w": 1200, "h": 1600},
    {"name": "a_portal_hero", "file": "portal.html", "w": 1200, "h": 950},
    {"name": "a_portal_full", "file": "portal.html", "w": 1200, "h": 1600},
    {"name": "c_academy_hero", "file": "academy.html", "w": 1200, "h": 950},
    {"name": "c_academy_full", "file": "academy.html", "w": 1200, "h": 1600},
    {"name": "d_shop_hero", "file": "shop.html", "w": 1200, "h": 950},
    {"name": "d_shop_full", "file": "shop.html", "w": 1200, "h": 1600},
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
    print(f"Captured {t['name']}.png: {os.path.exists(out_png)}")

print("All screenshots generated successfully.")
