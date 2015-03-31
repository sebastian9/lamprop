# vim:fileencoding=utf-8
# Copyright © 2015 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# $Date$
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

"""Rich Text Format output routines for lamprop."""

__version__ = '$Revision$'[11:-2]

import sys


def out(lam, eng, mat):
    """Rich Text Format main output function."""
    hdr = r"{\rtf1\ansi\ansicpg1252\deff0{\fonttbl{\f0\froman\fcharset0 " \
          r"Times New Roman;}{\f1\fnil\fcharset0 GreekC;}" \
          r"{\f2\fnil\fcharset0 Times New Roman;}}"
    print(hdr)  # RTF header
    if eng:
        _engprop(lam)
    if mat:
        _matrices(lam, not eng)
    print('}')  # Closing brace


def _engprop(l):
    """Prints the engineering properties in Rich Text Format."""
    print("Generated by lamprop {0}\\par".format(__version__))
    print("laminate: {0}\\par".format(l.name))
    s = "thickness: {0:.2f} mm, density: {1:4.2f} g/cm\\'b3\\par"
    print(s.format(l.thickness, l.ρ))
    s = "fiber volume fraction: {0:.1f}%, fiber weight fraction: {1:.1f}%\\par"
    print(s.format(l.vf*100, l.wf*100))
    s = "laminate weight: {0:.0f} g/m\\'b2, " \
        "resin consumption: {1:.0f} g/m\\'b2\\par"
    print(s.format(l.fiber_weight+l.resin_weight, l.resin_weight))
    rhdr = r"\trowd\trgaph20\trpaddl20\trpaddr20\trpaddfl3\trpaddfr3" \
           r"\cellx567\cellx1701\cellx2694\cellx3544\cellx9104\pard" \
           r"\intbl\sa200\sl276\slmult1"
    print(rhdr)
    thdr = r"num\cell weight\cell angle\cell vf\cell fiber\cell\row"
    print(thdr)
    s = "{0}\\cell {1:g}\\cell {3:g}\\cell {3:g}\\cell {4}\\cell\\row"
    for ln, la in enumerate(l.layers):
        print(rhdr)
        print(s.format(ln+1, la.fiber_weight, la.angle, la.vf, la.fiber.name))
    print("\\pard E_x  = {0:.0f} MPa\\par".format(l.Ex))
    print("E_y  = {0:.0f} MPa\\par".format(l.Ey))
    print("G_xy = {0:.0f} MPa\\par".format(l.Gxy))
    print("\\f1 n\\f0 _xy = {0:7.5f}\\par".format(l.νxy))
    print("\\f1 n\\f0 _yx = {0:7.5f}\\par".format(l.νyx))
    p = "\\f1 a\\f0 _x = {0:9.4g} K\\lang1043\\f2\\u713?\\'b9\\lang19\\f0 , " \
        "\\f1 a\\f0 _y = {1:9.4g} K\\lang1043\\f2\\u713?\\'b9\\lang19\\f0\\par"
    print(p.format(l.αx, l.αy))


def _matrices(l, printheader):
    """Prints the ABD and abd matrices Rich Text Format tables."""
    if printheader is True:
        print("Generated by lamprop {0}\\par".format(__version__))
        print("laminate: {0}\\par".format(l.name))
    print("Stiffness (ABD) matrix:\\lang1031\\par")
    matstr = "\\trowd\\trgaph108\\trleft-108\\trbrdrl\\brdrs\\brdrw10 " \
             "\\trbrdrr\\brdrs\\brdrw10 \\trpaddl108\\trpaddr108\\trpaddfl3" \
             "\\trpaddfr3 \\clbrdrl\\brdrw10\\brdrs \\cellx1427\\cellx2962" \
             "\\cellx4497\\cellx6032\\cellx7568\\clbrdrr\\brdrw10\\brdrs " \
             "\\cellx9104\\pard\\intbl\\fs22 {0:.4e}\\cell {1:.4e}\\cell " \
             "{2:.4e}\\cell {3:.4e}\\cell {4:.4e}\\cell {5:.4e}\cell\\row"
    for n in range(6):
        m = matstr.format(l.ABD[n, 0], l.ABD[n, 1], l.ABD[n, 2],
                          l.ABD[n, 3], l.ABD[n, 4], l.ABD[n, 5])
        print(m.replace('e+00', ''))
    print("\\pard\\sa200 Compliance (abd) matrix:\\par")
    for n in range(6):
        m = matstr.format(l.abd[n, 0], l.abd[n, 1], l.abd[n, 2],
                          l.abd[n, 3], l.abd[n, 4], l.abd[n, 5])
        print(m.replace('e+00', ''))
    print(r"\pard\sa200\sl276\slmult1\par")
