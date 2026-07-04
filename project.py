import argparse
import sys
from rich.console import Console
import os
import questionary
from compressor import (
    PRESETS,
    probe_media,
    compress,
    create_ffmpeg_command,
    EXTENSIONS,
    open_folder,
)

PROG_NAME = "ffmpyg"
PROG_DESCRIPTION = "Video compressor wrapping ffmpeg behind the scenes."
PROG_EPILOG = "CS50's final project created by @vitozaap."


def main():
    console = Console()
    args = parse_args()
    duration = None
    if use_interactive_mode():
        duration = interactive_mode(args)
    else:
        # Handling system exits here in main (way simple to test later)
        # Both functions also run inside interactive_mode() so I decided to dont run them again.
        if not validate_path(args.input):
            sys.exit("Error validating input file path.")
        duration = probe_media(args.input)
        if not duration:
            sys.exit("Check if you file is in a valid video format.")

    validated_args = validate_args(args)
    if type(validated_args) is not bool:
        sys.exit(validated_args)
    command = create_ffmpeg_command(args.input, args.output, options=args.preset)
    compress(command, duration)
    console.print(
        f'✅ [bold green]Your file is ready!\n🆕 Exported to: [/bold green][bold cyan]"{args.output}"'
    )
    if args.explorer:
        with console.status("[bold] Opening folder..."):
            open_folder(args.output)
            console.print("📂[bold green] Output folder opened in your file explorer.")
    console.rule(
        "[dim]made by [magenta]@vitozaap[/magenta] with [red]♥[/red] to CS50[/dim]"
    )


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
    :returns: `Namespace` if all arguments could be parse.
    :rtype: `Namespace`
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
        "-e",
        "--explorer",
        action="store_true",
        default=False,
        help="Open the output folder when finished. Default is false",
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
    args = parser.parse_args(argv)
    return args


def validate_path(file):
    return os.path.isfile(file)


def handle_output(args) -> None | str:
    input_name, input_ext = os.path.splitext(args.input)

    if args.output is None:
        args.output = f"{input_name}_compressed{input_ext}"
    else:
        output_name, output_ext = os.path.splitext(args.output)
        if output_ext not in EXTENSIONS and output_ext != "":
            return f'"{args.output}" has no valid extension: {sorted(EXTENSIONS)}'
        elif output_ext == "" and output_name == "":
            args.output = f"{input_name}_compressed{input_ext}"
        elif output_name != "" and output_ext == "":
            args.output = f"{output_name}{input_ext}"


def validate_args(args: argparse.Namespace) -> str | bool:
    """Validate arguments passed through argparse.

    :param args: Parsed arguments.
    :type args: `argparse.Namespace`
    :returns: `True` if all arguments are valid and ready to be used.
    :rtype: Boolean
    :raises: Will raise `SystemExit` if detected any invalid arguments.
    """
    if args.preset.lower() not in PRESETS.keys():
        return f'"{args.preset}" is not a valid preset option: {tuple(PRESETS)}'
    else:
        args.preset = args.preset.lower()

    output_validation = handle_output(args)
    if output_validation is not None:
        return output_validation
    
    # Because I used the flag -y in ffmpeg, I need to manually check if the output is different from input.
    # Could cause bugs, ffmpeg would write when still reading from file
    if os.path.normpath(args.input) == os.path.normpath(args.output):
        return f'input and output cannot have the exactly same path: "{args.input}"'
    
    return True


def interactive_mode(args=None) -> float:
    console = Console()
    console.rule("[bold cyan]FFMPYG")
    custom = questionary.Style(
        [
            ("question", "fg:cyan bold"),
            ("pointer", "fg:cyan bold"),
            ("highlighted", "fg:cyan bold"),
            ("instruction", "fg:gray italic"),
            ("completion-menu", "bg:black fg:white"),
            ("completion-menu.completion.current", "bg:cyan fg:#303030 bold"),
        ]
    )

    try:
        while True:
            path = questionary.path(
                "Enter file path (TAB to Auto-Complete):",
                style=custom,
                qmark="📁",
                validate=validate_path,
            ).unsafe_ask()
            duration = probe_media(path)
            if duration:
                args.input = path
                break
            console.print(
                f'[bold][dark_orange]"{path}"[/dark_orange] [red]is not a valid file to be compressed.[/red][/bold]'
            )

        args.preset = questionary.select(
            " Select the best compression preset",
            qmark="🪄",  # Remembers me from the OOP Class, defining a Wizard...
            choices=[
                questionary.Choice(
                    "high - Higher compression factor (Smaller size)", "high"
                ),
                questionary.Choice(
                    "mid - Balanced compression factor (Default)", "mid"
                ),
                questionary.Choice(
                    "low - Lower compression factor (Higher quality)", "low"
                ),
            ],
            style=custom,
        ).unsafe_ask()
        args.output = questionary.text(
            "Output path",
            qmark="💾",
            style=custom,
            instruction="(Empty = Same folder):",
        ).unsafe_ask()
        args.explorer = questionary.confirm(
            "Open compressed file folder when finished?",
            style=custom,
            default=False,
            qmark="📂",
        ).ask()
        return duration

    except KeyboardInterrupt:
        console.print("[bold red]Cancelling operation...")
        sys.exit(1)


def use_interactive_mode() -> bool:
    return len(sys.argv) <= 1


if __name__ == "__main__":
    main()
