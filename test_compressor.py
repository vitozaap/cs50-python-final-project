import subprocess
from pytest_mock import MockerFixture
import pytest
from compressor import PRESETS, probe_media, create_ffmpeg_command, open_folder
import os


def test_probe_media(mocker: MockerFixture):
    mock_process = subprocess.CompletedProcess(returncode=0, stdout="1", args="")
    mocker.patch("subprocess.run", return_value=mock_process)
    # Validate if a valid process response can pass without raising exceptions
    assert probe_media() == 1.0

    # Validate if an exception is raised when the returncode is different from 0
    mock_process = subprocess.CompletedProcess(
        returncode=1, stdout=None, args="", stderr="err"
    )
    mocker.patch("subprocess.run", return_value=mock_process)
    assert probe_media() is None


def test_probe_media_missing_ffprobe(mocker: MockerFixture):
    mocker.patch("subprocess.run", side_effect=FileNotFoundError)
    with pytest.raises(SystemExit):
        probe_media()


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
        os.path.normpath("folder/file.mp4"),
    ]
    # Validates if the input and output are being normalized and if the preset param is being used
    assert create_ffmpeg_command(inp, out, "high") == res
    # res[6]: after "-crf" before "-y" = str(PRESETS["high"]["crf"])
    res[6] = str(PRESETS["mid"]["crf"])
    # Validates if the default preset is being used
    assert create_ffmpeg_command(inp, out) == res


def test_open_folder_windows(mocker: MockerFixture):
    path = "input.mp4"
    mock_platform = mocker.patch("platform.system", return_value="Windows")
    mock_subprocess = mocker.patch("subprocess.run")
    mock_abspath = mocker.patch("os.path.abspath", return_value=f"C://Users/{path}")
    open_folder(path)
    mock_platform.assert_called_once()
    mock_abspath.assert_called_once_with(path)
    mock_subprocess.assert_called_once_with(
        ["explorer", "/select,", mock_abspath.return_value]
    )


def test_open_folder_linux(mocker: MockerFixture):
    path = "input.mp4"
    mock_platform = mocker.patch("platform.system", return_value="Linux")
    mock_subprocess = mocker.patch("subprocess.run")
    open_folder(path)
    mock_platform.assert_called_once()
    mock_subprocess.assert_called_once_with(["xdg-open", path])
