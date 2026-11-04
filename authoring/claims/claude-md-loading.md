# CLAUDE.md が複数あるときの読まれ方 の主張

- ドキュメント: https://code.claude.com/docs/en/memory#how-claude-md-files-load （と同じページの #choose-where-to-put-claude-md-files、#load-from-additional-directories、#claude-isnt-following-my-claudemd、#claude-ignores-the-end-of-my-subdirectory-claude-md、#instructions-seem-lost-after-compact。関連: https://code.claude.com/docs/en/large-codebases#choose-where-to-start-claude）（2026-11-04 に読んだ）
- 用語:
  - CLAUDE.md, CLAUDE.local.md などをまとめて呼ぶときは「指示書」。1つを指すときはファイル名で書く
  - working directory → 「起動したフォルダ」。directory → 「フォルダ」。subdirectory → 「サブフォルダ」、directory above → 「上のフォルダ」
  - load → 「読み込まれる」（Claude が Read ツールで開くことは「読む」と書き分ける）
  - concatenated → 「つながって全部入る」、override → 「上書き」
  - on demand → 「必要になったときに」
  - バージョンの意味では「バージョン」
- 確かめ方の「実機（クラウドで確認）」は、クラウドの `claude -p` や `turns.py` で確かめ、キットでは扱わないもの。理由は根拠の列に書く。

