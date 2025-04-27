# Transcriber Tool

音声ファイル（WAV, MP3など）をテキストに変換するPython製のCLIツールです。

## 特徴

- 複数の音声・動画形式に対応（MP3, MP4, WAV, MOV, AVI）
- [faster-whisper](https://github.com/guillaumekln/faster-whisper)を使用した高速な文字起こし
- 複数のモデルサイズに対応（tiny, base, small, medium, large）
- シンプルで使いやすいコマンドラインインターフェース

## インストール

### 前提条件

- Python 3.11以上
- [uv](https://github.com/astral-sh/uv)（Pythonパッケージマネージャー）

### インストール手順

```bash
# リポジトリをクローン
git clone https://github.com/karaage0703/transcriber_tool.git
cd transcriber_tool

# uvを使ってインストール
uv pip install -e .
```

または、直接インストールする場合：

```bash
uv pip install git+https://github.com/karaage070/transcriber_tool.git
```

## 使い方

### 基本的な使い方

```bash
# 基本的な文字起こし
transcriber_tool transcribe audio.mp3

# 出力先を指定
transcriber_tool transcribe audio.mp3 --output result.txt

# モデルサイズを指定
transcriber_tool transcribe audio.mp3 --model-size medium

# 出力ディレクトリを指定
transcriber_tool transcribe audio.mp3 --output-dir ./results
```

### コマンドラインオプション

```
transcribe [OPTIONS] FILE_PATH

  音声ファイルを文字起こしする

Options:
  -o, --output PATH         出力先のファイルパス（指定がない場合は自動生成）
  -m, --model-size [tiny|base|small|medium|large]
                            使用するモデルサイズ (デフォルト: base)
  -d, --output-dir PATH     出力ディレクトリ（指定がない場合はカレントディレクトリの下に
                            outputディレクトリを作成）
  --help                    ヘルプメッセージを表示
```

## モデルサイズと性能

| モデルサイズ | メモリ使用量 | 処理速度 | 精度 |
|------------|------------|---------|------|
| tiny       | 低         | 最速     | 低   |
| base       | 低         | 速い     | 中   |
| small      | 中         | 中       | 中   |
| medium     | 高         | 遅い     | 高   |
| large      | 最高       | 最遅     | 最高 |

## 開発

```bash
# 開発用インストール
uv pip install -e ".[dev]"

# テスト実行
pytest
```

## ライセンス

[MIT License](LICENSE)