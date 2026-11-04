# CLAUDE.md が複数あるときの読まれ方 の主張

- ドキュメント: https://code.claude.com/docs/en/memory#how-claude-md-files-load （と同じページの #choose-where-to-put-claude-md-files、#load-from-additional-directories、#instructions-seem-lost-after-compact。関連: https://code.claude.com/docs/en/large-codebases#layer-claude-md-files-by-directory）（2026-11-04 に読んだ）
- 用語:
  - CLAUDE.md, CLAUDE.local.md などをまとめて呼ぶときは「指示書」。1つを指すときはファイル名で書く
  - working directory → 「起動したフォルダ」。directory → 「フォルダ」。subdirectory → 「サブフォルダ」、directory above → 「上のフォルダ」
  - load → 「読み込まれる」（Claude が Read ツールで開くことは「読む」と書き分ける）
  - concatenated → 「つながって全部入る」、override → 「上書き」
  - on demand → 「必要になったときに」
  - バージョンの意味では「バージョン」

| ID | 主張 | 確かめ方 | 根拠 | 検証 | 判定 |
|---|---|---|---|---|---|
| C1 | 起動したフォルダと、その上のすべてのフォルダにある CLAUDE.md と CLAUDE.local.md が、起動時に読み込まれる | 実機 | #how-claude-md-files-load。クラウドで確認（2.1.318）。git リポジトリの境目でも止まらず、その上のフォルダのものも読み込まれた | 検証1 | 未判定 |
| C2 | 見つかった指示書は上書きし合わず、つながって全部入る | 実機 | #how-claude-md-files-load。クラウドで確認（2.1.318） | 検証1 | 未判定 |
| C3 | 並びは、ファイルシステムの上から起動したフォルダへ向かう順（上のフォルダのものが先） | 実機 | #how-claude-md-files-load。クラウドで確認（2.1.318） | 検証1 | 未判定 |
| C4 | 同じフォルダの中では、CLAUDE.local.md が CLAUDE.md のあとに付く | 実機 | #how-claude-md-files-load。クラウドで確認（2.1.318）。本体のコードでは、同じフォルダの中は CLAUDE.md → .claude/CLAUDE.md → .claude/rules/ → CLAUDE.local.md の順（2.1.318） | 検証1 | 未判定 |
| C5 | `./.claude/CLAUDE.md` も、`./CLAUDE.md` と同じくプロジェクトの指示書として読み込まれる | 実機 | #choose-where-to-put-claude-md-files。クラウドで確認（2.1.318）。両方あるときは両方入る | 検証1 | 未判定 |
| C6 | 範囲ごとの順は、会社の指示書 → 個人の `~/.claude/CLAUDE.md` → プロジェクト → CLAUDE.local.md（個人の指示書がプロジェクトより先） | 本体のコード | 読み込みの関数で Managed → User → フォルダごとの Project / Local の順に積む（2.1.318）。個人の指示書がプロジェクトより先なのは、設定フォルダを差し替えてクラウドで確認（2.1.318）。キットでは試す人の個人ファイルを変えないため扱わない | — | 記述どおり |
| C7 | サブフォルダの CLAUDE.md は起動時には読み込まれず、Claude がそのフォルダのファイルを読む・書く・編集したときに読み込まれる | 実機 | #how-claude-md-files-load。Read と Write でクラウドで確認（2.1.318）。画面には `Loaded <パス>` の行が出る（本体のコード、2.1.318） | 検証2 | 未判定 |
| C8 | 1つのファイルを `cat` や `head` で見る Bash も「読む」に数える | 実機 | #how-claude-md-files-load。`cat` でクラウドで確認（2.1.318）。`ls` では読み込まれなかった（ドキュメントに書かれていない） | 検証2 | 未判定 |
| C9 | サブフォルダの CLAUDE.md は、1つにつき1回だけ読み込まれる | 実機 | #how-claude-md-files-load（"loads each one once"） | 検証2 | 未判定 |
| C10 | 深いサブフォルダのファイルを読むと、途中のフォルダの CLAUDE.md も上から順に読み込まれる | 実機 | ドキュメントに書かれていない。クラウドで確認（2.1.318） | 検証2 | 未判定 |
| C11 | 必要になったときに読み込まれたサブフォルダの CLAUDE.md は、`/context` の Memory files の一覧には出ない | 実機 | ドキュメントに書かれていない（large-codebases は「読み込まれたファイルは `/context all` の Memory files で確かめる」と書く）。`/context` と `/context all` の両方でクラウドで確認（2.1.318） | 検証2 | 未判定 |
| C12 | ブロックの HTML コメント（`<!-- -->`）は消してから渡され、コードブロックの中のコメントは残る | ドキュメントの文 | #how-claude-md-files-load。クラウドで確認（2.1.318） | — | 記述どおり |
| C13 | `--add-dir` で足したフォルダの CLAUDE.md は、既定では読み込まれず、`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` で読み込まれる | ドキュメントの文 | #load-from-additional-directories。クラウドで確認（2.1.318）。読み込まれると、起動したフォルダのものより後に並ぶ | — | 記述どおり |
| C14 | `/compact` のあと、起動時に読み込まれた指示書は読み直され、サブフォルダの CLAUDE.md は必要になったときにまた読み込まれる | ドキュメントの文 | #instructions-seem-lost-after-compact。`turns.py` でクラウドで確認（2.1.318）。要約の前に読んだファイルが読み直されると、そのフォルダの CLAUDE.md もすぐ戻った。要約のテーマ（claude-compact-check）と重なるため、キットでは扱わない | — | 記述どおり |

