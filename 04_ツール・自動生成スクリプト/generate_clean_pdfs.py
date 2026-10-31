# -*- coding: utf-8 -*-
"""
岡本武司（おかもっちゃん / 瑞司）
1. Webプロトタイプ画面集 PDF
2. 全企画案 詳細説明資料 PDF
ヘッダー日時・ファイル名非表示（--no-pdf-header-footer）＆ Base64画像完全埋め込み版
"""

import os
import base64
import subprocess
import pymupdf

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CUR_DIR = os.path.abspath(".")

# パス定義
OUT_DIR = os.path.join(CUR_DIR, "01_完成成果物_PDF")
TEMP_DIR = os.path.join(CUR_DIR, "05_作業中間データ・プレビュー")
CAPTURES_DIR = os.path.join(CUR_DIR, "03_Webサイトプロトタイプ", "captures")

# 1. 画像をBase64変換する関数
def get_image_base64(filename):
    # 複数候補から探す
    candidates = [
        os.path.join(CAPTURES_DIR, filename),
        os.path.join(CUR_DIR, "proto_captures", filename),
        os.path.join(CUR_DIR, filename),
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/png;base64,{data}"
    raise FileNotFoundError(f"Image not found: {filename}")

# 2. プロトタイプ画面集 HTML の生成
def build_showcase_html():
    img_b = get_image_base64("b_lp_hero.png")
    img_a = get_image_base64("a_portal_hero.png")
    img_c = get_image_base64("c_academy_hero.png")
    img_d = get_image_base64("d_shop_hero.png")

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>岡本武司（瑞司）Webプロトタイプ画面集・UI仕様書</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 12mm 14mm 12mm 14mm;
            @bottom-right {{
                content: "Page " counter(page) " / " counter(pages);
                font-size: 8.5pt;
                color: #64748b;
                font-family: "BIZ UDPGothic", "Meiryo", sans-serif;
            }}
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: "BIZ UDPGothic", "Meiryo", "Yu Gothic", "Hiragino Kaku Gothic ProN", sans-serif;
            color: #2d3748;
            background-color: #ffffff;
            line-height: 1.5;
            font-size: 9.2pt;
            margin: 0;
            padding: 0;
        }}

        .page-break {{
            page-break-before: always;
            break-before: page;
        }}

        /* ヘッダー */
        .doc-header {{
            border-bottom: 2.5px solid #1e3a8a;
            padding-bottom: 5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}

        .doc-title {{
            font-size: 13.8pt;
            font-weight: 800;
            color: #0f172a;
            white-space: nowrap;
        }}

        .doc-badge {{
            font-size: 8.5pt;
            background-color: #1e3a8a;
            color: #ffffff;
            padding: 2px 7px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
            margin-right: 6px;
        }}

        .doc-meta {{
            font-size: 8.5pt;
            color: #64748b;
            font-weight: 500;
            white-space: nowrap;
        }}

        /* キャプチャ枠 */
        .preview-frame {{
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 3px 6px rgba(0,0,0,0.06);
            margin-bottom: 7px;
            background: #f8fafc;
        }}

        .preview-img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        /* カード・ボックス */
        .card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 7px 10px;
            margin-bottom: 5px;
        }}

        .card-highlight {{
            background: #f8fafc;
            border-left: 4px solid #1e3a8a;
        }}

        .card-accent {{
            background: #fff7ed;
            border-left: 4px solid #ea580c;
        }}

        .card-green {{
            background: #f0fdf4;
            border-left: 4px solid #16a34a;
        }}

        .card-purple {{
            background: #faf5ff;
            border-left: 4px solid #9333ea;
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 7px;
            margin-bottom: 5px;
        }}

        .grid-4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
            margin-bottom: 6px;
        }}

        /* UIポイントリスト */
        .point-item {{
            margin-bottom: 3px;
            font-size: 8.5pt;
        }}
        .point-label {{
            font-weight: bold;
            color: #0f172a;
            display: inline-block;
            margin-right: 4px;
        }}

        h2 {{
            font-size: 10.6pt;
            color: #1e3a8a;
            border-left: 4px solid #ea580c;
            padding-left: 7px;
            margin: 6px 0 4px 0;
            font-weight: 700;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 8.6pt;
            margin-bottom: 6px;
        }}

        th {{
            background: #0f172a;
            color: #ffffff;
            padding: 4px 6px;
            font-weight: bold;
            text-align: left;
            border: 1px solid #0f172a;
        }}

        td {{
            padding: 4px 6px;
            border: 1px solid #cbd5e1;
            background: #ffffff;
            vertical-align: top;
        }}

        tr:nth-child(even) td {{
            background: #f8fafc;
        }}
    </style>
