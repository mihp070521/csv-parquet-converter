"""Schema inference from CSV data."""
from typing import Any
import re

try:
    import pyarrow as pa
except ImportError:
    pa = None


def infer_type(value: str):
    """Infer the data type of a string value."""
    if not value or value.strip() == "":
        return "string"

    # Integer
    if re.match(r"^-?\d+$", value):
        return "int64"

    # Float
    if re.match(r"^-?\d+\.\d+$", value):
        return "float64"

    # Boolean
    if value.lower() in ("true", "false", "yes", "no", "1", "0"):
        return "bool"

    # Date
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return "date"

    return "string"


def infer_schema_from_csv(records: list[dict[str, Any]], sample_size: int = 100):
    """Infer Arrow schema from CSV records."""
    if not pa:
        raise ImportError("pyarrow required: pip install pyarrow")

    if not records:
        return pa.schema([])

    sample = records[:sample_size]
    columns = list(records[0].keys())

    fields = []
    for col in columns:
        types = set()
        for row in sample:
            val = str(row.get(col, ""))
            types.add(infer_type(val))

        # Pick the most specific common type
        if types == {"int64"}:
            dtype = pa.int64()
        elif types <= {"int64", "float64"}:
            dtype = pa.float64()
        elif types == {"bool"}:
            dtype = pa.bool_()
        elif types == {"date"}:
            dtype = pa.date32()
        else:
            dtype = pa.string()

        fields.append(pa.field(col, dtype))

    return pa.schema(fields)
