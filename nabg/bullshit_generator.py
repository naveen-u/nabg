"""
Generate randomized bullshhit sentences from a given vocabulary. Default vocabulary and sentence structure
is based on Seb Pearce's "New Age Bullshit Generator". Sentence patterns and vocabulary are defined in the
two accompanying Python files.

This program is derived from Kevin McQuiggin's python2-based CLI of the "New Age Bullshit Generator" by
Seb Pearce:
    New Age Bullshit Generator. Copyright 2014-15 Seb Pearce (sebpearce.com).
    Conversion by Kevin McQuiggin. Copyright 2017 K. McQuiggin.

Rewritten for python3 with additional features by Naveen Unnikrishnan.
Copyright Naveen Unnikrishnan, January 2021.
Licensed under the MIT License.
"""

import copy
import random
import re
from enum import Enum
from typing import Dict, List, Optional

from .default_patterns import sentence_patterns as patterns
from .default_vocabulary import bullshit_words as vocabulary
from .errors import InvalidTopicError, NoPatternsAvailableError


class BullshitGenerator:
    """
    BullshitGenerator class. Feed it sentence patterns and associated vocabulary
    to randomly generate bullshit sentences.

    Attributes:
        sentence_pool (Dict[str, List[str]]): The complete corpus of sentence patterns separated into topics.
        sentence_patterns (Dict[str, List[str]]): The remaining sentence patterns yet to be used in a run.
        vocabulary (Dict[str, List[str]]): The vocabulary of terms separated into types.
    """

    def __init__(
        self, sentence_patterns: Dict[str, List[str]], vocabulary: Dict[str, List[str]]
    ):
        """
        Constructor for BullshitGenerator.

        Args:
            sentence_patterns (Dict[str, List[str]]): The corpus of sentence patterns separated into topics.
            vocabulary (Dict[str, List[str]]): The vocabulary of terms separated into types.
        """
        self.sentence_pool = sentence_patterns
        self.sentence_patterns = copy.deepcopy(self.sentence_pool)
        self.vocabulary = vocabulary
        self._auto_reset_patterns = True
        self._out_of_patterns_behavior = self.OutOfPatternsBehavior.RANDOM_TOPIC
        self.shuffle_sentence_patterns()

    class OutOfPatternsBehavior(Enum):
        """
        Possible behavior when no patterns are available for a requested topic.

        Options:
            RANDOM_TOPIC -- Pick a new available topic at random
            RESET_POOL -- Reset the pattern pool and continue using the requested topic, albeit with repetitions
            RAISE_ERROR -- Raise a NoPatternsAvailableError
        """

        RANDOM_TOPIC = 1
        RESET_POOL = 2
        RAISE_ERROR = 3

    def list_topics(self) -> List[str]:
        """
        Get available topics.

        Returns:
            List[str]: List of available topics
        """
        return list(self.sentence_pool.keys())

    def list_available_topics(self) -> List[str]:
        """
        Get available topics that have unused patterns remaining in the run.

        Returns:
            List[str]: List of available topics
        """
        return list(self.sentence_patterns.keys())

    def enable_auto_reset(self):
        """
        Enable auto-resetting of pattern pool once all patterns have been used up.
        """
        self._auto_reset_patterns = True

    def disable_auto_reset(self):
        """
        Disable auto-resetting of pattern pool once all patterns have been used up.
        An error is raised if there are no unused patterns available.
        """
        self._auto_reset_patterns = False

    def use_random_topic_when_out_of_patterns(self):
        """
        Pick a random topic if no unused patterns are available for the requested topic.
        """
        self._out_of_patterns_behavior = self.OutOfPatternsBehavior.RANDOM_TOPIC

    def reset_pool_when_out_of_patterns(self):
        """
        Reset the pool and reuse patterns if no unused patterns are available for the requested topic.
        """
        self._out_of_patterns_behavior = self.OutOfPatternsBehavior.RESET_POOL

    def raise_error_when_out_of_patterns(self):
        """
        Raise a NoPatternsAvailableError if no unused patterns are available for the requested topic.
        """
        self._out_of_patterns_behavior = self.OutOfPatternsBehavior.RAISE_ERROR

    # ---------------------------------------------------------------------------- #
    #                               Utility functions                              #
    # ---------------------------------------------------------------------------- #

    @staticmethod
    def replace_a_with_an(sentence: str) -> str:
        """
        Replace 'a [vowel]' with 'an [vowel]'.

        Args:
            sentence (str): Sentence to modify

        Returns:
            str: Sentence with 'a [vowel]' replaced with 'an [vowel]'
        """
        p = re.compile(r"(^|\W)([Aa]) ([aeiou])")
        return p.sub(r"\1\2n \3", sentence)

    @staticmethod
    def insert_space_between_sentences(text: str) -> str:
        """
        Insert a space after periods and question marks.

        Args:
            text (str): Paragraph to be formatted

        Returns:
            str: Formatted paragraph.
        """
        p = re.compile(r"([\.\?])(\w)")
        return p.sub(r"\1 \2", text)

    @staticmethod
    def clean_sentence(sentence: str) -> str:
        """
        Tidy up a generated sentence.

        Args:
            sentence (str): Generated sentence to clean up

        Returns:
            str: Cleaned-up sentence
        """
        result = BullshitGenerator.replace_a_with_an(sentence)
        result = result[0].upper() + result[1:]
        return result

    # ---------------------------------------------------------------------------- #
    #                 Support routines related to the main program                 #
    # ---------------------------------------------------------------------------- #

    def shuffle_sentence_patterns(self):
        """
        Shuffle sentence patterns.
        """
        for sentenceList in self.sentence_patterns.values():
            random.shuffle(sentenceList)

    def reset_sentence_patterns(self):
        """
        Reset sentence patterns for a new run.
        """
        self.sentence_patterns = copy.deepcopy(self.sentence_pool)
        self.shuffle_sentence_patterns()

    def get_random_topic(self) -> str:
        """
        Choose a topic at random from the sentence pool.

        Returns:
            str: Randomly chosen topic
        """
        return random.choice(list(self.sentence_patterns.keys()))

    def retrieve_random_word_of_type(self, type: str) -> str:
        """
        Choose a random vocabulary word, based on a given word type.

        Args:
            type (str): Type of vocabulary word

        Returns:
            str: A vocabulary word of the requested type
        """
        return random.choice(self.vocabulary[type])

    def replace_vocab_patterns(self, sentence: str) -> str:
        """
        Replace type placeholders in the pattern with random words from the vocabulary.

        Args:
            sentence (str): Sentence to be modified

        Returns:
            str: Sentence where type placeholders have been replaced with random words from the vocabulary
        """
        sentence = re.sub(
            r"\$\{([^\}]*)\}",
            lambda matchobj: self.retrieve_random_word_of_type(matchobj.group(1)),
            sentence,
        )
        return sentence

    def generate_sentence(self, topic: str) -> str:
        """
        Generate a single sentence on a particular topic.

        Args:
            topic (str): Topic on which to generate a sentence

        Raises:
            KeyError: If topic is invalid

        Returns:
            str: Generated sentence
        """
        sentences = self.sentence_patterns[topic]
        pattern = sentences.pop()
        result = self.replace_vocab_patterns(pattern)
        if len(sentences) == 0:
            self.sentence_patterns.pop(topic, None)
        result = self.clean_sentence(result)
        return result

    def generate_text(self, number_of_sentences: int, sentence_topic: str) -> str:
        """
        Generate a set of sentences.

        Args:
            number_of_sentences (int): Number of sentences to generate
            sentence_topic (str): Topic to generate sentences in

        Returns:
            str: Generated text
        """
        full_text: str = ""
        for _ in range(number_of_sentences):
            if sentence_topic not in self.sentence_pool:
                raise InvalidTopicError(
                    sentence_topic,
                    f"Topic {sentence_topic} is not present in the pattern pool",
                )
            if len(self.sentence_patterns) == 0:
                self.handle_empty_patterns_set()
            if sentence_topic not in self.sentence_patterns:
                if (
                    self._out_of_patterns_behavior
                    == self.OutOfPatternsBehavior.RAISE_ERROR
                ):
                    raise NoPatternsAvailableError(
                        sentence_topic, f"Ran out of pattern in topic {sentence_topic}"
                    )
                elif (
                    self._out_of_patterns_behavior
                    == self.OutOfPatternsBehavior.RESET_POOL
                ):
                    self.reset_sentence_patterns()
                elif (
                    self._out_of_patterns_behavior
                    == self.OutOfPatternsBehavior.RANDOM_TOPIC
                ):
                    sentence_topic = random.choice(list(self.sentence_patterns.keys()))
            full_text = full_text + self.generate_sentence(sentence_topic)
        full_text = self.insert_space_between_sentences(full_text)
        return full_text

    def handle_empty_patterns_set(self):
        """
        Handle scenarios where all patterns have been used up.

        Raises:
            NoPatternsAvailableError: If no unused patterns are available and auto-reset is disabled
        """
        if not self._auto_reset_patterns:
            raise NoPatternsAvailableError(message="Ran out of patterns")
        self.reset_sentence_patterns()

    # ---------------------------------------------------------------------------- #
    #                                 Main program                                 #
    # ---------------------------------------------------------------------------- #

    def ionize(self, number_of_sentences: int = 1, topic: Optional[str] = None) -> str:
        """
        Generate bullshit.

        Args:
            number_of_sentences (int, optional): Number of sentences to be generated. Defaults to 1.
            topic (str, optional): Topic on which to generate text. Picks one at random if not provided.

        Returns:
            str: Generated bullshit.
        """
        if len(self.sentence_patterns) == 0:
            self.handle_empty_patterns_set()
        if topic is None:
            topic = self.get_random_topic()
        return self.generate_text(number_of_sentences, topic)


# ---------------------------------------------------------------------------- #
#                                     NABG                                     #
# ---------------------------------------------------------------------------- #


def ionize(number_of_sentences: int = 1, topic: Optional[str] = None) -> str:
    """
    Generate new-age bullshit.

    Args:
        number_of_sentences (int, optional): Number of sentences to generate. Defaults to 1.
        topic (str, optional): Topic on which to generate text. Picks one at random if not provided.
    """
    bullshit_generator = BullshitGenerator(patterns, vocabulary)
    return bullshit_generator.ionize(number_of_sentences, topic)


def list_topics() -> List[str]:
    """
    Get available topics.

    Returns:
        List[str]: List of available topics
    """
    return list(patterns.keys())
