引数として渡されたメモを作業ログに記録する。

## 手順

1. 以下の情報を特定する:
   - `PROJECT_SLUG`: transcript_path から導出（不明な場合は CWD から `echo "$PWD" | sed 's|/|-|g' | sed 's|^-||'` で生成）
   - `TODAY`: 今日の日付（UTC, `YYYY-MM-DD`）
   - `SESSION_ID`: 現在のセッションID（不明なら `unknown`）

2. 以下のコマンドでメモを JSONL ファイルに追記する:

   ```bash
   LOG_DIR="$HOME/.claude/logs/$PROJECT_SLUG"
   mkdir -p "$LOG_DIR"
   printf '{"type":"memo","timestamp":"%s","session_id":"%s","content":"%s"}\n' \
     "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$SESSION_ID" "$MEMO_CONTENT" \
     >> "$LOG_DIR/$TODAY-memo.jsonl"
   ```

   `$MEMO_CONTENT` は引数のテキスト。JSON 特殊文字（`"`, `\`, 改行）はエスケープすること。

3. 記録完了を簡潔に報告する（1行）。

## 使い方

```
/memo このアプローチは複雑すぎるので別の方法を検討する
/memo バグの原因は非同期処理のタイミング問題だった
/memo 明日Aさんに確認が必要
```
