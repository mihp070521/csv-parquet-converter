"""CSV file reader with schema inference."""
import csv
from typing import Any, Generator


class CSVReader:
    """Read CSV files with type inference."""

    def __init__(self, filepath: str, delimiter: str = ",", encoding: str = "utf-8"):
        self.filepath = filepath
        self.delimiter = delimiter
        self.encoding = encoding

    def read(self) -> list[dict[str, Any]]:
        """Read all records."""
        with open(self.filepath, encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            return list(reader)

    def stream(self, chunk_size: int = 1000) -> Generator[list[dict[str, Any]], None, None]:
        """Stream records in chunks."""
        with open(self.filepath, encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            chunk = []
            for row in reader:
                chunk.append(dict(row))
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk

    def headers(self) -> list[str]:
        """Read just the header row."""
        with open(self.filepath, encoding=self.encoding) as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            return next(reader)

    def count(self) -> int:
        """Count rows without loading data."""
        count = 0
        with open(self.filepath, encoding=self.encoding) as f:
            for _ in f:
                count += 1
        return max(0, count - 1)  # Subtract header
