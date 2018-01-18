import os, json, subprocess

from config import SMALL_MARKS_DIR, MARKS_DATA_FILE, SMALL_GENERATOR, SMALL_MARKS_EXTENSION

def add_small_mark(id, title, img, video, site):
    mark_dir = os.path.join(SMALL_MARKS_DIR, id)
    data = {}
    data['name'] = title
    data['res'] = video
    data['img'] = img
    data['site'] = site
    mark_data_file = os.path.join(mark_dir, MARKS_DATA_FILE)
    file = open(mark_data_file, 'w')
    file.write( json.dumps(data) )
    file.close()

def generate_small_mark(id):
    mark_dir = os.path.join(SMALL_MARKS_DIR, str(id))
    mark_file = os.path.join(mark_dir, str(id) + SMALL_MARKS_EXTENSION)
    if os.path.isfile(mark_file):
        return mark_file
    if not os.path.isdir(mark_dir):
        os.mkdir(mark_dir)
    subprocess.call(['java', '-jar', SMALL_GENERATOR, 'generate', str(id), mark_file])
    return mark_file
