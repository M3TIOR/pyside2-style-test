# pyside2-style-test
[![Build Status](https://travis-ci.org/M3TIOR/pyside2-style-test.svg?branch=master)](https://travis-ci.org/M3TIOR/pyside2-style-test)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/M3TIOR/pyside2-style-test/blob/master/LICENSE)

A Qt-5 live updating styleable component test kit.

This application displays Qt-5 compliant widgets with a live preview of edits
made to the desired stylesheet. It's currently intended to be used
as a standalone application, not a library; although future releases may
offer more features. I did make the functionality of this program available
as a Qt Widget if you'd like to extend the functionality or use it in another
program. So have at it.

The reason I decided to make this was to solve a issue I was running into
trying to develop a [QSS stylesheet][QSS] system variant of the
[Purplest Inc Theme for Github's Atom Text Editor][Purplest]. For some reason,
the Qt development team doesn't have any tools like this available to the
open source community. At least none that I could find, even in the private
sector! I found one on Sourceforge that was windows a exclusive release, and
that's it. I guess the Qt Core development team may not see it as useful
considering I only found one blog detailing the amazing feature that is
Qt supporting a CSS variant. It even hosted some stylesheets! But as amazing as
it is that I found someone who understands the beauty of CSS, it was tainted by the
fact that I was still out of a way to reliably preview my Qt stylesheets.

Now I hope nobody else has to feel that way.

### How to use:
Simply using ```pyside2-style-test.py /path/to/my/stylesheet``` at a terminal
should incur the loading of the application. Any edits made to the
stylesheet specified will be viewable while the application is running.

Alternatively, if you've downloaded this from PyPI using pip, then you
can ```pyside2-style-test /path/to/my/stylesheeet``` from anywhere.

### In the future:
Beyond version 1.0.0 leading into version 2.0.0, I do plan on making this
at least a little more modular and to optimize the way widgets are previewed.
I will eventually draft and upload a diagram of my future GUI. Just not today.
I've gotta dig myself out of my project hole first. So if this is something
you find helpful, look forward to that.

[Purplest]: https://github.com/PurplestInc/purplest-inc-syntax
[QSS]: https://doc.qt.io/qt-5/stylesheet-examples.html
