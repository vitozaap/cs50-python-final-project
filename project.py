import argparse
import sys
import os

PROG_NAME = "ffmpyg"
PROG_DESCRIPTION = "Video/Image compressor wrapping ffmpeg behind the scenes."
PROG_EPILOG = "CS50's final project created by @vitozaap."
PRESETS = [
    {"name": "high", "crf": 30},
    {"name": "mid", "crf": 20},
    {"name": "low", "crf": 10},
]
EXTENSIONS = ["mp4", "avi", "mkv", "mov"]


def main():
    args = parse_args()
    validate_path(args.input)
    validate_args(args)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description=PROG_DESCRIPTION,
        epilog=PROG_EPILOG,
    )
    parser.add_argument("input", help="The file input path")
    parser.add_argument(
        "-e",
        "--extension",
        help="The file output extensions. By default the input extension.",
        required=False,
    )
    parser.add_argument(
        "-p",
        "--preset",
        help="The compression preset (high, mid, low) Higher values means smaller file sizes. Default: Mid",
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
    if args.preset.lower() not in [preset["name"] for preset in PRESETS]:
        sys.exit(f"{args.preset} is not a valid preset option: high, mid, low")

    if args.extension is not None and args.extension not in EXTENSIONS:
        sys.exit(f"{args.extension} is not a valid output format: mp4, mkv, mov, avi")

    return True


if __name__ == "__main__":
    main()
