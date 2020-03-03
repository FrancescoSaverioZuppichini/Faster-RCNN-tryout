import pytube
import numpy as np
import cv2
from torch.utils.data import Dataset
from pathlib import Path
from logger import logging
import matplotlib.pyplot as plt
import tqdm

plt.ion()  # enables interactive mode


class VideoDataset(Dataset):
    """
    This class represents a Video dataset. A video is composed by frames, a series of images. Basically, 
    this is just a long list of tensors in which we can apply a transformation. It also provide 
    two useful methods to decompose video form youtube and from a video file.
    """

    def __init__(self, frames: list, transform=None, return_input=False):
        self.frames = frames
        self.transform = transform
        self.return_input = return_input

    def __getitem__(self, idx):
        x = self.frames[idx]
        if self.transform is not None:
            x = self.transform(x)
        if self.return_input:
            return x, self.frames[idx]
        return x

    def __len__(self):
        return len(self.frames)

    @classmethod
    def from_yt(csl, video_url: str, out_dir: Path, force: bool = False, *args, **kwargs):
        """
        Uses `pytube` to download a video from youtube using `video_url` and stores in `out_dir`. 
        The output filepath is computed using the video title.
        
        :param csl: [description]
        :type csl: [VideoDataset]
        :param video_url: video url
        :type video_url: str
        :param out_dir: directory in which the video will be stored
        :type out_dir: Path
        :param force: If True, it will override the existing video, if any, defaults to False.
        :type force: bool, optional
        :return: A new instance of VideoDataset
        :rtype: [VideoDataset]
        """

        youtube = pytube.YouTube(video_url)
        video = youtube.streams.first()
        file_path = out_dir / (video.title + '.mp4')
        if file_path.exists() and not force:
            logging.info(
                f'File already exist at {file_path}, skipping downloading.')
        else:
            logging.info(f'Downloading video from {video_url}.')
            video.download(out_dir)
        logging.info(f'Saved at {file_path}.')
        return csl.from_file(file_path, out_dir,  *args, **kwargs)

    @classmethod
    def from_root(cls, root: Path, *args, **kwargs):
        img_paths = root.glob('*.jpg')
        frames = [cv2.imread(str(path)) for path in img_paths]
        return cls(frames, *args, **kwargs)

    @classmethod
    def from_file(cls, video_path: Path, out_dir: Path, *args, **kwargs):
        """
        Open a video file and store each frame individually.
        
        :param video_path: [description]
        :type video_path: Path
        :param out_dir: [description]
        :type out_dir: Path
        :return: [description]
        :rtype: [type]
        """
        out_dir = out_dir / 'frames'
        if not out_dir.exists(): out_dir.mkdir()
        cap = cv2.VideoCapture(str(video_path))
        i = 0
        bar = tqdm.tqdm()
        frames = []
        while (cap.isOpened()):
            ret, frame = cap.read()
            cv2.imwrite(f"{out_dir}/{i}.jpg", frame)
            i += 1
            bar.update()
            frames.append(frame)
            if not ret: break
        return cls(frames, *args, **kwargs)

