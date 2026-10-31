import os
import re
import subprocess
import markdown
import pymupdf

WORK_DIR = r"C:\AI Workspace\1_Projects\おかもっちゃん"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

cards_data = [
    {
        "id": "CARD 01",
        "type": "高単価オーダー",
        "badge_color": "#2563eb",
        "title": "🏅 アスリート・名将向け「魂のメモリアル鉛筆肖像画」",
        "target": "プロ/実業団/大学の引退選手・名監督・OB会",
        "price": "15万円 〜 50万円 / 点",
        "annual": "300万円 〜 600万円 (年15〜20点)",
        "speed": "★★★★★",
        "profit": "★★★★★",
        "leverage": "★★☆☆☆",
        "strength": "早大競走部主将＆早明戦ラガーマンとしての「勝負の世界」の理解。筋肉の躍動、戦う男の瞳の光を魂ごと描き切る。",
        "action": "箱根駅伝・早明戦・高校部活の節目に合わせたOB会への提案ポートフォリオ（過去作サンプル）を制作。"
    },
    {
        "id": "CARD 02",
        "type": "高単価オーダー",
        "badge_color": "#2563eb",
        "title": "🏢 経営者向け「人生の原点を刻む ルーツ・ポートレート」",
        "target": "中小企業オーナー、創業社長、事業承継創業者",
        "price": "30万円 〜 100万円 / 点",
        "annual": "360万円 〜 800万円 (年8〜12点)",
        "speed": "★★★★☆",
        "profit": "★★★★★",
        "leverage": "★★☆☆☆",
        "strength": "「言葉を超える表現力」。ただの似顔絵ではなく、創業時の古い工場や原点の情景を背景に織り交ぜる叙情詩的アート。",
        "action": "ロータリークラブ・商工会議所での個展・寄贈から紹介獲得。"
    },
    {
        "id": "CARD 03",
        "type": "サブスク・ストック",
        "badge_color": "#16a34a",
        "title": "💻 おかもっちゃんの瑞司式 わくわく鉛筆画オンライン校",
        "target": "50代〜70代の絵心がないと思い込むシニア層",
        "price": "月額 3,980円 〜 9,800円",
        "annual": "1,200万円 〜 1,800万円 (会員150〜200名)",
        "speed": "★★★☆☆",
        "profit": "★★★★★",
        "leverage": "★★★★★",
        "strength": "「熱血高校教師のコーチング力」。誰でも簡単に描けるステップ配信と、受講生を肯定し自信を爆発させる声かけ。",
        "action": "月2本の基礎動画 ＋ 月1回Zoom生ライブ添削 ＋ 交流チャットでスタート。"
    },
    {
        "id": "CARD 04",
        "type": "BtoB・講演事業",
        "badge_color": "#d97706",
        "title": "🎤 企業講演『遅すぎる挑戦などない：常識打破の熱血突破力』",
        "target": "企業の社員総会、キックオフ、周年記念行事",
        "price": "20万円 〜 50万円 / 回 (60〜90分)",
        "annual": "300万円 〜 600万円 (月1〜2回登壇)",
        "speed": "★★★★☆",
        "profit": "★★★★★",
        "leverage": "★★★★☆",
        "strength": "陸上主将→ラグビー直談判→53歳で未経験から画家の生き様そのものが「リスキリング」「挑戦する組織風土」の教材。",
        "action": "講演タイトル・実績・登壇ダイジェスト動画をまとめた「講演専用Webページ（講師プロフィール）」の開設。"
    },
    {
        "id": "CARD 05",
        "type": "BtoB・企業研修",
        "badge_color": "#d97706",
        "title": "🤝 アート思考×対話「心理的安全性を高める観察力研修」",
        "target": "企業の人事部、新任管理職、新入社員チーム",
        "price": "30万円 〜 80万円 / 回 (半日〜1日)",
        "annual": "360万円 〜 600万円",
        "speed": "★★★☆☆",
        "profit": "★★★★★",
        "leverage": "★★★★☆",
        "strength": "「お互いの顔を描き合い、美点を発見する」ワークショップ。元ラグビー部名監督だからできるチームビルディング指導。",
        "action": "「固定観念を外して対象を見る」デッサンの基本をビジネスの傾聴・観察スキルへ転化。"
    },
    {
        "id": "CARD 06",
        "type": "ライセンス・組織化",
        "badge_color": "#9333ea",
        "title": "📜 瑞司式 鉛筆画ファシリテーター・認定講師制度",
        "target": "各地で絵画教室を開きたい受講生・元教え子",
        "price": "養成講座 30万円 ＋ 月額更新料 1万円/人",
        "annual": "400万円 〜 800万円",
        "speed": "★★☆☆☆",
        "profit": "★★★★★",
        "leverage": "★★★★★",
        "strength": "岡本氏1人の稼働に依存しない全国・世界展開。教育者として「先生を育てる」という天職の発揮。",
        "action": "公式カリキュラムと指導マニュアルをパッケージ化。認定校として看板を掲げられる権利と公式画材卸。"
    },
    {
        "id": "CARD 07",
        "type": "ファンクラブ・サロン",
        "badge_color": "#e11d48",
        "title": "🔥 オンラインサロン「おかもっちゃん ワクワク挑戦倶楽部」",
        "target": "元教え子、全国の熱狂的ファン、シニア挑戦者",
        "price": "月額 1,980円 〜 2,980円",
        "annual": "400万円 〜 700万円 (会員200〜300名)",
        "speed": "★★★☆☆",
        "profit": "★★★★☆",
        "leverage": "★★★★★",
        "strength": "教え子コミュニティの強固な絆と「岡本武司語録」の引力。",
        "action": "毎朝の「おかもっちゃん熱血名言配信」＋月1回「オンラインおかもっちゃんBAR」＋年1回「大同窓会リアル個展」。"
    },
    {
        "id": "CARD 08",
        "type": "IP・プロダクトEC",
        "badge_color": "#0891b2",
        "title": "✏️ 瑞司監修「はじめての鉛筆画スターターキット」＆カレンダー",
        "target": "初心者、SNSフォロワー、個展来場者",
        "price": "キット 4,980円〜8,800円 / 日めくり 2,000円",
        "annual": "200万円 〜 400万円",
        "speed": "★★★★☆",
        "profit": "★★★☆☆",
        "leverage": "★★★★★",
        "strength": "「何を買えばいいか分からない」初心者に向け、おかもっちゃんが実際に使う厳選鉛筆・紙・消しゴムをセット化。",
        "action": "解説動画QRコード付き。BASE/Shopify等のECで自動発送。"
    },
    {
        "id": "CARD 09",
        "type": "インバウンド・海外",
        "badge_color": "#ea580c",
        "title": "⛩️ 訪日外国人向け「Zen & Soul 鉛筆画ワークショップ」",
        "target": "京都・関西を訪れる訪日外国人観光客・台湾ファン",
        "price": "8,000円 〜 15,000円 / 人 (2時間)",
        "annual": "250万円 〜 500万円",
        "speed": "★★★☆☆",
        "profit": "★★★★☆",
        "leverage": "★★★☆☆",
        "strength": "「絵は言葉を超える」を地で行く国際親善コミュニケーション。台湾での個展実績をベースにしたアジア圏での親和性。",
        "action": "Airbnb Experiences、Klook、Tripadvisorへの登録・予約受付。"
    }
]

