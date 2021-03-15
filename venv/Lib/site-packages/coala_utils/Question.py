from pyprint.ConsolePrinter import ConsolePrinter
from coala_utils.string_processing.StringConverter import StringConverter


def ask_question(question,
                 default=None,
                 printer=ConsolePrinter(),
                 typecast=str,
                 **kwargs):
    """
    Asks the user a question and returns the answer.

    :param question:
        String to be used as question.
    :param default:
        The default answer to be returned if the user gives a void answer
        to the question.
    :param printer:
        The printer object used for console interactions. If this is not
        given, it defaults to a ``ConsolePrinter``.
    :param typecast:
        Type to cast the input to. Defaults to a ``str``.
    :param kwargs:
        The additional keyword arguments are held for backwards compatibility
        and for future use with the ``prompt_toolkit``.
    :return:
        The response from the user.
    """
    while True:
        printer.print(question, color="yellow", end=" ")
        if default:
            printer.print("[" + default + "]", end=" ")
        printer.print("")

        answer = input()
        if default and len(answer) == 0:
            answer = default

        try:
            answer = typecast(StringConverter(answer))
        except BaseException as e:
            printer.print(
                str(e) + "\nPlease enter a valid answer.",
                color="blue")
        else:
            return answer
