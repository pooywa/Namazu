from pathlib import Path

import pandas


def save_csv(filename: str, data: list[dict]):
    output_file = Path(filename)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df = pandas.DataFrame(data)

    df.to_csv(output_file, index=False, encoding="utf-8-sig")
