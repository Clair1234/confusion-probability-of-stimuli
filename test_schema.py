import argparse
import json
from jsonschema import validate, ValidationError


def main():
    parser = argparse.ArgumentParser(description="Validate REWIND input files")

    parser.add_argument("--stimuli", help="Path to stimuli JSON file")
    parser.add_argument("--jnd", help="Path to JND JSON file")
    parser.add_argument("--weights", help="Path to weights JSON file")

    args = parser.parse_args()

    # Count how many arguments were provided
    provided = [
        ("stimuli", args.stimuli, "src\\test\\schema\\stimuli.schema.json"),
        ("jnd", args.jnd, "src\\test\\schema\\jnd.schema.json"),
        ("weights", args.weights, "src\\test\\schema\\weights.schema.json"),
    ]

    selected = [(name, path, schema) for name, path, schema in provided if path]

    if len(selected) == 0:
        raise ValueError("You must provide one of: --stimuli, --jnd, or --weights")

    if len(selected) > 1:
        raise ValueError("Please provide only one input at a time")

    name, file_path, schema_path = selected[0]

    # Load JSON data
    with open(file_path, "r") as f:
        data = json.load(f)

    # Load schema
    with open(schema_path, "r") as f:
        schema = json.load(f)

    # Validate
    try:
        validate(instance=data, schema=schema)
        print(f"{name} file is valid")
    except ValidationError as e:
        print(f"{name} file is invalid")
        print(f"Error: {e.message}")

    
if __name__ == "__main__":
    main()
