# configuration figure
```plantuml
@startuml
!define RECTANGLE class

RECTANGLE "ブラウザ" as Browser

package "Flaskアプリケーション" {
    RECTANGLE "app.py" as App {
        RECTANGLE "ルート処理" as Routes
        RECTANGLE "データベース操作" as DBOps
    }
    RECTANGLE "Response Model" as Model
}

database "SQLite\nDatabase" as DB

RECTANGLE "survey.html" as SurveyTemplate
RECTANGLE "thank_you.html" as ThankYouTemplate
RECTANGLE "admin.html" as AdminTemplate
RECTANGLE "admin_results.html" as ResultsTemplate

Browser --> App : HTTPリクエスト
App --> Browser : HTTPレスポンス

Routes --> SurveyTemplate : レンダリング
Routes --> ThankYouTemplate : レンダリング
Routes --> AdminTemplate : レンダリング
Routes --> ResultsTemplate : レンダリング

DBOps --> DB : CRUD操作
Model --> DB : マッピング

@enduml
```

# Flask Survey Application Structure

このドキュメントでは、Flask Survey Applicationの構造を説明します。

## 主要コンポーネント

1. **ブラウザ**
   - ユーザーインターフェース
   - HTTPリクエストの送信とレスポンスの受信

2. **Flaskアプリケーション (app.py)**
   - アプリケーションのコアロジック
   - 以下のサブコンポーネントを含む：
     a. **ルート処理**: HTTPリクエストのハンドリング
     b. **データベース操作**: データの保存と取得
     c. **Response Model**: データ構造の定義

3. **SQLiteデータベース**
   - アンケート回答の永続化ストレージ

4. **HTMLテンプレート**
   - `survey.html`: アンケートフォーム
   - `thank_you.html`: 回答完了後の感謝ページ
   - `admin.html`: 管理者ログインページ
   - `admin_results.html`: アンケート結果表示ページ

## データフロー

1. ユーザーがブラウザからアプリケーションにアクセス
2. Flaskアプリケーションが適切なルートを処理
3. 必要に応じてデータベース操作を実行
4. 適切なHTMLテンプレートをレンダリング
5. レンダリングされたHTMLをブラウザに返す

## 主要な機能

1. **アンケート回答**:
   - ユーザーが`survey.html`でアンケートに回答
   - 回答がデータベースに保存
   - `thank_you.html`でユーザーに感謝を表示

2. **管理者機能**:
   - 管理者が`admin.html`でログイン
   - `admin_results.html`で回答結果を閲覧

## セキュリティ

- 管理者ページはパスワードで保護
- セッション管理によるログイン状態の維持

