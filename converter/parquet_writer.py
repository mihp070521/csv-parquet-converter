"""Parquet file writer."""
from typing import Any


class ParquetWriter:
    """Write records as Parquet files."""

    def __init__(self, filepath: str, compression: str = "snappy"):
        self.filepath = filepath
        self.compression = compression

    def write(self, records: list[dict[str, Any]]) -> int:
        """Write records to Parquet. Returns row count."""
        try:
            import pyarrow as pa
            import pyarrow.parquet as pq
        except ImportError:
            raise ImportError("pyarrow required: pip install pyarrow")

        if not records:
            return 0

        table = pa.Table.from_pylist(records)
        pq.write_table(table, self.filepath, compression=self.compression)
        return len(records)

    def write_batch(self, records: list[dict[str, Any]], schema) -> int:
        """Write with explicit schema."""
        import pyarrow as pa
        import pyarrow.parquet as pq

        table = pa.Table.from_pylist(records, schema=schema)
        pq.write_table(table, self.filepath, compression=self.compression)
        return len(records)