| ID | 主張 | 確かめ方 | 根拠 | 検証 | 判定 |
|---|---|---|---|---|---|
| C1 | 起動したフォルダと、その上のすべてのフォルダにある CLAUDE.md と CLAUDE.local.md が、起動時に読み込まれる | 実機 | #how-claude-md-files-load。クラウドで確認（2.1.318）。git リポジトリの境目でも止まらず、その上のフォルダのものも読み込まれた。本体のコードでは、ファイルシステムの一番上（`/`）の手前で止まる（2.1.318。試していない） | 検証1 | 未判定 |
| C2 | 見つかった指示書は上書きし合わず、つながって全部入る | 実機 | #how-claude-md-files-load。クラウドで確認（2.1.318） | 検証1 | 未判定 |
| C3 | 並びは、ファイルシステムの上から起動したフォルダへ向かう順（上のフォルダのものが先） | 実機 | #how-claude-md-files-load。クラウドで確認（2.1.318） | 検証1 | 未判定 |
| C4 | 同じフォルダの中では、CLAUDE.local.md が CLAUDE.md のあとに付く | 実機 | #how-claude-md-files-load。クラウドで確認（2.1.318）。`.claude/CLAUDE.md` との前後はドキュメントに書かれていない。本体のコードでは、同じフォルダの中は CLAUDE.md → .claude/CLAUDE.md → .claude/rules/ → CLAUDE.local.md の順（2.1.318） | 検証1 | 未判定 |
| C5 | `./.claude/CLAUDE.md` も、`./CLAUDE.md` と同じくプロジェクトの指示書として読み込まれる | 実機 | #choose-where-to-put-claude-md-files（"`./CLAUDE.md` or `./.claude/CLAUDE.md`"）。両方あるときは両方入る（クラウドで確認、2.1.318。ドキュメントに書かれていない） | 検証1 | 未判定 |
| C6 | 範囲ごとの順は、会社の指示書 → 個人の `~/.claude/CLAUDE.md` → プロジェクト → CLAUDE.local.md（個人の指示書がプロジェクトより先） | 本体のコード | 読み込みの関数で Managed → User → フォルダごとの Project / Local の順に積む（2.1.318）。個人の指示書がプロジェクトより先なのは、設定フォルダを差し替えてクラウドで確認（2.1.318）。キットでは試す人の個人ファイルを変えないため扱わない | — | 記述どおり |
| C7 | サブフォルダの CLAUDE.md と CLAUDE.local.md は起動時には読み込まれず、Claude がそのフォルダのファイルを読む・書く・編集したときに読み込まれる。読み込まれると、ターミナルに `Loaded` の行が出る | 実機 | #how-claude-md-files-load、#claude-isnt-following-my-claudemd（"a `Loaded` line with its path appears in the terminal"）。Read と Write でクラウドで確認（2.1.318）。サブフォルダの CLAUDE.local.md も Read で読み込まれた（クラウドで確認、2.1.318）。キットでは CLAUDE.md だけを扱う | 検証2 | 未判定 |
| C8 | 1つのファイルを `cat` や `head` で見る Bash も「読む」に数える | 実機 | #how-claude-md-files-load。`cat` でクラウドで確認（2.1.318）。`ls` では読み込まれなかった（ドキュメントに書かれていない） | 検証2 | 未判定 |
| C9 | 同じサブフォルダのファイルを2つ目に読んでも、そのフォルダの CLAUDE.md は読み込み直されない | 実機 | ドキュメントに書かれていない（#how-claude-md-files-load の "loads each one once Claude reads" の once は「〜したときに」の意味）。本体のコードでは、読み込んだパスを覚えて2回目を飛ばす（2.1.318） | 検証2 | 未判定 |
| C10 | 深いサブフォルダのファイルを読むと、途中のフォルダの CLAUDE.md も上から順に読み込まれる | 実機 | ドキュメントに書かれていない。クラウドで確認（2.1.318） | 検証2 | 未判定 |
| C11 | 必要になったときに読み込まれたサブフォルダの CLAUDE.md は、`/context all` の Memory files の一覧には出ない | 実機 | #claude-isnt-following-my-claudemd（"doesn't appear under **Memory files**, because it loads on demand"）。`/context` と `/context all` の両方でクラウドで確認（2.1.318）。large-codebases の「読み込まれたファイルは `/context all` で確かめる」は、起動時に読み込まれるものの話 | 検証2 | 未判定 |
| C12 | 矛盾する指示が2つの指示書にあると、Claude はどちらかを決まりなく選ぶことがある（後に並ぶ方が優先されるわけではない） | ドキュメントの文 | #write-effective-instructions（"Claude may pick one arbitrarily"）、#claude-isnt-following-my-claudemd も同じ。どちらが選ばれるかは決まらないため、試しても確かめられない。並び（C3・C4）を「優先の順」と読まないよう、ページの「気をつけること」に入れる | — | 未検証 |
| C13 | 必要になったときに読み込まれる指示書は、1つにつき文字数の上限（200K のコンテキストで 40,000 文字）を超えると、始めの部分しか渡されない。起動時に読み込まれるものには、この上限は無い（4 MiB を超えるファイルは飛ばされる） | 本体のコード | #claude-ignores-the-end-of-my-subdirectory-claude-md、#my-claudemd-is-too-large。本体のコードでは、上限は最小 40,000 文字でコンテキストの大きさに比例し、会社の指示書には当てはめない。4 MiB（4194304）の値もある（2.1.318） | — | 記述どおり |
| C14 | ブロックの HTML コメント（`<!-- -->`）は消してから渡され、コードブロックの中のコメントは残る | 実機（クラウドで確認） | #how-claude-md-files-load。クラウドで確認（2.1.318）。「どれが・どの順で・いつ」とは別の話なので、キットでは扱わず、ページでも「気をつけること」には入れない | — | 記述どおり |
| C15 | `--add-dir` で足したフォルダの CLAUDE.md は、既定では読み込まれず、`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` で読み込まれる | 実機（クラウドで確認） | #load-from-additional-directories。クラウドで確認（2.1.318）。読み込まれると、起動したフォルダのものより後に並ぶ（ドキュメントに書かれていない）。起動の仕方を変える話で、キットの重さを超えるため扱わない | — | 記述どおり |
| C16 | `/compact` のあと、プロジェクトの一番上の CLAUDE.md は読み直され、サブフォルダの CLAUDE.md は必要になったときにまた読み込まれる | 実機（クラウドで確認） | #instructions-seem-lost-after-compact。`turns.py` でクラウドで確認（2.1.318）。ドキュメントに書かれていないこと: 上のフォルダの CLAUDE.md や CLAUDE.local.md も含め、起動時に読み込まれたものは全部戻った。要約の前に読んだファイルが読み直されると、そのフォルダの CLAUDE.md もすぐ戻った。要約のテーマ（claude-compact-check）と重なるため、キットでは扱わない | — | 記述どおり |

## 検証の設計

