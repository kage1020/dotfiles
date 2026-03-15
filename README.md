# dotfiles

chezmoi で管理する macOS dotfiles。仕事/個人環境をテンプレートで分岐。

## セットアップ

```bash
# 1コマンドで完了
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply kage1020

# ターミナル再起動
```

## 更新

```bash
chezmoi update
```

## 構成

| ファイル | 説明 |
|---|---|
| `Brewfile.tmpl` | Homebrew パッケージ（環境別分岐あり） |
| `run_once_before_*` | Homebrew インストール、パッケージインストール |
| `run_once_after_*` | macOS defaults 設定 |
| `dot_zshrc.tmpl` | Zsh 設定 |
| `dot_zshenv.tmpl` | 環境変数 |
| `dot_gitconfig.tmpl` | Git 設定（email は環境別） |
| `dot_config/` | Ghostty, Starship, mise 設定 |
| `dot_claude/` | Claude Code 設定（環境別分岐あり） |
| `dot_agents/` | Codex 設定（環境別分岐あり） |
| `dot_agent` | Antigravity 設定（環境別分岐あり） |
| `shell/` | エイリアス、関数 |
| `devcontainer/` | AI Agent 用 devcontainer テンプレート |

## プロジェクト分離（AI Agent 安全運用）

OrbStack + devcontainer でコンテナ内に隔離して開発する。

```bash
# 新プロジェクト作成（devcontainer付き、エディタで自動オープン）
mkpj my-app

# GitHub リポジトリをクローンして作成
mkpj https://github.com/user/repo

# ランタイムはプロジェクト内で設定
mise use node@22
```
