from dataclasses import dataclass
from pathlib import Path

@dataclass
class Project:
    """
    This class represents our project. It stores useful information about the structure, e.g. paths.
    """
    base_dir: Path = Path(__file__).parents[0]
    data_dir = base_dir / 'dataset'
    checkpoint_dir = base_dir / 'checkpoint'
    video_dir = data_dir / 'video'
    yoda_dataset = data_dir / 'yoda'

    def __post_init__(self):
        # create the directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.checkpoint_dir.mkdir(exist_ok=True)
        self.video_dir.mkdir(exist_ok=True)
        self.yoda_dataset = self.yoda_dataset.mkdir(exist_ok=True)