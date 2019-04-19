"""Downloader module."""

import asyncio
import logging
import html.parser
import aiohttp

LOGGER_NAME = "wallpaper_logger"


class URLCollector(html.parser.HTMLParser):
    """HTML parser to extract all the anchor URLs from the HTML document."""

    def __init__(self):
        """Init parser."""
        html.parser.HTMLParser.__init__(self)
        self.links = []

    def error(self, message):
        """Print error message to the log."""
        logging.getLogger(LOGGER_NAME).error(message)

    def handle_starttag(self, tag, attrs):
        """Handle start tag and store the anchor's href attribute."""
        if tag == "a":
            self.links.append(dict(attrs).get("href", None))


async def download(year, month, res):
    """Download all the wallpapers of specified size to the current directory.

    Arguments:
        year {int} -- year
        month {int} -- month
        res {str} -- screen resolution (image size)
    """
    logger = logging.getLogger(LOGGER_NAME)
    async with aiohttp.ClientSession() as session:
        month_page = get_page_url(year, month)
        download_links = list(
            await extract_links(
                session,
                month_page,
                lambda s: s
                and (s.endswith(f"{res}.png") or s.endswith(f"{res}.jpg")),
            )
        )
        logger.info("Found %d files to download", len(download_links))
        if download_links:
            task = lambda url: download_image(session, url)
            await asyncio.wait(map(task, download_links))
            logger.info("Download complete")


async def download_image(session, url):
    """Download specified file to the current directory.

    Arguments:
        session {aiohttp.ClientSession} -- aiohttp client session
        url {str} -- file URL
    """
    logger = logging.getLogger(LOGGER_NAME)
    filename = url.split("/")[-1]
    try:
        logger.debug("Download %s", url)
        async with session.get(url) as response:
            with open(filename, "wb") as output:
                output.write(await response.read())
    except aiohttp.ClientError as exc:
        logger.error("Failed to download file '%s' (%s)", url, exc)


async def extract_links(session, url, filter_url):
    """Extract and filter the anchor URLs from the specified page.

    Arguments:
        session {aiohttp.ClientSession} -- aiohttp client session
        url {str} -- page URL
        filter_url {Callable} -- URL filter function

    Returns:
        Iterable -- iterable object (generator) contains extracted URLs

    """
    logging.getLogger(LOGGER_NAME).debug("Extract links from %s", url)
    async with session.get(url) as response:
        parser = URLCollector()
        parser.feed(await response.text())
        parser.close()
        return filter(filter_url, parser.links)


def get_page_url(year, month):
    """Get the 'wallpapers of the month' page URL.

    Arguments:
        year {int} -- year
        month {int} -- month

    Returns:
        str -- URL string

    """
    template = "https://www.smashingmagazine.com/{:04}/{:02}/desktop-wallpaper-calendars-{}-{:04}/"
    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    prev_year = year if month > 1 else year - 1
    prev_month = month - 1 if month > 1 else 12
    return template.format(prev_year, prev_month, months[month - 1], year)
