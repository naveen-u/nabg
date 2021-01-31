# nabg (New-Age Bullshit Generator)

Generate randomized sentences using patterns and a vocabulary. The default vocabulary and sentences are based on Seb Pearce's "New Age Bullshit Generator" (see http://sebpearce.com/bullshit).

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation

Run the following to install:

```python
pip3 install nabg
```

## Usage

```python
from nabg import ionize

# Generate random new-age bullshit
ionize()
```

## Developing nabg

1. Clone this repository.

```bash
git clone https://github.com/naveen-u/lets-play.git
```

2. Create and activate a virtual environment:

```bash
virtualenv venv
source venv/bin/activate
```

3. To install **nabg**, along with along with the tools you need to develop and run tests, run the following in your virtualenv:
   :

```bash
pip3 install -e .[dev]
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
