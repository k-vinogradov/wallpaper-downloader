"""Wallpaper Downloader Autotests."""

import os
import asyncio
import pytest
from wallpaperdownloader import download


@pytest.mark.parametrize(
    "args", [(1, 2017, "800x600", 30), (5, 2018, "1920x1080", 35)]
)
def test_full_sequence(tmpdir, args):
    """Test if images were successfully downloaded."""
    month, year, image_size, expected_number_of_files = args
    os.chdir(tmpdir)
    asyncio.run(download(year, month, image_size))
    file_list = os.listdir(tmpdir)
    assert len(file_list) == expected_number_of_files, "Invalid file count"
    for filepath in map(lambda s: os.path.join(tmpdir, s), file_list):
        assert os.path.getsize(filepath) > 0, "Invalid file size"
