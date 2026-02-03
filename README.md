# req-pinner

**Secure your Python dependencies with strict version pinning and integrity hashing.**

`req-pinner` converts a loose `requirements.txt` into a secure `requirements.lock` file by resolving the latest compatible versions and fetching SHA256 hashes from PyPI.

## Features
* **Version Pinning:** Resolves fuzzy specs (e.g., `flask>=2.0`) to exact versions.
* **Integrity Checks:** Adds SHA256 hashes to prevent supply chain attacks.
* **Pip Compatible:** Generates standard output usable with `pip install`.

## Setup

```bash
git clone [https://github.com/](https://github.com/)<YOUR_USERNAME>/req-pinner.git
cd req-pinner
pip install -r requirements.txt
```

## Usage

1. Generate Lock File
```bash
python main.py requirements.txt -o requirements.lock
```

2. Use the generated file to install dependencies with strict hash checking
```bash
pip install -r requirements.lock --require-hashes
```

## Structure
- `pinner/parser.py`: Parses input requirements
- `pinner/resolver.py`: Finds latest stable versions on PyPI
- `pinner/client.py`: Fetches metadata and hashes
- `pinner/writer.py`: Generates and formats the output file