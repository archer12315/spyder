# -*- coding: utf-8 -*-
#
# Copyright © 2009- The Spyder Development Team
# Licensed under the terms of the MIT License

"""Tests for syntaxhighlighters.py"""

import pytest
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QTextDocument

from spyderlib.utils.syntaxhighlighters import HtmlSH

def compare_formats(actualFormats, expectedFormats, sh):
    assert len(actualFormats) == len(expectedFormats)
    for actual, expected in zip(actualFormats, expectedFormats):
        assert actual.start == expected[0]
        assert actual.length == expected[1]
        # compare formats by looking at foreground colours only
        assert (actual.format.foreground().color().name()
                == sh.formats[expected[2]].foreground().color().name())

def test_HtmlSH_basic():
    txt = '<p style="color:red;">Foo <!--comment--> bar.</p>'
    doc = QTextDocument(txt)
    sh = HtmlSH(doc, color_scheme='Spyder')
    sh.rehighlightBlock(doc.firstBlock())

    # Expected result as list of tuples (begin, length, format)
    res = [(0, 2, 'builtin'),    # |<p|
           (2, 6, 'keyword'),    # | style|
           (8, 1, 'normal'),     # | |
           (9, 12, 'string'),    # |"color:red;"|
           (21, 1, 'builtin'),   # |>|
           (22, 4, 'normal'),    # |Foo |
           (26, 14, 'comment'),  # |<!--comment-->|
           (40, 5, 'normal'),    # | bar.|
           (45, 4, 'builtin')]   # |</p>|
    compare_formats(doc.firstBlock().layout().additionalFormats(), res, sh)


if __name__ == '__main__':
    pytest.main()
