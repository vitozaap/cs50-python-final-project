import compressor
import subprocess
from pytest_mock import MockerFixture
import pytest


def test_validate_media(mocker: MockerFixture):
    mock_process = subprocess.CompletedProcess(returncode=0, stdout="", args="")
    mocker.patch("subprocess.run", return_value=mock_process)
    # Validate if a valid process response can pass without raising exceptions
    assert compressor.validate_media()

    # Validate if an exception is raised when the returncode is different from 0
    with pytest.raises(SystemExit):
        mock_process = subprocess.CompletedProcess(
            returncode=1, stdout=None, args="", stderr="err"
        )
        mocker.patch("subprocess.run", return_value=mock_process)
        assert compressor.validate_media()
