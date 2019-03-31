#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Ruby Allison Rose (aka: M3TIOR)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE
"""This module is responsible specifically for making command line functions
provided by this library available to setuptools. However, it's left in the
public scope just in case someone decides they want to do more with it.
"""


from . import PySide2StyleTestWidget as _PySide2StyleTestWidget
from . import __version__, CommandLineError
from PySide2.QtWidgets import QApplication

import argparse
import sys


def main(*argv, test_widget=_PySide2StyleTestWidget):
	"""The main application of this library. Made available as a function
	for other scripts to extend it's function.

	Args:
		*argv: The command line arguments to supply to the program supplied as
			strings. If this is empty, `sys.argv` is used.
		test_widget (:obj:`QWidget`, optional): Any PySide2 compliant widget
			that will be used as the main display window once the program is
			initalized. By default this is an instance of `PySide2StyleTestWidget`.
	"""
	# NOTE:
	# 	Even though this won't be using any alternative UIs I'm going to
	#	write it as if there will be one. Just so it's done and I can
	#	copy and paste this code elsewhere if I want to.

	# Init qt-app as global so it can be used to parse arguments and collect
	# opperational data which can be used by other UI implementations.
	qt_application = QApplication(list(*argv) if len(argv) else sys.argv)
	qt_application.setApplicationName("pyside2-style-test")
	qt_application.setApplicationVersion(__version__)

	parser = argparse.ArgumentParser(
		description="""A QSS preview script.""",
		epilog="""NOTE: if specifying a stylesheet via the command line using
		the --stylesheet option, be aware that it will be overriden by whatever
		stylesheet you load after the file prompt or by the positional argument.
		One of which is required for the program to run."""
	)
	parser.add_argument("--file",
		help="the stylesheet you want to test",
		required=True,
	)

	arguments = parser.parse_args(qt_application.arguments()[1:])

	GUI = test_widget(arguments.file)
	GUI.show()

	# Hand off control of signal processing to Qt. This function is
	# blocking and only returns when the user exits from the GUI.
	#
	# XXX:
	#	(ONLY APPLIES TO MULTITHREADING AND THE REFS ARE ONLY
	#	INACCESSABLE INSIDE THE ASYNC FUNCTIONS)
	#
	#	This function must be called within the function that initializes
	#	all our graphical elements. Otherwise their references are destroyed
	#	by the trash collector and any other threads we made using those
	#	will crash.
	qt_application.exec_()


def _main():
	"""Main function alias for command line setuptools script"""
	main(sys.argv)
	sys.exit()
