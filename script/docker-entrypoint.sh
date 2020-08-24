#!/bin/bash
#====================================
# @file: docker-entrypoint.sh
# @brief Docker entry point
#
# Copyright (C) 2020 Stephen G. Tuggy and other vsUTCS contributors
#
# This file is part of Vega Strike: Upon the Coldest Sea ("vsUTCS").
#
# vsUTCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# vsUTCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with vsUTCS.  If not, see <https://www.gnu.org/licenses/>.


set -e

script/build
if ! [ -z "$TRAVIS_TAG" ]
then
    script/package
fi
