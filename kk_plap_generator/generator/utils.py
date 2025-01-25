import os
import typing
import xml.etree.ElementTree as et

from kk_plap_generator.generator.plap_generator import PlapGenerator


def generate_plaps(
    ref_single_file_path: str, groups: typing.List[typing.Dict[str, typing.Any]]
):
    xml_tree = et.ElementTree()
    xml_tree.parse(ref_single_file_path)
    plaps: typing.Dict[str, et.Element] = {}
    output: typing.List[str] = []

    for group in groups:
        plap_generator = PlapGenerator(**group)
        output.append(
            f"Generating plap for {plap_generator.plap_names} with pattern '{plap_generator.pattern_string}'"
        )
        print(output[-1])
        sfx_node, frame_count, first_last_frames = plap_generator.generate_plap_xml(
            xml_tree
        )
        for plap_folder in list(sfx_node):
            arr = plaps.get(plap_folder.get("alias"))
            if arr is None:
                output.append(
                    f"{plap_folder.get('alias')}:: Generated {frame_count} keyframes from time {first_last_frames[0]} to {first_last_frames[1]}"
                )
                print(output[-1])
                plaps[plap_folder.get("alias")] = plap_folder
            else:
                output.append(
                    f"{plap_folder.get('alias')}:: Adding {frame_count} keyframes from time {first_last_frames[0]} to {first_last_frames[1]}"
                )
                print(output[-1])
                for child in list(plap_folder):
                    arr.append(child)

    for plap_folder in list(plaps.values()):
        tree = et.ElementTree(et.Element("root"))
        tree.getroot().append(plap_folder)
        filename = os.path.join(
            os.path.dirname(ref_single_file_path), f"{plap_folder.get('alias')}.xml"
        )
        tree.write(filename)
        output.append(f"> Generated '{filename}'")
        print(output[-1])

    return output
