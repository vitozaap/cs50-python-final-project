import subprocess
import sys

PRESETS = {"high": {"crf": 30}, "mid": {"crf": 20}, "low": {"crf": 10}}
EXTENSIONS = [".mp4", ".avi", ".mkv", ".mov"]




def validate_media(path=""):
    cmd = ["ffprobe", "-v", "error", "-show_format", path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        result.check_returncode()
        return True
    except subprocess.CalledProcessError as err:
        sys.exit(f"{err.stderr.replace('\n', '')}")
    except FileNotFoundError:
        sys.exit("FFMPEG binaries not found")


def compress_media(media, output, options=PRESETS["mid"]): 
    cmd = ["ffmpeg", "-i", media, "-o", output]


