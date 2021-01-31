#! /usr/bin/env python3

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
__version__ = "1.0.0"

import random
import re
from typing import Dict, List

import click

import patterns
import vocabulary


class BullshitGenerator:
    """
    BullshitGenerator class. Feed it sentence patterns and associated vocabulary
    to randomly generate bullshit sentences.

    Attributes:
        sentence_pool (Dict[str, List[str]]): The complete corpus of sentence patterns separated into topics.
        sentence_patterns (Dict[str, List[str]]): The remaining sentence patterns yet to be used in a run.
        vocabulary (Dict[str, List[str]]): The vocabulary of terms separated into types.
    """

    sentence_pool: Dict[str, List[str]]
    sentence_patterns: Dict[str, List[str]]
    vocabulary: Dict[str, List[str]]

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
        self.sentence_patterns = sentence_patterns
        self.vocabulary = vocabulary
        self.shuffle_sentence_patterns()

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
        self.sentence_patterns = self.sentence_pool
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
        try:
            sentences = self.sentence_patterns[topic]
            if len(sentences) == 0:
                raise KeyError
        except KeyError:
            raise KeyError("Invalid topic")
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
        full_text = ""
        for _ in range(number_of_sentences):
            if sentence_topic not in self.sentence_patterns:
                sentence_topic = random.choice(list(self.sentence_patterns.keys()))
            full_text += self.generate_sentence(sentence_topic)
        full_text = self.insert_space_between_sentences(full_text)
        return full_text

    # ---------------------------------------------------------------------------- #
    #                                 Main program                                 #
    # ---------------------------------------------------------------------------- #

    def ionize(self, number_of_sentences: int = 1, topic: str = None) -> str:
        """
        Generate bullshit.

        Args:
            number_of_sentences (int, optional): Number of sentences to be generated. Defaults to 1.
            topic (str, optional): Topic on which to generate text. Picks one at random if not provided.

        Returns:
            str: Generated bullshit.
        """
        if topic is None:
            topic = self.get_random_topic()
        return self.generate_text(number_of_sentences, topic)


# ---------------------------------------------------------------------------- #
#                                     NABG                                     #
# ---------------------------------------------------------------------------- #


def ionize(number_of_sentences: int = 1, topic: str = None):
    """
    Generate new-age bullshit.

    Args:
        number_of_sentences (int, optional): Number of sentences to generate. Defaults to 1.
        topic (str, optional): Topic on which to generate text. Picks one at random if not provided.
    """
    bullshit_generator = BullshitGenerator(
        patterns.sentence_patterns, vocabulary.bullshit_words
    )
    return bullshit_generator.ionize(number_of_sentences, topic)


# ---------------------------------------------------------------------------- #
#                                      CLI                                     #
# ---------------------------------------------------------------------------- #


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-n", default=1, help="Number of sentences to generate.")
@click.option(
    "--topic", "-t", default=None, help="Topic on which to generate bullshit."
)
@click.option(
    "--list-topics", "-l", is_flag=True, default=False, help="List available topics."
)
def main(n: int, topic: str, list_topics: bool):
    """
    Generate new-age bullshit.
    """
    if list_topics:
        for topic in patterns.sentence_patterns.keys():
            print(topic)
        return
    print(ionize(n, topic))
