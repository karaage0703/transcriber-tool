"""
transcriber_tool CLI

音声ファイルをテキストに変換するCLIツール
"""

import os
import sys
import logging
import click
from typing import Optional, List, Tuple


def format_timestamp(seconds: float) -> str:
    """
    秒数をHH:MM:SS,mmm形式に変換する

    Args:
        seconds: 秒数

    Returns:
        フォーマットされたタイムスタンプ文字列
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{msecs:03d}"


def format_timestamp_simple(seconds: float) -> str:
    """
    秒数をMM:SS形式に変換する（短い音声用）

    Args:
        seconds: 秒数

    Returns:
        フォーマットされたタイムスタンプ文字列
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("transcriber_tool")


class Transcriber:
    """
    faster-whisperを使用して音声・動画ファイルの文字起こしを行うクラス
    """

    def __init__(self, model_size: str = "base", output_dir: Optional[str] = None, device: str = "cpu"):
        """
        Transcriberのコンストラクタ

        Args:
            model_size: 使用するモデルサイズ ("tiny", "base", "small", "medium", "large")
            output_dir: 文字起こし結果の出力ディレクトリ（指定がない場合は一時ディレクトリを使用）
            device: 使用するデバイス ("cpu", "cuda", "auto")
        """
        self.model = None
        self.model_size = model_size
        self.device = device
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir or os.path.join(os.getcwd(), "output")

        # 出力ディレクトリの作成
        os.makedirs(self.output_dir, exist_ok=True)

    def _load_model(self):
        """モデルを遅延ロードする"""
        if self.model is None:
            try:
                import faster_whisper

                self.logger.info(f"faster-whisperモデル '{self.model_size}' をデバイス '{self.device}' でロード中...")
                self.model = faster_whisper.WhisperModel(self.model_size, device=self.device)
                self.logger.info("モデルのロードが完了しました")
            except ImportError:
                self.logger.error("faster-whisperがインストールされていません")
                raise ImportError(
                    "faster-whisperがインストールされていません。'pip install faster-whisper'を実行してください。"
                )

    def _validate_file(self, file_path: str) -> bool:
        """
        ファイルの形式を検証する

        Args:
            file_path: 検証対象のファイルパス

        Returns:
            ファイルが有効な場合はTrue、そうでない場合はFalse
        """
        valid_extensions = [".mp3", ".mp4", ".wav", ".mov", ".avi"]
        file_ext = os.path.splitext(file_path)[1].lower()

        # ファイルの存在確認
        if not os.path.exists(file_path):
            self.logger.error(f"ファイル '{file_path}' が存在しません")
            return False

        # 拡張子の確認
        if file_ext not in valid_extensions:
            self.logger.error(f"ファイル形式 '{file_ext}' はサポートされていません")
            return False

        return True

    def transcribe(
        self,
        file_path: str,
        output_path: Optional[str] = None,
        output_format: str = "txt",
        timestamps: bool = False,
    ) -> str:
        """
        音声・動画ファイルを文字起こしし、結果をファイルに保存する

        Args:
            file_path: 文字起こし対象のファイルパス
            output_path: 出力先のファイルパス（指定がない場合は自動生成）
            output_format: 出力形式 ("txt", "srt", "vtt", "tsv")
            timestamps: タイムスタンプを含めるか（txt形式の場合のみ有効）

        Returns:
            文字起こし結果のファイルパス
        """
        # ファイルの検証
        if not self._validate_file(file_path):
            raise ValueError(f"無効なファイル: {file_path}")

        # モデルのロード
        self._load_model()

        self.logger.info(f"ファイル '{file_path}' の文字起こしを開始します")

        try:
            # faster-whisperでの文字起こし処理
            segments, info = self.model.transcribe(file_path)

            # セグメントをリストに変換（ジェネレータは一度しか使えないため）
            segment_list = list(segments)

            # 出力形式に応じて結果を生成
            if output_format == "srt":
                transcript = self._format_srt(segment_list)
                ext = ".srt"
            elif output_format == "vtt":
                transcript = self._format_vtt(segment_list)
                ext = ".vtt"
            elif output_format == "tsv":
                transcript = self._format_tsv(segment_list)
                ext = ".tsv"
            elif timestamps:
                transcript = self._format_timestamps(segment_list)
                ext = ".txt"
            else:
                transcript = " ".join([segment.text for segment in segment_list])
                ext = ".txt"

            self.logger.info(f"文字起こしが完了しました: {len(transcript)} 文字")

            # 出力ファイルパスの設定
            if output_path is None:
                # 出力ファイルパスの自動生成
                input_filename = os.path.basename(file_path)
                output_filename = f"{os.path.splitext(input_filename)[0]}_transcribed{ext}"
                output_path = os.path.join(self.output_dir, output_filename)
            else:
                # 出力ディレクトリの作成
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)

            # 結果をファイルに保存
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(transcript)

            self.logger.info(f"文字起こし結果を '{output_path}' に保存しました")

            return output_path

        except Exception as e:
            self.logger.error(f"文字起こし中にエラーが発生しました: {str(e)}")
            raise

    def _format_timestamps(self, segments: list) -> str:
        """タイムスタンプ付きテキスト形式でフォーマット"""
        lines = []
        for segment in segments:
            start = format_timestamp_simple(segment.start)
            lines.append(f"[{start}] {segment.text.strip()}")
        return "\n".join(lines)

    def _format_srt(self, segments: list) -> str:
        """SRT形式でフォーマット"""
        lines = []
        for i, segment in enumerate(segments, 1):
            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)
            lines.append(f"{i}")
            lines.append(f"{start} --> {end}".replace(",", ","))
            lines.append(segment.text.strip())
            lines.append("")
        return "\n".join(lines)

    def _format_vtt(self, segments: list) -> str:
        """VTT形式でフォーマット"""
        lines = ["WEBVTT", ""]
        for segment in segments:
            start = format_timestamp(segment.start).replace(",", ".")
            end = format_timestamp(segment.end).replace(",", ".")
            lines.append(f"{start} --> {end}")
            lines.append(segment.text.strip())
            lines.append("")
        return "\n".join(lines)

    def _format_tsv(self, segments: list) -> str:
        """TSV形式でフォーマット（タイムスタンプ分析用）"""
        lines = ["start\tend\ttext"]
        for segment in segments:
            start = format_timestamp_simple(segment.start)
            end = format_timestamp_simple(segment.end)
            text = segment.text.strip().replace("\t", " ")
            lines.append(f"{start}\t{end}\t{text}")
        return "\n".join(lines)


