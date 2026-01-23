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
uv tool install transcriber_tool
```

もしくは以下のようにuvxコマンドを使えばそのまま実行可能

```bash
uvx transcriber_tool
or
uv tool run transcriber_tool
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

### タイムスタンプ付き出力

```bash
# タイムスタンプ付きテキスト
transcriber_tool transcribe audio.mp3 --timestamps

# TSV形式（タイムスタンプ分析用）
transcriber_tool transcribe audio.mp3 --format tsv

# SRT字幕形式
transcriber_tool transcribe audio.mp3 --format srt

# VTT字幕形式
transcriber_tool transcribe audio.mp3 --format vtt
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
  -f, --format [txt|srt|vtt|tsv]
                            出力形式 (デフォルト: txt)
  -t, --timestamps          タイムスタンプを含める（txt形式の場合のみ有効）
  --device [cpu|cuda|auto]  使用するデバイス (デフォルト: cpu)
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

## 開発者向け

### PyPIへの公開

新しいバージョンをリリースする際は、以下の手順で公開します。

1. `pyproject.toml` のバージョンを更新
2. ビルドして公開

```bash
# ビルド
uv build

# PyPIに公開（トークンが必要）
uv publish --token <YOUR_PYPI_TOKEN>
```

### uvxで最新バージョンを使う

既にインストール済みの環境で最新バージョンを使うには：

```bash
# 方法1: ツールを再インストール
uv tool install transcriber_tool --force

# 方法2: @latestを指定して実行
uvx transcriber_tool@latest --version
```

## ライセンス

[MIT License](LICENSE)
