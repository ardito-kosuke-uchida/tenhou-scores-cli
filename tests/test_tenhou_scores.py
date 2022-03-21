import gzip
from datetime import datetime
from http import HTTPStatus

import pytest
from freezegun import freeze_time

from tenhou_scores import exceptions, models, tenhou_scores


@freeze_time("2022-03-19 23:59:59")
def test__log_url_1():
    expected = "https://tenhou.net/sc/raw/dat/sca20220319.log.gz"
    assert tenhou_scores._log_url(datetime(2022, 3, 19)) == expected


@freeze_time("2022-03-19 23:59:59")
def test__log_url_2():
    expected = "https://tenhou.net/sc/raw/dat/sca20220311.log.gz"
    assert tenhou_scores._log_url(datetime(2022, 3, 11)) == expected


@freeze_time("2022-03-19 23:59:59")
def test__log_url_3():
    expected = "https://tenhou.net/sc/raw/dat/2022/sca20220310.log.gz"
    assert tenhou_scores._log_url(datetime(2022, 3, 10)) == expected


def test__log_content_1(mocker):
    res_mock = mocker.MagicMock(
        content=gzip.compress("a\r\nb".encode("utf8")),
        status_code=HTTPStatus.OK,
    )
    mocker.patch("requests.get", return_value=res_mock)

    content = tenhou_scores._log_content("")
    assert [s for s in content] == ["a", "b"]


def test__log_content_2(mocker):
    res_mock = mocker.MagicMock(status_code=HTTPStatus.NOT_FOUND)
    mocker.patch("requests.get", return_value=res_mock)
    with pytest.raises(StopIteration):
        next(tenhou_scores._log_content("", raises=False))


def test__log_content_3(mocker):
    res_mock = mocker.MagicMock(
        status_code=HTTPStatus.NOT_FOUND,
        side_effect=Exception,
    )
    mocker.patch("requests.get", return_value=res_mock)
    with pytest.raises(Exception):
        next(tenhou_scores._log_content("", raises=True))


def test_games(mocker):
    records = [
        # tommorow
        ["C3630 | 00:01 | 四般南喰赤祝 | A(+57.0,+2枚) B(+20.0,+6枚) C(-24.0,-3枚) D(-53.0,-5枚)"],
        # today
        ["C3630 | 23:25 | 四般南喰赤祝 | A(+57.0,+2枚) B(+20.0,+6枚) C(-24.0,-3枚) D(-53.0,-5枚)"],
    ]

    mocker.patch(
        "tenhou_scores.tenhou_scores._log_content",
        side_effect=lambda *args, **kwargs: records.pop(),
    )

    # jscpd:ignore-start
    expected = {
        "games": [
            {
                "room": "C3630",
                "scores": None,
                "shugi_scores": [
                    {"name": "A", "point": 57.0, "shugi": 2},
                    {"name": "B", "point": 20.0, "shugi": 6},
                    {"name": "C", "point": -24.0, "shugi": -3},
                    {"name": "D", "point": -53.0, "shugi": -5},
                ],
                "started_at": datetime(2022, 1, 1, 23, 25),
                "type": "四般南喰赤祝",
            },
            {
                "room": "C3630",
                "scores": None,
                "shugi_scores": [
                    {"name": "A", "point": 57.0, "shugi": 2},
                    {"name": "B", "point": 20.0, "shugi": 6},
                    {"name": "C", "point": -24.0, "shugi": -3},
                    {"name": "D", "point": -53.0, "shugi": -5},
                ],
                "started_at": datetime(2022, 1, 2, 0, 1),
                "type": "四般南喰赤祝",
            },
        ]
    }
    # jscpd:ignore-end

    assert tenhou_scores.games(datetime(2022, 1, 1), 1, models.GameType.F2, "C3630", ("A",)).dict() == expected


def test__game_from_content():
    with pytest.raises(exceptions.InvalidLineFormat):
        tenhou_scores._game_from_content("hoge", datetime(2022, 1, 1))


def test__game_from_content_2():
    row = "L1002 | 00:44 | 四般南喰赤－ | しきさん(+61.0) NoName(0.0) あたまくん(-25.0) *芹澤六花*(-36.0)"
    tenhou_scores._game_from_content(row, datetime(2022, 1, 1))


def test__score_from_content():
    row = "hoge"
    with pytest.raises(exceptions.InvalidLineFormat):
        tenhou_scores._score_from_content(row)


def test__shugiscore_from_content():
    row = "hoge"
    with pytest.raises(exceptions.InvalidLineFormat):
        tenhou_scores._shugiscore_from_content(row)


def test__condition():
    condition = tenhou_scores._condition(None, "L1002", "しきさん")
    condition(
        models.Game(
            type="hoge",
            room="L1002",
            scores=[],
            started_at=datetime(2022, 1, 1),
        ),
    )
