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

"""Qt-5 Styleable Component Test Kit.

This application displays Qt-5 compliant widgets with a live preview of edits
made to the desired stylesheet. This program is currently intended to be used
as a standalone application, not a library; although future releases may
offer more features.

Example:
	Simply using ``qt5-style-test.py /path/to/my/stylesheet`` at a terminal
	should incur the loading of the application. Any edits made to the
	stylesheet specified will be viewable while the application is running.


Todo::
	* Finish implementing *QToolTip*, currently having issues and can't
	get it to display properly.
	* Finish implementing the horizontal QScrollBar instance so I can cover
	both horizontal and vertical states since the stylesheets allow using
	those as selectors for applying different styles.
"""


__all__ = [
	"PySide2StyleTestWidget"
]
__author__ = "Ruby Allison Rose (aka: M3TIOR)"
__version__ = "0.9.3"


# Import every widget from Qt5 since we'll be using one of each.
# NOTE:
#	As an important reminder, while PyQt5 and PySide2 are nearly identical,
#	we'll be using PySide2 because it's actively supported by the core Qt
#	team, available for enterprise use, and will most likely be the quickest
#	to see new C++ features bubble to the surface in python.
from PySide2.QtWidgets import *
from PySide2.QtCore import *

# Standard Library Imports
#from threading import Thread, Event
import sys, io


_qt_supported_html_subset = """
<html>
	<head>
		<title>Title Element</title>
		<meta >
	</head>
	<body>
		<h1>Level 1 Heading</h1>
		<h2>Level 2 Heading</h2>
		<h3>Level 3 Heading</h3>
		<h4>Level 4 Heading</h4>
		<h5>Level 5 Heading</h5>
		<h6>Level 6 Heading</h6>
		<span>spanned content!</span>
		<p>But more importantly... This is a paragraph...<br>
			<b>b</b>, <strong>strong</strong>
			<i>i</i>, <em>em</em>
			<s>strikethough</s>, <u>underline</u>
			<a href="https://www.whereeverthefuckdoyouthinkyouregoing.xxx">
				https://www.happysunshineland.com/this/is/a/hyperlink
			</a> <br>
			<var>var</var>, <code>code</code>, <samp>samp</samp>, <kbd>kbd</kbd>,
			<small>small</small>, <sup>sup</sup>, <sub>sub</sub>,
			<blockquote>blockquote</blockquote>, <cite>cite</cite>,
			<address>address</address>, <pre>pre</pre>, <dfn>dfn</dfn>
			<div>
				... and this is <i>div<i>ided from the strictly text portion!
				<ol>
					<li>Ordered</li>
					<li>List</li>
					<li>Items</li>
				</ol>
				<ul>
					<li>Unordered</li>
					<li>List</li>
					<li>Items</li>
				</ul>
				<dl>
					<dt>this</dt><dd>The element we're currently encapsulated within is a dl!</dd>
					<dt>dt</dt><dd>A key term: key terms in a dl</dd>
					<dt>dd</dt><dd>what that key term means... what you're reading rn...</dd>
				</dl>
			</div>
			<table>
				<tr><th>th</th><th>inside</th><th>a</th><th>tr</th></tr>
				<tr><td>td</td><td>inside</td><td>a</td><td>tr</td></tr>
			</table>
			following this is a horizontal line / separator...
			<hr>
			following this is a line break <br>
			<img href=""><!--Add temporary, generated image here-->
		</p>
	</body>
</html>
"""
"""str: HTML document with all QT supported tags excluding those not in
compliance with the latest HTML specification "HTML5".
For said list, refer to https://doc.qt.io/qt-5/richtext-html-subset.html

HTML 5 Compliance Checklist:
 - [x] `html` / `qt`, `head`, `body`
 - [x] `meta`, `title`
 - [x] `h1` - `h6`
 - [x] `b`, `i`, `s`, `u`, `a`
 - [x] `em`, `strong`, `var`, `code`, `samp`, `kbd`
 - [x] `small`, `sup`, `sub`, `blockquote`, `cite`, `address`, `pre`
 - [x] `dd`, `dfn`, `dl`, `dt`
 - [x] `ol`, `ul` & `li`
 - [x] `table`, `td`, `th`, `tr`
 - [x] `span`, `div`, `p`
 - [x] `br`, `hr`, `img`

Unconventional / Unused Elements:
 - `nobr`, `thead`, `tbody`, `tfoot`

Depricated Elements:
 - `big`, `center`, `font`, `tt`
"""


