# tenhou-scores-cli

[![GitHub Super-Linter](https://github.com/kuchidaxardito/tenhou-scores-cli/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)
![pytest](https://github.com/kuchidaxardito/tenhou-scores-cli/actions/workflows/test.yml/badge.svg)

天鳳のスコアをJSONで取得する.


## つかいかた

ドキュメント.

```sh
$ tenhou-scores --help
Usage: tenhou-scores [OPTIONS] ROOM [MEMBERS]...

Options:
  -s, --since [%Y-%m-%d]          Date to start from (default: today)
  -d, --days INTEGER              Number of days from since
  -t, --game-type [F1|F2|F3|F4|F5|F6|T1|T2|T3|T4]
                                  F1 (四般南喰赤) F2 (四般南喰赤) F3 (四般南喰赤) F4 (四般南喰赤)
                                  F5 (四般南喰赤) F6 (四般南喰赤) T1 (四般南喰赤) T2 (四般南喰赤)
                                  T3 (四般南喰赤) T4 (四般南喰赤)
  --output-type [json|csv]        Output type
  -o, --output FILENAME           Output file (default: stdout)
  --help                          Show this message and exit.
```

実行例 1.

```sh
$ tenhou-scores -s 2022-03-03 L1275 いっっちじょう
{"games": [{"started_at": "2022-03-03T22:20:00", "type": "\u56db\u822c\u6771\u55b0\u8d64", ...}]
```

実行例 2.

```sh
$ tenhou-scores -s 2022-03-03 L1275 いっっちじょう | jq .games[0]
{
  "started_at": "2022-03-03T22:20:00",
  "type": "四般東喰赤",
  "room": "L1275",
  "scores": [
    {
      "name": "NoName",
      "point": 40.6
    },
    {
      "name": "えださんまる",
      "point": 8.7
    },
    {
      "name": "高井",
      "point": -19.6
    },
    {
      "name": "いっっちじょう",
      "point": -29.7
    }
  ]
}
```


## インストール

```sh
$ pip install git+https://github.com/kuchidaxardito/tenhou-scores-cli.git@0.1.0
```
