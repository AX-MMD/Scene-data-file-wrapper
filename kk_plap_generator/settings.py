import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_DIR = os.path.join(PROJECT_DIR, "kk_plap_generator")
CONFIG_FOLDER = os.path.join(PACKAGE_DIR, "configs")
CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.toml")
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_FOLDER, "reference.toml")
TEMPLATE_FOLDER = os.path.join(PACKAGE_DIR, "resources")
TEMPLATE_FILE = os.path.join(TEMPLATE_FOLDER, "template.xml")
