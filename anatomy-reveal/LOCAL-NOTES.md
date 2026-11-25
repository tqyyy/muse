# Local notes (this machine)

- ImageMagick: only IM6 `convert` is installed (`/usr/bin/convert`), there is no IM7 `magick` binary. The skill's `template/motion/encode.mjs` reads the `MAGICK` env var and only uses it for `-evaluate-sequence mean` (frame averaging for motion blur), which IM6 `convert` supports identically. **Run the pipeline with `MAGICK=convert` in the environment.**
- Chrome for the render steps: `/opt/meta-chromium/chrome` (set `CHROME_PATH` if auto-detection fails).
- Node v24 and FFmpeg 8 are installed.
