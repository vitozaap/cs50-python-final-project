import argparse
import sys
from rich.console import Console
from rich.prompt import Prompt
import os
import questionary
from compressor import (
    PRESETS,
    validate_media,
    compress,
    create_ffmpeg_command,
    EXTENSIONS,
)

PROG_NAME = "ffmpyg"
PROG_DESCRIPTION = "Video/Image compressor wrapping ffmpeg behind the scenes."
PROG_EPILOG = "CS50's final project created by @vitozaap."


def main():
    args = parse_args()
    run_interactive(args)
    validate_path(args.input)
    validate_args(args)
    validate_media(args.input)
    command = create_ffmpeg_command(args.input, args.output, options=args.preset)
    compress(command)


def parse_args(argv=None):
    """Parses all CLI arguments.
        Arguments **(Flagged)**:
        - `preset`
            **-p, --preset**
            default: **mid**
        - `output`
            **-o, --output**
            default: **{input}_compressed**
        `input`
            **-i, --input**


    :param argv: Unparsed arguments directly from `sys.argv`.
    :type argv: `list[str]`
    :returns: `True` if all arguments could be parse.
    :rtype: Boolean
    :raises: Will raise the default pretty error message from `argparse` if detected any invalid arguments.
    """
    parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description=PROG_DESCRIPTION,
        epilog=PROG_EPILOG,
    )
    parser.add_argument(
        "-i", "--input", help="file input path", required=False, default=""
    )
    parser.add_argument(
        "-o",
        "--output",
        help='file output path (Should contain the file name and extension). By default the input name suffixed with "compressed".',
        required=False,
    )
    parser.add_argument(
        "-p",
        "--preset",
        help="compression preset (high, mid, low) Higher values means smaller file sizes. Default: Mid",
        required=False,
        default="mid",
    )
    return parser.parse_args(argv)


def validate_path(file=""):
    return os.path.isfile(file)


def validate_args(args: argparse.Namespace):
    """Validate arguments passed through argparse.

    :param args: Parsed arguments.
    :type args: `argparse.Namespace`
    :returns: `True` if all arguments are valid and ready to be used.
    :rtype: Boolean
    :raises: Will raise `SystemExit` if detected any invalid arguments.
    """
    # Extracting file's names and extensions

    input_name, input_ext = os.path.splitext(args.input)

    if args.preset.lower() not in PRESETS.keys():
        return f'"{args.preset}" is not a valid preset option: {tuple(PRESETS)}'
    else:
        args.preset = args.preset.lower()

    if args.output is None:
        args.output = f"{input_name}_compressed{input_ext}"
    else:
        _, output_ext = os.path.splitext(args.output)

        if output_ext not in EXTENSIONS and output_ext != "":
            return f'"{args.output}" has no valid extension: {sorted(EXTENSIONS)}'
        elif output_ext == "":
            args.output = f"{input_name}_compressed{input_ext}"

    return True


def run_interactive(args=None):
    if args.input != "":
        return None
    console = Console()
    console.rule("[bold cyan]FFMPYG")
    custom = questionary.Style(
        [
            ("question", "fg:cyan bold"),
            ("selected", "fg:cyan bold"),
            ("pointer", "fg:cyan bold"),
            ("highlighted", "fg:cyan"),
        ]
    )
    args.input = questionary.path(
        "Enter file path",
        style=questionary.Style(custom),
        qmark="📁",
    ).ask()
    
    questionary.select(
        "Select the best compression preset",
        choices=[
            questionary.Choice(
                "high - Higher compression factor (Smaller size)", "high"
            ),
            questionary.Choice("mid - Balanced compression factor (Default)", "mid"),
            questionary.Choice(
                "low - Lower compression factor (Higher quality)", "low"
            ),
        ],
        default="mid",
        style=custom,
    ).ask()
    args.output = Prompt.ask(
        "[bold cyan]💾 Output path[/]",
        default="output.mp4",
    )
    console.print("[bold green]✅ Ready to go!")


if __name__ == "__main__":
    main()
