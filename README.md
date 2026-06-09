# Hoppscotch to Postman Converter

## Overview

The **Hoppscotch to Postman Converter** is a Python CLI tool to convert Hoppscotch exports (collections & environments) into Postman v2.1 format.

## Features

- Convert Hoppscotch collections to Postman v2.1 collections
- Convert Hoppscotch environments to Postman environment format
- Supports various request types (GET, POST, PUT, DELETE, etc.)
- Maintains request headers, parameters, body, and auth
- Supports `application/json`, `multipart/form-data`, `application/x-www-form-urlencoded`, `text/plain`
- Converts Hoppscotch `<<variable>>` placeholders to Postman `{{variable}}` format
- Accepts file or directory input from any location on your computer
- Batch conversion of all JSON files in a directory
- Filter files by name pattern
- Custom output directory

## Installation

```bash
git clone https://github.com/yourusername/hoppscotch-to-postman-converter.git
cd hoppscotch-to-postman-converter
pip install .
```

For development (editable install):

```bash
pip install -e .
```

## Usage

### Convert Collection

```bash
# Single file (output: {name}-Postman_v2.1.json in current directory)
hoppscotch-converter collection /path/to/hoppscotch_collection.json

# All JSON files in a directory
hoppscotch-converter collection /path/to/hoppscotch-exports/

# Custom output directory
hoppscotch-converter collection /path/to/exports/ -o ~/Desktop/postman-output

# Filter files by name
hoppscotch-converter collection /path/to/exports/ -f "Login"
```

### Convert Environment

```bash
# Single environment file
hoppscotch-converter env /path/to/hoppscotch_exported_files/Local.json

# All environments in a directory
hoppscotch-converter env /path/to/hoppscotch_exported_files/

# Custom output directory
hoppscotch-converter env /path/to/envs/ -o ~/Desktop/postman-envs

# Filter files by name
hoppscotch-converter env /path/to/envs/ -f "Staging"
```

### Programmatic Usage

```python
from hoppscotch_converter import (
    convert_hoppscotch_to_postman_collection_v21,
    convert_hoppscotch_env_to_postman_env
)

# Convert collection
convert_hoppscotch_to_postman_collection_v21('/path/to/hoppscotch_export.json')

# Convert single environment
convert_hoppscotch_env_to_postman_env('/path/to/env.json')
```

## Project Structure

```
hoppscotch-to-postman-converter/
├── pyproject.toml
├── src/hoppscotch_converter/
│   ├── __init__.py
│   ├── converter.py    # Core conversion logic
│   └── cli.py          # CLI entry point
├── main.py             # Legacy script (optional)
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of [Hoppscotch](https://hoppscotch.io) and [Postman](https://www.postman.com) for their amazing tools.
