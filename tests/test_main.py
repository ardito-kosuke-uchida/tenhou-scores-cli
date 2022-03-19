import json

from click.testing import CliRunner

from tenhou_scores.main import main


def test_main(mocker):
    runner = CliRunner()
    mocker.patch("tenhou_scores.printers._json", mocker.MagicMock(return_value=json.dumps([])))
    mocker.patch("tenhou_scores.tenhou_scores.games")
    result = runner.invoke(
        main,
        [
            "-s",
            "2021-12-31",
            "L1234",
            "peter",
            "anne",
            "john",
            "eve",
        ],
    )
    assert result.exit_code == 0, result.output
    assert result.output == "[]\n"
