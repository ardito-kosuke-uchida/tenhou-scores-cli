import datetime

import click

from . import __version__, tenhou_scores
from .models import GameType
from .printers import OutputType


@click.command()
@click.version_option(__version__)
@click.option(
    "-s",
    "--since",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=datetime.datetime.now().strftime("%Y-%m-%d"),
    help="Date to start from (default: today)",
)
@click.option(
    "-d",
    "--days",
    type=click.INT,
    default=1,
    help="Number of days from since",
)
@click.option(
    "-t",
    "--game-type",
    type=click.Choice(map(lambda t: t.name, GameType)),
    help="\n".join(map(lambda t: f"{t.name} ({t.value})", GameType)),
)
@click.option(
    "--output-type",
    type=click.Choice(OutputType),
    default="json",
    help="Output type",
)
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    default="-",
    help="Output file (default: stdout)",
)
@click.argument("room")
@click.argument("members", nargs=-1)
def main(since, days, game_type, output_type, output, room, members):
    games = tenhou_scores.games(since, days, game_type, room, members)
    click.echo(output_type(games), output)
