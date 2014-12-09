# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
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

"""Simple PNG build status banner
"""

import os

from twisted.web import resource

from buildbot.status import results

import cairocffi as cairo
from Jinja2 import Template  # For now, might not use this


class ShieldStatusResource(resource.Resource):
    """Describe a single builder result as a PNG image
    """

    isLeaf = True
    status = None

    def __init__(self, status):
        self.status = status

    def getChild(self, name, request):
        """Just return itself
        """
        return self

    def render(self, request):
        """
        Renders a given build status as PNG file

        We don't care about pre or post paths here so we skip them, we only
        care about parameters passed in the URL, those are:

        :param builder: the builder name
        :param size: the size of the PNG than can be 'small', 'normal', 'large'
        :returns: a binary PNG
        """

        data = self.content(request)
        request.setHeader('content-type', data['content_type'])
        request.setHeader('cache-control', 'no-cache')
        request.setHeader(
            'content-disposition', 'inline; filename="%s"' % (data['filename'])
        )
        return data['image']

    def content(self, request):
        """Renders the image shield
        """
        # size not supported yet
        # size = request.args.get('size', ['normal'])[0]
        # if size not in ('small', 'normal', 'large'):
        #     size = 'normal'

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
                'content_type': mimetypes[filetype]
                }
        builder = request.args.get('builder', [None])[0]

        svgdata = self.makesvg("Error")
        if builder is not None and builder in self.status.getBuilderNames():
            # get the last build result from this builder
            build = self.status.getBuilder(builder).getBuild(b)
            if build is not None:
                result = build.getResults()
                svgdata = self.makesvg(results.Results[result])

        data['image'] = svgdata
        if filetype is not "svg":
            data['image'] = cairosvg.svg2png(svgdata)

        return data

    def textwidth(self, text, fontsize=14):
        surface = cairo.SVGSurface('undefined.svg', 1280, 200)
        cr = cairo.Context(surface)
        cr.select_font_face('Arial',
                            cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(fontsize)
        return cr.text_extents(text)[2]

    def makesvg(self, righttext, rightcolor, lefttext="Build Status",
                leftcolor="#555", style="plastic"):
        template = Template(open("templates/%s" % style).read()
        left = {
            "color": leftcolor,
            "text": lefttext,
            "width": self.textwidth(lefttext, 11)
        }
        right = {
            "color": rightcolor,
            "text": righttext,
            "width": self.textwidth(righttext, 11)
        }
        return template.render(left=left, right=right)
