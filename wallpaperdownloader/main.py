"""Wallpaper Downloader Main Module."""

import argparse
import asyncio
import logging
import sys
from datetime import datetime

from wallpaperdownloader.downloader import download, LOGGER_NAME


def abort(*args):
    """Print message to the stderr and exit the program."""
    print(*args, file=sys.stderr)
    sys.exit(1)


def check_args(args):
    """Check if arguments are valid."""
    month, year = (args.month, args.year)
    if month < 1 or month > 12:
        abort("Invalid month number %d", month)
    date_string = f"{year:04}{month:02}"
    if date_string < "201205":
        abort("There are no wallpapers older than May 2012")
    if date_string > datetime.now().strftime("%Y%M"):
        abort("Too early... come a bit later")


def configure_logger(level):
    """Configure console log output."""
    logger = logging.getLogger(LOGGER_NAME)
    handler = logging.StreamHandler()
    logger.setLevel(level)
    handler.setLevel(level)
    logger.addHandler(handler)


def main():
    """Run WD main routine."""
    parser = argparse.ArgumentParser(
        description="Download wallpapers from www.smashingmagazine.com"
    )
    parser.add_argument("month", type=int, help="Month number")
    parser.add_argument("year", type=int, help="Year")
    parser.add_argument("resolution", type=str, help="Image resolution")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()
    check_args(args)
    configure_logger(logging.DEBUG if args.verbose else logging.INFO)
    year, month, res = (args.year, args.month, args.resolution)
    asyncio.get_event_loop().run_until_complete(download(year, month, res))


if __name__ == "__main__":
    main()
