import subprocess, os
from config import SMALL_GENERATOR, SMALL_MARKS_DIR, SMALL_MARKS_EXTENSION


def generate_small_mark(id):
    mark_dir = os.path.join(SMALL_MARKS_DIR, str(id))
    mark_file = os.path.join(mark_dir, str(id) + SMALL_MARKS_EXTENSION)
    if os.path.isfile(mark_file):
        return mark_file
    if not os.path.isdir(mark_dir):
        os.mkdir(mark_dir)
    subprocess.call(['java', '-jar', SMALL_GENERATOR, 'generate', str(id), mark_file])
    return mark_file