キットのフォルダ（`topics/claude-md-loading/`）に、次の指示書を置く。中身はそれぞれ「この指示書の言葉は「△△」」の1行だけにし、場所を表す言葉は入れない（Claude が場所から並びを推し量って答えないようにするため）。`.txt` の中身は、言葉と関係のない1行（`abc` など）にする。

| ファイル | 言葉 |
|---|---|
| `CLAUDE.md` | やま |
| `CLAUDE.local.md` | かわ |
| `app/CLAUDE.md` | うみ |
| `app/.claude/CLAUDE.md` | そら |
| `app/CLAUDE.local.md` | もり |
| `side/CLAUDE.md`（ほかに `side/s.txt`） | にじ |
| `sub/CLAUDE.md`（ほかに `sub/a.txt`） | ほし |
| `sub/deep/CLAUDE.md`（ほかに `sub/deep/c.txt`） | つき |

- 名前の順（アルファベット順）では `.claude/CLAUDE.md` → `CLAUDE.local.md` → `CLAUDE.md` になる。予想の順（`CLAUDE.md` → `.claude/CLAUDE.md` → `CLAUDE.local.md`）と違うので、名前の順に並べているだけなら区別できる。
- clone した直後はファイルの更新日時がそろうので、更新日時の順とは関係しない。
- キットを作ったら、`git ls-files . | grep -c CLAUDE.local.md` で 2 と出るか確かめる（作る側の全体の gitignore に CLAUDE.local.md があると、commit から抜けるため）。
- 2つの検証は、large-codebases の「リポジトリの一番上で起動する／サブフォルダで起動する」の対比になっている。結果は「必ず入れたい指示は、起動するフォルダかその上に置く。サブフォルダのものは、Claude がそこのファイルに触れるまで入らず、`/context all` にも出ない」の形で書けるかを判定の観点にする。
- `/context all` を使うのは、全画面モードでも Memory files の一覧が畳まれないため（#how-claude-md-files-load の上の "In fullscreen mode, `/context` alone collapses that list"）。
- デスクトップアプリの Code タブでは、`cd` と `claude` の代わりに、そのフォルダを選んで新しいセッションを始める。worktree は使わない（worktree の中ではパスが変わり、worktree より上でリポジトリの中のフォルダはプロジェクトの指示書として読まれない。本体のコード、2.1.318）。`Loaded` の行はターミナルの表示と書かれているので、Code タブで出なければ、その欄は「出なかった」と書き、判定には言葉を聞いた答えを使う。
- 共通の約束に足すこと: ファイルを `@` で指さず、文で頼む（`@` で指すと Read を通らずに読み込まれる）。エディタで、このキットのファイルを開いたままにしない（IDE につないでいると、開いているファイルのフォルダの指示書が読み込まれる）。Esc 2回で巻き戻したら、その検証を `claude` の起動からやり直す（巻き戻すと、読み込み済みの記録も消える）。いずれも本体のコード（2.1.318）。
- 【環境】に足すこと: `/config` の Project instructions の値、`/permissions` に Read の拒否ルールがあるか、IDE につないでいるか。

### 検証1　app で起動すると、上のフォルダの分も含めて5つの指示書の言葉が、上から順にそろって答えられるか（C1〜C5）

- **記録の見出し**
  - 【1A】`/context all` の Memory files の表（そのまま貼る）
  - 【1B】「ファイルを読まずに、指示書の見出しの行（Contents of で始まる行）を上から順にそのまま書き写し、それぞれの言葉を添えて」と頼んだときの答え（そのまま貼る）
  - 【1C】起動したとき、指示書が止められた・読めなかったという行が出たか（出たらそのまま貼る）
  - 【1Z】手順以外に Claude が読んだファイル
- **用意するもの**: 上の表の `CLAUDE.md`、`CLAUDE.local.md`、`app/` の3つ
- **手順**: `cd app` → `claude`（Code タブでは `app` を選ぶ） → `/context all` → 見出しの行と言葉を聞く → `/exit`
- **予想**
  - 【1A】`CLAUDE.md` → `CLAUDE.local.md` → `app/CLAUDE.md` → `app/.claude/CLAUDE.md` → `app/CLAUDE.local.md` の順に5つ並ぶ（`app/` の中の3つの順は 2.1.318 の本体のコードから）。個人の `~/.claude/CLAUDE.md` や、このリポジトリより上のフォルダの CLAUDE.md があれば、それより前に並ぶ
  - 【1B】【1A】と同じ順で、やま → かわ → うみ → そら → もり
  - 【1C】出ない
