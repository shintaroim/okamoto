import os
import re
import subprocess
import pymupdf

WORK_DIR = r"C:\AI Workspace\1_Projects\おかもっちゃん"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def build_website_proposals_html():
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>岡本武司（おかもっちゃん）ウェブサイト構築提案書</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 14mm 16mm 14mm 16mm;
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
            font-size: 9.3pt;
            margin: 0;
            padding: 0;
        }}

        .page-break {{
            page-break-before: always;
            break-before: page;
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
            font-size: 13.5pt;
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
            padding: 4px 10px;
            margin: 12px 0 8px 0;
            border-radius: 0 4px 4px 0;
            page-break-after: avoid;
            break-after: avoid;
        }}

        h3 {{
            font-size: 10.2pt;
            font-weight: bold;
            color: #1a365d;
            margin: 8px 0 4px 0;
        }}

        p {{
            margin: 0 0 6px 0;
        }}

        ul, ol {{
            margin: 2px 0 6px 0;
            padding-left: 18px;
        }}

        li {{
            margin-bottom: 2px;
        }}

        /* Table */
        table.custom-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 8.6pt;
            margin: 8px 0 12px 0;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        table.custom-table th, table.custom-table td {{
            border: 1px solid #cbd5e0;
            padding: 6px 8px;
            text-align: left;
            vertical-align: top;
        }}

        table.custom-table th {{
            background-color: #edf2f7;
            color: #1a365d;
            font-weight: bold;
        }}

        table.custom-table tr:nth-child(even) {{
            background-color: #f7fafc;
        }}

        .highlight-blue {{ color: #2b6cb0; font-weight: bold; }}
        .highlight-gold {{ color: #c05621; font-weight: bold; }}

        /* Proposal Card */
        .proposal-card {{
            border: 1px solid #cbd5e0;
            border-radius: 8px;
            background: #ffffff;
            margin-bottom: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .p-card-header {{
            padding: 6px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #cbd5e0;
        }}

        .p-card-header h4 {{
            margin: 0;
            font-size: 10.5pt;
            font-weight: bold;
            color: #1a365d;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .p-badge {{
            font-size: 7.8pt;
            color: #ffffff;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 4px;
        }}

        .p-card-body {{
            padding: 8px 12px;
            font-size: 8.8pt;
            line-height: 1.5;
        }}

        .p-lead-quote {{
            background: #f8fafc;
            border-left: 3px solid #3182ce;
            padding: 4px 8px;
            margin-bottom: 6px;
            font-size: 8.6pt;
            font-weight: bold;
            color: #2b6cb0;
        }}

        .tree-box {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 6px 10px;
            font-family: Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 7.8pt;
            line-height: 1.35;
            color: #334155;
            margin: 4px 0 6px 0;
        }}

        .pros-cons-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: 6px;
            background: #fafaf9;
            padding: 6px 8px;
            border-radius: 6px;
            border: 1px dashed #cbd5e1;
            font-size: 8.2pt;
        }}

        /* 6 Killer Contents Grid */
        .killer-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin: 8px 0 12px 0;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .killer-box {{
            border-radius: 6px;
            padding: 8px 10px;
            border: 1px solid #cbd5e0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .k-1 {{ background: #ebf8ff; border-top: 4px solid #3182ce; }}
        .k-2 {{ background: #f0fff4; border-top: 4px solid #38a169; }}
        .k-3 {{ background: #fffaf0; border-top: 4px solid #dd6b20; }}
        .k-4 {{ background: #faf5ff; border-top: 4px solid #805ad5; }}
        .k-5 {{ background: #fdf2f8; border-top: 4px solid #db2777; }}
        .k-6 {{ background: #f0fdf4; border-top: 4px solid #16a34a; }}

        .killer-box h5 {{
            margin: 0 0 3px 0;
            font-size: 9.2pt;
            font-weight: bold;
            color: #1a365d;
        }}

        .killer-box p {{
            margin: 0;
            font-size: 8pt;
            color: #4a5568;
            line-height: 1.35;
        }}

        /* Integrated Flow */
        .integ-flow-container {{
            background: #ffffff;
            border: 1.5px solid #cbd5e0;
            border-radius: 8px;
            padding: 10px 12px;
            margin: 8px 0 12px 0;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .integ-row {{
            display: flex;
            align-items: stretch;
            gap: 6px;
            margin-bottom: 8px;
        }}

        .integ-col {{
            flex: 1;
            border-radius: 6px;
            padding: 7px 8px;
            border: 1px solid #cbd5e0;
        }}

        .ic-sns {{ background: #fdf2f8; border-top: 3.5px solid #db2777; }}
        .ic-web {{ background: #eff6ff; border-top: 3.5px solid #2563eb; }}
        .ic-line {{ background: #f0fdf4; border-top: 3.5px solid #16a34a; }}

        .integ-col h6 {{
            margin: 0 0 3px 0;
            font-size: 8.5pt;
            font-weight: bold;
        }}
        .ic-sns h6 {{ color: #be185d; }}
        .ic-web h6 {{ color: #1d4ed8; }}
        .ic-line h6 {{ color: #15803d; }}

        .integ-col ul {{
            margin: 0;
            padding-left: 14px;
            font-size: 7.6pt;
            color: #374151;
            line-height: 1.3;
        }}

        .integ-arrow {{
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94a3b8;
            font-size: 13pt;
            font-weight: bold;
        }}

        .integ-outcomes {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 6px;
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 6px;
            padding: 6px 8px;
        }}

        .io-card {{
            background: #ffffff;
            border-radius: 5px;
            padding: 5px 7px;
            border: 1px solid #e2e8f0;
            text-align: center;
        }}
        .io-card h6 {{
            margin: 0 0 2px 0;
            font-size: 8.2pt;
            color: #1e3a8a;
            font-weight: bold;
        }}
        .io-card p {{
            margin: 0;
            font-size: 7.5pt;
            color: #475569;
        }}

        /* Roadmap Steps */
        .step-timeline {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin: 8px 0 12px 0;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .step-card {{
            border-radius: 6px;
            padding: 8px 12px;
            border: 1px solid #cbd5e0;
            background: #ffffff;
            display: flex;
            gap: 12px;
            align-items: center;
        }}
        .s-c1 {{ border-left: 5px solid #2563eb; background: #eff6ff; }}
        .s-c2 {{ border-left: 5px solid #16a34a; background: #f0fdf4; }}
        .s-c3 {{ border-left: 5px solid #805ad5; background: #faf5ff; }}

        .step-num {{
            font-size: 12pt;
            font-weight: bold;
            white-space: nowrap;
        }}
        .s-c1 .step-num {{ color: #1d4ed8; }}
        .s-c2 .step-num {{ color: #15803d; }}
        .s-c3 .step-num {{ color: #6b46c1; }}

        .step-info h5 {{
            margin: 0 0 2px 0;
            font-size: 9.5pt;
            font-weight: bold;
            color: #0f172a;
        }}
        .step-info p {{
            margin: 0;
            font-size: 8.3pt;
            color: #475569;
            line-height: 1.4;
        }}
    </style>
</head>
<body>

    <!-- ================= PAGE 1 ================= -->
    <div class="doc-header">
        <div>
            <h1 class="doc-title">🌐 岡本武司（おかもっちゃん）ウェブサイト構築提案書</h1>
        </div>
        <div>
            <p class="doc-subtitle">事業最大化のためのWeb戦略・導線設計</p>
        </div>
    </div>

    <div class="quote-banner">
        <strong>理念：「絵は言葉を超える。ワクワクに年齢は関係ない」</strong><br>
        Webサイトの目的は単なる作品展示ではなく、<strong>「SNSの熱狂を、高単価肖像画・月額スクール・企業講演へと確実に繋ぐ【集客・成約の自動ハブ】」</strong>として機能させることです。
    </div>

    <div class="sec-title">🎯 1. 岡本武司氏におけるWebサイトの役割（4大ミッション）</div>

    <div class="killer-grid" style="margin-bottom: 10px;">
        <div class="killer-box k-1">
            <h5>① 信頼と感動の獲得（唯一無二のブランディング）</h5>
            <p>早大主将→早明戦ラガーマン→熱血名監督→53歳独学画家という劇的な人生体験を伝え、唯一無二の存在としてポジショニング。</p>
        </div>
        <div class="killer-box k-2">
            <h5>② 注文・依頼のハードル低減（迷わせない導線）</h5>
            <p>「どこに頼めばいいか」「いくらか」を解消し、肖像画・企業講演・絵画教室への明確な申込み口と明朗会計を提示。</p>
        </div>
        <div class="killer-box k-3">
            <h5>③ 見込み客リストの自動獲得（公式LINE連携）</h5>
            <p>無料レッスン動画プレゼント等を通じ、すべての訪問者をLINEへ誘導。一度の訪問で終わらせない継続的な接点を作る。</p>
        </div>
        <div class="killer-box k-4">
            <h5>④ 運営負荷の最小化（自動決済・動画配信）</h5>
            <p>岡本氏本人が創作や指導、講演に集中できるよう、予約受付・決済・動画提供をできる限りノーコードで自動化。</p>
        </div>
    </div>

    <div class="sec-title">📊 2. 目的・フェーズ別 4つのWebサイト設計案（比較一覧表）</div>

    <table class="custom-table">
        <thead>
            <tr>
                <th style="width: 14%;">案</th>
                <th style="width: 26%;">サイトタイプ</th>
                <th style="width: 32%;">主な目的・特徴</th>
                <th style="width: 16%;">推奨ツール</th>
                <th style="width: 12%; text-align: center;">難易度</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>【案A】</strong></td>
                <td><strong>総合ブランドポータル</strong></td>
                <td>全活動・作品・教室・講演を一元集約する公式母艦</td>
                <td>STUDIO / WP</td>
                <td style="text-align: center;">中</td>
            </tr>
            <tr>
                <td><strong>【案B】</strong></td>
                <td><strong>即効キャッシュ化LP</strong></td>
                <td>肖像画受注＆企業講演の即時成約に特化した1枚完結型</td>
                <td>STUDIO / ペライチ</td>
                <td style="text-align: center; color: #16a34a; font-weight: bold;">低（最速）</td>
            </tr>
            <tr>
                <td><strong>【案C】</strong></td>
                <td><strong>オンライン校＆サロン</strong></td>
                <td>月額制動画講座＋Zoom添削＋会員コミュニティ一体型</td>
                <td>Teachable / MOSH</td>
                <td style="text-align: center;">中〜高</td>
            </tr>
            <tr>
                <td><strong>【案D】</strong></td>
                <td><strong>作家ギャラリー＆越境EC</strong></td>
                <td>画材キット・カレンダー物販＆訪日客向け体験予約</td>
                <td>Shopify / BASE</td>
                <td style="text-align: center;">中</td>
            </tr>
        </tbody>
    </table>

    <!-- ================= PAGE 2 ================= -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <h1 class="doc-title">🗂️ 詳細設計：【案A】総合ポータル ＆ 【案B】高単価特化LP</h1>
        </div>
        <div>
            <p class="doc-subtitle">ブランド確立 ＆ 最速キャッシュ化の選択肢</p>
        </div>
    </div>

    <!-- 案A -->
    <div class="proposal-card" style="border-top: 4px solid #2b6cb0;">
        <div class="p-card-header" style="background: #ebf8ff;">
            <h4>🏛️【案A】総合ブランド＆ハブ型ポータルサイト（All-in-One Brand Portal）</h4>
            <span class="p-badge" style="background: #2b6cb0;">公式オフィシャルサイト</span>
        </div>
        <div class="p-card-body">
            <div class="p-lead-quote">「おかもっちゃん／鉛筆画家 瑞司のすべてが集まる公式母艦」</div>
            <p><strong>狙い：</strong>個人のファンから企業の人事担当者、メディア関係者まで、誰が来ても迷わず目的の情報にたどり着ける社会的信用の最高峰サイト。</p>
            
            <strong>■ サイト構造・ページマップ：</strong>
            <div class="tree-box">
[TOPページ]
  ├── [プロフィール] ─ 挫折と挑戦の軌跡（早大競走部主将→早明戦→熱血教師→53歳画家転身）
  ├── [作品ギャラリー] ─ 鉛筆肖像画 / 風景画 / パステル彩画 / 過去の代表作アーカイブ
  ├── [オーダー制作] ─ メモリアル肖像画 / 経営者ルーツ画（料金表・納期・制作の流れ）
  ├── [鉛筆画教室] ─ 「瑞司わくわく鉛筆画教室」（オンライン校 / 各地ワークショップ案内）
  ├── [企業・団体向け] ─ 講演・研修のご案内（テーマ・登壇実績・費用目安・ダイジェスト動画）
  ├── [メディア・お知らせ] ─ 個展情報、テレビ/新聞掲載、ブログ、YouTube更新情報
  └── [お問い合わせ / LINE] ─ 制作相談フォーム / 公式LINE友だち追加
            </div>

            <div class="pros-cons-grid">
                <div>⭕ <strong>メリット：</strong>社会的信用が最も高く、法人・教育機関・メディアからの大型案件の受け皿として盤石。</div>
                <div>❌ <strong>デメリット：</strong>ページ数が多く、初期制作に1〜2ヶ月程度の準備期間と素材収集が必要。</div>
            </div>
        </div>
    </div>

    <!-- 案B -->
    <div class="proposal-card" style="border-top: 4px solid #16a34a;">
        <div class="p-card-header" style="background: #f0fdf4;">
            <h4>⚡【案B】即効キャッシュ化・高単価LP特化型（High-Ticket Conversion LP）</h4>
            <span class="p-badge" style="background: #16a34a;">最速成約特化</span>
        </div>
        <div class="p-card-body">
            <div class="p-lead-quote">「迷わせない！『肖像画オーダー』と『熱血講演依頼』を最速で獲得する1枚完結LP」</div>
            <p><strong>狙い：</strong>複雑なメニューをあえて排除し、高単価で即効性の高い「① メモリアル肖像画」と「② 企業モチベーション講演」の2本柱に特化。</p>

            <strong>■ 1枚完結縦長LPのストーリー設計（上から下へ流れる成約導線）：</strong>
            <div class="tree-box">
1. ファーストビュー：圧倒的肖像画 ＋ おかもっちゃんの笑顔 ＋ 「言葉を超える鉛筆画」
2. 共感・問題提起：「大切な人の節目に一生の感動を」「組織の挑戦意欲に火をつけたい」
3. 2大サービスの提示：【Service 1】魂のメモリアル肖像画 ／ 【Service 2】熱血企業講演
4. 圧倒的実績・推薦の声：早大ラグビー部OB、箱根駅伝仲間、講演を受講した企業幹部の感想
5. 明朗な料金表・制作ステップ（不安を完全払拭）
6. 無料相談・お見積りCTA（公式LINEまたは簡易フォームへ直結）
            </div>

            <div class="pros-cons-grid">
                <div>⭕ <strong>メリット：</strong>制作期間1〜2週間でスピード公開可能。SNSや紹介からの直リンクで即売上に直結。</div>
                <div>❌ <strong>デメリット：</strong>オンラインスクールや画材物販など、多角的な情報を網羅するには不向き。</div>
            </div>
        </div>
    </div>

    <!-- ================= PAGE 3 ================= -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <h1 class="doc-title">🗂️ 詳細設計：【案C】オンライン校 ＆ 【案D】作家EC</h1>
        </div>
        <div>
            <p class="doc-subtitle">継続ストック収益 ＆ 自動物販・インバウンド展開</p>
        </div>
    </div>

    <!-- 案C -->
    <div class="proposal-card" style="border-top: 4px solid #805ad5;">
        <div class="p-card-header" style="background: #faf5ff;">
            <h4>💻【案C】オンラインアカデミー＆会員制プラットフォーム（Subscription & Community Hub）</h4>
            <span class="p-badge" style="background: #805ad5;">月額安定ストック</span>
        </div>
        <div class="p-card-body">
            <div class="p-lead-quote">「誰でも描ける！おかもっちゃんの瑞司式わくわく鉛筆画オンライン校」</div>
            <p><strong>狙い：</strong>月額3,980円〜9,800円の継続課金（ストック収益）を柱とする、オンライン動画講座と受講生コミュニティを一体化したWebプラットフォーム。</p>

            <strong>■ サイト構成（フロントLP ＋ 会員専用マイページ）：</strong>
            <div class="tree-box">
【フロントLP（一般公開）】
  ・「絵心ゼロでも大丈夫！鉛筆1本で始める大人のワクワク体験」
  ・受講生ビフォーアフター（生徒が15分で描いたリンゴや似顔絵の実例）
  ・無料レッスン動画プレゼント（LINE登録誘導） ＆ 月額受講プラン案内
【バックエンド（会員限定マイページ）】
  ・レベル別レッスン動画ライブラリ（基礎編、人物編、風景編）
  ・月1回Zoomライブ配信の受講リンク ＆ 「今月の添削コーナー（画像投稿）」
  ・受講生同士が作品を見せ合い褒め合う「わくわく掲示板」
            </div>

            <div class="pros-cons-grid">
                <div>⭕ <strong>メリット：</strong>会員が増えるほど自動的に収益が積み上がり、岡本氏の労働時間を切り売りせずに済む。</div>
                <div>❌ <strong>デメリット：</strong>初期の動画教材撮影・編集の手間と、月次のコミュニティ運営が必要。</div>
            </div>
        </div>
    </div>

    <!-- 案D -->
    <div class="proposal-card" style="border-top: 4px solid #dd6b20;">
        <div class="p-card-header" style="background: #fffaf0;">
            <h4>🎨【案D】作家ギャラリー＆越境EC・体験予約サイト（Art Gallery & Global EC）</h4>
            <span class="p-badge" style="background: #dd6b20;">自動物販＆インバウンド</span>
        </div>
        <div class="p-card-body">
            <div class="p-lead-quote">「原画・厳選画材・カレンダー販売 ＆ 訪日・海外向けワークショップ予約」</div>
            <p><strong>狙い：</strong>岡本氏監修の「画材スターターキット」や「日めくりカレンダー」を自動販売し、台湾ファンや訪日外国人向けのリアル体験を事前決済できる多言語サイト。</p>

            <strong>■ 主要機能・ページ構成：</strong>
            <div class="tree-box">
【オンラインショップ（BASE / Shopify）】
  ・瑞司監修「はじめての鉛筆画スターターキット」（特選鉛筆、消しゴム、紙、動画解説QR付）
  ・おかもっちゃん日めくりカレンダー（岡本武司語録入り）
  ・数量限定・直筆サイン入り複製原画（ジークレー版画・額装付き）
【ワークショップ予約（多言語：日・英・繁体字）】
  ・「Japanese Soul 鉛筆画体験（2時間）」カレンダー予約・事前オンライン決済
  ・国内・台湾での過去個展アーカイブ ＆ 展示会スケジュール
            </div>

            <div class="pros-cons-grid">
                <div>⭕ <strong>メリット：</strong>ECによる完全自動販売が実現し、海外（台湾等）や訪日観光客からの外貨獲得が可能。</div>
                <div>❌ <strong>デメリット：</strong>画材の仕入れ・在庫管理・梱包発送の体制（外注または家族等の協力）が必要。</div>
            </div>
        </div>
    </div>

    <!-- ================= PAGE 4 ================= -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <h1 class="doc-title">🔑 キラーコンテンツ ＆ 🔄 SNS×Web×LINE統合導線</h1>
        </div>
        <div>
            <p class="doc-subtitle">成約率を最大化する仕掛けとファネル設計</p>
        </div>
    </div>

    <div class="sec-title">💡 3. Webサイトに必ず組み込むべき「6大キラーコンテンツ」</div>

    <div class="killer-grid">
        <div class="killer-box k-1">
            <h5>①『人生のドラマ』ストーリー</h5>
            <p>早大主将→早明戦直談判→熱血教師→53歳画家。「何歳からでも挑戦できる」生き様そのものが最強の惹きつけ要素。</p>
        </div>
        <div class="killer-box k-2">
            <h5>②『奇跡のビフォーアフター』実例</h5>
            <p>「絵心がない」と思い込んでいた受講生が、わずか15分〜短期間で味のある絵を描けるようになった実例写真を多数掲載。</p>
        </div>
        <div class="killer-box k-3">
            <h5>③『魂の制作タイムラプス動画』</h5>
            <p>真っ白な紙から人物の瞳や表情が浮かび上がる瞬間を動画で埋め込み。「言葉を超える表現力」を一瞬で納得させる。</p>
        </div>
        <div class="killer-box k-4">
            <h5>④『明朗な料金表＆制作ステップ』</h5>
            <p>肖像画のサイズ別料金、納期、額装、修正対応を明記。「高そう」「頼み方が分からない」という心理的壁を完全排除。</p>
        </div>
        <div class="killer-box k-5">
            <h5>⑤『熱血・岡本武司語録ギャラリー』</h5>
            <p>教え子やファンに愛され続ける名言を絵とともに掲載。アートに「生きる元気と勇気」という付加価値をプラス。</p>
        </div>
        <div class="killer-box k-6">
            <h5>⑥『公式LINE登録 特典オファー』</h5>
            <p>「15分で立体感が描ける限定動画」や「元気が出る日めくり名言」を無料プレゼントし、訪問者を確実にリスト化。</p>
        </div>
    </div>

    <div class="sec-title">🔄 4. SNS × Webサイト × 公式LINEの統合導線設計（ファネル図）</div>

    <div class="integ-flow-container">
        <div class="integ-row">
            <div class="integ-col ic-sns">
                <h6>📱 1. 認知獲得（SNS）</h6>
                <ul>
                    <li>Instagram（完成作・リール）</li>
                    <li>YouTube（描画タイムラプス×語録）</li>
                    <li>Facebook（教え子・人脈交流）</li>
                </ul>
            </div>
            <div class="integ-arrow">➜</div>
            <div class="integ-col ic-web">
                <h6>🌐 2. 受皿（Webサイト/LP）</h6>
                <ul>
                    <li>作品・料金・理念の確認</li>
                    <li>「信頼」と「安心感」の獲得</li>
                    <li>LINE登録特典への誘導</li>
                </ul>
            </div>
            <div class="integ-arrow">➜</div>
            <div class="integ-col ic-line">
                <h6>🎁 3. 信頼醸成（公式LINE）</h6>
                <ul>
                    <li>無料動画レッスン即時配布</li>
                    <li>7日間ストーリーステップ配信</li>
                    <li>新作発表・先行案内</li>
                </ul>
            </div>
        </div>
        <div class="integ-outcomes">
            <div class="io-card">
                <h6>🖼️ 贈りたい・残したい方</h6>
                <p>メモリアル肖像画オーダー（15万〜100万円）</p>
            </div>
            <div class="io-card">
                <h6>💻 自分で描いてみたい方</h6>
                <p>オンライン鉛筆画校（月額 3,980円〜）</p>
            </div>
            <div class="io-card">
                <h6>🏢 組織に活力を入れたい方</h6>
                <p>熱血企業講演・研修（20万〜80万円）</p>
            </div>
        </div>
    </div>

    <!-- ================= PAGE 5 ================= -->
    <div class="page-break"></div>

    <div class="doc-header">
        <div>
            <h1 class="doc-title">🚀 実行計画：段階的導入ロードマップ ＆ ツール選定</h1>
        </div>
        <div>
            <p class="doc-subtitle">無理のない立ち上げステップと費用対効果の最大化</p>
        </div>
    </div>

    <div class="sec-title" style="margin-top: 0;">🗺️ 5. 推奨する「段階的導入ロードマップ」</div>

    <div class="step-timeline">
        <div class="step-card s-c1">
            <div class="step-num">Step 1</div>
            <div class="step-info">
                <h5>【今すぐ着手（1〜2ヶ月目）】案B「高単価特化LP」＋ 公式LINE構築</h5>
                <p>まずは制作が早くコストも抑えられる1枚完結LPを公開。肖像画受注と講演受付の窓口を固め、SNSからの流入を公式LINEでリスト化して即座に売上を立てる。</p>
            </div>
        </div>

        <div class="step-card s-c2">
            <div class="step-num">Step 2</div>
            <div class="step-info">
                <h5>【基盤構築（3〜5ヶ月目）】案C「オンライン校（サブスク教室）」のプレオープン</h5>
                <p>公式LINEで集まった見込み客に向けて、月額制の鉛筆画アカデミーやコミュニティを案内。毎月安定したストック収入基盤（月商100万円モデル）を確立する。</p>
            </div>
        </div>

        <div class="step-card s-c3">
            <div class="step-num">Step 3</div>
            <div class="step-info">
                <h5>【ブランド完成（6ヶ月目以降）】案A「総合ブランドポータル」へ統合拡張 ＋ 案D「公式EC」</h5>
                <p>全体のハブとなるオフィシャルサイトを完成させ、画材キットやカレンダーの自動物販、台湾・海外インバウンド向けの体験予約システムを本格稼働させる。</p>
            </div>
        </div>
    </div>

    <div class="sec-title">🛠️ 6. まとめ：制作ツールの推奨組み合わせ一覧</div>

    <table class="custom-table">
        <thead>
            <tr>
                <th style="width: 22%;">用途</th>
                <th style="width: 25%;">推奨ツール</th>
                <th style="width: 53%;">選定理由と特徴</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Webサイト / LP</strong></td>
                <td><strong class="highlight-blue">STUDIO (スタジオ)</strong></td>
                <td>日本発ノーコードツール。洗練されたデザインが直感的に作れ、サーバー管理不要。更新や修正が極めて簡単。</td>
            </tr>
            <tr>
                <td><strong>見込み客育成</strong></td>
                <td><strong class="highlight-blue">公式LINE (＋Lステップ等)</strong></td>
                <td>シニア層の利用率が極めて高く、メルマガより開封率が5〜10倍高い。ステップ配信で自動教育が可能。</td>
            </tr>
            <tr>
                <td><strong>ネットショップ物販</strong></td>
                <td><strong class="highlight-blue">BASE または Shopify</strong></td>
                <td>初期費用無料で即日ネットショップを開設可能。カード決済やコンビニ決済にも標準対応。海外ならShopify。</td>
            </tr>
            <tr>
                <td><strong>動画講座・コミュニティ</strong></td>
                <td><strong class="highlight-blue">MOSH または Teachable</strong></td>
                <td>日本語対応でシニアにも使いやすく、月額サブスク課金の自動管理やZoom連携が容易。</td>
            </tr>
        </tbody>
    </table>

    <div class="quote-banner" style="margin-top: 10px; border-left-color: #16a34a; background: #f0fdf4; color: #15803d;">
        <strong>岡本武司氏のWeb展開の成功の鍵：</strong><br>
        「絵の技術」を売るのではなく、岡本氏の<strong>「人間愛・熱血コーチング・何歳からでも挑戦できる勇気」</strong>をWeb上で体感できるように設計することです。まずは【Step 1の特化LP】から素早くスタートすることをおすすめします。
    </div>

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
    website_html = os.path.join(WORK_DIR, "website_proposals_temp.html")
    website_pdf = os.path.join(WORK_DIR, "岡本武司_ウェブサイト構築提案書.pdf")
    
    with open(website_html, 'w', encoding='utf-8') as f:
        f.write(build_website_proposals_html())
    
    convert_html_to_pdf(website_html, website_pdf)
    imgs = render_pdf_to_images(website_pdf, os.path.join(WORK_DIR, "preview_website_v2"))
    print(f"Website Proposals PDF generated: {len(imgs)} pages")

if __name__ == '__main__':
    main()
