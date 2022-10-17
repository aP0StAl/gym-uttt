from dataclasses import dataclass
from typing import Optional


@dataclass
class Action:
    row: int
    col: int
    player: Optional[int]
