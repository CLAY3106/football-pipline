import re
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
OUT_DIR = PROJECT_ROOT / "infra" / "db" / "init"

SQL_PREFIX = "002_raw_"  # keeps ordering in init folder

# return standardized name
def clean_name(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if not s:
        s = "x"
    if s[0].isdigit():
        s = f"t_{s}"
    return s

# return standardized column names
def clean_col(name: str) -> str:
    s = clean_name(name)
    if not s:
        s = "col"
    return s

# return array of unique column names
def uniqueify(names: list[str]) -> list[str]:
    seen = {}
    out = []
    for n in names:
        if n not in seen:
            seen[n] = 0
            out.append(n)
        else:
            seen[n] += 1
            out.append(f"{n}_{seen[n]}")
    return out

# create table name from filename (without extension using .stem)
def table_name_from_file(path: Path) -> str:
    return clean_name(path.stem)

# 
def generate_sql_for_csv(csv_file: Path) -> tuple[str, list[tuple[str, str]]]:
    df = pd.read_csv(csv_file, nrows=0, encoding ="latin1")
    orig_cols = list(df.columns)
    cleaned = [clean_col(c) for c in orig_cols]
    final_cols = uniqueify(cleaned)

    table = table_name_from_file(csv_file)

    sql_lines = [
        f"CREATE TABLE IF NOT EXISTS raw.{table} (",
        "    " + ",\n    ".join([f"{c} TEXT" for c in final_cols]),
        ");\n",
    ]
    mapping = list(zip(orig_cols, final_cols))
    return "\n".join(sql_lines), mapping

# main function
def main():
    if not DATA_RAW.exists():
        raise FileNotFoundError(f"Missing folder: {DATA_RAW}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(DATA_RAW.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {DATA_RAW}")

    report_lines = []
    for csv_file in csv_files:
        table = table_name_from_file(csv_file)
        out_sql = OUT_DIR / f"{SQL_PREFIX}{table}.sql"

        sql, mapping = generate_sql_for_csv(csv_file)
        out_sql.write_text(sql, encoding="utf-8")

        report_lines.append(f"\n# {csv_file.name} -> raw.{table}")
        for o, n in mapping:
            report_lines.append(f"{o} -> {n}")

        print("Wrote:", out_sql)

    (OUT_DIR / f"{SQL_PREFIX}column_mapping_report.txt").write_text(
        "\n".join(report_lines), encoding="utf-8"
    )
    print("Wrote mapping report:", OUT_DIR / f"{SQL_PREFIX}column_mapping_report.txt")

# run main
if __name__ == "__main__":
    main()
