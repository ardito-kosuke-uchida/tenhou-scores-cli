import gzip
import re
from datetime import datetime, timedelta
from http import HTTPStatus
from io import BytesIO
from typing import Iterator

import requests

from . import exceptions, models
from .config import config

line_member_pat = re.compile(config.LINE_MEMBER_PAT)
line_shugi_pat = re.compile(config.LINE_SHUGI_PAT)
line_pat = re.compile(config.LINE_PAT)


def _log_url(started_at: datetime, log_url: str = config.LOG_URL) -> str:
    if datetime.now().date() - timedelta(days=config.RECENT_DAYS) < started_at.date():
        return log_url.format(started_at.strftime("%Y%m%d"))
    else:
        return "/".join(
            sum(
                [
                    log_url.split("/")[:-1],
                    [str(started_at.year)],
                    [log_url.split("/")[-1]],
                ],
                [],
            )
        ).format(started_at.strftime("%Y%m%d"))


def _log_content(url: str, raises: bool = True) -> Iterator[str]:
    response = requests.get(url)
    if response.status_code != HTTPStatus.OK:
        if raises:
            response.raise_for_status()
        else:
            return

    with gzip.open(BytesIO(response.content), "rb") as gzip_file:
        content = gzip_file.read().decode("utf8")
        for line in content.strip().split("\r\n"):
            yield line


def _condition(game_type, room, members):
    def __condition(game):
        if game.scores is not None:
            game_members = [s.name for s in game.scores]
        else:
            game_members = [s.name for s in game.shugi_scores]

        conditions = [
            room == game.room,
            set(members) & set(game_members),
        ]

        if game_type is not None:
            conditions.append(game.type == game_type)

        return all(conditions)

    return __condition


def _score_from_content(row):
    mem_res = re.match(line_member_pat, row)
    if mem_res is None:
        raise exceptions.InvalidLineFormat(row)

    name, score = mem_res.group("name", "score")
    return models.Score(name=name, point=float(score))


def _shugiscore_from_content(row):
    mem_res = re.match(line_shugi_pat, row)
    if mem_res is None:
        raise exceptions.InvalidLineFormat(row)

    name, score, shugi = mem_res.group("name", "score", "shugi")
    return models.ShugiScore(name=name, point=float(score), shugi=int(shugi))


def _game_from_content(row: str, since: datetime):
    line_res = re.match(line_pat, row)
    if line_res is None:
        print("xxx", line_pat, row, line_res)
        raise exceptions.InvalidLineFormat(row)

    room = line_res.group("room")
    game_type = line_res.group("type").replace("－", "")
    started_at = datetime.combine(
        since.date(),
        datetime.strptime(line_res.group("time"), "%H:%M").time(),
    )

    if "祝" in game_type:
        score_fieldname = "shugi_scores"
        score_from_content = _shugiscore_from_content
    else:
        score_fieldname = "scores"
        score_from_content = _score_from_content

    scores = [score_from_content(m) for m in line_res.group("members").split(" ")]
    return models.Game(
        room=room,
        type=game_type,
        started_at=started_at,
        **{score_fieldname: scores},
    )


def games(since, days, game_type, room, members):
    games = [_game_from_content(row, since) for row in _log_content(_log_url(since))]
    for d in range(1, days + 1):
        since_ext = since + timedelta(days=d)
        games.extend(
            map(lambda row: _game_from_content(row, since_ext), _log_content(_log_url(since_ext), raises=False))
        )

    return models.Games(games=list(filter(_condition(game_type, room, members), games)))
