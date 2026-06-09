# Hoppscotch to Postman Converter

## Overview

The **Hoppscotch to Postman Converter** is a Python CLI tool to convert Hoppscotch exports (collections & environments) into Postman v2.1 format.

## Features

- Auto-detect file type (collection or environment)
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

### Homebrew (macOS/Linux)

```bash
brew install fathurlambang/tap/hoppscotch-converter
```

### Pip (Windows/macOS/Linux)

```bash
pip install hoppscotch-to-postman
```

### From Source (Windows/macOS/Linux)

```bash
git clone https://github.com/fathurlambang/hoppscotch-to-postman-converter.git
cd hoppscotch-to-postman-converter
pip install .
```

For development (editable install):

```bash
pip install -e .
```

## Usage

### Convert File

```bash
# Auto-detect (collection or environment)
hoppscotch-converter /path/to/hoppscotch_file.json

# Force type if auto-detect fails
hoppscotch-converter /path/to/file.json -t collection
hoppscotch-converter /path/to/file.json -t env
```

### Convert Directory

```bash
# Convert all JSON files in a directory
hoppscotch-converter /path/to/hoppscotch-exports/

# Custom output directory
hoppscotch-converter /path/to/exports/ -o ~/Desktop/postman-output

# Filter files by name
hoppscotch-converter /path/to/exports/ -f "Staging"
```

### Examples

```bash
# Convert single collection
hoppscotch-converter ~/Downloads/HiRevo.json

# Convert all environments to specific folder
hoppscotch-converter ~/hoppscotch/env/ -o ~/Desktop/postman-envs

# Convert only files containing "Login"
hoppscotch-converter ~/hoppscotch/ -f "Login"
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
