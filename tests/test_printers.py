import datetime
import json

import pytest

from tenhou_scores import models
from tenhou_scores.printers import OutputType


def test_json():
    result = OutputType.JSON(
        models.Games(
            games=[
                models.Game(
                    started_at=datetime.datetime(2021, 12, 31, 23, 59, 59),
                    type="ルール1",
                    room="L1000",
                    scores=[
                        models.Score(name="a", point=1),
                        models.Score(name="b", point=2),
                        models.Score(name="c", point=3),
                        models.Score(name="d", point=4),
                    ],
                ),
            ],
        ),
    )
    assert json.loads(result) == {
        "games": [
            {
                "started_at": "2021-12-31T23:59:59",
                "type": "ルール1",
                "room": "L1000",
                "scores": [
                    {"name": "a", "point": 1},
                    {"name": "b", "point": 2},
                    {"name": "c", "point": 3},
                    {"name": "d", "point": 4},
                ],
            }
        ]
    }


def test_csv():
    with pytest.raises(NotImplementedError):
        OutputType.CSV([])
