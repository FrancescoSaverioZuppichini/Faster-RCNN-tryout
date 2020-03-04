from Project import Project
import shutil

EXT = 'jpg'

pr = Project()
in_dir = pr.data_dir / 'video' / 'frames'
out_dir = pr.data_dir / 'yoda'

annotations_paths = out_dir.glob('*.txt')
ids = [p.name.split('.')[0] for p in annotations_paths]

for i in ids:
    shutil.copy(f'{in_dir}/{i}.{EXT}', f'{out_dir}/{i}.{EXT}')