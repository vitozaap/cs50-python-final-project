# FFMPYG
#### Video Demo: 
#### Description:
`ffmpyg` is a command-line tool that wraps `ffmpeg` to compress video files with minimal effort. `ffmpeg` is one of the most powerful media tools available, but its command-line interface is really hard for anyone who is not comfortable memorizing flags and codec options. `ffmpyg` hides that complexity behind three simple presets and a friendly
interface, so the user only needs to choose a file/video and how much they want to compress it. Behind the scenes, `ffmpyg` build and run the correct `ffmpeg` command.

`Ffmpyg` offers two ways to run. In **fast mode**, the user passes arguments directly on the command line, for example `python project.py -i video.mp4 -p high -o output.mp4`. This mode helps when you want to compress things faster, using the CLI arguments directly. In **interactive mode**, launched simply by running the program with no CLI arguments, `ffmpyg` starts a wizard created using both `rich` and `questionary` modules that asks for the input path (with tab auto-completion for the input path and real-time validation), the compression preset, the output path, and if they want to open the output folder when finished. Both modes builds the same `argparse` namespace and converge on the same flow, so there is no duplicated logic between them.

The process of compression itself is controlled by three presets (high, mid, and low) which holds different CRF (Constant Rate Factor) values passed to the `libx264` encoder. A higher CRF means more compression and a smaller file size, but costs a little bit of video quality, so the "high" preset compresses the most and "low" the least. I chose to always force `-c:v libx264` instead of letting the output container pick a default encoder, because CRF is understood by the codec, not the container: without forcing it, a format such as `.avi` would silently ignore CRF and fall back to a different quality setting. Forcing libx264 guarantees the presets behave consistently across mp4, mkv, mov, and avi.

While `ffmpeg` runs, `ffmpyg` reads its machine-readable progress output (`-progress pipe:1`) line by line and updates a live progress bar built with the `rich` library, so the user always knows the tool is working and roughly how long is left, instead of thinking the terminal just froze and the program crashed. To make this possible, a single `ffprobe` call both validates that the file is a real video supported by `ffmpeg` and returns its total duration, which the progress bar needs as its total duration param.

The project is separated into two main files to keep it testable. `project.py` holds the orchestration (validating, parsing user arguments, etc...), while `compressor.py` holds the "compression" layer that actually talks to the `ffmpeg` and `ffprobe` through subprocess (`run` and `Popen`). This separation means most of the logic can be tested with mocked subprocess calls, without needing FFmpeg installed.

## How to run
To run the `ffmpyg` you must install the ffmpeg binaries for your current machine, and if needed, add it to the `PATH` so the program can find it.
Don't forget to run `pip install -r requirements.txt` to install all modules needed.