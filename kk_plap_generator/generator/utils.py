import os
import typing
import xml.etree.ElementTree as et

import toml

from kk_plap_generator import settings
from kk_plap_generator.generator.plap_generator import PlapGenerator


def generate_plaps(ref_single_file_path):
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

    xml_tree = et.ElementTree()
    xml_tree.parse(ref_single_file_path)
    plaps: typing.Dict[str, et.Element] = {}

    for group in groups:
        plap_generator = PlapGenerator(**group)
        print(
            f"Generating plap for {plap_generator.plap_names} with pattern '{plap_generator.pattern_string}'"
        )
        sfx_node, frame_count, first_last_frames = plap_generator.generate_plap_xml(
            xml_tree
        )
        for plap_folder in list(sfx_node):
            arr = plaps.get(plap_folder.get("alias"))
            if arr is None:
                print(
                    f"{plap_folder.get('alias')}:: Generated {frame_count} keyframes from time {first_last_frames[0]} to {first_last_frames[1]}"
                )
                plaps[plap_folder.get("alias")] = plap_folder
            else:
                print(
                    f"{plap_folder.get('alias')}:: Adding {frame_count} keyframes from time {first_last_frames[0]} to {first_last_frames[1]}"
                )
                for child in list(plap_folder):
                    arr.append(child)

    for plap_folder in list(plaps.values()):
        tree = et.ElementTree(et.Element("root"))
        tree.getroot().append(plap_folder)
        filename = os.path.join(
            os.path.dirname(ref_single_file_path), f"{plap_folder.get('alias')}.xml"
        )
        tree.write(filename)
        print(f"Generated '{filename}'")
