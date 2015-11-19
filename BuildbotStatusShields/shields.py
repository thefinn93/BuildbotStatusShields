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

    defaults = {
        "left_text": "Build Status",
        "left_color": "#555",
        "template_name": "badge.svg.j2",
        "font_face": "DejaVu Sans",
        "font_size": 11,
        "color_scheme": {
            "exception": "#007ec6",  # blue
            "failure": "#e05d44",    # red
            "retry": "#007ec6",      # blue
            "skipped": "a4a61d",     # yellowgreen
            "success": "#4c1",       # brightgreen
            "unknown": "#9f9f9f",    # lightgrey
            "warnings": "#dfb317"    # yellow
        }
    }
    leftText = None
    leftColor = None
    templateName = None
    fontFace = None
    fontSize = None
    colorScheme = defaults['color_scheme']

    env = jinja2.Environment(loader=jinja2.ChoiceLoader([
        jinja2.PackageLoader('BuildbotStatusShields'),
        jinja2.FileSystemLoader('templates')
        ]))

    def __init__(self, webstatus, left_text=None, left_color=None,
                 template_name=None, font_face=None, font_size=None,
                 color_scheme=None):
        self.webstatus = webstatus
        self.left_text = left_text or self.defaults['left_text']
        self.left_color = left_color or self.defaults['left_color']
        self.template_name = template_name or self.defaults['template_name']
        self.font_face = font_face or self.defaults['font_face']
        self.font_size = font_size or self.defaults['font_size']
        self.color_scheme = color_scheme or self.defaults['color_scheme']

    def getChild(self, *_):
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
        build_number = int(request.args.get('number', [-1])[0])

        # branch
        branch = request.args.get('branch', [''])[0]

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

        builder_name= request.args.get('builder', [None])[0]

        svgdata = self.makesvg("Unknown", left_text="Image Error")
        if builder_name is not None and builder_name in status.getBuilderNames():
			builder = status.getBuilder(builder_name)
			#get the last build from this branch:
			if branch:
				number = builder.nextBuildNumber - 1
				while number > 0:
					build = builder.getBuildByNumber(number)
					if branch in [ss.branch for ss in build.getSourceStamps()]:
						break
					number -= 1
				if number > 0:
					build_number = number
		 	if not branch or build_number > 0:
				# get the last build result from this builder
				build = builder.getBuild(build_number)
				if build is not None:
					result = build.getResults()
					svgdata = self.makesvg(results.Results[result],
							   results.Results[result], left_text=self.left_text + ": " + branch)
				else:
					svgdata = self.makesvg("No builds", left_text="Image Error")
        else:
            svgdata = self.makesvg("Invalid builder", left_text="Image Error")

        data['image'] = str(svgdata)
        if filetype == "png":
            data['image'] = cairosvg.svg2png(svgdata)

        return data

    def textwidth(self, text):
        """Calculates the width of the specified text.
        """
        surface = cairo.SVGSurface(None, 1280, 200)
        ctx = cairo.Context(surface)
        ctx.select_font_face(self.font_face,
                             cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(self.font_size)
        return ctx.text_extents(text)[2]

    def makesvg(self, right_text, status=None, left_text=None,
                left_color=None):
        """Renders an SVG from the template, using the specified data
        """
        right_color = "#9f9f9f"  # Grey
        if status in self.color_scheme:
            right_color = self.color_scheme[status]

        left_text = left_text or self.left_text
        left_color = left_color or self.left_color

        left = {
            "color": left_color,
            "text": left_text,
            "width": self.textwidth(left_text)
        }
        right = {
            "color": right_color,
            "text": right_text,
            "width": self.textwidth(right_text)
        }

        template = self.env.get_template(self.template_name)
        return template.render(left=left, right=right)
