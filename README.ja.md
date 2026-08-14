# Vedic Astro Skills

生年月日・正確な出生時刻・出生地から出生図を直接計算し、そのまま検証と
総合分析へ進める、8つの連携型ヴェーダ占星術（Jyotish）Skill です。

PDF やスクリーンショットの読み込みにも対応していますが、事前にチャートを
用意する必要はありません。出生情報だけで、計算、データ検証、惑星監査、
分割図照合、人生テーマ分析まで一つの流れで実行できます。

[简体中文](README.md) · [English](README.en.md)

## 収録 Skill

| Skill | 役割 | 日本語での依頼例 |
|---|---|---|
| `vedic-calculator` | 出生情報から完全な出生図を計算 | 「この出生情報でヴェーダ占星術の出生図を作って」 |
| `vedic-reader` | PDF・画像・テキストからチャートを抽出、標準化、検証 | 「この JHora のチャートを読み込んで検証して」 |
| `vedic-core` | 標準版の惑星監査、分割図照合、ハウス診断、人生テーマ分析 | 「この出生図をヴェーダ占星術で総合鑑定して」 |
| `vedic-career` | 適職、役割適性、働き方、時期を分析 | 「仕事運とキャリアの方向性を見て」 |
| `vedic-love` | 恋愛傾向、関係性、恋愛・結婚の時期を分析 | 「恋愛傾向と今後の時期を見て」 |
| `vedic-rectifier` | 出来事と分割図の切替から不確かな出生時刻を修正 | 「出生時刻が曖昧なので絞り込みたい」 |
| `vedic-synastry` | 二つの出生図を比較し、相互作用と共通時期を分析 | 「二人のチャートを比較して相性を見て」 |
| `vedic-prashna` | 一つの具体的質問について質問時刻図を作成・判定 | 「この件をプラシュナで見て」 |

## 主な特徴

- 出生情報から直接チャートを計算。外部 PDF は不要です。
- 下流 Skill が共通利用する検証済み `structured_data.md` を生成します。
- D1 と各分割図、Vimshottari Dasha、MD/AD/PD、Chara Dasha、Shadbala、
  SAV/BAV、品位、ハウス支配星、ヨーガ関連データを扱います。
- 本命分析、出生時刻修正、二人のチャート比較、Prashna を独立した
  ワークフローとして保持します。
- 日本語・英語・中国語の会話、質問票、進捗表示、警告、レポート、Q&A、
  HTML レポートに対応します。
- Codex、Claude Code、Antigravity 向けの配布構成を収録しています。

## インストール

### Codex

```bash
git clone https://github.com/CNWU16/vedic-astro-skills.git
cp -r vedic-astro-skills/codex/skills/vedic-* ~/.codex/skills/
```

Codex では、8つの Skill に加えて実行ルールパッチを入れる構成を推奨します。
パッチは Skill の方式を変更せず、フェーズ順序、ユーザー文脈と占星術証拠の
分離、Standard/Pro レポート系譜、出力ルーティング、顧客向け表現を補強します。

[Codex パッチの日本語インストールガイド](codex-patch/README.ja.md)

### Claude Code

```bash
git clone https://github.com/CNWU16/vedic-astro-skills.git
cp -r vedic-astro-skills/claude-code/skills/vedic-* ~/.claude/skills/
```

### Antigravity

`antigravity/skills/` にある8つの `vedic-*` フォルダを、使用している
Antigravity の Skill ディレクトリへコピーしてください。多くの下流 Skill が
`vedic-calculator` の標準データを使うため、8つまとめての導入を推奨します。

## Python 環境

対応バージョンは Python **3.8～3.13** です。天文計算の C 拡張依存のため、
Python 3.14 は現在サポートしていません。

`requirements.txt` を直接インストールせず、付属のセットアップスクリプトを
使用してください。

```bash
python path/to/vedic-calculator/scripts/setup_env.py
```

## クイックスタート

### 出生情報から始める

```text
ヴェーダ占星術の出生図を作ってください。
生年月日：1990-01-01
出生時刻：08:00
出生地：Tokyo, Japan
```

計算器が標準データ `structured_data.md` を生成します。検証後は次のように
続けられます。

```text
この出生図を標準版で総合分析してください。日本語でお願いします。
```

### 既存チャートから始める

JHora、Parashara's Light、その他のヴェーダ占星術ソフトの PDF、画像、
テキストを添付して次のように依頼します。

```text
このヴェーダ占星術チャートを読み込んで、日本語で検証してください。
```

### 二人のチャート比較

二人分の検証済み `structured_data.md` を用意するか、不足する人の出生情報を
渡して計算します。

```text
この二人のチャートを、仕事上のパートナーシップとして比較してください。
```

### Prashna

Prashna は本命分析とは独立しています。具体的な質問を一つ、その質問が
確定した正確な日時と場所を渡してください。

```text
この具体的な質問について、質問時刻図を立てて判断してください。
```

古典標準レイヤーが先に実行されます。Tajika と KP は任意の独立方式であり、
標準判定と混ぜて投票しません。

## 日本語対応の仕組み

各 Skill の `SKILL.md` が計算、証拠、フェーズ、スコア、成果物の唯一の真源です。
日本語実行時だけ、各 Skill 内の `resources/ja-*.md` を追加で読み込みます。

この日本語レイヤーが固定するのは次の項目です。

- 日本で読みやすい専門用語と初出時の説明
- 自然な `です・ます` 調
- 情報入力、確認、進捗表示の言い回し
- 各モジュールの顧客向けセクション名と回答順序
- 日本語 HTML の表紙、目次、見出し、フッター、フォント

ファイル名、`structured_data.md` schema、CLI フラグ、JSON key、候補ラベル、
技術コード、サンスクリット／英語の識別子、証拠、スコア、結論、フェーズ状態、
レポート系譜は翻訳しません。日本語 HTML は
`report_builder.py --lang ja` で生成します。

## リポジトリ構成

```text
antigravity/skills/   公開内容の基準となる Skill
claude-code/skills/   Claude Code 配布版
codex/skills/         Codex 配布版（agents/openai.yaml を追加）
codex-patch/          Codex 用の推奨実行ルールパッチ
scripts/              三つの配布面の一致チェック
```

変更後は次のコマンドで三つの配布面が一致していることを確認します。

```bash
python3 scripts/check_skill_parity.py
```

## 利用範囲

本リポジトリは、伝統的なヴェーダ占星術の学習、文化的研究、構造化された
自己理解のためのワークフローです。医療、法律、金融、安全に関わる専門的な
判断を代替するものではありません。

## ライセンス

AGPL-3.0。個人利用はライセンス条件の範囲で自由です。商用利用・ネットワーク
サービスについては [commercial notice](COMMERCIAL_NOTICE) も確認してください。