@click.group()
@click.version_option()
def cli():
    """音声ファイルをテキストに変換するCLIツール"""
    pass


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="出力先のファイルパス（指定がない場合は自動生成）")
@click.option(
    "--model-size",
    "-m",
    type=click.Choice(["tiny", "base", "small", "medium", "large"]),
    default="base",
    help="使用するモデルサイズ (デフォルト: base)",
)
@click.option(
    "--output-dir",
    "-d",
    type=click.Path(),
    help="出力ディレクトリ（指定がない場合はカレントディレクトリの下にoutputディレクトリを作成）",
)
@click.option(
    "--device",
    type=click.Choice(["cpu", "cuda", "auto"]),
    default="cpu",
    help="使用するデバイス (デフォルト: cpu)",
)
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["txt", "srt", "vtt", "tsv"]),
    default="txt",
    help="出力形式 (デフォルト: txt, srt/vttは字幕形式, tsvはタイムスタンプ分析用)",
)
@click.option(
    "--timestamps",
    "-t",
    is_flag=True,
    help="タイムスタンプを含める（txt形式の場合のみ有効）",
)
def transcribe(
    file_path: str,
    output: Optional[str],
    model_size: str,
    output_dir: Optional[str],
    device: str,
    output_format: str,
    timestamps: bool,
):
    """音声ファイルを文字起こしする"""
    try:
        transcriber = Transcriber(model_size=model_size, output_dir=output_dir, device=device)
        output_path = transcriber.transcribe(
            file_path,
            output,
            output_format=output_format,
            timestamps=timestamps,
        )
        click.echo(f"文字起こしが完了しました: {output_path}")
    except Exception as e:
        click.echo(f"エラー: {str(e)}", err=True)
        sys.exit(1)


def main():
    """CLIのエントリーポイント"""
    cli()


if __name__ == "__main__":
    main()
