import datetime

from tenhou_scores.models import Game

LINE_F1 = "L1002 | 00:44 | 四般南喰赤－ | しきさん(+61.0) NoName(0.0) あたまくん(-25.0) *芹澤六花*(-36.0)"
LINE_F2 = "C3630 | 23:25 | 四般南喰赤祝 | 残飯くん(+57.0,+2枚) Ryon(+20.0,+6枚) はるちゃんぱぱ(-24.0,-3枚) そこに北はある(-53.0,-5枚)"
LINE_F3 = "L4290 | 19:58 | 四般南喰－－ | 西田和子(+79.0) 滝口和江(-6.0) kigoron(-29.0) 冨澤研二(-44.0)"
LINE_F4 = "L1832 | 12:58 | 四般南－－－ | B-まこと(+59.0) m-ｈiroko(+11.0) o-きみよ(-29.0) o-けいこ(-41.0)"
LINE_F5 = "L1479 | 00:05 | 四般東喰赤－ | ぷぐすけ(+49.0) あおあ(+12.0) いぇい(-22.0) ジェイル02(-39.0)"
LINE_F6 = "C2570 | 21:50 | 四般東喰赤祝 | アイスティーあべ(+47.0,-2枚) SHOXXX(+9.0,-1枚) オカルトちゃん(-17.0,0枚) よろしくです(-39.0,+3枚)"
LINE_T1 = "L1045 | 00:02 | 三般南喰赤－ | ごつごつ(+75.0) RaFaFa(-13.0) はらこはらこ(-62.0)"
LINE_T2 = "C2661 | 02:17 | 三般南喰赤祝 | ブシトリル(+40.0,+1枚) いちろ(+6.0,-2枚) あさやま(-46.0,+1枚)"
LINE_T3 = "L1150 | 12:11 | 三般東喰赤－ | かーおー(+42.0) のぐのぐ(-8.0) いだうこ(-34.0)"
LINE_T4 = "C1993 | 21:09 | 三般東喰赤祝 | よもやリーチだ(+76.0,+14枚) たままに(-13.0,-4枚) Yamaken(-63.0,-10枚)"


def test_game_from_row_f1():
    game = Game.from_row(LINE_F1, datetime.datetime(2021, 12, 31))
    assert game.dict() == {
        "room": "L1002",
        "type": "四般南喰赤",
        "scores": [
            {"name": "しきさん", "point": 61.0},
            {"name": "NoName", "point": 0.0},
            {"name": "あたまくん", "point": -25.0},
            {"name": "*芹澤六花*", "point": -36.0},
        ],
        "shugi_scores": None,
        "started_at": datetime.datetime(2021, 12, 31, 0, 44),
    }


def test_game_from_row_f2():
    game = Game.from_row(LINE_F2, datetime.datetime(2021, 12, 31))
    assert game.dict() == {
        "room": "C3630",
        "scores": None,
        "shugi_scores": [
            {"name": "残飯くん", "point": 57.0, "shugi": 2},
            {"name": "Ryon", "point": 20.0, "shugi": 6},
            {"name": "はるちゃんぱぱ", "point": -24.0, "shugi": -3},
            {"name": "そこに北はある", "point": -53.0, "shugi": -5},
        ],
        "started_at": datetime.datetime(2021, 12, 31, 23, 25),
        "type": "四般南喰赤祝",
    }