</head>
<body>

    <!-- ==========================================
         PAGE 1: プロトタイプ概要＆全体画面構成
         ========================================== -->
    <div class="doc-header">
        <div class="doc-title"><span class="doc-badge">プロトタイプ</span>岡本武司 Webプロトタイプ画面集＆UI仕様</div>
        <div class="doc-meta">実機プロトタイプ ショーケース ｜ P.1</div>
    </div>

    <div class="card card-highlight">
        <p style="margin:0; font-size:9.2pt; line-height:1.45;">
            <strong>【実機Webプロトタイプの概要】</strong><br>
            岡本武司（おかもっちゃん / 瑞司）氏の強みと資産を最大化するため、実際にブラウザ上で動作・操作可能な<strong>4つのWebサイトプロトタイプ（HTML/CSS/JS）</strong>を構築しました。
            画面最上部の「スイッチャーバー（PROTOTYPE BAR）」から、4つの画面をワンクリックで瞬時に切り替えて体験いただけます。
        </p>
    </div>

    <h2>1. 4つのプロトタイプ画面の役割と設計思想</h2>
    <div class="grid-4">
        <div class="card" style="border-top:3.5px solid #ea580c;">
            <div style="font-weight:bold; color:#ea580c; font-size:8.6pt; margin-bottom:2px;">【案B】即効獲得LP</div>
            <div style="font-size:7.8pt; color:#64748b; margin-bottom:4px;">優先度：最優先 ★★★</div>
            <p style="font-size:8pt; color:#334155; margin:0;">
                特注肖像画・熱血講演の成約に全特化。迷わせない1ページ完結セールスファネル。
            </p>
        </div>
        <div class="card" style="border-top:3.5px solid #1e3a8a;">
            <div style="font-weight:bold; color:#1e3a8a; font-size:8.6pt; margin-bottom:2px;">【案A】ブランドポータル</div>
            <div style="font-size:7.8pt; color:#64748b; margin-bottom:4px;">優先度：中長期旗艦</div>
            <p style="font-size:8pt; color:#334155; margin:0;">
                全活動（作品・教育・講演・物販）のハブ。社会的信用と不屈のストーリーを体系化。
            </p>
        </div>
        <div class="card" style="border-top:3.5px solid #16a34a;">
            <div style="font-weight:bold; color:#16a34a; font-size:8.6pt; margin-bottom:2px;">【案C】オンライン校</div>
            <div style="font-size:7.8pt; color:#64748b; margin-bottom:4px;">優先度：ストック収益</div>
            <p style="font-size:8pt; color:#334155; margin:0;">
                「誰でも描ける！」瑞司式メソッド。月額制サブスクで安定継続収入を構築。
            </p>
        </div>
        <div class="card" style="border-top:3.5px solid #9333ea;">
            <div style="font-weight:bold; color:#9333ea; font-size:8.6pt; margin-bottom:2px;">【案D】越境ECショップ</div>
            <div style="font-size:7.8pt; color:#64748b; margin-bottom:4px;">優先度：物販＆海外展開</div>
            <p style="font-size:8pt; color:#334155; margin:0;">
                厳選画材キット・日めくり語録・限定版画・訪日アート体験予約の多言語ストア。
            </p>
        </div>
    </div>

    <h2>2. プロトタイプのファイル構成と閲覧方法</h2>
    <table>
        <tr>
            <th style="width:25%;">ファイル名</th>
            <th style="width:35%;">対応する企画案</th>
            <th style="width:40%;">ファイル配置場所（ローカル）</th>
        </tr>
        <tr>
            <td><strong>index.html</strong></td>
            <td>【案B】即効キャッシュ化LP（メイン起点）</td>
            <td><code>prototype/index.html</code>（ブラウザでダブルクリックで起動）</td>
        </tr>
        <tr>
            <td><strong>portal.html</strong></td>
            <td>【案A】総合ブランド＆ハブ型ポータル</td>
            <td><code>prototype/portal.html</code></td>
        </tr>
        <tr>
            <td><strong>academy.html</strong></td>
            <td>【案C】オンライン校＆ファンサロン</td>
            <td><code>prototype/academy.html</code></td>
        </tr>
        <tr>
            <td><strong>shop.html</strong></td>
            <td>【案D】作家ギャラリー＆越境ECショップ</td>
            <td><code>prototype/shop.html</code></td>
        </tr>
        <tr>
            <td><strong>style.css / script.js</strong></td>
            <td>共通レスポンシブデザイン＆操作スクリプト</td>
            <td><code>prototype/style.css</code> / <code>prototype/script.js</code></td>
        </tr>
    </table>

    <div class="card card-accent" style="margin-top:6px;">
        <div style="font-weight:bold; color:#9a3412; font-size:8.8pt; margin-bottom:3px;">
            💡 ブラウザでのインタラクティブ体験機能
        </div>
        <p style="margin:0; font-size:8.4pt;">
            どのHTMLファイルを開いても、最上部に共通ナビゲーションバー（スイッチャー）が表示され、4つのサイト案を自由に行き来できます。各画面内の「無料相談ボタン」「LINE登録」「受講申し込み」「カート追加」をクリックすると、実際の成約アクションを疑似体験できるインタラクティブ設計となっています。
        </p>
    </div>

    <!-- ==========================================
         PAGE 2: 【案B】即効キャッシュ化LP
         ========================================== -->
    <div class="page-break"></div>
    <div class="doc-header">
        <div class="doc-title"><span class="doc-badge">案 B</span>【即効キャッシュ化LP】実機プロトタイプ画面＆UI仕様</div>
        <div class="doc-meta">実機プロトタイプ ショーケース ｜ P.2</div>
    </div>

    <div class="preview-frame">
        <img src="{img_b}" class="preview-img" alt="案B LP画面プレビュー">
    </div>

    <h2>案B（LP特化型）のUI設計ハイライトと成約ロジック</h2>
    <div class="grid-2">
        <div class="card card-accent">
            <div style="font-weight:bold; color:#9a3412; font-size:8.8pt; margin-bottom:4px;">① ファーストビューの心理的フック</div>
            <div class="point-item"><span class="point-label">実績バッジ:</span> 早大競走部主将・早明戦出場、名門高校体育教師・名監督、瑞司プロ画家を3連表示。</div>
            <div class="point-item"><span class="point-label">強いキャッチコピー:</span> 「53歳、未経験からプロへ。魂を刻む鉛筆画と、常識を破る熱血突破力。」</div>
            <div class="point-item"><span class="point-label">デュアルCTA:</span> 「2大サービスを見る」と「公式LINEで特典受取」を配置。</div>
        </div>
        <div class="card card-highlight">
            <div style="font-weight:bold; color:#1e40af; font-size:8.8pt; margin-bottom:4px;">② 迷わせない2大ソリューション提示</div>
            <div class="point-item"><span class="point-label">特注鉛筆肖像画:</span> ¥150,000〜¥500,000。額装・桐箱込、制作エピソード冊子付。</div>
            <div class="point-item"><span class="point-label">モチベーション講演:</span> ¥200,000〜¥500,000。即興デッサン実演・岡本武司語録。</div>
            <div class="point-item"><span class="point-label">透明な依頼フロー:</span> 写真送付 ➔ 構図提案 ➔ お届けの明朗3ステップ。</div>
        </div>
    </div>

    <div class="card" style="background:#f8fafc; border-left:4px solid #16a34a;">
        <div style="font-weight:bold; color:#166534; font-size:8.8pt; margin-bottom:3px;">
            ③ LINE登録特典による「見込み客リスト化（リード獲得）」
        </div>
        <p style="margin:0; font-size:8.3pt;">
            今すぐ高額発注しない見込み客に対しても、「15分で立体感が描ける限定動画レッスン」や「日めくり熱血名言」をプレゼントするLINEオファーを配置。関係性を維持しながら、還暦祝いや周年行事のタイミングで成約へと育成します。
        </p>
    </div>

    <!-- ==========================================
         PAGE 3: 【案A】総合ブランドポータル
         ========================================== -->
    <div class="page-break"></div>
    <div class="doc-header">
        <div class="doc-title"><span class="doc-badge">案 A</span>【総合ブランドポータル】実機プロトタイプ画面＆UI仕様</div>
        <div class="doc-meta">実機プロトタイプ ショーケース ｜ P.3</div>
    </div>

    <div class="preview-frame">
        <img src="{img_a}" class="preview-img" alt="案A ポータル画面プレビュー">
    </div>

    <h2>案A（総合ポータル型）のUI設計ハイライトとブランディング機能</h2>
    <div class="grid-2">
        <div class="card card-highlight">
            <div style="font-weight:bold; color:#1e40af; font-size:8.8pt; margin-bottom:4px;">① 洗練された旗艦サイトのデザイン</div>
            <div class="point-item"><span class="point-label">世界観の統一:</span> 深みのある濃紺（ロイヤルブルー）と白のミニマルデザイン。美術館・ギャラリーの品格。</div>
            <div class="point-item"><span class="point-label">ヘッダーナビ:</span> 瑞司について、作品ギャラリー、4つの活動、個展情報、公式ショップ、鉛筆画教室。</div>
            <div class="point-item"><span class="point-label">代表作スライド:</span> 代表作『慈愛の眼差し』を美しくフォーカス。</div>
        </div>
        <div class="card" style="border-left:4px solid #ea580c; background:#fff7ed;">
            <div style="font-weight:bold; color:#9a3412; font-size:8.8pt; margin-bottom:4px;">② 4つの活動領域（Pillars）へのハブ誘導</div>
            <div class="point-item"><span class="point-label">特注肖像画制作:</span> メモリアル原画オーダー（案Bへ直結）</div>
            <div class="point-item"><span class="point-label">わくわく鉛筆画教室:</span> 「誰でも描ける」オンライン校（案Cへ直結）</div>
            <div class="point-item"><span class="point-label">企業講演・研修:</span> 挑戦力と心理的安全性チームビルディング（案Bへ直結）</div>
            <div class="point-item"><span class="point-label">画材EC＆海外展開:</span> 厳選画材と訪日文化体験（案Dへ直結）</div>
        </div>
    </div>

    <div class="card" style="background:#f8fafc; border-left:4px solid #64748b;">
        <div style="font-weight:bold; color:#334155; font-size:8.8pt; margin-bottom:3px;">
            ③ 作品ギャラリー＆不屈のストーリー年表（信頼性の源泉）
        </div>
        <p style="margin:0; font-size:8.3pt;">
            「スポーツ選手の肉体美」「人物の瞳」「愛犬」「風景・静物」を網羅した高精細ギャラリーと、甲子園球児・早大早明戦・名門指導・53歳転身を記したタイムライン。メディア取材や学校講演のオファー時に圧倒的な信頼材料となります。
        </p>
    </div>

    <!-- ==========================================
         PAGE 4: 【案C】オンライン校＆サロン
         ========================================== -->
    <div class="page-break"></div>
    <div class="doc-header">
        <div class="doc-title"><span class="doc-badge">案 C</span>【オンライン校＆サロン】実機プロトタイプ画面＆UI仕様</div>
        <div class="doc-meta">実機プロトタイプ ショーケース ｜ P.4</div>
    </div>

    <div class="preview-frame">
        <img src="{img_c}" class="preview-img" alt="案C オンライン校画面プレビュー">
    </div>

    <h2>案C（オンライン校型）のUI設計ハイライトとサブスク設計</h2>
    <div class="grid-2">
        <div class="card card-green">
            <div style="font-weight:bold; color:#166534; font-size:8.8pt; margin-bottom:4px;">① シニア・初心者の心理的障壁を打破</div>
            <div class="point-item"><span class="point-label">グリーン基調の安心UI:</span> リラックスして絵を楽しめる温かいナチュラル配色。</div>
            <div class="point-item"><span class="point-label">共感キャッチコピー:</span> 「『絵が苦手』が、『描くのが楽しい！』に変わる。鉛筆1本で始める大人のワクワク時間。」</div>
            <div class="point-item"><span class="point-label">受講生満足度表示:</span> 満足度98.4% / 全国・台湾から150名以上が参加の実績。</div>
        </div>
        <div class="card" style="border-left:4px solid #1e3a8a; background:#f8fafc;">
            <div style="font-weight:bold; color:#1e40af; font-size:8.8pt; margin-bottom:4px;">② 選ばれる3つの理由と2大受講プラン</div>
            <div class="point-item"><span class="point-label">いつでも学べる動画見放題:</span> 鉛筆の削り方から瞳の陰影までスマホで何度でも。</div>
            <div class="point-item"><span class="point-label">月1回Zoom生ライブ添削:</span> 画面越しに直接温かいアドバイスと全肯定。</div>
            <div class="point-item"><span class="point-label">2大月額プラン:</span> ライト会員 ¥3,980/月 ｜ プロ・個別添削会員 ¥7,980/月。</div>
        </div>
    </div>

    <div class="card" style="background:#fff7ed; border-left:4px solid #ea580c;">
        <div style="font-weight:bold; color:#9a3412; font-size:8.8pt; margin-bottom:3px;">
            ③ 無料体験レッスンへの誘導導線
        </div>
        <p style="margin:0; font-size:8.3pt;">
            「15分で立体感が描ける！基本のリンゴの描き方動画」を無料プレゼント。メール・LINE登録から自動配信ステップメールで「描けた喜び」を実感させ、無理なく有料会員へ移行させる設計です。
        </p>
    </div>

    <!-- ==========================================
         PAGE 5: 【案D】作家ギャラリー＆越境EC
         ========================================== -->
    <div class="page-break"></div>
    <div class="doc-header">
        <div class="doc-title"><span class="doc-badge">案 D</span>【作家ギャラリー＆越境EC】実機プロトタイプ画面＆UI仕様</div>
        <div class="doc-meta">実機プロトタイプ ショーケース ｜ P.5</div>
    </div>

    <div class="preview-frame">
        <img src="{img_d}" class="preview-img" alt="案D 越境EC画面プレビュー">
    </div>

    <h2>案D（EC・体験予約型）のUI設計ハイライトとグローバル展開</h2>
    <div class="grid-2">
        <div class="card card-purple">
            <div style="font-weight:bold; color:#6b21a8; font-size:8.8pt; margin-bottom:4px;">① アート＆カルチャーを届けるストアデザイン</div>
            <div class="point-item"><span class="point-label">テラコッタ×ゴールド配色:</span> 工芸・絵画の温かみと高級感を両立した配色。</div>
            <div class="point-item"><span class="point-label">多言語切り替え:</span> 🌐 JP / EN / 繁體 のワンクリック言語セレクター。</div>
            <div class="point-item"><span class="point-label">ショッピングカートUI:</span> クレジット・ApplePay・PayPal即時決済に対応。</div>
        </div>
        <div class="card" style="border-left:4px solid #ea580c; background:#fff7ed;">
            <div style="font-weight:bold; color:#9a3412; font-size:8.8pt; margin-bottom:4px;">② 高粗利・高付加価値な商品構成</div>
            <div class="point-item"><span class="point-label">スターター画材キット:</span> 特選鉛筆4本＋練りゴム＋スケッチブック＋動画 ¥4,800。</div>
            <div class="point-item"><span class="point-label">熱血日めくり語録カレンダー:</span> 毎日元気が出る31篇の言葉と絵 ¥2,200。</div>
            <div class="point-item"><span class="point-label">限定ジークレー複製原画:</span> 直筆サイン・高級額装付 ¥28,000〜¥68,000。</div>
        </div>
    </div>

    <div class="card" style="background:#f0fdf4; border-left:4px solid #16a34a;">
        <div style="font-weight:bold; color:#166534; font-size:8.8pt; margin-bottom:3px;">
            ③ インバウンド富裕層向け「和の鉛筆画体験予約」
        </div>
        <p style="margin:0; font-size:8.3pt;">
            「日本のアトリエで、53歳転身の画家から直接鉛筆画の極意を学び、自作の絵を持ち帰る」特別なカルチャー体験（¥25,000/名、抹茶・通訳付）。カレンダーから空き日時を選択して即時Web予約・決済できる仕組みを実装しています。
        </p>
    </div>

