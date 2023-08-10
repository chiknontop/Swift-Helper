"""
The Logging Config
"""

import colorama
import logging


class ColourFormatter(logging.Formatter):
    """The Colour Formatter for Logging"""

    LEVEL_COLOURS = [
        (logging.DEBUG, colorama.Fore.CYAN),
        (logging.INFO, colorama.Fore.GREEN),
        (logging.WARNING, colorama.Fore.YELLOW),
        (logging.ERROR, colorama.Fore.RED),
        (logging.CRITICAL, colorama.Fore.MAGENTA),
    ]

    FORMATS = {
        level: logging.Formatter(
            f"%(asctime)s {colour}|{colorama.Fore.WHITE} [ {colour}%(levelname)s {colorama.Fore.WHITE}] {colour}=> {colorama.Fore.WHITE}%(message)s{colorama.Fore.RESET}",
            datefmt=f"{colorama.Fore.WHITE}%d-%m-%Y {colour}| {colorama.Fore.WHITE}%H:%M:%S{colorama.Fore.RESET}"
        )
        for level, colour in LEVEL_COLOURS
    }


    def format(self, record: logging.LogRecord) -> str:
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"{colorama.Fore.RED}{text}{colorama.Fore.RESET}\n"

        output = formatter.format(record)

        record.exc_text = None
        return output


def get_Formatter(handler: logging.StreamHandler) -> logging.Formatter:
    """Returns the Formatter"""

    import selfcord as discord

    return ColourFormatter()

    if discord.utils.stream_supports_colour(handler.stream):
        return ColourFormatter()
    else:
        return logging.Formatter(
            f"%(asctime)s | [ %(levelname)s ] => %(message)s",
            datefmt=f"%d-%m-%Y | %H:%M:%S"
        )
