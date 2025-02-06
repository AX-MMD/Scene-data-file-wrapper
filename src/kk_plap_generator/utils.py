import os
import typing
import xml.etree.ElementTree as et
from typing import Dict, List

import toml

from kk_plap_generator.generator.plap_generator import PlapGenerator
from kk_plap_generator.models import PlapGroupConfig


def load_config_file(path: str) -> Dict[str, List[PlapGroupConfig]]:
    with open(path, "r", encoding="UTF-8") as f:
        return toml.load(f)


def generate_plaps(ref_single_file_path: str, groups: typing.List[PlapGroupConfig]):
    xml_tree = et.ElementTree()
    xml_tree.parse(ref_single_file_path)
    plaps: typing.Dict[str, et.Element] = {}
    output: typing.List[str] = []

    for group in groups:
        plap_generator = PlapGenerator(**group)
        names = (f"{sc['name']}" for sc in plap_generator.sound_components)
        output.append(
            f"Generating plap for ({' '.join(names)})\nUsing pattern '{plap_generator.pattern_string}'"
        )
        print(output[-1])
        sfx_node, frame_count, first_last_frames = plap_generator.generate_plap_xml(
            xml_tree
        )
        for sound_component in list(sfx_node):
            arr = plaps.get(sound_component.get("alias"))
            if arr is None:
                output.append(
                    f"{sound_component.get('alias')}:: Generated {frame_count} keyframes from time {first_last_frames[0]} to {first_last_frames[1]}"
                )
                print(output[-1])
                plaps[sound_component.get("alias")] = sound_component
            else:
                output.append(
                    f"{sound_component.get('alias')}:: Adding {frame_count} keyframes from time {first_last_frames[0]} to {first_last_frames[1]}"
                )
                print(output[-1])
                for child in list(sound_component):
                    arr.append(child)
        output.append("==================================================================")
        print(output[-1])

    for sound_component in list(plaps.values()):
        tree = et.ElementTree(et.Element("root"))
        tree.getroot().append(sound_component)
        filename = os.path.join(
            os.path.dirname(ref_single_file_path), f"{sound_component.get('alias')}.xml"
        )
        tree.write(filename)
        output.append(f"> Generated '{filename}'")
        print(output[-1])

    return output
