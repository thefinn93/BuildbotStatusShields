#!/usr/bin/env pytho
from shields import *


def bind(webstatus, path="badge"):
    webstatus.putChild("%s.png" % path, ShieldStatusResource(webstatus))
    webstatus.putChild("%s.svg" % path, ShieldStatusResource(webstatus))
    return webstatus
