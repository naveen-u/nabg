import re

import patterns
import vocabulary


def test_vocabulary_contains_all_types_used_in_patterns():
    for sentences in patterns.sentence_patterns.values():
        for sentence in sentences:
            for matchobj in re.finditer(r"\$\{([^\}]*)\}", sentence):
                print(matchobj)
                vocab_type = matchobj.group(1)
                assert (
                    vocab_type in vocabulary.bullshit_words
                    and len(vocabulary.bullshit_words[vocab_type]) > 0
                ), f"Could not find words in the vocabulary for type {vocab_type}"
