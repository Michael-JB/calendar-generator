# calendar-generator

A python script which generates A4 year-to-page PDF calendars.

## Outputs

The `outputs` directory contains some example calendars which have been generated by this script.

## Usage

This project uses Python at version [3.9](.python-version). You can use
[pyenv](https://github.com/pyenv/pyenv) manage your installed versions. To install dependencies,
install [Poetry](https://github.com/python-poetry/poetry) (the dependency manager for this project),
then run `poetry install` in this directory.

To generate a calendar, you must specify an output PDF file and (optionally) a year. For example,
you can generate a calendar for the year 2021 and save it to the file `example.pdf` as follows:

```bash
poetry run python calendar_generator.py example.pdf --year 2021
```

For help, run:

```bash
poetry run python calendar_generator.py --help
```

### Developing

If making modifications, the `format.sh` script can be used to format your code.
