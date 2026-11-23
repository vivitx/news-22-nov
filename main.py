"""Copy the committed entry.png to the output directory.

The image was drawn in-session by draw.py (PIL) and committed as entry.png.
This program is stdlib-only: it copies that file, so both runs write the
same bytes. The output directory comes from MAKEFUN_OUTPUT_DIR, or /output.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