## 検証の設計

キットのフォルダ（`topics/claude-md-loading/`）に、次の指示書を置く。中身はそれぞれ「〇〇の言葉は「△△」」の1行だけにする。

| ファイル | 言葉 |
|---|---|
| `CLAUDE.md` | やま |
| `CLAUDE.local.md` | かわ |
| `app/CLAUDE.md` | うみ |
| `app/.claude/CLAUDE.md` | そら |
| `app/CLAUDE.local.md` | もり |
| `side/CLAUDE.md` と `side/s.txt` | にじ |
| `sub/CLAUDE.md` と `sub/a.txt`、`sub/b.txt` | ほし |
| `sub/deep/CLAUDE.md` と `sub/deep/c.txt` | つき |

- 名前の順（アルファベット順）では `.claude/CLAUDE.md` → `CLAUDE.local.md` → `CLAUDE.md` になる。予想の順（`CLAUDE.md` → `.claude/CLAUDE.md` → `CLAUDE.local.md`）と違うので、名前の順に並べているだけなら区別できる。
- clone した直後はファイルの更新日時がそろうので、更新日時の順とは関係しない。

### 検証1　上のフォルダの CLAUDE.md も含めて、全部が上から順に読み込まれるか（C1〜C5）

- **記録の見出し**
  - 【1A】`/context` の Memory files の表（そのまま貼る）
  - 【1B】「ファイルを読まずに、指示書の言葉を現れる順に」と聞いたときの答え（そのまま貼る）
  - 【1Z】手順以外に Claude が読んだファイル
- **用意するもの**: 上の表の `CLAUDE.md`、`CLAUDE.local.md`、`app/` の3つ
- **手順**: `cd app` → `claude` → `/context` → 言葉を聞く → `/exit`
- **予想**
  - 【1A】`CLAUDE.md` → `CLAUDE.local.md` → `app/CLAUDE.md` → `app/.claude/CLAUDE.md` → `app/CLAUDE.local.md` の順に5つ並ぶ。個人の `~/.claude/CLAUDE.md` や、このリポジトリより上のフォルダの CLAUDE.md があれば、それより前に並ぶ
  - 【1B】やま → かわ → うみ → そら → もり
- **外れたら何が分かるか**
  - 上の2つが無い: 上のフォルダは読み込まれない（C1 が違う）
  - 言葉が1つしか出ない: 上書きされている（C2 が違う）
  - `app/` のものが先: 並びが逆（C3 が違う）
  - `CLAUDE.local.md` が `CLAUDE.md` より先: C4 が違う。名前の順に並んでいるだけかもしれない
  - `app/.claude/CLAUDE.md` が無い: C5 が違う
  - 【1A】と【1B】で順が違う: 表の並びと、Claude に渡る並びが違う
- **紛れと潰し方**
  - Claude が README や指示書を Read で開いて答える → 「ファイルを読まずに」を付ける。【1Z】に書く
  - auto memory に前の名残 → 準備と検証の始めに `/memory` で消す
  - 個人の `~/.claude/CLAUDE.md`、会社の指示書、このリポジトリより上のフォルダの CLAUDE.md が混ざる → 【1A】にそのまま出るので、それらを除いて判定する。【環境】にも書く
  - 個人の設定の `claudeMdExcludes` や「Project instructions」の設定で外される → 【環境】で `/config` の Project instructions を記録する。表に出ないファイルがあったら補足で読み方を書く
  - 起動したフォルダが違う → `app` で起動する（この検証だけ、テーマのフォルダではなく `app` で起動する）。【1A】のパスで分かる
  - 許可の名残 → 準備で `ls ../../.claude`
