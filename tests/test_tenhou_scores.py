import gzip
from datetime import datetime

from freezegun import freeze_time

from tenhou_scores import tenhou_scores
from tenhou_scores import models


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


def test__log_content(mocker):
    res_mock = mocker.MagicMock(content=gzip.compress("a\r\nb".encode("utf8")))
    mocker.patch("requests.get", return_value=res_mock)

    content = tenhou_scores._log_content("")
    assert [s for s in content] == ["a", "b"]


def test_games(mocker):
    mocker.patch(
        "tenhou_scores.tenhou_scores._log_content",
        return_value=[
            "C3630 | 23:25 | 四般南喰赤祝 | 残飯くん(+57.0,+2枚) Ryon(+20.0,+6枚) はるちゃんぱぱ(-24.0,-3枚) そこに北はある(-53.0,-5枚)",
        ],
    )
    games = tenhou_scores.games(
        datetime(2022, 1, 1),
        0,
        models.GameType.F2,
        "C3630",
        ("はるちゃんぱぱ",),
    )

    assert games.dict() == {
    'games': [{'room': 'C3630',
            'scores': None,
            'shugi_scores': [{'name': '残飯くん', 'point': 57.0, 'shugi': 2},
                             {'name': 'Ryon', 'point': 20.0, 'shugi': 6},
                             {'name': 'はるちゃんぱぱ', 'point': -24.0, 'shugi': -3},
                             {'name': 'そこに北はある', 'point': -53.0, 'shugi': -5}],
            'started_at': datetime(2022, 1, 1, 23, 25),
            'type': '四般南喰赤祝'}]}

