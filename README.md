# Transcriber Tool

音声ファイル（WAV, MP3など）をテキストに変換するPython製のCLIツールです。

## 特徴

- 複数の音声・動画形式に対応（MP3, MP4, WAV, MOV, AVI）
- [faster-whisper](https://github.com/guillaumekln/faster-whisper)を使用した高速な文字起こし（CPU）
- [openai-whisper](https://github.com/openai/whisper)によるGPU文字起こしに対応
- 複数のモデルサイズに対応（tiny, base, small, medium, large）
- 複数の出力形式に対応（txt, srt, vtt, tsv）
- 言語指定オプション（`--language`）で誤検出を防止
- 進捗表示オプション（`--verbose`）で長時間処理の状況を確認
- シンプルで使いやすいコマンドラインインターフェース

## インストール

### 前提条件

- Python 3.11以上
- [uv](https://github.com/astral-sh/uv)（Pythonパッケージマネージャー）

### CPU版（デフォルト）

```bash
uv tool install transcriber_tool
```

### GPU版（NVIDIA GPU搭載マシン向け）

```bash
# x86_64
uv tool install "transcriber_tool[gpu]"

# ARM64（DGX Spark等）— PyTorchのcu130ビルドが必要
uv tool install "transcriber_tool[gpu]" --extra-index-url https://download.pytorch.org/whl/cu130
```

GPU版ではopenai-whisper + PyTorchバックエンドが使用されます。ctranslate2がCUDA対応の場合はfaster-whisperがGPUで動作します。

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

### 言語指定（推奨）

言語を明示的に指定することで、誤検出を防止できます。特に日本語音声では `--language ja` を推奨します。

```bash
# 日本語音声
transcriber_tool transcribe audio.mp3 --language ja

# 英語音声
transcriber_tool transcribe audio.mp3 --language en
```

> **注意**: 言語を指定しない場合、自動検出が行われますが、短い音声や特殊な音声では誤検出（例: ウェールズ語と判定）が発生し、処理がハングする場合があります。

### 進捗表示

`--verbose` オプションで、文字起こし中のセグメント単位の進捗を表示できます（openai-whisperバックエンド時）。

```bash
transcriber_tool transcribe audio.mp3 --verbose --language ja
```

### 出力形式

```bash
# SRT字幕形式
transcriber_tool transcribe audio.mp3 --format srt

# VTT字幕形式
transcriber_tool transcribe audio.mp3 --format vtt

# TSVタイムスタンプ分析用
transcriber_tool transcribe audio.mp3 --format tsv

# テキスト形式でタイムスタンプ付き
transcriber_tool transcribe audio.mp3 --timestamps
```

### デバイス指定

```bash
# 自動検出（デフォルト）
transcriber_tool transcribe audio.mp3 --device auto

# GPU強制
transcriber_tool transcribe audio.mp3 --device cuda

# CPU強制
transcriber_tool transcribe audio.mp3 --device cpu
```

### コマンドラインオプション

```
transcribe [OPTIONS] FILE_PATH

  音声ファイルを文字起こしする

Options:
  -o, --output PATH         出力先のファイルパス（指定がない場合は自動生成）
  -m, --model-size [tiny|base|small|medium|large]
                            使用するモデルサイズ (デフォルト: base)
  -d, --output-dir PATH     出力ディレクトリ
  --device [cpu|cuda|auto]  使用するデバイス (デフォルト: auto)
  -f, --format [txt|srt|vtt|tsv]
                            出力形式 (デフォルト: txt)
  -t, --timestamps          タイムスタンプを含める（txt形式の場合のみ）
  -v, --verbose             進捗ログを表示する
  -l, --language TEXT       言語コード（例: ja, en）。日本語は --language ja を推奨
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

## ライセンス

[MIT License](LICENSE)
