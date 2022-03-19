from enum import Enum


def _json(games):
    return games.json(exclude_none=True)


def _csv(games):
    raise NotImplementedError()


class OutputType(str, Enum):
    JSON = "json"
    CSV = "csv"

    def __call__(self, games):
        return {OutputType.JSON: _json, OutputType.CSV: _csv}[self](games)
