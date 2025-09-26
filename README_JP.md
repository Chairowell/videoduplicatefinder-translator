# Video Duplicate Finder 翻訳ツール

[Engliash](./README.md) | [中文](./README_CN.md) | [日本語](./README_JP.md)

これは、`0x90d/videoduplicatefinder` プロジェクトを翻訳するための **Python スクリプトツール**です。

## 自分の言語の翻訳版を作成する方法

> [!TIP]
> 以下に記載されている操作は、**このツールがあるリポジトリではなく、あなたの翻訳リポジトリ内**で行います。

### 1. オリジナルリポジトリをフォークする: `https://github.com/0x90d/videoduplicatefinder`

フォークする際に、リポジトリ名の末尾に**あなたの言語名**（例: `CN`、`JP`、`FR` など）を追加することをお勧めします。これにより、他のユーザーがあなたの翻訳版を識別しやすくなります。

### 2. ローカルにあなたの翻訳リポジトリをクローンし、ディレクトリに移動する

```bash
git clone https://github.com/<your-username>/videoduplicatefinder_<language>.git
cd videoduplicatefinder_<language>
```

### 3. この翻訳ツールをあなたの翻訳リポジトリにサブモジュールとして追加する

```bash
git submodule add https://github.com/Chairowell/videoduplicatefinder-translator.git Translator
```

この時点で、あなたの翻訳リポジトリ内に **`Translator`** という名前のディレクトリが表示されます。これがこの翻訳ツールのサブモジュールです。

### 4. 翻訳リポジトリでサブモジュールの参照情報をコミットする

```bash
git add .gitmodules Translator
git commit -m "Add Translator submodule"
git push
```