- **外れたら何が分かるか**
  - 上の2つが無い: 上のフォルダは読み込まれない（C1 が違う）。ただし【1C】に行が出ていたら、会社の設定や Read の拒否ルールで止められた（`app` で起動すると、テーマのフォルダは作業フォルダの外になるため）
  - 言葉が1つしか出ない: 上書きされている（C2 が違う）
  - `app/` のものが先: 並びが逆（C3 が違う）
  - やま → うみ → そら → かわ → もり（CLAUDE.md の仲間を全部並べてから CLAUDE.local.md を並べる）: 並びはフォルダごとではなく種類ごと。C3 は合っていて、C4 の「同じフォルダの中で」の読み方が違う
  - `CLAUDE.local.md` が `CLAUDE.md` より先: C4 が違う。名前の順に並んでいるだけかもしれない
  - `app/.claude/CLAUDE.md` が無い: C5 が違う
  - 【1A】と【1B】で順が違う: 表の並びと、Claude に渡る並びが違う
- **紛れと潰し方**
  - Claude が README や指示書を Read で開いて答える → 「ファイルを読まずに」を付ける。【1Z】に書く
  - Claude が見出しの行のパスから並びを推し量って答える → 見出しの行をそのまま書き写させる。言葉に場所を表す語を入れない
  - auto memory に前の名残 → 準備と検証の始めに `/memory` で消す
  - 個人の `~/.claude/CLAUDE.md`、会社の指示書、このリポジトリより上のフォルダの CLAUDE.md が混ざる → 【1A】にそのまま出るので、それらを除いて判定する。【環境】にも書く
  - 個人の設定の `claudeMdExcludes` や「Project instructions」の設定で外される → 【環境】に記録する。表に出ないファイルがあったら補足で読み方を書く
  - 起動したフォルダが違う → `app` で起動する（この検証だけ、テーマのフォルダではなく `app` で起動する）。【1A】のパスで分かる
  - 許可の名残 → 準備で `ls ../../.claude`
- **人にしかできない操作**: `cd app`、`/context all`（2つ）
- **補足に書くこと**: 本体のコードでは、同じフォルダの `.claude/rules/` は `.claude/CLAUDE.md` と `CLAUDE.local.md` の間に入る。並びは優先の順ではない（C12）

### 検証2　テーマのフォルダで起動すると、サブフォルダの指示書の言葉は、Claude がそのフォルダのファイルを開くまで答えられないか（C7〜C11）

- **記録の見出し**
  - 【2A】起動直後に言葉を聞いたときの答え（そのまま貼る）
  - 【2B】Claude に `ls side` を実行させたあと、`Loaded` で始まる行が出たか、と、そのあと言葉を聞いたときの答え（そのまま貼る）
  - 【2C】Claude に `cat side/s.txt` を実行させたあとの、`Bash(` で始まる行と `Loaded` で始まる行（そのまま貼る）
  - 【2D】Claude に Read ツールで `sub/deep/c.txt` を読ませたあと、`Loaded` で始まる行（全部そのまま貼る）
  - 【2E】Claude に Read ツールで `sub/a.txt` を読ませたあと、`Loaded` で始まる行が出たか
  - 【2F】最後に言葉を聞いたときの答え（そのまま貼る）
  - 【2G】`/context all` の Memory files の表（そのまま貼る）
  - 【2Z】手順以外に Claude が読んだファイル（とくに、CLAUDE.md そのものを開いたか）
