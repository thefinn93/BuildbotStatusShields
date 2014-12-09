#!/usr/bin/env python
from shields import *

colors = {
    "exception": "#007ec6",  # blue
    "failure": "#e05d44",    # red
    "retry": "#007ec6",      # blue
    "skipped": "a4a61d",     # yellowgreen
    "success": "#4c1",       # brightgreen
    "unknown": "#9f9f9f",    # lightgrey
    "warnings": "#dfb317"    # yellow
}


def bind(webstatus, path="badge", leftText="Build Status", leftColor="#555",
         templateName="badge.svg.j2", fontFace="DejaVu Sans",
         fontSize=11, colorScheme=colors):
    for filetype in ["png", "svg"]:
        webstatus.putChild("%s.%s" % (path, filetype),
                           ShieldStatusResource(webstatus,
                                                leftText=leftText,
                                                leftColor=leftColor,
                                                templateName=templateName,
                                                fontFace=fontFace,
                                                fontSize=fontSize,
                                                colorScheme=colorScheme))
    return webstatus
