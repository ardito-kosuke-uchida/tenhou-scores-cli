import re
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from .config import config


class GameType(str, Enum):

    """四般南喰赤"""
    F1 = "F1"

    """四般南喰赤祝"""
    F2 = "F2"

    """四般南喰"""
    F3 = "F3"

    """四般南"""
    F4 = "F4"

    """四般東喰赤"""
    F5 = "F5"

    """四般東喰赤祝"""
    F6 = "F6"

    """三般南喰赤"""
    T1 = "T1"

    """三般南喰赤祝"""
    T2 = "T2"

    """三般東喰赤"""
    T3 = "T3"

    """三般東喰赤祝"""
    T4 = "T4"


line_member_pat = re.compile(config.LINE_MEMBER_PAT)


class Score(BaseModel):
    name: str
    point: float

    @staticmethod
    def from_row(row):
        mem_res = re.match(line_member_pat, row)
        name, score = mem_res.group("name", "score")
        return Score(name=name, point=float(score))


line_shugi_pat = re.compile(config.LINE_SHUGI_PAT)


class ShugiScore(Score):
    shugi: int

    @staticmethod
    def from_row(row):
        mem_res = re.match(line_shugi_pat, row)
        name, score, shugi = mem_res.group("name", "score", "shugi")
        return ShugiScore(name=name, point=float(score), shugi=shugi)


line_pat = re.compile(config.LINE_PAT)


class Game(BaseModel):
    started_at: datetime
    type: str
    room: str
    scores: Optional[List[Score]]
    shugi_scores: Optional[List[ShugiScore]]

    @staticmethod
    def from_row(row: str, since: datetime):
        line_res = re.match(line_pat, row)

        room = line_res.group("room")
        game_type = line_res.group("type").replace("－", "")
        started_at = datetime.combine(
            since.date(),
            datetime.strptime(line_res.group("time"), "%H:%M").time(),
        )

        score_class = [Score, ShugiScore]["祝" in game_type]
        if "祝" in game_type:
            score_class = ShugiScore
            score_fieldname = "shugi_scores"
        else:
            score_class = Score
            score_fieldname = "scores"

        scores = [score_class.from_row(m) for m in line_res.group("members").split(" ")]
        return Game(
            room=room,
            type=game_type,
            started_at=started_at,
            **{score_fieldname: scores},
        )


class Games(BaseModel):
    games: List[Game]
