# csv-parquet-converter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

CLI tool for converting CSV files to Parquet with automatic schema inference and compression.

## Features

- 📊 **Schema Inference** — auto-detects int, float, bool, date, string
- 📦 **Compression** — snappy, gzip, lz4, zstd
- 🔄 **Streaming** — handles large files with chunked processing
- 📈 **Progress Bar** — visual feedback for large conversions
- 📉 **Size Reporting** — shows compression ratio

## Installation

```bash
pip install csv-parquet-converter
```

## Usage

```bash
# Basic conversion
csv2parquet data.csv data.parquet

# With options
csv2parquet data.csv data.parquet --compression gzip --delimiter ";"

# Large files (streaming)
csv2parquet huge.csv huge.parquet --chunk-size 50000
```

## API

```python
from converter import CSVReader, ParquetWriter, infer_schema_from_csv

reader = CSVReader("data.csv")
records = reader.read()

schema = infer_schema_from_csv(records)
writer = ParquetWriter("data.parquet", compression="gzip")
writer.write_batch(records, schema)
```

## License

[MIT](LICENSE)