def render_cards_html(cards_subset):
    html = ""
    for c in cards_subset:
        html += f'''
        <div class="biz-card" style="border-left: 5px solid {c['badge_color']};">
            <div class="biz-card-top">
                <span class="biz-badge" style="background-color: {c['badge_color']};">{c['type']}</span>
                <span class="biz-id">{c['id']}</span>
                <h4 class="biz-title">{c['title']}</h4>
            </div>
            <div class="biz-tags-row">
                <div class="biz-tag"><strong>対象:</strong> {c['target']}</div>
                <div class="biz-tag"><strong>単価:</strong> <span class="highlight-blue">{c['price']}</span></div>
                <div class="biz-tag"><strong>想定年商:</strong> <span class="highlight-gold">{c['annual']}</span></div>
            </div>
            <div class="biz-ratings">
                <span>即効性: <b class="star">{c['speed']}</b></span>
                <span>収益性: <b class="star">{c['profit']}</b></span>
                <span>レバレッジ: <b class="star">{c['leverage']}</b></span>
            </div>
            <div class="biz-body">
                <div class="biz-field"><strong>💡 強みの掛け算:</strong> {c['strength']}</div>
                <div class="biz-field"><strong>🎯 具体アクション:</strong> {c['action']}</div>
            </div>
        </div>
        '''
    return html

