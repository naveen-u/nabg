import re

from nabg import patterns
from nabg import vocabulary


def test_vocabulary_contains_all_types_used_in_patterns():
    for sentences in patterns.values():
        for sentence in sentences:
            for matchobj in re.finditer(r"\$\{([^\}]*)\}", sentence):
                print(matchobj)
                vocab_type = matchobj.group(1)
                assert (
                    vocab_type in vocabulary and len(vocabulary[vocab_type]) > 0
                ), f"Could not find words in the vocabulary for type {vocab_type}"
