import copy
import math
import sys, os, traceback
import typing

from xml.etree import ElementTree as et
import toml

from plap_generator import PlapGenerator


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <single_file_path>")
        sys.exit(1)
    
    ref_single_file_path = sys.argv[1]
    workdir = os.path.dirname(os.path.abspath(__file__))
    config_name = "config.toml"
    config_path = os.path.join(workdir, config_name)
    
    if not os.path.isfile(ref_single_file_path):
        print(f"The path '{ref_single_file_path}' is not valid.")
        sys.exit(1)
    if not os.path.isfile(config_path):
        print(f"Missing '{config_name}' in '{workdir}'")
        sys.exit(1)
    try:
        with open(config_path, "r") as file:
            groups = toml.load(file).get("plap_group")

        if not isinstance(groups, list):
            raise ValueError("You must define each group of parameters under a [[plap_group]] tag")
        
        xml_tree = et.ElementTree()
        xml_tree.parse(ref_single_file_path)
        plaps = {}

        for group in groups:
            plap_generator = PlapGenerator(**group)
            print(f"Generating plap for {plap_generator.plap_names} with pattern '{plap_generator.pattern_string}'")
            sfx_node, frame_count, first_last_frames = plap_generator.generate_plap_xml(xml_tree)
            for plap_folder in list(sfx_node):
                arr = plaps.get(plap_folder.get("alias"))
                if arr is None:
                    print(f"{plap_folder.get('alias')}:: Generated {frame_count} keyframes from time {first_last_frames[0]} to {first_last_frames[1]}")
                    plaps[plap_folder.get("alias")] = plap_folder
                else:
                    print(f"{plap_folder.get('alias')}:: Adding {frame_count} keyframes from time {first_last_frames[0]} to {first_last_frames[1]}")
                    for child in list(plap_folder):
                        arr.append(child)

        for plap_folder in list(plaps.values()):
            tree = et.ElementTree(et.Element("root"))
            tree.getroot().append(plap_folder)
            filename = os.path.join(
                os.path.dirname(ref_single_file_path), 
                f"{plap_folder.get('alias')}.xml"
            )
            tree.write(filename)
            print(f"Generated '{filename}'")
             
    except Exception as e:
        traceback.print_exc()
    finally:
        input("Press Enter to exit...")
        exit()
