# Mapper and grouper
A nice example of mapping and aggregating list of entities using pure python.
- mapping rule input format:
```csv
source;destination;source_type;destination_type
winter;Winter;season;season
summer;Summer;season;season
```
The mapping can go match even by deepest degree of attribute set
- mapping rule output tree:
```python
{
    "season": {
        "winter": {"_mapping": mapping("season", "Winter")},
        "summer": {"_mapping": mapping("season", "Summer")},
    }
}
```

## how to run:
```bash
python -m mapreduce

# different output file
python -m mapreduce --output_file=WHERE_TO_WRITE_OUTPUT_STREAM

```
## how to run tests:
```bash
poetry shell
poetry install
pytest -v
```