def build_dashboard_html():
    cards_p2 = render_cards_html(cards_data[0:2])  # CARD 01, 02
    cards_p3 = render_cards_html(cards_data[2:5])  # CARD 03, 04, 05
    cards_p4 = render_cards_html(cards_data[5:9])  # CARD 06, 07, 08, 09

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>岡本武司（おかもっちゃん）ビジネスアイデア・ビジュアルカタログ＆収益ダッシュボード</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 14mm 15mm 14mm 15mm;
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
            line-height: 1.55;
            font-size: 9.5pt;
            margin: 0;
            padding: 0;
        }}

        .doc-header {{
            border-bottom: 2.5px solid #2b6cb0;
            padding-bottom: 5px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}

        .doc-title {{
            font-size: 13.8pt;
            font-weight: bold;
            color: #1a365d;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }}

        .doc-subtitle {{
            font-size: 8.2pt;
            color: #4a5568;
            margin: 0;
            text-align: right;
            font-weight: 600;
            white-space: nowrap;
        }}

        .quote-banner {{
            background: linear-gradient(135deg, #ebf8ff 0%, #f7fafc 100%);
            border-left: 4.5px solid #3182ce;
            padding: 8px 12px;
            border-radius: 0 6px 6px 0;
            margin-bottom: 12px;
            font-size: 9pt;
            color: #2c5282;
            line-height: 1.5;
        }}
        .quote-banner strong {{
            color: #1a365d;
            font-size: 9.5pt;
        }}

        .sec-title {{
            font-size: 11pt;
            font-weight: bold;
            color: #1a365d;
            background: #edf2f7;
            border-left: 4.5px solid #3182ce;
            padding: 5px 10px;
            margin: 12px 0 10px 0;
            border-radius: 0 4px 4px 0;
            page-break-after: avoid;
            break-after: avoid;
        }}

        /* 4象限ポジショニングマトリクス（カラー拡大版） */
        .matrix-container {{
            background: #ffffff;
            border: 1.5px solid #cbd5e0;
            border-radius: 8px;
            padding: 10px 12px;
            margin-bottom: 14px;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .matrix-header-y {{
            text-align: center;
            font-weight: bold;
            color: #1a365d;
            font-size: 9pt;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }}

        .axis-tag {{
            background: #ebf8ff;
            color: #2b6cb0;
            padding: 2px 10px;
            border-radius: 12px;
            border: 1px solid #bee3f8;
            font-size: 8.2pt;
        }}

        .matrix-body {{
            display: flex;
            align-items: stretch;
            gap: 8px;
        }}

        .matrix-axis-x {{
            width: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-weight: bold;
            font-size: 7.8pt;
            line-height: 1.25;
            padding: 6px 2px;
            border-radius: 4px;
            writing-mode: vertical-rl;
            letter-spacing: 2px;
        }}
        .matrix-axis-x.left {{
            background: #edf2f7;
            color: #4a5568;
            border: 1px solid #cbd5e0;
        }}
        .matrix-axis-x.right {{
            background: #f0fff4;
            color: #276749;
            border: 1px solid #c6f6d5;
        }}

        .matrix-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            flex: 1;
        }}

        .matrix-card {{
            border-radius: 6px;
            padding: 8px 10px;
            border: 1px solid #e2e8f0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .matrix-card.q-order {{
            background: #ebf8ff;
            border-top: 4px solid #3182ce;
            border-color: #bee3f8;
        }}
        .matrix-card.q-btob {{
            background: #fffbeb;
            border-top: 4px solid #d97706;
            border-color: #fde68a;
        }}
        .matrix-card.q-stock {{
            background: #f0fff4;
            border-top: 4px solid #38a169;
            border-color: #c6f6d5;
        }}
        .matrix-card.q-scale {{
            background: #faf5ff;
            border-top: 4px solid #805ad5;
            border-color: #e9d8fd;
        }}

        .matrix-card-title {{
            font-weight: bold;
            font-size: 9pt;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .matrix-card.q-order .matrix-card-title {{ color: #2b6cb0; }}
        .matrix-card.q-btob .matrix-card-title {{ color: #b45309; }}
        .matrix-card.q-stock .matrix-card-title {{ color: #276749; }}
        .matrix-card.q-scale .matrix-card-title {{ color: #6b46c1; }}

        .matrix-pill {{
            font-size: 7.2pt;
            padding: 1px 6px;
            border-radius: 8px;
            font-weight: bold;
            background: #ffffff;
            border: 1px solid rgba(0,0,0,0.1);
        }}

        .matrix-item {{
            font-size: 8.4pt;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 4px;
            padding: 3px 6px;
            margin-bottom: 3px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid rgba(0,0,0,0.04);
        }}
        .matrix-item strong {{
            color: #1a202c;
        }}
        .matrix-item span {{
            font-size: 7.8pt;
            color: #4a5568;
            font-weight: 600;
        }}

        .matrix-footer-y {{
            text-align: center;
            font-weight: bold;
            color: #4a5568;
            font-size: 8.8pt;
            margin-top: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }}
        .matrix-footer-y .axis-tag {{
            background: #edf2f7;
            color: #4a5568;
            border-color: #cbd5e0;
        }}

        /* Table */
        table.dash-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 8.8pt;
            margin-bottom: 12px;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        table.dash-table th, table.dash-table td {{
            border: 1px solid #cbd5e0;
            padding: 6px 8px;
            text-align: left;
        }}

        table.dash-table th {{
            background-color: #edf2f7;
            color: #1a365d;
            font-weight: bold;
        }}

        table.dash-table tr:nth-child(even) {{
            background-color: #f7fafc;
        }}

        .highlight-blue {{
            color: #2b6cb0;
            font-weight: bold;
        }}
        .highlight-gold {{
            color: #c05621;
            font-weight: bold;
        }}

        /* 集客ファネル（カラー拡大HTMLフロー） */
        .funnel-flow-container {{
            background: #ffffff;
            border: 1.5px solid #cbd5e0;
            border-radius: 8px;
            padding: 12px 14px;
            margin-bottom: 14px;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .funnel-steps {{
            display: flex;
            align-items: stretch;
            gap: 8px;
            margin-bottom: 10px;
        }}

        .funnel-step {{
            flex: 1;
            border-radius: 6px;
            padding: 8px 10px;
            border: 1px solid #cbd5e0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .f-step1 {{ background: #fdf2f8; border-color: #fbcfe8; border-top: 4px solid #db2777; }}
        .f-step2 {{ background: #f0fdf4; border-color: #bbf7d0; border-top: 4px solid #16a34a; }}
        .f-step3 {{ background: #eff6ff; border-color: #bfdbfe; border-top: 4px solid #2563eb; }}

        .f-step-title {{
            font-size: 8.8pt;
            font-weight: bold;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .f-step1 .f-step-title {{ color: #be185d; }}
        .f-step2 .f-step-title {{ color: #15803d; }}
        .f-step3 .f-step-title {{ color: #1d4ed8; }}

        .f-step-body {{
            font-size: 8pt;
            color: #374151;
            line-height: 1.4;
        }}

        .funnel-arrow {{
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94a3b8;
            font-size: 14pt;
            font-weight: bold;
        }}

        .funnel-outcomes {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 6px;
            padding: 8px 10px;
        }}

        .f-outcome-card {{
            background: #ffffff;
            border-radius: 5px;
            padding: 6px 8px;
            border: 1px solid #e2e8f0;
            text-align: center;
        }}
        .f-outcome-card h6 {{
            margin: 0 0 2px 0;
            font-size: 8.5pt;
            color: #1e3a8a;
            font-weight: bold;
        }}
        .f-outcome-card p {{
            margin: 0;
            font-size: 7.8pt;
            color: #475569;
        }}

        .page-break {{
            page-break-before: always;
            break-before: page;
        }}

        /* Cards Layout */
        .cards-container {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .biz-card {{
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            background: #ffffff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            page-break-inside: avoid;
            break-inside: avoid;
            overflow: hidden;
            font-size: 9pt;
        }}

        .biz-card-top {{
            background: #f7fafc;
            border-bottom: 1px solid #e2e8f0;
            padding: 6px 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .biz-badge {{
            color: #ffffff;
            font-size: 7.5pt;
            font-weight: bold;
            padding: 2px 7px;
            border-radius: 4px;
            white-space: nowrap;
        }}

        .biz-id {{
            font-size: 8pt;
            font-weight: 800;
            color: #718096;
        }}

        .biz-title {{
            margin: 0;
            font-size: 10.5pt;
            font-weight: bold;
            color: #1a365d;
        }}

        .biz-tags-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            padding: 5px 10px;
            background: #ffffff;
            border-bottom: 1px dashed #e2e8f0;
        }}

        .biz-tag {{
            font-size: 8.2pt;
            background: #edf2f7;
            padding: 2px 7px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
            color: #4a5568;
        }}

        .biz-ratings {{
            display: flex;
            gap: 14px;
            padding: 4px 10px;
            background: #fafaf9;
            font-size: 8pt;
            color: #4a5568;
            border-bottom: 1px solid #edf2f7;
        }}
        .biz-ratings .star {{
            color: #dd6b20;
            font-size: 8.5pt;
        }}

        .biz-body {{
            padding: 6px 10px;
            line-height: 1.45;
        }}

        .biz-field {{
            margin-bottom: 3px;
        }}
        .biz-field strong {{
            color: #2d3748;
        }}

        /* Roadmap Grid */
        .roadmap-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            margin: 8px 0;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .roadmap-card {{
            border-radius: 6px;
            border: 1px solid #cbd5e0;
            background: #f7fafc;
            padding: 8px 10px;
        }}
        .roadmap-card.rm-p1 {{ border-top: 4px solid #3182ce; background: #ebf8ff; }}
        .roadmap-card.rm-p2 {{ border-top: 4px solid #d69e2e; background: #fffaf0; }}
        .roadmap-card.rm-p3 {{ border-top: 4px solid #38a169; background: #f0fff4; }}

        .roadmap-card h5 {{
            margin: 0 0 5px 0;
            font-size: 9pt;
            font-weight: bold;
            border-bottom: 1px solid rgba(0,0,0,0.08);
            padding-bottom: 3px;
        }}
        .rm-p1 h5 {{ color: #2b6cb0; }}
        .rm-p2 h5 {{ color: #b7791f; }}
        .rm-p3 h5 {{ color: #276749; }}

        .roadmap-card ul {{
            margin: 0;
            padding-left: 15px;
            font-size: 8.2pt;
        }}
        .roadmap-card li {{
            margin-bottom: 3px;
        }}

        .action-box {{
            background: #ebf8ff;
            border: 1.5px solid #3182ce;
            border-radius: 6px;
            padding: 8px 12px;
            margin-top: 8px;
            font-size: 8.5pt;
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        .action-box strong {{
            color: #2b6cb0;
            font-size: 9pt;
        }}
        .action-box ol {{
            margin: 4px 0 0 0;
            padding-left: 18px;
        }}
        .action-box li {{
            margin-bottom: 2px;
        }}
    </style>
</head>
<body>

    <!-- ================= PAGE 1 ================= -->
    <div class="doc-header">
        <div>
            <h1 class="doc-title">🎨 岡本武司（おかもっちゃん）ビジネスアイデア・ビジュアルカタログ</h1>
        </div>
        <div>
            <p class="doc-subtitle">直感型 収益設計・事業ダッシュボード</p>
        </div>
    </div>

    <div class="quote-banner">
        <strong>理念：「絵は言葉を超える。ワクワクに年齢は関係ない」</strong><br>
        【早大競走部主将＆早明戦ラガーマンの突破力】×【熱血高校名監督の教育コーチング力】×【53歳独学画家・瑞司】の圧倒的掛け算。
    </div>

    <div class="sec-title">📊 1. 収益ポートフォリオ・4象限ポジショニングマトリクス</div>

    <div class="matrix-container">
        <div class="matrix-header-y">
            <span class="axis-tag">▲ 高単価・高利益率（1件 15万〜100万円）</span>
        </div>
        <div class="matrix-body">
            <div class="matrix-axis-x left">◄ 労働集約・個別提供</div>
            <div class="matrix-grid">
                <!-- Q1: 高単価オーダー -->
                <div class="matrix-card q-order">
                    <div class="matrix-card-title">
                        <span>【1】高単価・オーダー型</span>
                        <span class="matrix-pill">フロー・即効</span>
                    </div>
                    <div>
                        <div class="matrix-item">
                            <strong>🏅 01. レジェンドメモリアル肖像画</strong>
                            <span>15万〜50万円</span>
                        </div>
                        <div class="matrix-item">
                            <strong>🏢 02. 経営者ルーツ肖像画</strong>
                            <span>30万〜100万円</span>
                        </div>
                        <div class="matrix-item">
                            <strong>🧘 経営者マインドフルネス個人指導</strong>
                            <span>50万〜100万円</span>
                        </div>
                    </div>
                </div>

                <!-- Q2: 法人BtoB -->
                <div class="matrix-card q-btob">
                    <div class="matrix-card-title">
                        <span>【2】法人BtoB・レバレッジ型</span>
                        <span class="matrix-pill">高権威・高単価</span>
                    </div>
                    <div>
                        <div class="matrix-item">
                            <strong>🎤 04. 常識打破の熱血企業講演</strong>
                            <span>20万〜50万円/回</span>
                        </div>
                        <div class="matrix-item">
                            <strong>🤝 05. アート思考チーム研修</strong>
                            <span>30万〜80万円/回</span>
                        </div>
                        <div class="matrix-item">
                            <strong>📜 06. 認定講師養成・ライセンス</strong>
                            <span>受講30万+月1万</span>
                        </div>
                    </div>
                </div>

                <!-- Q3: サブスク・ストック -->
                <div class="matrix-card q-stock">
                    <div class="matrix-card-title">
                        <span>【3】サブスク・ストック型</span>
                        <span class="matrix-pill">安定継続基盤</span>
                    </div>
                    <div>
                        <div class="matrix-item">
                            <strong>💻 03. わくわく鉛筆画オンライン校</strong>
                            <span>月額 3,980円〜</span>
                        </div>
                        <div class="matrix-item">
                            <strong>🔥 07. おかもっちゃん挑戦サロン</strong>
                            <span>月額 1,980円〜</span>
                        </div>
                        <div class="matrix-item">
                            <strong>👥 教え子・OB複合コミュニティ</strong>
                            <span>継続課金</span>
                        </div>
                    </div>
                </div>

                <!-- Q4: IP・物販・インバウンド -->
                <div class="matrix-card q-scale">
                    <div class="matrix-card-title">
                        <span>【4】IP・物販・インバウンド型</span>
                        <span class="matrix-pill">自動化・拡散</span>
                    </div>
                    <div>
                        <div class="matrix-item">
                            <strong>📚 書籍・熱血日めくりカレンダー</strong>
                            <span>1,500〜2,500円</span>
                        </div>
                        <div class="matrix-item">
                            <strong>✏️ 08. 瑞司監修 画材スターターキット</strong>
                            <span>4,980〜8,800円</span>
                        </div>
                        <div class="matrix-item">
                            <strong>⛩️ 09. 訪日客向け和の鉛筆画体験</strong>
                            <span>8,000〜15,000円</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="matrix-axis-x right">レバレッジ・組織展開 ►</div>
        </div>
        <div class="matrix-footer-y">
            <span class="axis-tag">▼ 低中単価・スケール型（月額 1,980円〜 / 物販・体験）</span>
        </div>
    </div>

    <div class="sec-title">💰 2. 目標収益シミュレーション（月商 250万円 / 年商 3,000万円モデル）</div>

    <table class="dash-table">
        <thead>
            <tr>
                <th style="width: 19%;">収益の柱</th>
                <th style="width: 33%;">対象商品・サービス</th>
                <th style="width: 18%; text-align: center;">単価目安</th>
                <th style="width: 12%; text-align: center;">想定販売数</th>
                <th style="width: 11%; text-align: right;">月間売上</th>
                <th style="width: 7%; text-align: center;">負荷</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>柱①：安定ストック</strong></td>
                <td>オンライン鉛筆画教室 ＆ サロン</td>
                <td style="text-align: center;">¥4,980 /月</td>
                <td style="text-align: center;">200名</td>
                <td style="text-align: right;" class="highlight-blue">約100万円</td>
                <td style="text-align: center;">🟢低</td>
            </tr>
            <tr>
                <td><strong>柱②：法人・講演</strong></td>
                <td>企業講演 ＆ チーム研修</td>
                <td style="text-align: center;">¥300,000 /回</td>
                <td style="text-align: center;">月2回</td>
                <td style="text-align: right;" class="highlight-blue">約60万円</td>
                <td style="text-align: center;">🟡中</td>
            </tr>
            <tr>
                <td><strong>柱③：高付加価値原画</strong></td>
                <td>メモリアル肖像画・経営者原画</td>
                <td style="text-align: center;">¥250,000 /枚</td>
                <td style="text-align: center;">月2枚</td>
                <td style="text-align: right;" class="highlight-blue">約50万円</td>
                <td style="text-align: center;">🔴高</td>
            </tr>
            <tr>
                <td><strong>柱④：物販・IP・体験</strong></td>
                <td>画材セット・書籍・インバウンド</td>
                <td style="text-align: center;">¥5,000〜¥15,000</td>
                <td style="text-align: center;">計40件</td>
                <td style="text-align: right;" class="highlight-blue">約40万円</td>
                <td style="text-align: center;">🟢自動</td>
            </tr>
            <tr style="background-color: #edf2f7; font-weight: bold;">
                <td colspan="4" style="text-align: right;">合計（月商） / 年間インパクト</td>
                <td style="text-align: right;" class="highlight-gold">🔥250万円</td>
                <td style="text-align: center;" class="highlight-gold">年3,000万</td>
            </tr>
        </tbody>
    </table>

    <!-- ================= PAGE 2 ================= -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <h1 class="doc-title">🔄 集客ファネル ＆ 🗂️ 高単価オーダー事業</h1>
        </div>
        <div>
            <p class="doc-subtitle">自動集客の導線設計 ＆ メモリアルアート</p>
        </div>
    </div>

    <div class="sec-title" style="margin-top: 0;">🔄 集客から購入までの自動導線（ファネル設計）</div>
    <div class="funnel-flow-container">
        <div class="funnel-steps">
            <div class="funnel-step f-step1">
                <div class="f-step-title">📱 STEP 1: SNS無料発信</div>
                <div class="f-step-body">
                    ・Instagram / YouTube Shorts<br>
                    ・タイムラプス描画 × 熱血語録音声<br>
                    <strong>【認知拡大・圧倒的ファン化】</strong>
                </div>
            </div>
            <div class="funnel-arrow">➜</div>
            <div class="funnel-step f-step2">
                <div class="f-step-title">🎁 STEP 2: 公式LINE登録</div>
                <div class="f-step-body">
                    ・特典「15分で立体感が描ける限定動画」<br>
                    ・おかもっちゃん熱血メッセージ<br>
                    <strong>【見込み客リストの自動獲得】</strong>
                </div>
            </div>
            <div class="funnel-arrow">➜</div>
            <div class="funnel-step f-step3">
                <div class="f-step-title">📩 STEP 3: 7日間ステップ</div>
                <div class="f-step-body">
                    ・挫折と挑戦のストーリー<br>
                    ・『絵は言葉を超える』理念共感<br>
                    <strong>【熱狂的な信頼関係の構築】</strong>
                </div>
            </div>
        </div>
        <div class="funnel-outcomes">
            <div class="f-outcome-card">
                <h6>💻 学びたい方へ</h6>
                <p>オンライン鉛筆画校（月額 ¥3,980〜）</p>
            </div>
            <div class="f-outcome-card">
                <h6>🖼️ 記念・贈答の方へ</h6>
                <p>特注肖像画オーダー（¥150,000〜）</p>
            </div>
            <div class="f-outcome-card">
                <h6>🏢 企業・団体の方へ</h6>
                <p>熱血企業講演・研修（¥200,000〜）</p>
            </div>
        </div>
    </div>

    <div class="sec-title">🗂️ ビジネスアイデア：高単価メモリアルアート</div>
    <div class="cards-container">
        {cards_p2}
    </div>

    <!-- ================= PAGE 3 ================= -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <h1 class="doc-title">🗂️ ビジネスアイデア：スクール・BtoB法人事業</h1>
        </div>
        <div>
            <p class="doc-subtitle">教育力と指導実績を活かした高収益・レバレッジモデル</p>
        </div>
    </div>

    <div class="cards-container" style="margin-top: 4px;">
        {cards_p3}
    </div>

    <!-- ================= PAGE 4 ================= -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <h1 class="doc-title">🗂️ ビジネスアイデア：組織化・ファン化・物販・海外</h1>
        </div>
        <div>
            <p class="doc-subtitle">ライセンス・コミュニティ・自動物販・インバウンド展開</p>
        </div>
    </div>

    <div class="cards-container" style="margin-top: 4px;">
        {cards_p4}
    </div>

    <!-- ================= PAGE 5 ================= -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <h1 class="doc-title">⚡ 難易度マトリクス ＆ 🚀 90日スプリント計画</h1>
        </div>
        <div>
            <p class="doc-subtitle">収益化の優先順位とロードマップ</p>
        </div>
    </div>

    <div class="sec-title" style="margin-top: 0;">⚡ 3. 難易度 × 収益性 マトリクス一覧表</div>
    <table class="dash-table">
        <thead>
            <tr>
                <th>アイデア名</th>
                <th>カテゴリ</th>
                <th style="text-align: center;">導入スピード</th>
                <th style="text-align: center;">粗利率</th>
                <th style="text-align: center;">労働依存度</th>
                <th style="text-align: right;">年商ポテンシャル</th>
                <th style="text-align: center;">推奨着手</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>01. メモリアル肖像画</strong></td>
                <td>フロー受注</td>
                <td style="text-align: center;">⚡ 即日可能</td>
                <td style="text-align: center;">95%</td>
                <td style="text-align: center;">高（制作）</td>
                <td style="text-align: right;" class="highlight-blue">300万〜600万円</td>
                <td style="text-align: center; color: #c53030; font-weight:bold;">第 1 位</td>
            </tr>
            <tr>
                <td><strong>04. 常識打破の企業講演</strong></td>
                <td>BtoB法人</td>
                <td style="text-align: center;">⚡ 1ヶ月（資料化）</td>
                <td style="text-align: center;">90%</td>
                <td style="text-align: center;">低（登壇のみ）</td>
                <td style="text-align: right;" class="highlight-blue">300万〜600万円</td>
                <td style="text-align: center; color: #c53030; font-weight:bold;">第 2 位</td>
            </tr>
            <tr>
                <td><strong>03. オンライン鉛筆画スクール</strong></td>
                <td>サブスク</td>
                <td style="text-align: center;">⏳ 2〜3ヶ月</td>
                <td style="text-align: center;">90%</td>
                <td style="text-align: center;">極低（配信）</td>
                <td style="text-align: right;" class="highlight-gold">1,200万〜1,800万円</td>
                <td style="text-align: center; color: #c53030; font-weight:bold;">第 3 位</td>
            </tr>
            <tr>
                <td><strong>08. スターターキット＆物販</strong></td>
                <td>物販・EC</td>
                <td style="text-align: center;">⏳ 1〜2ヶ月</td>
                <td style="text-align: center;">50%</td>
                <td style="text-align: center;">自動（発送代行）</td>
                <td style="text-align: right;">200万〜400万円</td>
                <td style="text-align: center;">第 4 位</td>
            </tr>
            <tr>
                <td><strong>07. 挑戦サロン（ファンクラブ）</strong></td>
                <td>サブスク</td>
                <td style="text-align: center;">⏳ 2ヶ月</td>
                <td style="text-align: center;">95%</td>
                <td style="text-align: center;">低（交流）</td>
                <td style="text-align: right;">400万〜700万円</td>
                <td style="text-align: center;">第 5 位</td>
            </tr>
            <tr>
                <td><strong>02. 経営者ルーツ肖像画</strong></td>
                <td>フロー受注</td>
                <td style="text-align: center;">⏳ 2〜3ヶ月</td>
                <td style="text-align: center;">95%</td>
                <td style="text-align: center;">高（制作）</td>
                <td style="text-align: right;">360万〜800万円</td>
                <td style="text-align: center;">第 6 位</td>
            </tr>
            <tr>
                <td><strong>05. チームビルディング研修</strong></td>
                <td>BtoB法人</td>
                <td style="text-align: center;">⏳ 3ヶ月</td>
                <td style="text-align: center;">90%</td>
                <td style="text-align: center;">中（ワーク指導）</td>
                <td style="text-align: right;">360万〜600万円</td>
                <td style="text-align: center;">第 7 位</td>
            </tr>
            <tr>
                <td><strong>06. 認定講師養成制度</strong></td>
                <td>ライセンス</td>
                <td style="text-align: center;">⏳ 6ヶ月〜1年</td>
                <td style="text-align: center;">95%</td>
                <td style="text-align: center;">極低（組織運営）</td>
                <td style="text-align: right;">400万〜800万円</td>
                <td style="text-align: center;">第 8 位</td>
            </tr>
            <tr>
                <td><strong>09. インバウンド体験</strong></td>
                <td>体験・観光</td>
                <td style="text-align: center;">⏳ 3〜4ヶ月</td>
                <td style="text-align: center;">85%</td>
                <td style="text-align: center;">中（現場対応）</td>
                <td style="text-align: right;">250万〜500万円</td>
                <td style="text-align: center;">第 9 位</td>
            </tr>
        </tbody>
    </table>

    <div class="sec-title">🚀 4. 収益ダッシュボードを起動する「90日スプリント＆直前アクション」</div>
    
    <div class="roadmap-grid">
        <div class="roadmap-card rm-p1">
            <h5>Phase 1（1〜30日）即時キャッシュ化</h5>
            <ul>
                <li>公式LP・受注ポートフォリオ整備</li>
                <li>スポーツ関係・OB会への肖像画案内</li>
                <li>ショート動画（描画×語録）毎日投稿</li>
            </ul>
        </div>
        <div class="roadmap-card rm-p2">
            <h5>Phase 2（31〜60日）BtoB＆リスト構築</h5>
            <ul>
                <li>企業講演用企画書＆実績動画完成</li>
                <li>公式LINE特典（初心者動画）公開</li>
                <li>地元経営者・商工会議所へのアプローチ</li>
            </ul>
        </div>
        <div class="roadmap-card rm-p3">
            <h5>Phase 3（61〜90日）ストック収益始動</h5>
            <ul>
                <li>オンライン鉛筆画スクール プレローンチ</li>
                <li>オリジナル日めくりカレンダー・画材販売</li>
                <li>認定講師制度のカリキュラム構想</li>
            </ul>
        </div>
    </div>

    <div class="action-box">
        <strong>🎯 今すぐ着手すべき「最初の3アクション」:</strong>
        <ol>
            <li><strong>作品・価格表をまとめた「公式ポートフォリオLP」の作成</strong>（似顔絵・肖像画を迷わず注文できる窓口を作る）</li>
            <li><strong>Instagram / YouTube ショートで「タイムラプス × 熱血語録」の毎日発信</strong>（再生数とフォロワーの爆発的獲得）</li>
            <li><strong>企業講演向け「講師プロフィールシート（A4 表裏 1枚）」のPDF化</strong>（知人経営者や企業窓口へ直接提案）</li>
        </ol>
    </div>

</body>
</html>'''
    return html

def build_report_html():
    md_path = os.path.join(WORK_DIR, "岡本武司_ビジネスアイデア集.md")
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove all markdown horizontal rules (---) to avoid unwanted page breaks
    content = re.sub(r'^\s*---\s*$', '', content, flags=re.MULTILINE)

    # Replace Mermaid flowchart in report with a compact, beautiful colored HTML funnel container
    colored_funnel_html = '''
<div class="funnel-flow-container" style="margin: 8px 0 10px 0;">
    <div class="funnel-steps">
        <div class="funnel-step f-step1">
            <div class="f-step-title">📱 STEP 1: SNS無料発信</div>
            <div class="f-step-body">
                ・Instagram / YouTube Shorts<br>
                ・タイムラプス描画 × 熱血語録音声<br>
                <strong>【認知拡大・圧倒的ファン化】</strong>
            </div>
        </div>
        <div class="funnel-arrow">➜</div>
        <div class="funnel-step f-step2">
            <div class="f-step-title">🎁 STEP 2: 公式LINE登録</div>
            <div class="f-step-body">
                ・特典「15分で立体感が描ける限定動画」<br>
                ・おかもっちゃん熱血メッセージ<br>
                <strong>【見込み客リストの自動獲得】</strong>
            </div>
        </div>
        <div class="funnel-arrow">➜</div>
        <div class="funnel-step f-step3">
            <div class="f-step-title">📩 STEP 3: 7日間ステップ</div>
            <div class="f-step-body">
                ・挫折と挑戦のストーリー<br>
                ・『絵は言葉を超える』理念共感<br>
                <strong>【熱狂的な信頼関係の構築】</strong>
            </div>
        </div>
    </div>
    <div class="funnel-outcomes">
        <div class="f-outcome-card">
            <h6 style="color: #1e3a8a; margin: 0 0 1px 0; font-size: 8.2pt;">💻 学びたい方へ</h6>
            <p style="margin: 0; font-size: 7.5pt; color: #475569;">オンライン鉛筆画校（月額 ¥3,980〜）</p>
        </div>
        <div class="f-outcome-card">
            <h6 style="color: #1e3a8a; margin: 0 0 1px 0; font-size: 8.2pt;">🖼️ 記念・贈答の方へ</h6>
            <p style="margin: 0; font-size: 7.5pt; color: #475569;">特注肖像画オーダー（¥150,000〜）</p>
        </div>
        <div class="f-outcome-card">
            <h6 style="color: #1e3a8a; margin: 0 0 1px 0; font-size: 8.2pt;">🏢 企業・団体の方へ</h6>
            <p style="margin: 0; font-size: 7.5pt; color: #475569;">熱血企業講演・研修（¥200,000〜）</p>
        </div>
    </div>
</div>
'''
    content_processed = re.sub(r'```mermaid\n(.*?)\n```', colored_funnel_html, content, flags=re.DOTALL)

    html_body = markdown.markdown(content_processed, extensions=['tables', 'fenced_code', 'nl2br'])

    # Explicit clean page breaks for exactly 6 pages:
    # Page 1: Title, Lead, Category 1
    # Page 2: Category 2 (Education / School / License)
    # Page 3: Category 3 (BtoB Lecture & Training)
    # Page 4: Category 4 (Community) & Category 5 (IP / Products)
    # Page 5: Category 6 (Funnel & Strategy)
    # Page 6: Roadmap & Conclusion
    html_body = html_body.replace('<h2>カテゴリ2：', '<div class="page-break"></div><h2>カテゴリ2：')
    html_body = html_body.replace('<h2>カテゴリ3：', '<div class="page-break"></div><h2>カテゴリ3：')
    html_body = html_body.replace('<h2>カテゴリ4：', '<div class="page-break"></div><h2>カテゴリ4：')
    html_body = html_body.replace('<h2>カテゴリ6：', '<div class="page-break"></div><h2>カテゴリ6：')
    html_body = html_body.replace('<h2>ロードマップ：', '<div class="page-break"></div><h2>ロードマップ：')

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>岡本武司（瑞司／おかもっちゃん）強み最大化＆経済的豊かさを実現するビジネスアイデア集</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 13mm 16mm 13mm 16mm;
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
            font-size: 9.3pt;
            margin: 0;
            padding: 0;
        }}

        .page-break {{
            page-break-before: always;
            break-before: page;
        }}

        h1 {{
            font-size: 15.5pt;
            font-weight: bold;
            color: #1a365d;
            border-bottom: 2.5px solid #2b6cb0;
            padding-bottom: 6px;
            margin-top: 0;
            margin-bottom: 10px;
            line-height: 1.35;
        }}

        h2 {{
            font-size: 12pt;
            font-weight: bold;
            color: #2b6cb0;
            background: #ebf8ff;
            border-left: 4.5px solid #3182ce;
            padding: 4px 10px;
            margin-top: 8px;
            margin-bottom: 6px;
            page-break-after: avoid;
            break-after: avoid;
        }}

        h3 {{
            font-size: 10.2pt;
            font-weight: bold;
            color: #1a365d;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 3px;
            margin-top: 10px;
            margin-bottom: 5px;
            page-break-after: avoid;
            break-after: avoid;
        }}

        pre {{
            background: #f7fafc;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 8.6pt;
            overflow-x: auto;
            page-break-inside: avoid;
            break-inside: avoid;
            font-family: Consolas, "Liberation Mono", Menlo, monospace;
            line-height: 1.35;
            color: #2d3748;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8px 0 12px 0;
            font-size: 8.8pt;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #cbd5e0;
            padding: 6px 9px;
            text-align: left;
        }}

        th {{
            background-color: #edf2f7;
            color: #1a365d;
            font-weight: bold;
        }}

        tr:nth-child(even) {{
            background-color: #f7fafc;
        }}

        ul, ol {{
            margin: 3px 0 6px 0;
            padding-left: 18px;
        }}

        li {{
            margin-bottom: 2px;
        }}

        /* Colored Funnel for Report */
        .funnel-flow-container {{
            background: #ffffff;
            border: 1.5px solid #cbd5e0;
            border-radius: 8px;
            padding: 8px 10px;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .funnel-steps {{
            display: flex;
            align-items: stretch;
            gap: 6px;
            margin-bottom: 6px;
        }}

        .funnel-step {{
            flex: 1;
            border-radius: 5px;
            padding: 6px 8px;
            border: 1px solid #cbd5e0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .f-step1 {{ background: #fdf2f8; border-color: #fbcfe8; border-top: 3.5px solid #db2777; }}
        .f-step2 {{ background: #f0fdf4; border-color: #bbf7d0; border-top: 3.5px solid #16a34a; }}
        .f-step3 {{ background: #eff6ff; border-color: #bfdbfe; border-top: 3.5px solid #2563eb; }}

        .f-step-title {{
            font-size: 8.4pt;
            font-weight: bold;
            margin-bottom: 2px;
        }}
        .f-step1 .f-step-title {{ color: #be185d; }}
        .f-step2 .f-step-title {{ color: #15803d; }}
        .f-step3 .f-step-title {{ color: #1d4ed8; }}

        .f-step-body {{
            font-size: 7.6pt;
            color: #374151;
            line-height: 1.3;
        }}

        .funnel-arrow {{
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94a3b8;
            font-size: 12pt;
            font-weight: bold;
        }}

        .funnel-outcomes {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 6px;
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 5px;
            padding: 5px 6px;
        }}

        .f-outcome-card {{
            background: #ffffff;
            border-radius: 4px;
            padding: 4px 6px;
            border: 1px solid #e2e8f0;
            text-align: center;
        }}

        hr {{
            display: none;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>'''
    return html

def convert_html_to_pdf(html_path, pdf_path):
    cmd = [
        CHROME_PATH,
        '--headless=new',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        '--virtual-time-budget=6000',
        f'--print-to-pdf={pdf_path}',
        '--no-pdf-header-footer',
        html_path
    ]
    subprocess.run(cmd, check=True)

def render_pdf_to_images(pdf_path, output_prefix):
    doc = pymupdf.open(pdf_path)
    img_paths = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        img_path = f"{output_prefix}_page_{i+1}.png"
        pix.save(img_path)
        img_paths.append(img_path)
    return img_paths

def main():
    # 1. Dashboard PDF (5 pages)
    dashboard_html = os.path.join(WORK_DIR, "dashboard_temp.html")
    dashboard_pdf = os.path.join(WORK_DIR, "岡本武司_ビジネスアイデア_収益ダッシュボード.pdf")
    with open(dashboard_html, 'w', encoding='utf-8') as f:
        f.write(build_dashboard_html())
    convert_html_to_pdf(dashboard_html, dashboard_pdf)
    imgs1 = render_pdf_to_images(dashboard_pdf, os.path.join(WORK_DIR, "preview_dashboard_final"))
    print(f"Dashboard PDF generated: {len(imgs1)} pages")

    # 2. Report PDF (6 pages)
    report_html = os.path.join(WORK_DIR, "report_temp.html")
    report_pdf = os.path.join(WORK_DIR, "岡本武司_ビジネスアイデア集.pdf")
    with open(report_html, 'w', encoding='utf-8') as f:
        f.write(build_report_html())
    convert_html_to_pdf(report_html, report_pdf)
    imgs2 = render_pdf_to_images(report_pdf, os.path.join(WORK_DIR, "preview_report_final"))
    print(f"Report PDF generated: {len(imgs2)} pages")

if __name__ == '__main__':
    main()
