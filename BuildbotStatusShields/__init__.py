#!/usr/bin/env python
"""Displays the status of the build using these hip new shields everyone uses
"""
from shields import ShieldStatusResource


def bind(webstatus, path="badge", left_text=None, left_color=None,
         template=None, font_face=None, font_size=None, color_scheme=None):
    """Installs the ShieldStatusResource in the given WebStatus instance
    """
    left_text = left_text or ShieldStatusResource.defaults['left_text']
    left_color = left_color or ShieldStatusResource.defaults['left_color']
    template_name = template or ShieldStatusResource.defaults['template_name']
    font_face = font_face or ShieldStatusResource.defaults['font_face']
    font_size = font_size or ShieldStatusResource.defaults['font_size']
    color_scheme = color_scheme or ShieldStatusResource.defaults['color_scheme']

    for filetype in ["png", "svg"]:
        webstatus.putChild("%s.%s" % (path, filetype),
                           ShieldStatusResource(webstatus,
                                                left_text=left_text,
                                                left_color=left_color,
                                                template_name=template_name,
                                                font_face=font_face,
                                                font_size=font_size,
                                                color_scheme=color_scheme))
    return webstatus
