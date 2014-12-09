# BuildBot Status Shields

[Buildbot](http://buildbot.org) offers build status shields in PNG form at
`/png` from the WebStatus server. However, they look pretty ugly and there isn't
any configuration available. So I made this here thing to allow expanded use of
the status shield/badge/thing.

## Installation

```bash
$ pip install buildbotstatusshields
```

or from this directory

```bash
$ python setup.py install
```

## Usage
In your `master.cfg` file, use `BuildbotStatusShields.bind(WebStatus)` to bind
to the WebStatus server:

```python
import BuildbotStatusShields as shields

c['status'].append(shields.bind(html.WebStatus(http_port=8010, authz=authz_cfg)))
```

Then place a template for the shield you want at `templates/badge.svg.j2`. Some
examples (from [shields.io](http://shields.io)) can be found in the templates
folder of this repository.

You can pass `bind()` options to change configuration settings. For example:
```python
import BuildbotStatusShields as shields

c['status'].append(shields.bind(html.WebStatus(http_port=8010, authz=authz_cfg), path="shield"))
```

Will make it bind to `/shield.png` and `/shield.svg`. See below for all
configuration options.

## Configuration
There are several options available, here's a quick list that I'll probably
forget to update. Check `shields.py` for the full list:

* `path` - path to bind to. Defaults to `badge` (binds to `/badge.png` and `/badge.svg`)
* `leftText` - the text on the left of the badge. Defaults to "Build Status"
* `leftColor` - the color of the left side of the badge. Defaults to `#555`
* `templatePath` - The path to the badge template. Defaults to `templates/badge.svg.j2`
* `fontFace` - The font face to use when rendering the badge. Defaults to `DejaVu Sans`
* `fontSize` - fontsize to use, defaults to 11
* `colorScheme` - a dict of colors to use based on the status. See `__init__.py` for defaults
