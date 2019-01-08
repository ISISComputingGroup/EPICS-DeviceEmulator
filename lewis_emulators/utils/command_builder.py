"""
A fluent command builder for lewis.
"""

import re
from lewis.adapters.stream import Cmd, regex

from lewis_emulators.utils.constants import STX, ACK, EOT, ETX, ENQ


class CmdBuilder(object):
    """
    Build a command for the stream adapter.

    Do this by creating this object, adding the values and then building it (this uses a fluent interface).

    For example to read a pressure the ioc might send "pres?" and when that happens this should call get_pres
    command would be:
    >>> CmdBuilder("get_pres").escape("pres?").build()
    This will generate the regex needed by Lewis. The escape is just making sure none of the characters are special
    reg ex characters.
    If you wanted to set a pressure the ioc might send "pres <pressure>" where <pressure> is a floating point number,
    the interface should call set_pres with that number. Now use:
    >>> CmdBuilder("set_pres").escape("pres ").float().build()
    this add float as a regularly expression capture group for your argument. It is equivalent to:
    >>> Cmd("set_pres", r"pres ([+-]?\d+\.?\d*)")
    There are various arguments like int and digit. Finally some special characters are included so if your protocol
    uses enquirey character ascii 5 you can match is using
    >>> CmdBuilder("set_pres").escape("pres?").enq().build()
    """

    def __init__(self, target_method, arg_sep="", ignore="", ignore_case=False):
        """
        Create a builder. Use build to create the final object

        :param target_method: name of the method target to call when the reg ex matches
        :param arg_sep: separators between arguments which are next to each other
        :param ignore: set of characters to ignore between text and arguments
        :param ignore_case: ignore the case when matching command
        """
        self._target_method = target_method
        self._arg_sep = arg_sep
        self._current_sep = ""
        if ignore is None or ignore == "":
            self._ignore = ""
        else:
            self._ignore = "[{0}]*".format(ignore)
        self._reg_ex = self._ignore

        self._ignore_case = ignore_case

    def _add_to_regex(self, regex, is_arg):
        self._reg_ex += regex + self._ignore
        if not is_arg:
            self._current_sep = ""

    def escape(self, text):
        """
        Add some text to the regex which is escaped.
        
        :param text: text to add
        :return: builder
        """
        self._add_to_regex(re.escape(text), False)
        return self

    def regex(self, regex):
        """
        Add a regex to match but not as an argument.

        :param regex: regex to add
        :return: builder
        """
        self._add_to_regex(regex, False)
        return self

    def spaces(self, at_least_one=False):
        """
        Add a regex for any number of spaces
        Args:
            at_least_one: true there must be at least one space; false there can be any number including zero

        Returns: builder

        """
        wildcard = "+" if at_least_one else "*"

        self._add_to_regex(" " + wildcard, False)
        return self

    def arg(self, arg_regex):
        """
        Add an argument to the command.

        :param arg_regex: regex for the argument (capture group will be added)
        :return: builder
        """
        self._add_to_regex(self._current_sep + "(" + arg_regex + ")", True)
        self._current_sep = self._arg_sep
        return self

    def string(self, length=None):
        """
        Add an argument which is a string of a given length (if blank string is any length)
        :param length: length of string; None for any length
        :return: builder
        """
        if length is None:
            self.arg(".+")
        else:
            self.arg(".{{{}}}".format(length))
        return self

    def float(self):
        """
        Add a float argument.

        :return: builder
        """
        return self.arg(r"[+-]?\d+\.?\d*")

    def digit(self):
        """
        Add a single digit argument.

        :return: builder
        """
        return self.arg(r"\d")

    def char(self, not_chars=None):
        """
        Add a single character argument.

        Args:
            not_chars: characters that the character can not be; None for can be anything

        Returns: builder

        """
        if not_chars is None:
            return self.arg(r".")
        return self.arg("[^{}]".format("".join(not_chars)))

    def int(self):
        """
        Add an integer argument.

        :return: builder
        """
        return self.arg(r"[+-]?\d+")

    def any(self):
        """
        Add an argument that matches anything.

        :return: builder
        """
        return self.arg(r".*")

    def endOfString(self):
        self._reg_ex += "$"
        return self

    def build(self, *args, **kwargs):
        """
        Builds the CMd object based on the target and regular expression.

        :param args: arguments to pass to Cmd constructor
        :param kwargs: key word arguments to pass to Cmd constructor
        :return: Cmd object
        """
        if self._ignore_case:
            pattern = regex(self._reg_ex)
            pattern.compiled_pattern = re.compile(self._reg_ex, re.IGNORECASE)
        else:
            pattern = self._reg_ex
        return Cmd(self._target_method, pattern, *args, **kwargs)

    def add_ascii_character(self, char_number):
        """
        Add a single character based on its integer value, e.g. 49 is 'a'.

        :param char_number: character number
        :return: self
        """
        self._add_to_regex(chr(char_number), False)
        return self

    def stx(self):
        """
        Add the STX character (0x2) to the string.

        :return: builder
        """
        return self.escape(STX)

    def etx(self):
        """
        Add the ETX character (0x3) to the string.

        :return: builder
        """
        return self.escape(ETX)

    def eot(self):
        """
        Add the EOT character (0x4) to the string.

        :return: builder
        """
        return self.escape(EOT)

    def enq(self):
        """
        Add the ENQ character (0x5) to the string.

        :return: builder
        """
        return self.escape(ENQ)

    def ack(self):
        """
        Add the ACK character (0x6) to the string.

        :return: builder
        """
        return self.escape(ACK)

    def eos(self):
        """
        Adds the regex end-of-string character to a command.

        :return: builder
        """
        self._reg_ex += "$"
        return self
