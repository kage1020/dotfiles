# GUI Settings

自動化できないため手動で設定する項目。

## システム設定

- ディスプレイ
    - 輝度を自動調節：OFF
    - 輝度：50%
- キーボード
    - 環境光が暗い場合にキーボードの輝度を調整：OFF
    - キーボードの輝度：50%

## AzooKey

- 「設定」＞「テキスト入力」＞「入力ソース」＞「編集」＞「＋」＞「azooKey（日本語）」
- 「設定」＞「テキスト入力」＞「入力ソース」＞「編集」＞「＋」＞「azooKey（英語）」

## Finder サイドバー

- 最近の項目：OFF
- AirDrop：OFF
- アプリケーション：OFF
- kage1020：ON
- iCloud Drive：OFF
- 共有：OFF
- 最近使ったタグ：OFF
- ゴミ箱の追加
    - Dock のゴミ箱を開き、「ファイル」＞「サイドバーに追加」

## Automator クリーン zip

1. Automator を開き、「新規書類」＞「クイックアクション」＞「ユーティリティ」＞「シェルスクリプトを実行」をダブルクリック
2. 設定を以下に変更
    - ワークフローが受け取る現在の項目：「ファイルまたはフォルダ」
    - 検索対象：Finder.app
    - 入力の引き渡し方法：引数として

    ```bash
    first="$1"
    dir="$(dirname "$first")"
    cd "$dir" || exit 1
    zipname="$(basename "$first").zip"
    if [ -e "$zipname" ]; then
      zipname="$(basename "$first")_$(date +%Y%m%d_%H%M%S).zip"
    fi
    items=()
    for f in "$@"; do
      items+=("$(basename "$f")")
    done
    zip -r "$zipname" "${items[@]}" -x "*.DS_Store"
    ```

3. 「zip」という名前で保存
4. 圧縮したいフォルダで「クイックアクション」＞「zip」を選択

## Safari

- 表示
    - サイドバーを表示
    - お気に入りバーを表示

## Google Chrome

- 表示
    - ブックマークバーを常に表示：ON
- 拡張機能
    - [Bitwarden](https://chromewebstore.google.com/detail/bitwarden-password-manage/nngceckbapebfimnlniiiahkandclblb)
        - フォームフィールドに自動入力の候補を表示する：OFF
    - [DeepL](https://chromewebstore.google.com/detail/deepl%EF%BC%9Aai%E7%BF%BB%E8%A8%B3%E3%81%A8%E6%96%87%E7%AB%A0%E4%BD%9C%E6%88%90%E3%83%84%E3%83%BC%E3%83%AB/cofdbpoegempjloogbagkncekinflcnj)
    - [Google Scholar PDF Reader](https://chromewebstore.google.com/detail/google-scholar-pdf-reader/dahenjhkoodjbpjheillcadbppiidmhp)
    - [Raindrop.io](https://chromewebstore.google.com/detail/raindropio/ldgfbffkinooeloadekpmfoklnobpien)
    - [User JavaScript and CSS](https://chromewebstore.google.com/detail/user-javascript-and-css/nbhcbdghjpllgmfilhnhkllmkecfmpld)
    - [Vercel](https://chromewebstore.google.com/detail/vercel/lahhiofdgnbcgmemekkmjnpifojdaelb)
    - [Wappalyzer](https://chromewebstore.google.com/detail/wappalyzer-technology-pro/gppongmhjkpfnbhagpmjfkannfbllamg)
    - [Keepa](https://chromewebstore.google.com/detail/keepa-amazon-price-tracke/neebplgakaahbhdphmkckjjcegoiijjo)
    - [Save Image As Type](https://chromewebstore.google.com/detail/save-image-as-type/gabfmnliflodkdafenbcpjdlppllnemd)
    - [Raycast Companion](https://chromewebstore.google.com/detail/raycast-companion/fgacdjnoljjfikkadhogeofgjoglooma)
- 設定
    - 検索エンジン＞サイト内検索
        - Perplexity: ショートカット `p`, URL `https://www.perplexity.ai/search/new?q=%s`
        - Gmail: ショートカット `gmail`, URL `https://mail.google.com/mail/u/0/#inbox`
        - Google Map: ショートカット `gmap`, URL `https://www.google.com/maps`
        - Google Drive: ショートカット `gdrive`, URL `https://drive.google.com/drive/u/0/home`

## Raycast

- Settings
    - General
        - Raycast Hotkey: Cmd+Space
        - Show Raycast in menu bar: OFF
    - Extensions
        - Next Display: Cmd+Shift+Right
        - Previous Display: Cmd+Shift+Left
        - Translate into Japanese: Cmd+Cmd+T
        - Paste as Plain Text: Opt+Cmd+V
- Extensions をインストール
    - [Paste as Plain Text](https://www.raycast.com/koinzhang/paste-as-plain-text)
    - [Cheatsheets Remastered](https://www.raycast.com/smcnab1/cheatsheets-remastered)

## Notion

- 設定
    - メニューバーに Notion を表示する：OFF

## Obsidian

1. リポジトリ `obsidian-private` を clone
2. 「Open Folder as Vault」で vault を作成
3. `.gitignore` に `.obsidian` を追加してコミット
- オプション
    - エディタ
        - デフォルト編集モード：ソースモード
    - ホットキー
        - 下の行と入れ替える：Opt+Down
        - 上の行と入れ替える：Opt+Up
- コミュニティプラグイン
    - [Git](obsidian://show-plugin?id=obsidian-git)
        - Auto commit-and-sync interval: 60 min
        - Auto commit-and-sync after stopping file edits: ON
        - Auto pull interval: 60 min
        - Pull on startup: ON
        - Author name: kage1020
        - Author email: 4624528@ed.tus.ac.jp
    - [Marp](obsidian://show-plugin?id=marp)
        - Theme Folder Location: `.marp`
    - [Obsidian GitHub Copilot](obsidian://show-plugin?id=github-copilot)

## LINE

- 設定
    - トーク
        - 送信方法：Command + Enter

## Zed

Zed で再現できない VS Code 設定:

- ミニマップ（機能なし）
- コピー時シンタックスハイライト無効化（`editor.copyWithSyntaxHighlighting: false` 相当の設定なし）
- Unicode ハイライト許可文字（機能なし）
- ファイルネスティング（`explorer.fileNesting` 相当の機能なし）
- タブのカスタムラベル（`workbench.editor.customLabels` 相当の機能なし）
- Jupyter ノートブック（未サポート）
- Git Graph / Draw.io / Marp / Hex Editor（同等拡張なし）
- Code Spell Checker（同等拡張なし、typos-lsp で部分代替可能）
- Gitmoji / ECDC / Word Counter（同等拡張なし）

## 手動 DMG インストール

- Comet: `/Users/kage1020/Documents/comet_latest.dmg`
- Atlas: `/Users/kage1020/Documents/ChatGPT_Atlas.dmg`
- Nani!?: `/Users/kage1020/Documents/nani-mac-latest.dmg`
