# What I want to do.
- 再現性が高い開発環境を作成する
  - VScodeの拡張機能、devcontainerを使う

- Pros
  - 同じ開発環境をすぐに提供できる
  - ツール・ライブラリのバージョンをプロジェクト毎に決められる
  - ホストの環境を汚さずにちょっとお試しができる
  - Dockerの設定によっては構築時の最新バージョンのツールを構築することもできる
- Cons
  - Docker Desktopの企業利用は有料になる場合がある
  - Dockerを動作させる為、それなりのPCスペックが必要
  - Dockerで管理できないツール(VSCodeを除くGUIツール)は対応不可
  - 構築するコンテナ環境によってはビルドが遅い
  - コンテナ環境の準備にはある程度の知識が必要

- Ref.
  - https://code.visualstudio.com/docs/devcontainers/containers
    - ![image](https://code.visualstudio.com/assets/docs/devcontainers/containers/architecture-containers.png)
  - https://zenn.dev/harurow/articles/c903de5f479a57#fnref-01a2-3
  - 