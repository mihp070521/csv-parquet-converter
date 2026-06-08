"""CLI interface for CSV to Parquet conversion."""
import os
import click
from .csv_reader import CSVReader
from .parquet_writer import ParquetWriter
from .schema import infer_schema_from_csv


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--compression", default="snappy", type=click.Choice(["snappy", "gzip", "lz4", "zstd", "none"]))
@click.option("--delimiter", default=",", help="CSV delimiter")
@click.option("--encoding", default="utf-8", help="CSV encoding")
@click.option("--chunk-size", default=10000, help="Rows per chunk for large files")
@click.option("--infer/--no-infer", default=True, help="Infer types from data")
def main(input_file: str, output_file: str, compression: str, delimiter: str, encoding: str, chunk_size: int, infer: bool):
    """Convert CSV to Parquet with schema inference."""

    click.echo(f"Reading {input_file}...")
    reader = CSVReader(input_file, delimiter=delimiter, encoding=encoding)

    total_rows = reader.count()
    click.echo(f"Found {total_rows:,} rows")

    if total_rows < chunk_size:
        # Small file: load all at once
        records = reader.read()

        if infer:
            schema = infer_schema_from_csv(records)
            writer = ParquetWriter(output_file, compression=compression)
            count = writer.write_batch(records, schema)
        else:
            writer = ParquetWriter(output_file, compression=compression)
            count = writer.write(records)
    else:
        # Large file: stream in chunks
        click.echo(f"Processing in chunks of {chunk_size:,}...")
        all_records = []
        with click.progressbar(length=total_rows, label="Converting") as bar:
            for chunk in reader.stream(chunk_size):
                all_records.extend(chunk)
                bar.update(len(chunk))

        writer = ParquetWriter(output_file, compression=compression)
        if infer:
            schema = infer_schema_from_csv(all_records)
            count = writer.write_batch(all_records, schema)
        else:
            count = writer.write(all_records)

    output_size = os.path.getsize(output_file)
    input_size = os.path.getsize(input_file)
    ratio = (1 - output_size / input_size) * 100 if input_size > 0 else 0

    click.echo(f"\n✅ Converted {count:,} rows → {output_file}")
    click.echo(f"   Size: {input_size:,} → {output_size:,} bytes ({ratio:.1f}% reduction)")
    click.echo(f"   Compression: {compression}")


if __name__ == "__main__":
    main()
