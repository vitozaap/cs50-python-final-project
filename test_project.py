import pytest
import argparse
from project import parse_args, validate_args, PRESETS, validate_path, main
from pytest_mock import MockerFixture


def test_parse_args():
    # validate if raises an exception when missing arguments
    with pytest.raises(SystemExit):
        parse_args([])


def test_main(mocker: MockerFixture):
    mock_args = argparse.Namespace(input="file", preset="mid", extension="mp4")

    # Mocking functions
    mock_validate_path = mocker.patch("project.validate_path", return_value=True)
    mock_parse_args = mocker.patch("project.parse_args", return_value=mock_args)
    mock_validate_args = mocker.patch("project.validate_args", return_value=True)
    
    main()
    
    # validate if main is calling the functions correctly
    mock_parse_args.assert_called_once()
    mock_validate_path.assert_called_once_with(mock_parse_args.return_value.input)
    mock_validate_args.assert_called_once_with(mock_parse_args.return_value)


def test_validate_path(tmp_path):
    # Mocking temp file
    file = tmp_path / "test.txt"
    file.write_text("Valid temporary file", encoding="utf-8")
    assert validate_path(file)
    # validate if an invalid path raises an exception
    with pytest.raises(SystemExit):
        validate_path("invalid_path")


def test_validate_output(mocker: MockerFixture, tmp_path):
    file = tmp_path / "test.mp4"
    file.write_text("Valid temporary file", encoding="utf-8")
    # mocking arguments
    mock_args = argparse.Namespace(input=file, preset="mid", extension="mp4")
    # validate if validate_args pass
    assert validate_args(mock_args)
    # validate if an invalid extension raises an exception
    with pytest.raises(SystemExit):
        mock_args.extension = "invalid"
        validate_args(mock_args)


def test_validate_args_valid_file(mocker: MockerFixture, tmp_path):
    file = tmp_path / "test.mp4"
    file.write_text("Valid temporary file", encoding="utf-8")
    # mocking arguments
    mock_args = argparse.Namespace(input=file, preset="mid", extension="mp4")
    # validates if a valid file can pass
    assert validate_args(mock_args)


def test_validate_args_presets(mocker: MockerFixture, tmp_path):
    file = tmp_path / "test.mp4"
    file.write_text("Valid temporary file", encoding="utf-8")

    # Checks if all valid presets passes
    for preset in PRESETS:
        mock_args_presets = argparse.Namespace(
            input=file, preset=preset["name"], extension="mp4"
        )
        assert validate_args(mock_args_presets)

    # Checks if an invalid preset is caught
    with pytest.raises(SystemExit):
        mock_args_presets.preset = "invalid"
        validate_args(mock_args_presets)
