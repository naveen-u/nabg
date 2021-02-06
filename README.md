# nabg (New-Age Bullshit Generator)

[![PyPI version](https://badge.fury.io/py/nabg.svg)](https://badge.fury.io/py/nabg)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is it?

**nabg** lets you generate randomized sentences using pre-defined sentence patterns and a vocabulary. The default vocabulary and sentences are based on [Seb Pearce's "New Age Bullshit Generator"](http://sebpearce.com/bullshit). You can also provide your own sentence patterns and word lists to generate customized bullshit.

## Installing nabg

**nabg** is available on [PyPI](https://pypi.org/project/nabg/):

```bash
pip install nabg
```

## Usage

### Generating New-Age Bullshit

**nabg** comes with Seb Pearce's "New-Age Bullshit Generator". To generate new-age bullshit, in python you can do:

```python
import nabg

# Generate new-age bullshit
nabg.ionize()

# List the available topics
nabg.list_topics()

# Generate 5 bullshit sentences with topic history
nabg.ionize(5, "history")
```

Or, you can use the CLI:

```bash
# Generate new-age bullshit
$ nabg

# List the available topics
$ nabg --list-topics

# Generate 5 bullshit sentences with topic history
$ nabg -n 5 -t history
```

### Generating Custom Bullshit

**nabg** also lets you use your own sentence patterns and vocabulary to generate sentences.

```python
from nabg import BullshitGenerator

# ---------------------------------------------------------------------------- #
# Custom sentence patterns. A dictionary with a list of patterns for each      #
# topic. All instances of ${vocabType} will be replaced with a randomly picked #
# word of type "vocabType" from the vocabulary.                                #
# ---------------------------------------------------------------------------- #

patterns = {
    "topic1": [
        "This is a ${adj} sentence.",
        "This is a ${adjPrefix}${adj} sentence."
    ],
    "topic2": [
        "We can no longer afford to live with ${nMassBad}.",
        "Without ${nMass}, one cannot ${viPerson}.",
    ],
}


# ---------------------------------------------------------------------------- #
# Custom vocabulary. A dictionary with a list of buzzwords for each type.      #
# Each type used in a sentence pattern must have at least one word in the      #
# vocabulary.                                                                  #
# ---------------------------------------------------------------------------- #

vocabulary = {
    "adj": [
        "fantastic",
        "stupid",
        "amazing",
    ],
    "adjPrefix": [
        "ultra-",
        "semi-",
    ],
    "nMass": [
        "knowledge",
        "truth",
    ],
    "nMassBad": [
        "pain",
        "suffering",
    ],
    "viPerson": [
        "exist",
        "believe",
    ],
}

# Create a bullshit generator object
bullshit_generator = BullshitGenerator(patterns, vocabulary)

# Generate custom bullshit
bullshit_generator.ionize(5, "topic1")
```

`BullshitGenerator` ensures that sentence patterns aren't repeated on multiple calls to `BullshitGenerator.ionize()`. If there are no unused sentence patterns remaining in the pool for the requested topic, another topic is chosen at random. This behavior can be customised by calling any of the three methods below:

```python
# The three methods below can be used to set BullshitGenerator's behavior
# when no more unused patterns are available for the requested topic.

# Pick a different topic at random. This is the default behavior.
bullshit_generator.use_random_topic_when_out_of_patterns()

# Reset the pool. This would cause previously used patterns to repeat.
bullshit_generator.reset_pool_when_out_of_patterns()

# Raise a NoPatternsAvailableError.
bullshit_generator.raise_error_when_out_of_patterns()
```

When all sentence patterns across all topics have been used up, the pool is reset. This behavior can be customised by calling any of the two methods below:

```python
# The two methods below can be used to set BullshitGenerator's behavior
# when all patterns across topics have been used up.

# Automatically reset the pool. This is the default behavior.
bullshit_generator.enable_auto_reset()

# Raise a NoPatternsAvailableError.
bullshit_generator.disable_auto_reset()
```

You can reset the pool manually at any time by calling:

```python
bullshit_generator.reset_sentence_patterns()
```

_Note_: Successive calls to `nabg.ionize()` are not guaranteed to have distinct sentence patterns across calls (or in other words, the pool is reset after each call to `nabg.ionize()`). However, the sentence patterns and vocabulary for the default new-age bullshit generator can be used to create your own instance of `BullshitGenerator` to customize this behaviour:

```python
from nabg import BullshitGenerator, patterns, vocabulary

# Create a BullshitGenerator object using Seb Pearce's pattern and vocabulary set
bullshit_generator = BullshitGenerator(patterns, vocabulary)

# The calls below are guaranteed to use different sentence patterns
print(bullshit_generator.ionize(3))
print(bullshit_generator.ionize(5))
print(bullshit_generator.ionize(2))

# Reset the pool
bullshit_generator.reset_sentence_patterns()

# The below call might use the same sentence pattern as one of the above calls as the pool has been reset
print(bullshit_generator.ionize())
```

## Developing nabg

- Clone [the repository](https://github.com/naveen-u/nabg).

```bash
git clone https://github.com/naveen-u/nabg.git
```

- Create and activate a virtual environment:

```bash
virtualenv venv
source venv/bin/activate
```

- To install **nabg**, along with along with the tools you need to develop and run tests, run the following in your virtualenv:
  :

```bash
pip3 install -e .[dev]
```

## References

- The original New-Age Bullshit Generator by Seb Pearce - [sebpearce](https://github.com/sebpearce/bullshit).
- The Python2 CLI - [mcquiggi](https://github.com/mcquiggi/bullshit/tree/gh-pages/python).

## Authors

- **Naveen Unnikrishnan** - _Initial work_ - [naveen-u](https://github.com/naveen-u)

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/) - see the [LICENSE.md](LICENSE.md) file for details.
