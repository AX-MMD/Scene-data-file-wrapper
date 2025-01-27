import os
import sys
import traceback

import toml

from kk_plap_generator import settings
from kk_plap_generator.generator.utils import generate_plaps

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <single_file_path>")
        sys.exit(1)

    ref_single_file_path = sys.argv[1]

    if not os.path.isfile(ref_single_file_path):
        raise FileNotFoundError(f"The path '{ref_single_file_path}' is not valid.")
    if not os.path.isfile(settings.CONFIG_FILE):
        raise FileNotFoundError(
            f"Missing '{settings.CONFIG_FILE}' in '{settings.CONFIG_FOLDER}'"
        )

    with open(settings.CONFIG_FILE, "r") as file:
        groups = toml.load(file).get("plap_group")

    if not isinstance(groups, list):
        raise ValueError(
            "You must define each group of parameters under a [[plap_group]] tag"
        )

    try:
        generate_plaps(ref_single_file_path, groups)
    except Exception:
        traceback.print_exc()
    finally:
        input("Press Enter to exit...")
        exit()
