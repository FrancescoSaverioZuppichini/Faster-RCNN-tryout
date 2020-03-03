import shutil
from data.VideoDataset import VideoDataset
from Project import Project
from tqdm.autonotebook import tqdm

pr = Project()
# ds = VideoDataset.from_yt('https://www.youtube.com/watch?v=mg4dhQJ6YQo', out_dir = pr.video_dir)

frames = (pr.video_dir / 'frames').glob('*')
to_dir = pr.video_dir / 'frames-light'
to_dir.mkdir(exist_ok = True)

SKIP = 15

for file in tqdm(list(frames)[::15]):
    shutil.copy(str(file), f'{to_dir}/{file.name}')


