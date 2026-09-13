---
title_ja: pstack完全ガイド 第1部
description: Lauren Tan（@poteto）The Complete Guide to pstack Pt.1 の非公式日本語訳。検証スキルが土台である理由を説明する。
eyebrow: 完全ガイド 非公式日本語訳
subtitle: Verification is all you need
fetched_on: 2026-09-13
published_at: 2026-08-31
source_url: https://x.com/poteto/status/2094457600259842065
status_id: "2094457600259842065"
---

このページは、Lauren Tan（@poteto）が X に公開した記事「The Complete Guide to pstack Pt. 1」の非公式日本語訳です。このリポジトリ独自の実践入門ではありません。原文は [https://x.com/poteto/status/2094457600259842065](https://x.com/poteto/status/2094457600259842065) です。取得日は 2026-09-13 です。

この連載では、厳密なエンジニアリング作業のために私が使っている個人のスキル集、pstack の使い方を説明します。これによって、月に 2,000 本の PR を高い確信を持って本番へ出せるようになりました。

私はもともと、自分がどれだけの行数や PR を入れたかを重視してきませんでした。エージェント以前は、誰も気にしていませんでした。それは妥当です。生の生産性は、品質やユーザーに見える成果と一致するとは限らなかったからです。単なる見栄えの指標でした。

しかし pstack を作る過程で、量は重要だとわかりました。特に、エージェントでプロダクトの品質を維持し、さらに上げられるときはそうです。たとえば私は約 2 か月前、まだ初期でコードベースが新しく、伸び始めたころに Grok @Bot の作業を始めました。チームは増え、いまでは 1 日に数百本の PR が Grok @Bot のコードベースに入ります。それでも pstack のおかげで、コードを監視し、リファクタし、新しい lint とチェックを足し、機能も作りながら、全員のために品質を高く保てています。

Grok @Bot の庭師であり保守者でいられたのは、pstack があったからです。プロトタイプを作ったあとの勢いは強く、多くの人がチームに加わっていました。作られ、拡張され続けている最中に、停止時間なしでコードベース全体を強い土台へリファクタする、決定的な機会がありました。エンジニアの人数に関係なく、そして何より非エンジニアが貢献しても、品質が保てるコードベースです。この仕事は、Grok Bot が作られている最中に土台をリファクタし、改善し続ける必要があります。土台が貢献の数に追いつけるときだけ、それができます。

証拠は Grok @Bot そのものです。これから数週間で、pstack を使って高品質なアプリを作り、保守するために必要なことをすべて話します。

## 第1部 検証こそすべて

道具箱の中でいちばん重要なスキルは、高品質な検証スキルです。このスキルは持っておき、保守する価値がそれほど高いので、私は「ただのスキル」ではなく重要インフラだと思っています。よい検証スキルは、非エンジニアを含むチーム全体の成果を増幅します。うまくやれば、チーム全体の成果は 100 倍から 1000 倍になります。

用語に馴染みがないなら、verification とは、エージェントが自分の作業を自分で確かめられることです。あなたがボトルネックにならずにループを閉じられるので、タスクが成功するまで進み続けられます。Cursor 向けに最初の検証スキルを作った経緯を知りたい人は、以前の投稿 Loops You Can Trust を見てください。

## 検証スキルを一緒に作る

まず pstack を入れ、`/create-verification-skill` を実行します。高品質なボット作りを助ける私のボット、Dr Eggbot もロスターに入れることを勧めます。Dr Eggbot は pstack に同梱されます。コーディングボットに使い方を教え、同じ厳密さで非コーディングボットも作れます。

Dr Eggbot にエンジニアボットを作らせ、そのボットに `/create-verification-skill` を実行させ、`/maintain-verification-skill` を毎日走らせるルーティンを組ませることもできます。

それが走っているあいだに、このスキルが何をするか、どうやって高品質な検証スキルを作るかを説明します。

私は、Grok @Bot と Cursor を作るときに使う検証スキルをすべて蒸留して、一種のメタスキルにしました。自分のアプリ向けに高品質な検証スキルを作る方法を、エージェントに教えます。

ここで技術スタックの選択が重要になります。たとえば Electron や Web のアプリなら、JS 生態系の豊富なデバッグ道具を使えます。Chrome DevTools Protocol（CDP）なら、ブラウザの開発者ツールと同じ道具が使えます。iOS アプリならシミュレータを使います。

理想は、手で開発するときと同じように、アプリを操作し、デバッグし、perf トレースを取り、その他のデバッグと開発の道具を使えることです。使える豊かなランタイムがなければ、エージェントに道具を作らせる必要があります。lldb を使う、開発環境で sidecar として動く独自パッケージを使う、などです。手元にあるものを使うだけでも構いません。

エージェントによる検証は、それほど重要だと私は思っています。冗談抜きで、自分で豊かなデバッグ道具を作ること、あるいは技術スタック自体を変えることまで勧めます。ソフトウェア開発で不当に有利になり、極端な生産性を得るためです。先に書いたとおり、エージェントが自分の作業を確かめられるようにすると、組織の誰もが貢献でき、自分の変更が本当に動くかを確認できます。デバッグしにくく、制御しにくい技術スタックほど、エージェントを生産的に使うのが難しくなります。

## 再現可能にする

pstack には「Build the Lever」という原則があります。スキルを作る文脈では、エージェントには markdown だけではなく道具を渡す、という意味です。検証スキルでは、アプリの操作とデバッグをスクリプト化する、小さくてエージェント向きの CLI を作ります。何かをクリックするためだけの使い捨てスクリプトを書く代わりに CLI コマンドを実行するので、トークン消費が減り、検証スキルは再現しやすく、試しやすくなります。

Electron アプリ向けにエージェントが作るかもしれない、仮想の CLI の例です。

```
# health
node .cursor/skills/verify-atlas/control-atlas.mjs doctor

# open a blank thread and send
node .cursor/skills/verify-atlas/control-atlas.mjs new-session
node .cursor/skills/verify-atlas/control-atlas.mjs send "list open tasks in this project"

# keyboard path
node .cursor/skills/verify-atlas/control-atlas.mjs press "Meta+KeyN"

# accessibility snapshot of the live UI
node .cursor/skills/verify-atlas/control-atlas.mjs snapshot

# screenshot for evidence
node .cursor/skills/verify-atlas/control-atlas.mjs screenshot /tmp/atlas-proof.png

# wait for streaming / layout to settle
node .cursor/skills/verify-atlas/control-atlas.mjs wait-settle

# flip a feature flag for the session
node .cursor/skills/verify-atlas/control-atlas.mjs feature-flag rooms_v2 on
```

これで、どのエージェントもこの CLI を使ってアプリを素早く操作し、デバッグできます。アプリ開発の開発体験についても考え始めてください。

- 開発用データベースのシード
- 認証、テストユーザー、テストまたはステージング環境への API 呼び出しの扱い
- 開発環境を一貫したやり方で入れ、立ち上げること

手でコードを書いていたときにも、たぶん考えていたことです。エージェントがアプリで開発するための、主な道具だと思ってください。保守し、テストし続けてください。

ほかに検討したいコマンドの例です。

```
- **Inspection:** `info`, `snapshot`, `screenshot`, `components`
- **Navigation:** `home`, `new-session`, `select-project`, `select-runtime`, `scroll`
- **Interaction:** `send`, `click`, `click-xy`, `aria-click`, `type`, `press`, `eval`, `upload-image`, `add-context`, `feature-flag`
- **Performance:** `trace`, `profile`, `record`, `perf-metrics`, `wait-settle`
- **Streaming:** `console`, `network-log`, `network-summary`
- **Health & cleanup:** `doctor`, `cleanup`, `watch --restart`
```

この基本ができれば、エージェントはすでに大きく良くなっているはずです。アプリの中を歩き、楽にデバッグできるはずです。

もっと難しいことをする前に、この CLI を良くし、誤りをなくす時間を取ってください。エージェント向きの CLI を設計すること、あるいはエージェントに設計させることも考えてください。参照できる資料はネットにたくさんあります。私が好む性質は次です。

- API が合成しやすい。John Ousterhout の deep modules の考え方です
- 破壊的な副作用があり得るコマンドには `--dry-run` がある
- 機能を一度に全部出さず、サブコマンドで段階的に見せる
- エラーメッセージは非常に具体的で、代わりに何をすべきかを伝える
- `--help` が厚い
- 出力は機械可読（たとえば JSON）

## worktree ではなく Cloud Agents で並列化する

検証スキルでいくつか PR を入れられるようになると、もっと並列化できないかと考え始めるでしょう。エージェントがプロンプトを受けて、だいたいマージできる状態まで進められるなら、自分はもっと多くのエージェントを動かせるのではないか、ということです。

最初の直感は、worktree 対応を足すことです。git でリポジトリの追跡コピーを作り、メインのチェックアウトから隔離して変更できるようにします。理論上は、変更がぶつからずに複数エージェントを同時に動かせます。

私はこれを勧めません。一つには、マシンのディスクと資源を多く使います。リポジトリの大きさとマシンの性能次第で、worktree なら並列 10 エージェントくらいまでは行けるかもしれません。もっと良いやり方があります。

Cursor の cloud agents は、Cursor のインフラ上のクラウドで動くエージェントです。本物のコンピュータがあり、依存関係を入れ、アプリを起動し、動画とスクリーンショットを撮り、本物のユーザーと同じようにアプリを操作できます。前の段階で開発体験を十分良くしていれば、cloud agents のセットアップは大きな追加作業にはなりません。クラウド環境を最初に組むとき、セットアップと動作確認を助けるエージェントが送られます。最初のビルドのあとスナップショットを取るので、その後の cloud agent 実行はすぐ始まります。

cloud agents のセットアップに時間を使うことを強く勧めます。並列化の生産性が大きく上がります。後の投稿で、クラウドで数百のサブエージェントを並列に動かす方法を見せます。いまは環境を整え、エージェントをすべてクラウドで動かしても大丈夫だと思える状態にしてください。

## Feature Map でエージェントを賢く保つ

アプリが複雑になると、エージェントは機能を見つけ、操作するための案内がもっと必要になります。そのために私が考えたのが Feature Map です。名前のとおり、アプリにある機能、それが何をするか、ユーザー視点でそこにどう行くかの、検索しやすい地図です。

架空のアプリ Atlas 向けに用意した Feature Map の例があります。検証スキルの `SKILL.md` から言及される、いくつかの markdown ファイルです。

置き場所は自由です。`/create-verification-skill` では、`references/features` ディレクトリと `README.md` を自動で作ります。readme が地図そのものです。主要な機能の概要と、詳細へのリンクです。機能の例は次のような形です。

```
# Preferences

Full-screen preferences overlay and its tab set.

## Sub-features

- settings-overlay: full-screen overlay opened from the gear or Cmd/Ctrl+,
- settings-nav: left nav of tabs (General, Appearance, Models, Plan & Usage, ...).
- settings-search: in-overlay search (Cmd/Ctrl+K while settings is open).
- theme-picker: quick theme control on Appearance.

## How to get to it (user POV)

Click the gear next to the account avatar, or press Cmd/Ctrl+,. Pick a tab from the left nav. Type in the preferences search box to jump. Escape or the close control dismisses.

## Driving it with control-atlas

bash
node .cursor/skills/verify-atlas/control-atlas.mjs press "Meta+Comma"
node .cursor/skills/verify-atlas/control-atlas.mjs snapshot
node .cursor/skills/verify-atlas/control-atlas.mjs press "Escape"

- Overlay root: look for a dialog/region named Preferences in the a11y tree.
- Tabs: click by visible name. Plan & Usage may be absent for some account states.
- While settings is open, Cmd/Ctrl+K is preferences search, not the global palette (see `multi-surface-journeys.md`).

## Gotchas

- Closing settings mid-suite can leave focus nowhere useful. `new-session` or `home` recovers.
- Some tabs are entitlement-gated. Skip with an explicit account reason.
```

自分で書く必要はありません。`/create-verification-skill` を走らせると、エージェントがアプリを見てカタログし、これらの参照を作ります。

Feature Map と CLI の組み合わせが、pstack の検証スキルが強い主因の一つです。エージェントはすべての機能と行き方の文脈を持ち、コンテキストウィンドウの貴重なトークンを節約し、それが何のためで、どう行くかを正確に教わります。

Feature Map は「実体化した記憶」だと考えてください。エージェントを長く使っている人なら、記憶という概念は知っているでしょう。ふつうは単純な markdown（Obsidian の保管庫など）か、ベクトルデータベースのような、もう少し複雑なものです。私は、コードベースこそ最終的な記憶だと思っています。コードは、あなたとチームがした判断の投影であり、何が起き、実際にどう動くかの正本です。Feature Map は、それをトークン節約向けに圧縮した形です。スキル内の markdown なので、コードベースに貢献する全員がこの共有記憶の恩恵を受けます。

だから検証スキルの保守は本当に重要です。エージェントがアプリ操作の最新詳細を常に持つよう、`/maintain-verification-skill` は少なくとも 1 日 1 回走らせてください。検証スキルを使うほど、作業中にエージェントが自分で更新することもあります。取りこぼしは `/maintain-verification-skill` が拾います。

## 検証スキルの使い方

参照用に、架空アプリ向けの検証スキルの例があります。https://github.com/poteto/verification-skill-example 。繰り返しですが、基本の CLI と Feature Map 付きで作るには `/create-verification-skill` を実行します。

pstack と一緒に使うときの、私のやり方です。

まず、プロンプトを `/poteto-mode` で始めます。Cursor で pstack を使っているなら、`/poteto-mode` の補完で Enter だけではなく Opt + Enter を押せます。スキルが Custom Mode として足され、固定されるので、新しいターンごとにスキルを使うようエージェントへリマインドされます。

Grok @Bot では、プラグインを入れたあと `/poteto-mode` と入力します。

### 例: 新機能を作る

新機能を作るときは、検証スキルを `/poteto-mode` と一緒に使い、エージェントに作業を確かめさせます。たとえば次のように頼むことがあります。

```
/poteto-mode build <description of feature, any useful context>. use /control-app to verify your changes and show me a video and screenshots as proof
```

`/control-app` は `/create-verification-skill` の結果です。Grok @Bot では、次のように頼むことがあります。

```
spawn a cloud agent to use /poteto-mode to build <description of feature, any useful context>. use /control-app to verify your changes and show me a video and screenshots as proof
```

小さな違いは、Grok @Bot ではボット自身に作業させず、cloud agent を spawn させることです。ボットを他のことに空け、コンテキストウィンドウをきれいに保つためです。その意味で、私はボットを、cloud agents を管理し監督するコーディネータだと思っています。Cloud agents なら、Cursor で使えるモデル一式を、それぞれ別マシンで使えます。ボットのコンピュータは他のことに空きます。

### 例: パフォーマンス改善

```
spawn a cloud agent to use /poteto-mode to improve the initial loading time of our app. first use /control-app to take a trace of the status quo, and identify opportunities for improvement. then do a targeted fix and use /control-app + a /swarm to confirm the win
```

`/swarm` は、検証スキルと組み合わせる最良のスキルの一つです。任意の数の cloud agents を広げて検証スキルを走らせます。十分な標本数で perf の改善を確認する、アプリを fuzz して壊していないことや回帰がないことを確かめる、といったことができます。

### 例: ユーザー報告を自動で再現する

検証スキルに満足したら、Grok @Bot の routines や Cursor Automations に入れられます。スケジュールで走らせたり、イベントで発火させたりできます。

たとえばユーザーフィードバックを Slack に流している、あるいは社内のフィードバックチャネルがあるなら、すべての報告をボットに聞かせ、cloud agent で自動再現を試みさせられます。検証スキルと Feature Map が十分よければ、自動修正まで決めることもあるでしょう。

検証が道具箱でいちばん重要なスキルの一つだと言った理由が、ここにあります。新しいスキルとルーティンを載せる土台になります。そして何より、チームの全員が得をします。

## 検証スキルに投資する

検証スキルを作ったら、`/maintain-verification-skill` で鋭く保ってください。CLI を改善し続け、重要インフラと同じようにこのスキルへ投資してください。オンコール当番を置きたくなるかもしれません。チームの生産性を 100 倍から 1000 倍にするには、それほど重要です。

このスキルは、この pstack ガイドでこれから扱う多くのスキルの土台であり、どれともきれいに合成されます。

- pstack: https://x.ai/bot/plugin/9717366 （GitHub へのリンクもあります）
- Dr Eggbot: https://x.ai/bot/93gOz3op1UQdBdbekQFLK

高品質なボット作りを助ける私のボット、Dr Eggbot をロスターに入れることを勧めます。Dr Eggbot は pstack に同梱されます。コーディングボットに使い方を教え、同じ厳密さで非コーディングボットも作れます。

Dr Eggbot にエンジニアボットを作らせ、そのボットに `/create-verification-skill` を実行させ、`/maintain-verification-skill` を毎日走らせるルーティンを組ませることもできます。

読んでくれてありがとう。第2部をお待ちください。
