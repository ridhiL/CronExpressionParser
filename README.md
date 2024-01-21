# Cron Expression Parser

 This is a simple command line application which parses a cron string and expands each field
to show the times at which it will run in a tabular format.

## Prerequisites

- Python 3.11

## Setup
Clone the git repository into your machine using:
```bash
    git clone "https://github.com/ridhiL/CronExpressionParser.git"
```

Create a python virtual environment once inside the directory and install requirements

```bash
    python -m venv venv
    sourver venv/bin/activate
    pip install -r requirements.txt
```

## Usage

Run the program with a cron expression as an argument. For example:

```bash
   python cli.py "*/15 0 1,15 * 1-5 /usr/bin/find"
```

Replace `"*/15 0 1,15 * 1-5 /usr/bin/find"` with desired cron expression.

To run the unit tests, run the following:
```bash
     python -m pytest
```
For any of the above commands, in case "python" doesn't work, use "python3".