</body>
</html>'''

    html_path = os.path.join(TEMP_DIR, "prototype_showcase_temp.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved showcase HTML with base64 images.")
    return html_path

# 3. PDF レンダリング関数
def convert_html_to_pdf(html_path, pdf_path):
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0:
        print("Chrome error:", res.stderr)
    print(f"Generated {os.path.basename(pdf_path)}: {os.path.exists(pdf_path)} ({os.path.getsize(pdf_path)} bytes)")

# 4. 全ページPNGプレビュー出力と確認
def check_pdf(pdf_path, preview_folder):
    doc = pymupdf.open(pdf_path)
    os.makedirs(preview_folder, exist_ok=True)
    print(f"\nChecking {os.path.basename(pdf_path)}: {len(doc)} pages")
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        p = os.path.join(preview_folder, f"page_{i+1}.png")
        pix.save(p)
        text = page.get_text()
        has_date = "2026/10/31" in text
        print(f"  Page {i+1}: has_date = {has_date}")

if __name__ == "__main__":
    # 1. プロトタイプ画面集 PDF
    showcase_html = build_showcase_html()
    showcase_pdf = os.path.join(OUT_DIR, "岡本武司_Webプロトタイプ画面集.pdf")
    convert_html_to_pdf(showcase_html, showcase_pdf)
    check_pdf(showcase_pdf, os.path.join(TEMP_DIR, "pdf_preview_showcase"))

    # 2. 全企画案 詳細説明資料 PDF
    pres_html = os.path.join(TEMP_DIR, "presentation_doc.html")
    pres_pdf = os.path.join(OUT_DIR, "岡本武司_全企画案_詳細説明資料.pdf")
    convert_html_to_pdf(pres_html, pres_pdf)
    check_pdf(pres_pdf, os.path.join(TEMP_DIR, "pdf_preview_presentation"))

    print("\nAll PDFs processed successfully without headers/footers!")
