from pydantic import BaseConfig


class Config(BaseConfig):
    LOG_URL: str = "https://tenhou.net/sc/raw/dat/sca{}.log.gz"

    LINE_PAT: str = r"(?P<room>^[A-Z0-9]+)\s+\|\s+(?P<time>[0-9]+:[0-9]+)\s+\|\s+(?P<type>\S+)\s+\|\s+(?P<members>.*)$"
    LINE_MEMBER_PAT: str = r"(?P<name>\S+)\((?P<score>[\-\+]{0,1}[0-9]+\.[0-9]+)\)"
    LINE_SHUGI_PAT: str = r"(?P<name>\S+)\((?P<score>[\-\+]{0,1}[0-9]+\.[0-9]+),(?P<shugi>[\-\+]{0,1}[0-9]+)枚\)"

    RECENT_DAYS: int = 9


config = Config()
