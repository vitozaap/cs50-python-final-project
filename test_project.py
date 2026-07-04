import argparse
from project import (
    parse_args,
    validate_args,
    PRESETS,
    validate_path,
    main,
    EXTENSIONS,
)
from pytest_mock import MockerFixture



def test_parse_args():
    # Testing parsing defaults
    args = parse_args([])
    assert args.input == "" and args.preset == "mid" and args.output is None


def test_main_fast_mode(mocker: MockerFixture):
    mock_args = argparse.Namespace(input="file", preset="mid", output="mp4")

    # Mocking functions
    mock_validate_path = mocker.patch("project.validate_path", return_value=True)
    mock_parse_args = mocker.patch("project.parse_args", return_value=mock_args)
    mock_validate_args = mocker.patch("project.validate_args", return_value=True)
    mock_validate_media = mocker.patch("project.validate_media", return_value=True)
    mock_interactive_mode = mocker.patch("project.interactive_mode", return_value=None)
    mocker.patch("project.use_interactive_mode", return_value=False)
    mocker.patch("project.create_ffmpeg_command")
    mocker.patch("project.compress")

    main()

    # validate if main is calling the functions correctly
    mock_parse_args.assert_called_once()
    mock_interactive_mode.assert_not_called()
    mock_validate_media.assert_called_once_with(mock_parse_args.return_value.input)
    mock_validate_path.assert_called_once_with(mock_parse_args.return_value.input)
    mock_validate_args.assert_called_once_with(mock_parse_args.return_value)


def test_main_interactive_mode(mocker: MockerFixture):
    mock_args = argparse.Namespace(input="", preset="mid", output=None)

    # Mocking functions
    mock_validate_path = mocker.patch("project.validate_path")
    mock_parse_args = mocker.patch("project.parse_args", return_value=mock_args)
    mock_validate_args = mocker.patch("project.validate_args", return_value=True)
    mock_validate_media = mocker.patch("project.validate_media")
    mock_interactive_mode = mocker.patch("project.interactive_mode", return_value=None)
    mocker.patch("project.use_interactive_mode", return_value=True)
    mocker.patch("project.create_ffmpeg_command")
    mocker.patch("project.compress")

    main()

    # validate if main is calling the functions correctly
    mock_parse_args.assert_called_once()
    mock_interactive_mode.assert_called_once()
    mock_validate_media.assert_not_called()
    mock_validate_path.assert_not_called()
    mock_validate_args.assert_called_once_with(mock_parse_args.return_value)


def test_validate_path(tmp_path):
    # Mocking temp file
    file = tmp_path / "test.txt"
    file.write_text("Valid temporary file", encoding="utf-8")
    assert validate_path(file)
    assert validate_path("invalid") is False


def test_validate_output(tmp_path):
    file = tmp_path / "test.mp4"
    file.write_text("Valid temporary file", encoding="utf-8")
    # mocking arguments
    mock_args = argparse.Namespace(input=file, preset="mid", output="file.mp4")
    # validate if validate_args pass
    assert validate_args(mock_args)
    # validate if an invalid output raises an exception

    mock_args.output = "invalid.mp5"
    assert (
        validate_args(mock_args)
        == f'"invalid.mp5" has no valid extension: {sorted(EXTENSIONS)}'
    )


def test_validate_args_valid_file(tmp_path):
    file = tmp_path / "test.mp4"
    file.write_text("Valid temporary file", encoding="utf-8")
    # mocking arguments
    mock_args = argparse.Namespace(input=file, preset="mid", output="file.mp4")
    # validates if a valid file can pass
    assert validate_args(mock_args)


def test_validate_args_presets(tmp_path):
    file = tmp_path / "test.mp4"
    file.write_text("Valid temporary file", encoding="utf-8")

    # Checks if all valid presets passes
    for preset in PRESETS:
        mock_args_presets = argparse.Namespace(
            input=file, preset=preset, output="file.mp4"
        )
        assert validate_args(mock_args_presets)

    # Checks if an invalid preset returns an error message
    mock_args_presets.preset = "invalid"
    assert (
        validate_args(mock_args_presets)
        == f'"invalid" is not a valid preset option: {tuple(PRESETS)}'
    )
