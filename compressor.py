import subprocess
import sys
import os

PRESETS = {"high": {"crf": 28}, "mid": {"crf": 23}, "low": {"crf": 18}}
EXTENSIONS = [".mp4", ".avi", ".mkv", ".mov"]


def validate_media(path=""):
    cmd = ["ffprobe", "-v", "error", path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        result.check_returncode()
        return True
    except subprocess.CalledProcessError as err:
        sys.exit(f"{err.stderr.replace('\n', '')}")
    except FileNotFoundError:
        sys.exit("ffprobe binaries not found")


def create_ffmpeg_command(media, output, options="mid"):
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

def compress(cmd):
    ...
