import os

from python_qt_binding import QtGui

from hyperspyui.smartcolorsvgiconengine import SmartColorSVGIconEngine


here = os.path.abspath(os.path.dirname(__file__))
images_dir = os.path.join(here, '..', 'hyperspyui', 'images')
svg_file = os.path.join(images_dir, 'open.svg')


def test_icon_from_svg(qapp):
    ie = SmartColorSVGIconEngine()
    icon = QtGui.QIcon(ie)
    icon.addFile(svg_file)