- **人にしかできない操作**: `cd app`、`/context`（2つ）
- **補足に書くこと**: 本体のコードでは、同じフォルダの `.claude/rules/` は `.claude/CLAUDE.md` と `CLAUDE.local.md` の間に入る

### 検証2　サブフォルダの CLAUDE.md は、そのフォルダのファイルを読んだときに初めて読み込まれるか（C7〜C11）

- **記録の見出し**
  - 【2A】起動直後に言葉を聞いたときの答え（そのまま貼る）
  - 【2B】`ls side` のあと、`Loaded` で始まる行が出たか（出たらそのまま貼る）
  - 【2C】`cat side/s.txt` のあと、`Loaded` で始まる行（そのまま貼る）
  - 【2D】`sub/a.txt` を読んだあと、`Loaded` で始まる行（そのまま貼る）
  - 【2E】`sub/b.txt` を読んだあと、`Loaded` で始まる行が出たか
  - 【2F】`sub/deep/c.txt` を読んだあと、`Loaded` で始まる行（そのまま貼る）
  - 【2G】最後に言葉を聞いたときの答え（そのまま貼る）
  - 【2H】`/context` の Memory files の表（そのまま貼る）
  - 【2Z】手順以外に Claude が読んだファイル
- **用意するもの**: 上の表の `side/`、`sub/`、`sub/deep/`
- **手順**: テーマのフォルダで `claude` → 言葉を聞く → `ls side` → `cat side/s.txt` → Read で `sub/a.txt` → Read で `sub/b.txt` → Read で `sub/deep/c.txt` → 言葉を聞く → `/context` → `/exit`
- **予想**
  - 【2A】やま → かわ だけ（`app/`、`side/`、`sub/` のものは出ない）
  - 【2B】出ない（2.1.318 クラウドで、`ls` では読み込まれなかった）
  - 【2C】`Loaded side/CLAUDE.md`
  - 【2D】`Loaded sub/CLAUDE.md`
  - 【2E】出ない（1回だけ）
  - 【2F】`Loaded sub/deep/CLAUDE.md`
  - 【2G】やま → かわ → にじ → ほし → つき
  - 【2H】`CLAUDE.md` と `CLAUDE.local.md` の2つだけ。サブフォルダのものは出ない（2.1.318 クラウドで試したときの結果）
- **外れたら何が分かるか**
  - 【2A】にサブフォルダの言葉: 起動時に読み込まれている（C7 が違う）か、Claude が先にファイルを開いた（【2Z】を見る）
  - 【2B】に行が出る: `ls` も読むに数える
  - 【2C】に行が出ない: `cat` は読むに数えない（C8 が違う）
  - 【2E】に行が出る: 2回読み込まれる（C9 が違う）
  - 【2D】で `sub/deep/CLAUDE.md` まで出る、または【2F】で `sub/CLAUDE.md` が出る: 読み込む範囲の考え方が違う（C10）
  - 【2H】にサブフォルダのものが出る: 実機では `/context` で確かめられる（C11 が違う）
- **紛れと潰し方**
  - Claude が手順の前に `sub/` や `side/` のファイルを開く（Glob や ls で探す、など）→ 【2A】の質問に「ファイルを読まずに」を付ける。【2Z】に書き、どの手順のあとか分かるようにする
  - `cat` を Bash でなく Read ツールで読み替える → 「Bash で」と指定する。画面の `Bash(cat side/s.txt)` の行で分かる
  - `Loaded` の行が折りたたまれて見えない、または表示が違う → 【2G】の答えでも確かめられるようにしてある
  - 言葉を聞いたとき、会話に出たファイル名から推測して答える → 言葉はファイルの中にしか無く、ファイル名からは分からない
  - auto memory、許可の名残、前の会話 → 共通の約束どおり
- **人にしかできない操作**: `/context`（1つ）
- **補足に書くこと**: Write でもそのフォルダの CLAUDE.md が読み込まれた（2.1.318 クラウド）。`/compact` のあとは、要約の前に読んだファイルが読み直されると、そのフォルダの CLAUDE.md も戻る（C14）

### 重さ

- 検証は2つ、ターミナル1つ、所要15〜20分ほど
- 試す人のリポジトリの状態を変えない（ファイルを作らない・書き換えない。Write は手順に入れない）
- スクリプトは使わない
