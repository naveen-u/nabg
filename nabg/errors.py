from typing import Optional

# ---------------------------------------------------------------------------- #
#                              Exceptions for nabg                             #
# ---------------------------------------------------------------------------- #


class Error(Exception):
    """
    Base class for exceptions in this module.

    Attributes:
        topic -- topic which caused the error occurred
        message -- explanation of the error
    """

    def __init__(self, topic: Optional[str], message: Optional[str]):
        self.topic = topic
        self.message = message


class InvalidTopicError(Error):
    """
    Exception raised for errors caused by invalid topic.

    Attributes:
        topic -- input topic which caused the error
        message -- explanation of the error
    """

    def __init__(self, topic: str, message: Optional[str] = None):
        super().__init__(topic, message)


class NoPatternsAvailableError(Error):
    """
    Raised when there are no more unused patterns available.

    Attributes:
        topic -- input topic for which patterns are unavailable; None if no topic was passed
            and no patterns are available for any topic
        message -- explanation of the error
    """

    def __init__(self, topic: Optional[str] = None, message: Optional[str] = None):
        super().__init__(topic, message)
