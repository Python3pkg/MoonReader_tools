import abc


class BaseParser(object, metaclass=abc.ABCMeta):
    """Base class for every parser"""

    @abc.abstractmethod
    def from_text(self, text):
        """Parse given string and return a sequence of note objects"""
        pass

    @abc.abstractmethod
    def to_string(self):
        """Dump given book back to the readable string
        (no compression applied)"""

    @abc.abstractmethod
    def to_file(self, filepath):
        """Dump given book to the string ready to be
        written in file"""
