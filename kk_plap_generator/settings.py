import os
import sys

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # sets the sys._MEIPASS attribute to the path of the bundle.
    WORKDIR = os.path.dirname(sys.executable)
else:
    # If the application is run as a script, use the directory of the script.
    WORKDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

PACKAGE_DIR = os.path.join(WORKDIR, "kk_plap_generator")
CONFIG_FOLDER = os.path.join(WORKDIR, "configs")
CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.toml")
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_FOLDER, "reference.toml")
TEMPLATE_FOLDER = os.path.join(WORKDIR, "resources")
TEMPLATE_FILE = os.path.join(TEMPLATE_FOLDER, "template.xml")
