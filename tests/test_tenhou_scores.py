import gzip
from datetime import datetime

from freezegun import freeze_time

from tenhou_scores import tenhou_scores


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
    tenhou_scores.games
