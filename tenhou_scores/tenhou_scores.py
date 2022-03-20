import gzip
from datetime import datetime, timedelta
from io import BytesIO
from typing import Iterator

import requests

from . import models
from .config import config


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
    if raises:
        response.raise_for_status()

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


def games(since, days, game_type, room, members):
    games = [models.Game.from_row(row, since) for row in _log_content(_log_url(since))]
    for d in range(1, days + 1):
        since_ext = since + timedelta(days=d)
        games.extend(
            map(
                lambda row: models.Game.from_row(row, since_ext),
                _log_content(_log_url(since_ext), raises=False)
            )
        )

    return models.Games(games=list(filter(_condition(game_type, room, members), games)))
