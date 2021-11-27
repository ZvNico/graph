from enum import Enum


class RankComputeMode(Enum):
    starting_node_elimination = 1
    count_parent_without_rank = 2
    recursive = 3


