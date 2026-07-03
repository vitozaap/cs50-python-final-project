import subprocess
from pytest_mock import MockerFixture
import pytest
from compressor import PRESETS, validate_media, create_ffmpeg_command

def test_validate_media(mocker: MockerFixture):
    mock_process = subprocess.CompletedProcess(returncode=0, stdout="", args="")
    mocker.patch("subprocess.run", return_value=mock_process)
    # Validate if a valid process response can pass without raising exceptions
    assert validate_media()

    # Validate if an exception is raised when the returncode is different from 0
    with pytest.raises(SystemExit):
        mock_process = subprocess.CompletedProcess(
            returncode=1, stdout=None, args="", stderr="err"
        )
        mocker.patch("subprocess.run", return_value=mock_process)
        assert validate_media()


def test_create_ffmpeg_command():
    inp = "./file.mp4"
    out = "folder///file.mp4"
    res = [
        "ffmpeg",
        "-i",
        "file.mp4",
        "-c:v",
        "libx264",
        "-crf",
        str(PRESETS["high"]["crf"]),
        "-y",
        r"folder\file.mp4",
    ]
    # Validates if the input and output are being normalized and if the preset param is being used
    assert create_ffmpeg_command(inp, out, "high") == res
    # res[6]: after "-crf" before "-y" = str(PRESETS["high"]["crf"])
    res[6] = str(PRESETS["mid"]["crf"])
    # Validates if the default preset is being used
    assert create_ffmpeg_command(inp, out) == res


def test_compress(): ...


def test_open_folder(): ...
