import re

from lewis.adapters.stream import Cmd


class CmdBuilder(object):
    """
    Build a command for the stream adapter
    """

    def __init__(self, target_method, arg_sep=",", ignore=""):
        """
        Create a builder. Use build to create the final objecy
        Args:
            target_method: name of the method target to call when the reg ex matches
            arg_sep: seperators between the arguments
            ignore: set of characters to ignore between text and arguments

        Returns:

        """
        self._target_method = target_method
        self._arg_sep = arg_sep
        self._current_sep = ""
        if ignore is None or ignore == "":
            self._ignore = ""
        else:
            self._ignore = "[{0}]*".format(ignore)
        self._reg_ex = self._ignore

    def escape(self, text):
        """
        Add some text to the regex which is esacped
        Args:
            text: text to add

        Returns: builder

        """
        self._reg_ex += re.escape(text) + self._ignore
        return self

    def arg(self, arg_regex):
        """
        Add an argument to the command
        Args:
            arg_regex: regex for the argument (capture group will be added)

        Returns: builder

        """
        self._reg_ex += self._current_sep + "(" + arg_regex + ")" + self._ignore
        self._current_sep = self._arg_sep
        return self

    def float(self):
        """
        Add a float argument
        Returns: builder

        """
        return self.arg(r"[+-]?\d+\.?\d*")

    def digit(self):
        """
        Add a single digit argument
        Returns: builder

        """
        return self.arg(r"\d")

    def int(self):
        """
        Add an integer argument
        Returns: builder

        """
        return self.arg(r"\d+")

    def build(self, *args, **kwargs):
        """
        Builds the CMd object based on the target and regular expression
        Args:
            *args: arguments to pass to Cmd constructor
            **kwargs: key word arguments to pass to Cmd constructor

        Returns: Cmd object

        """
        return Cmd(self._target_method, self._reg_ex, *args, **kwargs)

    def add_ascii_character(self, char_number):
        """
        Add a single character based on its integer value, e.g. 49 is a
        :param char_number: character number
        :return: self
        """
        self._reg_ex += chr(char_number)

        return self

    def stx(self):
        """
        Add the STX character (0x2) to the string
        :return: builder
        """
        return self.add_ascii_character(2)

    def etx(self):
        """
        Add the ETX character (0xe) to the string
        :return: builder
        """
        return self.add_ascii_character(3)
