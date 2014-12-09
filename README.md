# BuildBot Status Shields

*For Buildbot Nine, see the nine branch or
[BuildbotStatusShields](https://pypi.python.org/pypi/BuildbotStatusShields) on
PyPI*

[Buildbot](http://buildbot.org) version eight offers build status shields in PNG
form at `/png` from the WebStatus server. However, they look pretty ugly and
there isn't any configuration available. So I made this here thing to allow
expanded use of the status shield/badge/thing.

## Usage

*Note: This whole `bind()` thing feels wrong, I just haven't worked out how to
do it right. Please drop me a note if you wish to enlighten me*

In your `master.cfg` file, use `BuildbotStatusShields.bind(WebStatus)` to bind
to the WebStatus server:

```python
import BuildbotStatusShields as shields

c['status'].append(shields.bind(html.WebStatus(http_port=8010, authz=authz_cfg)))
```

You can pass `bind()` options to change configuration settings. For example:
```python
import BuildbotStatusShields as shields

c['status'].append(shields.bind(html.WebStatus(http_port=8010, authz=authz_cfg), path="shield"))
```

Will make it bind to `/shield.png` and `/shield.svg`. See below for all
configuration options.


When it is configured, run the buildbot master. Badges will be available at
`/badge.svg` and `/badge.png` (by default), and can be passed the following
parameters:

* `builder` (required) - The name of the builder to return the status of
* `number` (optional) - The build number to return the status of. `-1` (default)
returns the most build

## Configuration
There are several options available, here's a quick list that I'll probably
forget to update. Check `shields.py` for the full list:

* `path` - path to bind to. Defaults to `badge` (binds to `/badge.png` and `/badge.svg`)
* `leftText` - the text on the left of the badge. Defaults to "Build Status"
* `leftColor` - the color of the left side of the badge. Defaults to `#555`
* `templateName` - The name to the badge template. Defaults to `badge.svg.j2`
* `fontFace` - The font face to use when rendering the badge. Defaults to `DejaVu Sans`
* `fontSize` - fontsize to use, defaults to 11
* `colorScheme` - a dict of colors to use based on the status. See `__init__.py` for defaults

You can also customize the badge. Simply place an SVG Jinja2 template at
`templates/badge.svg.j2` in the buildbot master folder. Several examples from
[shields.io](http://shields.io) can be found in the `templates/` folder of this
package.
