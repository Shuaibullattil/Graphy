def extract_fields(data: list[dict], fields: list[str]) -> list[dict]:
    """Dynamically extract specified fields from MongoDB-style data"""
    return [
        {
            field: int(value["$numberInt"]) if isinstance(value, dict) and "$numberInt" in value
                else int(value["$numberLong"]) if isinstance(value, dict) and "$numberLong" in value
                else value
            for field, value in entry.items()
            if field in fields
        }
        for entry in data
    ]