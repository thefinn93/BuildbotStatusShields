# This file is part of BuildbotStatusShields.  BuildbotStatusShields is free
# software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, version
# 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members
# Copyright 2013 (c) Mamba Developers
# Copyright 2014 (c) Finn Herzfeld

"""Simple build status shields. Based heavily from buildbot's pngstatus.py
"""

import os

from twisted.web import resource

from buildbot.status import results

import cairocffi as cairo
import cairosvg
import jinja2


class ShieldStatusResource(resource.Resource):
    """Describe a single builder result as a PNG image
    """

    isLeaf = True
    webstatus = None

    leftText = None
    leftColor = None
    templateName = None
    fontFace = None
    fontSize = None
    colorScheme = {
        "exception": "#007ec6",  # blue
        "failure": "#e05d44",    # red
        "retry": "#007ec6",      # blue
        "skipped": "a4a61d",     # yellowgreen
        "success": "#4c1",       # brightgreen
        "unknown": "#9f9f9f",    # lightgrey
        "warnings": "#dfb317"    # yellow
    }

    env = jinja2.Environment(loader=jinja2.ChoiceLoader([
        jinja2.PackageLoader('BuildbotStatusShields'),
        jinja2.FileSystemLoader('templates')
        ]))

    def __init__(self, webstatus, leftText="Build Status", leftColor="#555",
                 templateName="badge.svg.j2", fontFace="DejaVu Sans",
                 fontSize=11, colorScheme=colorScheme):
        self.webstatus = webstatus
        self.leftText = leftText
        self.leftColor = leftColor
        self.templateName = templateName
        self.fontFace = fontFace
        self.fontSize = fontSize
        self.colorScheme = colorScheme

    def getChild(self, name, request):
        """Just return itself
        """
        return self

    def render(self, request):
        """
        Renders a given build status

        We don't care about pre or post paths here so we skip them, we only
        care about parameters passed in the URL, those are:

        :param builder: the builder name
        :returns: either a binary PNG or an SVG, based on the requested path
        """

        data = self.content(request)
        request.setHeader('content-type', data['content_type'])
        request.setHeader('cache-control', 'no-cache')
        request.setHeader(
            'content-disposition', 'inline; filename="%s"' % (data['filename'])
        )
        return data['image']

    def content(self, request):
        """Renders the shield image
        """
        # size not supported yet
        # size = request.args.get('size', ['normal'])[0]
        # if size not in ('small', 'normal', 'large'):
        #     size = 'normal'

        status = self.webstatus.getStatus()
        # build number
        b = int(request.args.get('number', [-1])[0])

        filetype = request.path.split(".")[-1].lower()
        mimetypes = {
            "svg": "image/svg+xml",
            "png": "image/png"
        }
        if filetype not in mimetypes:
            filetype = "png"

        data = {'filename': 'status.%s' % filetype,
                'image': None,
                'content_type': mimetypes[filetype]}

        builder = request.args.get('builder', [None])[0]

        svgdata = self.makesvg("Unknown", leftText="Image Error")
        if builder is not None and builder in status.getBuilderNames():
            # get the last build result from this builder
            build = status.getBuilder(builder).getBuild(b)
            if build is not None:
                result = build.getResults()
                svgdata = self.makesvg(results.Results[result],
                                       results.Results[result])
            else:
                svgdata = self.makesvg("No builds", leftText="Image Error")
        else:
            svgdata = self.makesvg("Invalid builder", leftText="Image Error")

        data['image'] = str(svgdata)
        if filetype == "png":
            data['image'] = cairosvg.svg2png(svgdata)

        return data

    def textwidth(self, text):
        surface = cairo.SVGSurface(None, 1280, 200)
        cr = cairo.Context(surface)
        cr.select_font_face(self.fontFace,
                            cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(self.fontSize)
        return cr.text_extents(text)[2]

    def makesvg(self, righttext, status=None, leftText=None, leftColor=None):
        rightColor = "#9f9f9f"  # Grey
        if status in self.colorScheme:
            rightColor = self.colorScheme[status]

        if leftText is None:
            leftText = self.leftText
        if leftColor is None:
            leftColor = self.leftColor

        left = {
            "color": leftColor,
            "text": leftText,
            "width": self.textwidth(self.leftText)
        }
        right = {
            "color": rightColor,
            "text": righttext,
            "width": self.textwidth(righttext)
        }

        template = self.env.get_template(self.templateName)
        return template.render(left=left, right=right)
