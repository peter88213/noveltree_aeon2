"""Synchronize Aeon Timeline 2 and yWriter

Version @release
Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import argparse
import os
from pathlib import Path

from novxlib.config.configuration import Configuration
from novxlib.novx_globals import _
from novxlib.ui.set_icon_tk import set_icon
from novxlib.ui.ui import Ui
from novxlib.ui.ui_tk import UiTk
from nvaeon2lib.aeon2_converter import Aeon2Converter

SUFFIX = ''
APPNAME = 'nv_aeon2'
SETTINGS = dict(
    narrative_arc='Narrative',
    property_description='Description',
    property_notes='Notes',
    property_moonphase='Moon phase',
    role_location='Location',
    role_item='Item',
    role_character='Participant',
    type_character='Character',
    type_location='Location',
    type_item='Item',
    color_section='Red',
    color_event='Yellow',
)
OPTIONS = dict(
    add_moonphase=False,
    lock_on_export=False,
)


def run(sourcePath, silentMode=True, installDir='.'):
    if silentMode:
        ui = Ui('')
    else:
        ui = UiTk(f'{_("Synchronize Aeon Timeline 2 and novelibre")} @release')
        set_icon(ui.root, icon='aLogo32')

    #--- Try to get persistent configuration data
    sourceDir = os.path.dirname(sourcePath)
    if not sourceDir:
        sourceDir = '.'
    iniFileName = f'{APPNAME}.ini'
    iniFiles = [f'{installDir}/{iniFileName}', f'{sourceDir}/{iniFileName}']
    configuration = Configuration(SETTINGS, OPTIONS)
    for iniFile in iniFiles:
        configuration.read(iniFile)
    kwargs = {'suffix': SUFFIX}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)
    converter = Aeon2Converter()
    converter.ui = ui

    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Synchronize Aeon Timeline 2 and yWriter',
        epilog='')
    parser.add_argument('sourcePath',
                        metavar='Sourcefile',
                        help='The path of the aeonzip or novx file.')

    parser.add_argument('--silent',
                        action="store_true",
                        help='suppress error messages and the request to confirm overwriting')
    args = parser.parse_args()
    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.novxlib/{APPNAME}/config'
    except:
        installDir = '.'
    run(args.sourcePath, args.silent, installDir)