def _generic_action():
	"""A simple function that does nothing. Serves the purpose of duping no-op
	QT buttons/ actions that are for the sake of display rather than execution"""
	pass

class Error(Exception):
	"""Generic base class error for this module."""
	pass

class CommandLineError(Error):
	"""Any error occuring because the CLI was used improperly.

	Args:
        message (str): Human readable string describing the exception.
        argument (str): The name of the command line argument which caused the error.

    Attributes:
        message (str): Human readable string describing the exception.
        argument (str): The name of the command line argument which caused the error.
	"""
	def __init__(self, argument, message):
		self.argument = argument
		self.message = message


class PySide2StyleTestWidget(QMainWindow):
	"""This Application's Qt User Interface. Displays all of QT-5's styleable
	elements so modders can actively see their changes to their styles take
	effect.

	Args::
		stylesheet (str): The path to the stylesheet you want to test.

	Implemented Core Qt Elements (with Active States) Checklist::
		 - [x] *QAbstractScrollArea*
		 - [x] *QCheckBox*
		 - [x] *QComboBox*
		 - [x] *QDockWidget*
		 - [x] *QGroupBox*
		 - [x] *QHeaderView*
		 - [x] *QLabel*
		 - [x] *QLineEdit*
		 - [x] *QListView* / *QListWidget*
		 - [x] *QMainWindow*
		 - [x] *QMenu*
		 - [x] *QMenuBar*
		 - [x] *QProgressBar*
		 - [x] *QPushButton*
		 - [x] *QRadioButton*
		 - [x] *QScrollBar*
		 - [x] *QSizeGrip*
		 - [x] *QSlider*
		 - [x] *QSpinBox*
		 - [x] *QSplitter*
		 - [x] *QStatusBar*
		 - [x] *QTabWidget* and *QTabBar*
		 - [x] *QTableView* / *QTableWidget*
		 - [x] *QToolBar*
		 - [x] *QToolBox*
		 - [x] *QToolButton*
		 - [x] *QTreeView* / *QTreeWidget*
		 - [x] *QTreeWidgetItem*

	Unnecessary Elements::
	  	 - *QFrame* is inherited by all widgets that can have a frame.
	 	   Which is most of them, however I'm specifically noting *QGroupBox*.
	"""
	# NOTE: leaving this here in case I decide to try reimplementing async
	#_threads = []
	#
	#def _terminate_threads(self):
	#	"""Notifies all the threads spawned by this class to terminate and
	#	waits for them to finish."""
	#
	#	# Then wait for all of them to catch up before we try and exit()
	#	for t in self._threads:
	#		t.join(1)

	def _init_QStatusBar_preview(self):
		status = QStatusBar()

		return status

	def _init_QMenuBar_preview(self, statusbar):
		bar = QMenuBar()
		menu = QMenu("Menu")
		submenu = QMenu("Submenu")

		# These are just to see if I can style the actions based on what they do.
		bar.addAction("Event", _generic_action)
		bar.addAction("Check").setCheckable(True)
		bar.addAction("Status").triggered.connect(
			lambda : statusbar.showMessage("Mainbar Action Click", 10000))
		bar.addSeparator()

		menu.addSection("Events")
		menu.addAction("Menu Check").setCheckable(True)
		menu.addAction("Menu Event", _generic_action)
		menu.addAction("Menu Status").triggered.connect(
			lambda : statusbar.showMessage("Menu Action Click", 10000))

		submenu.addAction("Submenu Event", _generic_action)
		submenu.addAction("Menu Status").triggered.connect(
			lambda : self.statusbar.showMessage("Submenu Action Click", 10000))
		submenu.addSection("Checkables")
		submenu.addAction("Submenu Check").setCheckable(True)

		menu.addMenu(submenu)
		bar.addMenu(menu)

		return bar

	def _init_QCheckBox_preview(self):
		checklayout = QHBoxLayout()

		nocheck = QCheckBox("Unchecked")
		nocheck.setTristate(False)
		nocheck.setCheckState(Qt.CheckState.Unchecked)

		ischecked = QCheckBox("Checked")
		ischecked.setTristate(False)
		ischecked.setCheckState(Qt.CheckState.Checked)

		partial = QCheckBox("Partial")
		partial.setTristate(True)
		partial.setCheckState(Qt.CheckState.PartiallyChecked)

		checklayout.addWidget(ischecked)
		checklayout.addWidget(partial)
		checklayout.addWidget(nocheck)

		return checklayout

	def _init_QRadioButton_preview(self):
		radiolayout = QHBoxLayout()

		toggled = QRadioButton("checked")
		untoggled = QRadioButton("unchecked")

		toggled.click()

		radiolayout.addWidget(toggled)
		radiolayout.addWidget(untoggled)

		return radiolayout

	def _init_QDockWidget_preview(self):
		# the dock's background display is a non issue, the styling only
		# applies to the window's docked titlebar display.
		dockhtml = """
		<h3 style="text-align: center">QLabel Widget</h3><br>
		<p style="text-align: center;">
			QDockWidget's Styles only<br>
			affect the docking bar, <br>
			not it's child widgets.
		</p>
		"""
		docker = QDockWidget("Dock Widget")
		docker.setWidget(QLabel(dockhtml))
		#docklayout = QVBoxLayout()

		return docker

	def _init_QLineEdit_preview(self):
		lineeditwidget = QLineEdit("Default Text")

		return lineeditwidget

	def _init_QListWidget_preview(self):
		listwidget = QListWidget()

		for each in ("List", "all", "the", "things!"):
			listwidget.addItem(each)

		return listwidget

	def _init_QTabelWidget_preview(self):
		# Also QHeaderView here because they're used in QTableView and QTreeView
		tablewidget = QTableWidget(5, 5)

		for x, y in ((x, y) for x in range(5) for y in range(5)):
			tablewidget.setItem(x, y, QTableWidgetItem("(%d, %d)" % (x, y)))

		tablewidget.setHorizontalHeaderItem(0, QTableWidgetItem("QHeaderView Objects"))
		tablewidget.setItem(0,0, QTableWidgetItem("QTableView Objects"))

		return tablewidget

	def _init_QGroupBox_preview(self):
		groupboxwidget = QGroupBox("Group Label")
		groupboxlayout = QVBoxLayout()

		groupboxlayout.addWidget(QLabel("Oh holy crap guys..."))
		groupboxlayout.addWidget(QLabel("(UwU)"))
		groupboxlayout.addWidget(QLabel("We're grouped together!"))

		groupboxwidget.setLayout(groupboxlayout)

		return groupboxwidget

	def _init_QComboBox_preview(self):
		comboboxwidget = QComboBox()

		comboboxwidget.addItems([str(x) for x in range(5)])

		return comboboxwidget

	def _init_QProgressBar_preview(self):
		progressbarwidget = QProgressBar()
		progressbarwidget.setValue(50)

		#def timed_progression():
		#	# I hate (with stuff: jargon) stupid extra whitespace
		#	# NOTE:
		#	#	I'm just guessing this is where the segfaults I'm getting
		#	#	are comming from. No telling yet exactly but I think it
		#	#	started happening when I implemented the multithreading
		#	#	solution for the progress bar. Will look into it later.
		#	#
		#	#	Couldn't find a way to circumvent segfault caused by this
		#	#	function, abandoning for now.
		#	#
		#	#	It's definitely caused by a redraw or paint event.
		#
		#
		#	while not self.close.wait(timeout=3):
		#
		#		cval = progressbarwidget.value()
		#		if (cval < progressbarwidget.maximum()):
		#			progressbarwidget.setValue(cval + 1)
		#		else:
		#			progressbarwidget.reset()
		#
		#progress_t = Thread(
		#	target=timed_progression,
		#	name="progression_bar_inc"
		#)
		#progress_t.start()
		#self._threads.append(progress_t)

		return progressbarwidget

	def _init_QSliderBox_preview(self):
		sliderlayout = QHBoxLayout()

		Vslider = QSlider(Qt.Orientation.Vertical)
		Hslider = QSlider(Qt.Orientation.Horizontal)

		# Thank god the slider tick positions aren't stylable lol
		# don't have to worry about them.

		sliderlayout.addWidget(Vslider)
		sliderlayout.addWidget(Hslider)

		return sliderlayout

	def _init_QPushButton_preview(self):
		pushbutton = QPushButton("Push My Button!")

		return pushbutton

	def _init_QSplitter_preview(self):
		Vsplitter = QSplitter(Qt.Orientation.Vertical)
		Hsplitter = QSplitter(Qt.Orientation.Horizontal)

		Hsplitter.addWidget(QLabel("Pull"))
		Hsplitter.addWidget(QLabel("us"))
		Vsplitter.addWidget(Hsplitter)
		Vsplitter.addWidget(QLabel("apart!"))
		Vsplitter.resize(100, 300) # Doesn't work... Oh well...
		# I just wanna get this done. I'm sooooo tired.

		return Vsplitter

	def _init_QSpinBox_preview(self):
		spinner = QSpinBox()
		#spinner.setRange(0, 100)

		return spinner

	def _init_QTabWidget_preview(self):
		tabs = QTabWidget()
		tabs.addTab(QLabel("Tab Window"), "Uno")
		tabs.addTab(QLabel("Tab Window"), "Dos")
		tabs.addTab(QLabel("Tab Window"), "Tres")

		return tabs

	def _init_QScrollBar_preview(self):
		# Since the style can influence both horizontal and vertical states
		# differently we'll need to display one of each. This is Vertical.
		pass

	def _init_QToolBox_preview(self):
		tools = QToolBox()
		tools.addItem(QLabel("Display Me"), "I'm")
		tools.addItem(QLabel("<b>Display Me</b>"), "A")
		tools.addItem(QLabel("<i>Display Me</i>"), "FREAKING")
		tools.addItem(QLabel("<b><i>Display Me</i></b>"), "TOOLBOX!")

		return tools

	def _init_QToolBar_preview(self):
		toolbar = QToolBar()
		toolbar.addAction("QToolBars")
		toolbar.addAction("Contain")
		toolbar.addAction("QToolButtons")

		return toolbar

	def _init_QToolTip_preview(self):
		#TODO FINISH THIS, HAVING ISSUES

		tooltip = QLabel("<h2>Hover over here to see the QToolTip</h2>")
		tooltip.setToolTip("I'm the QToolTip!")
		tooltip.setToolTipDuration(1000)
		#tooltip.setWhatsThis("I'm the QToolTip!")

		return tooltip

	def _init_QTreeView_preview(self):
		treeview = QTreeWidget()
		treeview.setColumnCount(1)

		# Create a numeral tree representing hundreds, tens, and ones
		# for users to open and test their styling with. May use a more complex
		# format in later versions to accomidate for more styling options.
		hundreds = [ QTreeWidgetItem(["item: %i00"% (h)]) for h in range(10) ]
		for h, hundred in enumerate(hundreds):
			tens = [ QTreeWidgetItem(["item: %i%i0"% (h,t)]) for t in range(10) ]
			for t, ten in enumerate(tens):
				ones = [ QTreeWidgetItem(["item: %i%i%i"% (h,t,o)]) for o in range(10) ]
				ten.addChildren( ones )
			hundred.addChildren( tens )
		treeview.addTopLevelItems( hundreds )

		return treeview

	def _init_rich_text_preview(self):
		richtext = QTextEdit(_qt_supported_html_subset)
		richtext.setReadOnly(True) #disabled editing

		return richtext

	def __init__(self, stylesheet):
		"""Construct the GUI in memory."""
		QMainWindow.__init__(self)

		# IOBase in python3 provides __del__ meta function by default
		# upon variable destruction to close the file so we don't have to.
		try:
			self._stylesheet = open(stylesheet, "r")
		except (OSError) as e:
			print("%s `%s`" %(e.strerror, e.filename), file=sys.stderr)
			sys.exit(e.errno)

		def refresh_stylesheet():
			print("refreshing stylesheet!")
			self._stylesheet.seek(0)
			self.setStyleSheet(self._stylesheet.read())

		self.watcher = QFileSystemWatcher()
		self.watcher.addPath(stylesheet)
		# BUG: must use q_watcher.addPath because otherwise
		# passing the stylesheet through the class init
		# results in the file not actually being watched.
		self.watcher.fileChanged.connect(refresh_stylesheet)

		# QStatusBar must come before QMenuBar because QMenuBar hooks onto it.
		statusbar = self._init_QStatusBar_preview()
		self.setStatusBar(statusbar)
		self.setMenuBar(self._init_QMenuBar_preview(statusbar))
		self.addToolBar(self._init_QToolBar_preview())
		self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._init_QDockWidget_preview())

		# Define core layout features.
		tabs = QTabWidget()
		basicview = QFormLayout()
		#basicview.setSizeConstraint(QLayout.SetMinAndMaxSize)

		# We have to assign our container layout to a widget before we can
		# apply any kind of scroll area because the scroll area object
		# expects a widget and not a layout.
		scrollcontent = QWidget()
		scrollcontent.setLayout(basicview)

		# Configure our scroll area to scroll vertically and pass our container
		basicview_scrollarea = QScrollArea() # Inherits QAbstractScrollArea
		basicview_scrollarea.setWidget(scrollcontent)
		# always have it visible so we can see how styling changes it.
		basicview_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		basicview_scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
		basicview_scrollarea.setWidgetResizable(True)

		# Add all of our Qt Widget previews to the basic main window.
		basicview.addRow("QCheckBoxes", self._init_QCheckBox_preview())
		basicview.addRow("QRadioButton", self._init_QRadioButton_preview())
		basicview.addRow("QPushButton", self._init_QPushButton_preview())
		basicview.addRow("QLineEdit", self._init_QLineEdit_preview())
		basicview.addRow("QTabWidget", self._init_QTabWidget_preview())
		basicview.addRow("QSpinBox", self._init_QSpinBox_preview())
		basicview.addRow("QProgressBar", self._init_QProgressBar_preview())
		basicview.addRow("QSlider", self._init_QSliderBox_preview())
		basicview.addRow("QSplitter", self._init_QSplitter_preview())
		basicview.addRow("QComboBox", self._init_QComboBox_preview())
		basicview.addRow("QGroupBox", self._init_QGroupBox_preview())
		basicview.addRow("QListWidget", self._init_QListWidget_preview())
		basicview.addRow("QTableView", self._init_QTabelWidget_preview())
		basicview.addRow("QToolBox", self._init_QToolBox_preview())
		basicview.addRow("QToolTip", self._init_QToolTip_preview())
		#basicview.addRow("QTreeView", self._init_QTreeView_preview())

		# And finally, add our basic, and more complicated views into their
		# spots on the tabbed view in order of least to most complex.
		tabs.addTab(basicview_scrollarea, "Simple Elements")
		tabs.addTab(self._init_rich_text_preview(), "Rich Text")
		tabs.addTab(self._init_QTreeView_preview(), "QTreeView")

		self.setCentralWidget(tabs)

		# call at least once after the application loads incase
		# the stylesheet is never modified or has an error.
		refresh_stylesheet()
