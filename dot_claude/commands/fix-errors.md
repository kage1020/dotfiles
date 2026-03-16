現在のプロジェクトのエラーを自動検出・修正する。

1. TypeScriptの型エラーを検出して修正する（`pnpm tsc --noEmit` または IDE診断を使用）
2. テストの失敗を検出して修正する（`pnpm test` を実行）
3. Lintエラーを検出して修正する（`pnpm lint` を実行）
4. すべてのエラーが解消されるまで繰り返す
5. 最後に `pnpm build` で全体の整合性を確認する

注意:
- any型での回避は禁止
- biome-ignore / eslint-disable での回避は禁止
- it.skip / it.todo での回避は禁止
- 根本原因を特定して正しく修正すること
