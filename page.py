# structure for a musical page of 

from collections import defaultdict
from typing import List, Dict
import numpy as np

class ScorePages():
    # class mapping to a score page of different instruments
    # suppose we have a mapping of instruments to index, like {"erhu": [1], "piano": [0,2], ...}
    def __init__(self, instrument_index_dict: Dict[str, List[int]]):
        self.instrument_index_dict = instrument_index_dict
        self.pages = defaultdict(list)
        self.page_height = 0 # TODO: set the page height using a config

    def add_page(self, page: list):
        # page is a list of pixel matrices
        for k, v in self.instrument_index_dict.items():
            pic = np.concatenate([page[i] for i in v], axis=1)
            self.pages[k].append(pic)

    def _concatenate_part(self, part: List[np.ndarray]) -> np.ndarray:
        result_list = []
        pic = np.empty((0, part[0].shape[1]))
        for p in part:
            

    def export(self):
        for k,v 
        