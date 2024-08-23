# pyls

`pyls` is a custom Python implementation of the `ls` command designed to work with JSON-structured directories. It allows users to navigate and list files and directories stored in JSON files with various options, including human-readable file sizes, filtering, and sorting.

## Features

- **List directory contents**: Displays files and directories within JSON structures.
- **Human-readable file sizes**: Converts file sizes to a more readable format (e.g., KB, MB).
- **Filtering**: Show only files or directories.
- **Sorting**: Sort by modification time, with options to reverse the order.
- **Custom scripts**: Install as a system-wide command using `pyproject.toml`.

## Installation

### Requirements

- Python 3.10 or later
- `setuptools` and `wheel` for packaging
- `pytest` for testing

### Install the package

To install the `pyls` package, navigate to the root of your project directory (where `pyproject.toml` is located) and run:

```bash
pip install .
```

### Installing for Development

For development purposes, you might want to install the package in "editable" mode:

```bash
pip install -e .
```

This allows you to modify the code and immediately see the effects without needing to reinstall the package.

## Usage

Once installed, you can use the `pyls` command to navigate and list directory contents:

### Basic Usage

```bash
pyls
```

This command lists the files and directories in the root of the JSON structure.

### Options

- `-l`, `--long`: Display detailed information about each file or directory.
- `-A`, `--all`: Include entries that start with a dot (hidden files).
- `-r`, `--reverse`: Reverse the order of the sort.
- `-t`, `--time`: Sort by modification time, oldest first.
- `-h`, `--human-readable`: Display file sizes in human-readable format.
- `--filter`: Filter output to show only files or directories (`file` or `dir`).
- `--json-file`: Specify the path to the JSON file containing the directory structure. Defaults to `xdata/structure.json` if not provided.

### Examples

List all files and directories in a JSON structure:

```bash
pyls
```

List detailed information in human-readable format:

```bash
pyls -l -h
```

Filter to show only directories:

```bash
pyls --filter=dir
```

List all files and directories with detailed information using a custom JSON file.

```bash
pyls -l --json-file=/path/to/your/custom_structure.json
```
## Development

### Setting Up the Development Environment

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AshishMahendra/pyls_project.git
   cd pyls
   ```

2. **Install dependencies**:

   ```bash
   pip install -e .
   ```

### Running Tests

To ensure everything works as expected, you can run the tests using `pytest`:

```bash
pytest
```

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b my-new-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin my-new-feature`).
5. Create a new Pull Request.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspiration: This project was inspired by the need for a custom `ls` implementation tailored to JSON-structured directories.
