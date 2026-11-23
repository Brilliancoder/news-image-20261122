"""news-image-20261122 entry: copies the pre-rendered entry.png (built by build.py) to /output/entry.png.

Standard library only. Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

out = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
out.mkdir(parents=True, exist_ok=True)
shutil.copyfile(Path(__file__).with_name('entry.png'), out / 'entry.png')
