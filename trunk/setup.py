#!/usr/bin/env python

# Dev2 - pair programming development tool
# Copyright (C) 2005-2006 Alexandre Saint <stalst@gmail.com>

# This file is part of Dev2.

# Dev2 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# Dev2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import time
from distutils.core import setup

import dev2lib

VERSION = dev2lib.__version__ + "-" + time.strftime("%Y%m%d%H%M%S")
AUTHOR = dev2lib.__author__
AUTHOR_EMAIL = dev2lib.__author_email__

setup(name='dev2',
        version=VERSION,
        description='pair programming tool',
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=AUTHOR,
        maintainer_email=AUTHOR_EMAIL,
        url='http://dev2.berlios.de',
        scripts=[],
        packages=['dev2lib',
                  'dev2lib.net',
                  'dev2lib.tests',
                  ],
        package_dir={},
        package_data={},
        )
