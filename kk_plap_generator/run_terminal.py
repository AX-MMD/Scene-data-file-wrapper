import os
import sys
import traceback

from kk_plap_generator import settings
from kk_plap_generator.generator.utils import generate_plaps

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <single_file_path>")
        sys.exit(1)

    ref_single_file_path = sys.argv[1]

    try:
        generate_plaps(ref_single_file_path)
    except Exception:
        traceback.print_exc()
    finally:
        input("Press Enter to exit...")
        exit()
