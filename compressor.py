import subprocess
import sys
import os
from rich.progress import Progress
import platform

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
        result = subprocess.run(cmd, capture_output=True, text=True)
        result.check_returncode()
        return float(result.stdout.strip())
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        sys.exit("ffprobe binaries not found.")


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

    # I want to capture progress from ffmpeg, so I need Popen to do not lock the thread and be able to run the process in background
    process = subprocess.Popen(
        cmd + ["-progress", "pipe:1", "-nostats", "-stats_period", "0.125"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,  # Dont want to show debug error from ffmpeg
        text=True,
    )
    with Progress(transient=True, refresh_per_second=20) as progress:
        progress_line = progress.add_task("[bold green]Compressing...", total=duration)
        for line in process.stdout:
            key, _, value = line.partition("=")
            seconds = parse_progress(key, value)
            if seconds is not None:
                progress.update(progress_line, completed=seconds)
        progress.update(progress_line, completed=duration)

    process.wait()
    if process.returncode != 0:
        sys.exit("An error ocurred during the compression.")


def parse_progress(key, value):
    if key == "out_time_us":
        try:
            return int(value) / 1_000_000
        except ValueError:
            return None
    return None


def open_folder(path):
    if platform.system() == "Windows":
        # Just making sure that is the absolute path
        abspath = os.path.abspath(path)
        # Call the specific explorer command (only work on windows) and use the /select to select the output file in the folder
        subprocess.run(["explorer", "/select,", abspath])
    else:
        # Search the internet about this, I didnt know that Windows and linux could have these differences here in python, cool!
        subprocess.run(["xdg-open", path])
