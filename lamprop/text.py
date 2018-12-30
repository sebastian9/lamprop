# file: text.py
# vim:fileencoding=utf-8:ft=python:fdm=marker
# Copyright © 2011-2018 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2011-03-27 13:59:17 +0200
# Last modified: 2018-12-30T12:23:39+0100
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"""Text output routines for lamprop."""

# import sys
from .version import __version__

# Data

_t = ["thickness: {0:.2f} mm, density: {1:4.2f} g/cm³",
      "laminate weight: {0:.0f} g/m², resin consumption: {1:.0f} g/m²",
      "ν_xy = {0:7.5f}",
      "ν_yx = {0:7.5f}",
      "α_x = {0:9.4g} K⁻¹, α_y = {1:9.4g} K⁻¹",
      "    [g/m²]   [°]  [%]"]

# Platforms that don't support UTF-8 get ASCII text.
# enc = sys.stdout.encoding
# if not enc or enc.lower() != 'utf-8':
#     _t = ["thickness: {0:.2f} mm, density: {1:4.2f} g/cm3",
#           "laminate weight: {0:.0f} g/m2, resin consumption: {1:.0f} g/m2",
#           "v_xy = {0:7.5f}",
#           "v_yx = {0:7.5f}",
#           "a_x = {0:9.4g} 1/K, a_y = {1:9.4g} 1/K",
#           "    [g/m2] [deg]  [%]"]


def out(lam, eng, mat):  # {{{1
    """Return the output as a list of lines."""
    lines = []
    if eng:
        lines += engprop(lam)
    if mat:
        lines += matrices(lam, not eng)
    lines.append('')
    return lines


def engprop(l):  # {{{1
    """Return the engineering properties as a plain text table in the form of
    a list of lines."""
    s = "fiber volume fraction: {0:.3g}%, fiber weight fraction: {1:.3g}%"
    lines = [
        "Generated by lamprop {0}".format(__version__),
        "laminate: {0}".format(l.name),
        _t[0].format(l.thickness, l.ρ),
        s.format(l.vf*100, l.wf*100),
        _t[1].format(l.fiber_weight+l.resin_weight, l.resin_weight),
        "num weight angle   vf fiber",
        _t[5]
    ]
    s = "{0:3} {1:6g} {2:5g} {3:4.3g} {4}"
    for ln, la in enumerate(l.layers, start=1):
        lines.append(s.format(ln, la.fiber_weight, la.angle, la.vf*100, la.fiber.name))
    lines += [
        "E_x  = {0:.0f} MPa".format(l.Ex),
        "E_y  = {0:.0f} MPa".format(l.Ey),
        "G_xy = {0:.0f} MPa".format(l.Gxy),
        _t[2].format(l.νxy),
        _t[3].format(l.νyx),
        _t[4].format(l.αx, l.αy)
    ]
    return lines


def matrices(l, header=False):  # {{{1
    """Return the ABD and abd matrices as plain text."""
    if header is True:
        lines = [
            "Generated by lamprop {0}".format(__version__),
            "laminate: {0}".format(l.name)
        ]
    else:
        lines = ["Stiffness (ABD) matrix:"]
    matstr = "|{:< 10.4} {:< 10.4} {:< 10.4} " \
             "{:< 10.4} {:< 10.4} {:< 10.4}|"
    for n in range(6):
        m = matstr.format(l.ABD[n][0], l.ABD[n][1], l.ABD[n][2],
                          l.ABD[n][3], l.ABD[n][4], l.ABD[n][5])
        lines.append(m)
    lines.append("Compliance (abd) matrix:")
    for n in range(6):
        m = matstr.format(l.abd[n][0], l.abd[n][1], l.abd[n][2],
                          l.abd[n][3], l.abd[n][4], l.abd[n][5])
        lines.append(m)
    return lines
