from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class GameType(Enum):
    F1 = "四般南喰赤"
    F2 = "四般南喰赤祝"
    F3 = "四般南喰"
    F4 = "四般南"
    F5 = "四般東喰赤"
    F6 = "四般東喰赤祝"
    T1 = "三般南喰赤"
    T2 = "三般南喰赤祝"
    T3 = "三般東喰赤"
    T4 = "三般東喰赤祝"

    def __eq__(self, other):
        """
        >>> GameType.F4 == "四般南"
        True
        >>> GameType.F4 == GameType.F3
        False
        """
        if isinstance(other, str):
            return self.value == other
        else:
            return super().__eq__(other)


class Score(BaseModel):
    name: str
    point: float


class ShugiScore(Score):
    shugi: int


class Game(BaseModel):
    started_at: datetime
    type: str
    room: str
    scores: Optional[List[Score]]
    shugi_scores: Optional[List[ShugiScore]]


class Games(BaseModel):
    games: List[Game]
