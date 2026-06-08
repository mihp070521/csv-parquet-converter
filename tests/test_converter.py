import csv
import pytest
from converter.csv_reader import CSVReader
from converter.parquet_writer import ParquetWriter
from converter.schema import infer_type, infer_schema_from_csv


@pytest.fixture
def sample_csv(tmp_path):
    filepath = tmp_path / "test.csv"
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "age", "active"])
        writer.writeheader()
        writer.writerows([
            {"id": "1", "name": "Alice", "age": "30", "active": "true"},
            {"id": "2", "name": "Bob", "age": "25", "active": "false"},
            {"id": "3", "name": "Charlie", "age": "35", "active": "true"},
        ])
    return str(filepath)


def test_csv_reader(sample_csv):
    reader = CSVReader(sample_csv)
    records = reader.read()
    assert len(records) == 3
    assert records[0]["name"] == "Alice"


def test_csv_headers(sample_csv):
    reader = CSVReader(sample_csv)
    assert reader.headers() == ["id", "name", "age", "active"]


def test_csv_count(sample_csv):
    reader = CSVReader(sample_csv)
    assert reader.count() == 3


def test_csv_stream(sample_csv):
    reader = CSVReader(sample_csv)
    chunks = list(reader.stream(chunk_size=2))
    assert len(chunks) == 2
    assert len(chunks[0]) == 2
    assert len(chunks[1]) == 1


def test_infer_types():
    assert infer_type("42") == "int64"
    assert infer_type("3.14") == "float64"
    assert infer_type("true") == "bool"
    assert infer_type("2024-01-15") == "date"
    assert infer_type("hello") == "string"
    assert infer_type("") == "string"


def test_schema_inference(sample_csv):
    reader = CSVReader(sample_csv)
    records = reader.read()
    schema = infer_schema_from_csv(records)

    field_names = [f.name for f in schema]
    assert "id" in field_names
    assert "name" in field_names