- **用意するもの**: 上の表の `side/`、`sub/`、`sub/deep/`
- **手順**: テーマのフォルダで `claude` → 言葉を聞く → Claude に「Bash で `ls side` を実行して、結果を見せるだけにして、ほかのファイルは開かないで」と頼む → 言葉を聞く → Claude に「Bash で `cat side/s.txt` を、記号を足さずにそのまま実行して」と頼む → Read で `sub/deep/c.txt` → Read で `sub/a.txt` → 言葉を聞く → `/context all` → `/exit`。`ls` と `cat` は、人が `!` を付けて打たず、Claude に頼む
- **予想**
  - 【2A】やま → かわ だけ（`app/`、`side/`、`sub/` のものは出ない）
  - 【2B】行は出ない。言葉もやま → かわ だけ（2.1.318 クラウドで、`ls` では読み込まれなかった）
  - 【2C】`Bash(cat side/s.txt)` と `Loaded side/CLAUDE.md`
  - 【2D】`Loaded sub/CLAUDE.md` と `Loaded sub/deep/CLAUDE.md` の2行（深いファイルを先に読むので、途中の `sub/` の分も一緒に読み込まれる。2.1.318 クラウドで試したときの結果）
  - 【2E】出ない（`sub/CLAUDE.md` は【2D】で読み込み済み。2.1.318 の本体のコードから）
  - 【2F】やま → かわ → にじ → ほし → つき
  - 【2G】`CLAUDE.md` と `CLAUDE.local.md` の2つだけ。サブフォルダのものは出ない
- **外れたら何が分かるか**
  - 【2A】にサブフォルダの言葉: 起動時に読み込まれている（C7 が違う）か、Claude が先にファイルを開いた（【2Z】を見る）
  - 【2B】に行が出る、または言葉が増える: `ls` も読むに数える
  - 【2C】に `Loaded` の行が出ない（ターミナル版で）: `cat` は読むに数えない（C8 が違う）。ただし `Bash(` の行に `|` や `>`、`cd` が入っていたら、手順どおりでない。【2Z】で `side/CLAUDE.md` を開いていたら、読み込み済みとして飛ばされた
  - 【2D】が `sub/deep/CLAUDE.md` の1行だけ: 途中のフォルダは読み込まれない（C10 が違う）
  - 【2E】に行が出る: 2回読み込まれる（C9 が違う）
  - 【2G】にサブフォルダのものが出る: C11 が違う
- **紛れと潰し方**
  - Claude が手順の前に `sub/` や `side/` のファイルを開く（Glob や ls で探す、など）→ 言葉を聞くときは「ファイルを読まずに」を付ける。【2Z】に書き、どの手順のあとか分かるようにする
  - `ls side` の結果に `CLAUDE.md` が見え、Claude がそれを開く → 開いたファイルは読み込み済みとして飛ばされ、【2C】で行が出なくなる。「ほかのファイルは開かないで」と頼み、【2Z】に書く
  - `cat` を Read ツールで読み替える、`|` や `2>/dev/null` を足す、`cd side && cat s.txt` にする → 記号を含むコマンドや、つないだコマンドは「読む」に数えられない（本体のコード、2.1.318）。「記号を足さずにそのまま」と頼み、`Bash(` の行を貼ってもらう
  - `Loaded` の行が折りたたまれて見えない、表示が違う、Code タブで出ない → 【2B】と【2E】の「出ない」は、【2C】か【2D】で行が見えた人の結果だけで判定する。言葉の答え（【2B】【2F】）でも確かめる
  - 言葉を聞いたとき、会話に出たファイル名から推測して答える → 言葉は指示書の中にしか無く、`.txt` の中身とも関係がない
  - IDE や `@` の経路、巻き戻し、auto memory、許可の名残、前の会話 → 共通の約束どおり
- **人にしかできない操作**: `/context all`（1つ）
- **補足に書くこと**: Write でもそのフォルダの CLAUDE.md が読み込まれた（2.1.318 クラウド）。サブフォルダの CLAUDE.local.md も同じように読み込まれた（C7）。必要になったときに読み込まれるものには文字数の上限がある（C13）。`/compact` のあとは、要約の前に読んだファイルが読み直されると、そのフォルダの CLAUDE.md も戻る（C16）

### 重さ

- 検証は2つ、ターミナル1つ、所要15〜20分ほど
- 試す人のリポジトリの状態を変えない（ファイルを作らない・書き換えない。Write は手順に入れない）
- スクリプトは使わない
