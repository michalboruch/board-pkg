'''
TODO:

* vim: pep, autocomplete

1. Create empty board at requested size         Done

2. Actors
2.0 Render board at initial stage               Done
2.1 Obstacle                                    
2.2 Pray                    
2.3 Predator

3. Setup agent and its target
3.1 Create interface to manage the agent
3.2 Record agent interactions

4. Render history, animation?
5. Return history, stats
'''
import math
import random
from abc import ABC
from enum import Enum
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np


class Actors(Enum):
    EMPTY = 0
    OBSTACLE = 1
    PRAY = 2
    PREDATOR = 3


class ActorBase(ABC):
    pass


class Obstacle(ActorBase):
    pass


class Pray(ActorBase):
    pass


class Predator(ActorBase):
    pass


class Board:
    def __init__(self, width: Optional[int] = 100, height: Optional[int] = 100) -> None:
        board = np.zeros(
            shape=(width, height),
            dtype=np.int8
        ) 
        board = self.set_actors(board)
        self.board = board

    @staticmethod
    def set_actors(
            b: np.array,
            obstacle_coverage_perc: Optional[int] = 15,
            pray_coverage_perc: Optional[int] = 10,
            predator_coverage_perc: Optional[int] = 5
    ) -> np.array:
        # TODO: find smarter way
        rows, cols = b.shape
        no_of_obstacles = math.floor(rows * cols * obstacle_coverage_perc / 100)
        no_of_prays = math.floor(rows * cols * pray_coverage_perc / 100)
        no_of_predators = math.floor(rows * cols * predator_coverage_perc / 100)

        def get_random_empty_spot() -> Tuple:
            def _get_random_empty_spot() -> Tuple:
                r = random.choice(range(rows))
                c = random.choice(range(cols))
                if b[r][c] != Actors.EMPTY.value:
                    _get_random_empty_spot()
                return r, c
            return _get_random_empty_spot()

        for i in range(no_of_obstacles):
            r, c = get_random_empty_spot()
            b[r][c] = Actors.OBSTACLE.value

        for i in range(no_of_prays):
            r, c = get_random_empty_spot()
            b[r][c] = Actors.PRAY.value

        for i in range(no_of_predators):
            r, c = get_random_empty_spot()
            b[r][c] = Actors.PREDATOR.value

        return b


    def render(self):
        # TODO: this should be closer to the actors
        pallete = np.array([
            [255, 255, 255],  # empty/path (white)
            [  0,   0,   0],  # obstacle (black)
            [  0, 255,   0],  # pray (green)
            [255,   0,   0]   # predator (red)
        ])
        rgb = pallete[self.board]  # broadcasting
        plt.imshow(rgb)
        plt.show()
