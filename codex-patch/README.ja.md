# Vedic Astro Skills 用 Codex パッチ

> Codex Patch v1.3.0。Vedic Skill Suite 本体、Blind QA プロトコル、
> 分析者編集プロトコルとは独立したバージョンで管理されます。

このパッチは Codex 向けの実行互換レイヤーです。Vedic Skill の代替ではなく、
各 `SKILL.md` が引き続き標準ワークフローの真源です。

Codex で起こりやすいフェーズの省略、ユーザー文脈への過剰適合、機械的な採点、
Standard/Pro レポートの混在、成果物ルーティング、顧客向け文章の問題を抑えます。
クライアント向け言語はユーザーの指定に従い、計算データ、ファイル名、証拠、
判断、フェーズ状態は言語変更の影響を受けません。

[English](README.en.md) · [中文](README.md)

## 内容

- `AGENTS.md` — Vedic Skill 全体の実行ルーター
- `vedic_uc_firewall.md` — 全 Vedic タスク共通のユーザー文脈証拠ファイアウォール
- `vedic_client_voice.md` — 顧客向けの読みやすさと語り口
- `vedic_core_life_rendering.md` — Standard/Pro の人生テーマ部分の成文規則
- `vedic_qa_rendering.md` — 正式に Q&A へ入った後の回答表現
- `vedic_output_router.md` — Q&A、完全レポート、編集版、HTML の成果物選択
- `vedic_blind_qa_prompt.md` — 本命 Core の全量ブラインド Q&A
- `vedic_consultative_integration_prompt.md` — 任意の分析者編集版レポート
- `vedic_rectifier_execution_overlay.md` — 出生時刻修正の実行ルーター
- `vedic_rectifier_settlement.md` — 候補時刻の決着と反対材料監査
- `vedic_rectifier_question_design.md` — 選択中のSkillにある正規の
  `resources/calibration_quiz.md` への互換ポインタ
- `vedic_rectifier_interval_guard.md` — 探索区間と代表チャートの保護規則

`PACKAGE_INTRO.md` はパッケージの位置づけを説明する文書で、実行ルールでは
ありません。

## インストール

### 1. 有効な Codex home を確認する

既定値は `~/.codex` です。`CODEX_HOME` を設定している場合は、以下のコピー先を
すべて実際のディレクトリに読み替えてください。

### 2. Vedic Skill を先に導入する

必要な `vedic-*` Skill を先にインストールします。`vedic-core-pro` は任意です。
Standard 版の `vedic-core` だけでも動作します。

### 3. Vedic ルーターを安全に統合する

既存のグローバル `AGENTS.md` を上書きしないでください。

- `<CODEX_HOME>/AGENTS.md` がなければ、このパッケージの `AGENTS.md` をコピーします。
- すでにある場合は、`# Vedic Skill Suite Execution Router` から始まる完全な
  セクションを、実際に有効な指示ファイルへ統合します。
- `<CODEX_HOME>/AGENTS.override.md` がある場合は、グローバルルーターを上書き
  していないか確認します。

### 4. ルーティング対象モジュールをコピーする

次の11ファイルを、名前を変えずに有効な `CODEX_HOME` 直下へコピーします。

```text
vedic_uc_firewall.md
vedic_client_voice.md
vedic_core_life_rendering.md
vedic_rectifier_execution_overlay.md
vedic_rectifier_settlement.md
vedic_rectifier_question_design.md
vedic_rectifier_interval_guard.md
vedic_blind_qa_prompt.md
vedic_consultative_integration_prompt.md
vedic_output_router.md
vedic_qa_rendering.md
```

### 5. 新しい Codex タスクを開始する

グローバル指示はタスク開始時に読み込まれる場合があります。更新後は新しい
Codex タスクを作成し、ルーターと必要なモジュールが利用できることを確認します。

## Standard と Pro の選択

新しい本命 Core 分析が最初の成果物を書く前に、次の規則を適用します。

- ユーザーが Standard を明示した場合は `vedic-core`
- ユーザーが Pro を明示した場合は `vedic-core-pro`
- 両方が導入済みで指定がなければ、Codex が一度だけ確認
- 一方しかない場合は、利用可能な Core をそのまま使用

選択した Core はその実行のレポート系譜になります。続き、通常 Q&A、Blind QA、
分析者編集、HTML 化は同じ系譜を引き継ぎます。Standard と Pro の成果物を
自動的に混ぜることはありません。

Pro 専用パッチは不要です。Standard と Pro は同じ証拠境界、表現、ルーティング、
出生時刻修正、言語規則を使用し、それぞれの `SKILL.md` に従います。

## 出生時刻修正の証拠区分

現行の `vedic-rectifier` に合わせ、判断を主、参考点を補助として扱います。日付付き
出来事とDashaの対応、ならびに事実・特性・経験と候補間で実際に変化するチャート
構造の対応を、一つの全候補マッピング表に記録します。同じ構造で説明される材料は
一組として扱い、参考点は監査用に表示するだけで決着基準にはしません。各層は主線
判断、次点候補の弁護（一度のみ）、信頼度、決定的または最も識別力の高い材料で
決着します。一方の候補が強く予測し、他方が反対を予測する、ユーザー確認済みの
客観的事実または日付付き出来事だけが、単独で候補対を決められます。信頼度が低い
場合は `resources/calibration_quiz.md` の7段階・3検査で最大2ラウンド質問し、回答を
全候補表へ戻して再判断します。廃止済みの二レッグ等重み合計、点差基準、除外ゲート、
設問ごとの加点方式は復活させません。

## 日本語実行

クライアント向け言語は明示された指定を優先し、指定がなければ直近の実質的な
ユーザーメッセージに合わせます。会話、情報入力、質問票、進捗、警告、レポート、
Q&A、分析者編集、HTML に適用されます。

日本語実行時は、選択した Skill が自身の `resources/ja-*.md` を読み込みます。
このファイルは専門用語、`です・ます` 調、入力文、顧客向け見出しだけを制御します。
パッチは実行順序と証拠境界を制御し続けます。

次の内部契約は翻訳しません。

- ファイル名と schema 見出し
- CLI フラグ、JSON key、技術コード
- サンスクリット／英語の識別子
- 候補ラベル、スコア、証拠引用
- チャート判断、フェーズ状態、レポート系譜

## ユーザー文脈の境界

ユーザー文脈には、会話、要約、レポート、ファイル名、スクリーンショット、
アーカイブ、`user_context.md` に見える既知事実が含まれます。選択 Skill が
現在のフェーズで証拠として明示的に許可しない限り、これらは占星術証拠には
なりません。

許可された校正フェーズ以外では、チャート由来の判断を先に固定し、その後で
許可された文脈を表現、倫理確認、現実の選択肢への対応づけに使います。既知の
事実を、チャートから独立に予測した内容として提示してはいけません。

Standard Core の Step 4.5 と Pro の Step 6.5 は、判断確定後に行う読み取り専用の
表現校訂です。選択 Skill が指定したファイルの文言と現実上の着地点だけを修正し、
評価、時期、領域、配偶者像、Yoga、Dasha、表、信頼度、上流の技術成果物は変更
しません。内部で付けたセンシティブ分類ラベルをレポート本文へ再掲することも
禁止です。

## 更新

ルーターと11のモジュールは、一つの整合したパッケージとして更新してください。
新しいルーターと任意の古いモジュールを混在させないでください。更新後は新しい
Codex タスクで有効な構成を確認します。

このパッチは Vedic `SKILL.md` を変更しません。グローバルルーターの Vedic
セクションと11のモジュールを削除すれば、Skill 単体の動作へ戻ります。
