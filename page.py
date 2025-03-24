# structure for a musical page of

from collections import defaultdict
from typing import List, Dict
import numpy as np
import os
from PIL import Image
import json


class ScorePages:
    # class mapping to a score page of different instruments
    # suppose we have a mapping of instruments to index, like {"erhu": [1], "piano": [0,2], ...}
    def __init__(self, score_images_dir: str, instrument_config: str):
        self.pages = defaultdict(list)
        self.page_height = 0  # TODO: set the page height
        # list all the images in the score_images_dir
        self.score_image_files = []
        for root, dirs, files in os.walk(score_images_dir):
            for file in files:
                self.score_image_files.append(os.path.join(root, file))
        self.score_image_files.sort()
        self.instrument_index_dict = defaultdict(list)
        with open(instrument_config, "r", encoding="utf-8") as f:
            self.instrument_config = json.load(f)
        for i, k in enumerate(self.instrument_config["instruments"]):
            self.instrument_index_dict[k].append(i)

        self.output_path = self.instrument_config["output_dir"]
        os.makedirs(self.output_path, exist_ok=True)
        self.title = self.instrument_config["title"]
        self.current_index = 0

    def set_page_height(self, height: int):
        self.page_height = height

    def slice_current_page(self, coords: List[float]):
        # coords is the proportion of the page height
        # slice the current page according to the coords
        # 1. input the current image
        pic = Image.open(self.score_image_files[self.current_index])
        # 2. convert to numpy array
        pic = np.array(pic)
        if self.page_height == 0:
            self.page_height = pic.shape[0]
        # 3. get the coordinates
        coords = [int(pic.shape[0] * c) for c in coords]
        # 4. slice the image
        pics = []
        for i in range(len(coords) - 1):
            pics.append(pic[coords[i] : coords[i + 1], :])
        self.add_page(pics)

    def add_page(self, page: list):
        # page is a list of pixel matrices
        for k, v in self.instrument_index_dict.items():
            pic = np.concatenate([page[i] for i in v], axis=1)
            self.pages[k].append(pic)

    def _concatenate_part(self, part: List[np.ndarray]) -> List[np.ndarray]:
        result_list: List[np.ndarray] = []
        pic = np.empty((0, part[0].shape[1], 3), dtype=np.uint8)
        for p in part:
            if pic.shape[0] + p.shape[0] > self.page_height:
                result_list.append(pic)
                pic = np.empty((0, part[0].shape[1], 3), dtype=np.uint8)
            pic = np.concatenate([pic, p], axis=0)
        if pic.shape[0] > 0:
            result_list.append(pic)
        # pad pic to standard height
        result_list[-1] = np.concatenate(
            [
                result_list[-1],
                np.ones(
                    (
                        self.page_height - result_list[-1].shape[0],
                        result_list[-1].shape[1],
                        3,
                    ),
                    dtype=np.uint8,
                )
                * 255,
            ],
            axis=0,
        )
        return result_list

    def export(self):
        return_dict = {}
        for k, v in self.pages.items():
            return_dict[k] = self._concatenate_part(v)
        for k, v in return_dict.items():
            os.makedirs(os.path.join(self.output_path, k), exist_ok=True)
            for i, pic in enumerate(v):
                # convert ndarray pic to image
                im = Image.fromarray(pic)
                im.save(os.path.join(self.output_path, k, f"{self.title}_{k}_{i}.png"))
        # copy anything left in self.image_file_list to another folder called "full"
        os.makedirs(os.path.join(self.output_path, "full"), exist_ok=True)
        for i, file in enumerate(self.score_image_files):
            # TODO: copy to
            # os.path.join(self.output_path, "full", f"{self.title}_{i}.png"))
            im = Image.open(file)
            im.save(os.path.join(self.output_path, "full", f"{self.title}_full_{i}.png"))
