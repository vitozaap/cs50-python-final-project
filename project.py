import argparse
import sys
import os
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
    validate_path(args.input)
    validate_args(args)
    validate_media(args.input)
    command = create_ffmpeg_command(args.input, args.output, options=args.preset)
    compress(command)


def parse_args(argv=None):
    """Parses all CLI arguments.
       Required Arguments **(Positional)**:
        - `input`
       Optional Arguments **(Flagged)**:
        - `preset`
            **-p, --preset**
            default: **mid**
        - `output`
            **-o, --output**
            default: **{input}_compressed**


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
    parser.add_argument("input", help="file input path")
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


def validate_path(file):
    if not os.path.isfile(file):
        sys.exit(f'Invalid path: "{file}"')
    return True


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
        sys.exit(f'"{args.preset}" is not a valid preset option: {tuple(PRESETS)}')
    else:
        args.preset = args.preset.lower()

    if args.output is None:
        args.output = f"{input_name}_compressed{input_ext}"
    else:
        _, output_ext = os.path.splitext(args.output)

        if output_ext not in EXTENSIONS and output_ext != "":
            sys.exit(f'"{args.output}" has no valid extension: {sorted(EXTENSIONS)}')
        elif output_ext == "":
            args.output = f"{input_name}_compressed{input_ext}"

    return True


if __name__ == "__main__":
    main()
