import subprocess
import sys
import os

PRESETS = {"high": {"crf": 28}, "mid": {"crf": 23}, "low": {"crf": 18}}
EXTENSIONS = [".mp4", ".avi", ".mkv", ".mov"]


def probe_media(path="") -> float | None:
    # Will checks if the file is a supported media type
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        path,
    ]
    try:
        # Capturing output because if dont, will leak at the user's CLI (not pretty)
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        result.check_returncode()
        return float(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        sys.exit("ffprobe binaries not found")


def create_ffmpeg_command(media, output, options="mid") -> list:
    media, output = (os.path.normpath(media), os.path.normpath(output))
    cmd = [
        "ffmpeg",
        "-i",
        media,
        "-c:v",
        "libx264",
        "-crf",
        str(PRESETS[options]["crf"]),
        "-y",
        output,
    ]
    return cmd


def compress(cmd, duration):

    # I want to capture progress from ffmpeg, so I need Popen to do not lock the thread and be able to run process in background
    process = subprocess.Popen(
        cmd + ["-progress", "pipe:1", "-nostats"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )


def open_folder(path): ...
