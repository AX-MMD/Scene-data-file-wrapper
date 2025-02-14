import copy
import math
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union, cast
from xml.etree import ElementTree as et

from kk_plap_generator import settings
from kk_plap_generator.generator.utils import InfiniteIterator
from kk_plap_generator.models import SoundComponentConfig


class PlapGenerator:
    """
    Generate sound sequences for animations based on a given pattern and keyframe data.

    Parameters
    ----------
    interpolable_path : str
        The path to the interpolable to use as reference for the SFX.
    ref_keyframe_time : str
        The reference keyframe time where the subject is fully inserted.
    offset : float, optional
        Offset in seconds, positive or negative, to adjust the timing of the SFX.
    min_pull_out : float, optional
        Minimum percent distance (0.0 to 1.0) the subject needs to pull away from the contact point before re-enabling plaps.
    min_push_in : float, optional
        Minimum percent distance (0.0 to 1.0) the subject needs to push toward the contact point for a plap to register.
    time_ranges : list of tuple of str, optional
        Optional list of time ranges for the SFX, each range is a pair of strings (MM:SS.SS).
    pattern_string : str, optional
        The pattern string to generate the plap sequence.
    sound_components : list of str, optional
        List of names of the components to use (Those containing the sound items).
        Default is ["Plap1", "Plap2", "Plap3", "Plap4"].
    template_path : str, optional
        Path to the template XML file.

    Attributes
    ----------
    valid_patern_chars : list of str
        Valid characters for the pattern string.

    Methods
    -------
    generate_plap_xml(self, timeline_xml_tree: et.ElementTree) -> et.Element:
        Generates the plap XML nodes based on the given timeline XML tree.
    """

    VALID_PATTERN_CHARS = ["V", "A", "W", "M", "\\", "/"]

    class ReferenceNotFoundError(Exception):
        def __init__(self, time: str):
            self.time = time
            self.message = f"Reference keyframe not found at {time}."
            super().__init__(self.message)

    def __init__(
        self,
        # config file params START ###
        interpolable_path: str,
        ref_keyframe_time: str,
        sound_components: List[SoundComponentConfig],
        offset: float = 0.0,
        min_pull_out: float = 0.2,
        min_push_in: float = 0.8,
        time_ranges: List[Tuple[str, str]] = [],
        pattern_string: str = "V",
        template_path: str = settings.TEMPLATE_FILE,
        # config file params END ###
        # GUI params START ###
        auto_search: bool = True,
        # GUI params END ###
    ):
        # config file params START ###
        self.interpolable_path = interpolable_path
        self.ref_keyframe_time = ref_keyframe_time
        self.offset = float(offset)  # Just in case we receive a string
        self.min_pull_out = float(min_pull_out)
        self.min_push_in = float(min_push_in)
        self.time_ranges = time_ranges
        self.pattern_string = pattern_string.upper()
        for pattern_char in self.pattern_string:
            if pattern_char not in self.VALID_PATTERN_CHARS:
                raise ValueError(
                    f"Invalid pattern {self.pattern_string}, valid characters are {', '.join(self.VALID_PATTERN_CHARS)} or a combination of them."
                )

        self.sound_components: List = sound_components
        self.plap_count = len(sound_components)
        self.template_path = template_path
        # config file params END ###

        # GUI params START ###
        self.auto_search = auto_search
        # GUI params END ###

        self.patterns: Dict[str, List[int]] = self.get_patterns()
        self.sequence = self.generate_sequence(pattern_string)

    @property
    def ref_keyframe_time(self):
        return self._ref_keyframe_time

    @ref_keyframe_time.setter
    def ref_keyframe_time(self, value):
        self._ref_keyframe_time = value
        self._ref_kf_seconds = self._std_time(convert_KKtime_to_seconds(value))

    def get_time_ranges_sec(self) -> List[Tuple[float, float]]:
        if self.time_ranges:
            return [
                (convert_KKtime_to_seconds(tg[0]), convert_KKtime_to_seconds(tg[1]))
                for tg in self.time_ranges
            ]
        else:
            return [(0.0, math.inf)]

    def generate_plap_xml(self, timeline_xml_tree: et.ElementTree):
        # Create the base plap nodes from template
        tree = et.parse(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), self.template_path)
        )

        sfx_node = tree.getroot().find("""interpolableGroup[@name='SFX']""")
        if sfx_node is None:
            raise NodeNotFoundError(
                "interpolableGroup", tag="name", value="SFX", xml_path=self.template_path
            )

        base_plap = sfx_node.find("""interpolable[@alias='Plap']""")
        if base_plap is None:
            raise NodeNotFoundError(
                "interpolable", tag="alias", value="Plap", xml_path=self.template_path
            )

        base_keyframe = base_plap.find("keyframe")
        if base_keyframe is None:
            raise NodeNotFoundError("keyframe", xml_path=self.template_path)
        else:
            base_keyframe.set("value", "false")

        # Remove the template plap from our sfx copy
        for child in list(sfx_node):
            sfx_node.remove(child)

        # Remove the template keyframes from our base plap node
        for child in list(base_plap):
            base_plap.remove(child)

        # Create the patern
        sequence = self.generate_sequence(self.pattern_string)

        # Get the rythm from source single_file, will use parameters from the config to locate the node
        if self.auto_search:
            interpolable = deep_find_interpolable(
                list(timeline_xml_tree.getroot()), self.interpolable_path.split(".")[-1]
            )
        else:
            interpolable = find_interpolable(
                timeline_xml_tree.getroot(), self.interpolable_path
            )

        keyframes = list(interpolable)

        # We find the reference keyframe and directionnal information
        reference = self.get_reference(keyframes)

        keyframe_times = self.get_keyframe_times(keyframes, reference)

        # Create the plap nodes
        for i, sc in enumerate(self.sound_components):
            plap = copy.deepcopy(base_plap)
            plap.set("alias", f"{sc['name']}")
            plap.set("objectIndex", f"{plap.get('objectIndex')}{i + 1}")
            sfx_node.append(plap)

        # Generate the plap keyframes
        plaps = list(sfx_node)
        pattern_iter = InfiniteIterator(sequence)
        for time in keyframe_times:
            i = next(pattern_iter)
            plap = plaps[i]
            pc = self.sound_components[i]
            mute_keyframe = copy.deepcopy(base_keyframe)
            mute_keyframe.set("time", str(time - 0.1 + self.offset + pc["offset"]))
            mute_keyframe.set("value", "false")
            plap.append(mute_keyframe)
            new_keyframe = copy.deepcopy(base_keyframe)
            new_keyframe.set("time", str(time + self.offset + pc["offset"]))
            new_keyframe.set("value", "true")
            plap.append(new_keyframe)
            if pc["cutoff"] < math.inf:
                cutoff_keyframe = copy.deepcopy(base_keyframe)
                cutoff_keyframe.set(
                    "time", str(time + self.offset + pc["offset"] + pc["cutoff"])
                )
                cutoff_keyframe.set("value", "false")
                plap.append(cutoff_keyframe)

        return sfx_node, len(keyframe_times), (keyframe_times[0], keyframe_times[-1])

    def get_keyframe_times(
        self, keyframes: List[et.Element], reference: "KeyframeReference"
    ) -> List[float]:
        keyframe_times = []
        for time_start, time_end in self.get_time_ranges_sec():
            did_plap = False

            for keyframe in keyframes:
                time = self._std_time(keyframe.get("time", 0.0))
                if time <= time_start:
                    continue
                if time > time_end:
                    # Reached the end of the time range
                    break

                value = keyframe_get(keyframe, reference.axis)
                distance = abs(reference.value - value)
                if did_plap:
                    # Only re-enable plapping after a minimum distance is reached
                    if (
                        reference.out_direction == 1
                        and value > reference.value
                        or reference.out_direction == -1
                        and value < reference.value
                    ) and distance >= self._round(  # Round to avoid floating point errors
                        self.min_pull_out * reference.estimated_pull_out
                    ):
                        did_plap = False
                else:
                    if (
                        reference.out_direction == 1
                        and value <= reference.value
                        or reference.out_direction == -1
                        and value >= reference.value
                    ) or distance < self._round(
                        (1.0 - self.min_push_in) * reference.estimated_pull_out
                    ):
                        keyframe_times.append(time)
                        did_plap = True

        return keyframe_times

    def generate_sequence(self, pattern_string: str):
        last_index = len(pattern_string) - 1
        sequence = []
        for p, char in enumerate(pattern_string):
            pattern_chunk = self._get_pattern_for_char(char)
            sequence += pattern_chunk
            if p != last_index:
                sequence.append(pattern_chunk[0])

        return sequence

    def is_reference_time(self, time: float):
        return time + 0.00001 >= self._ref_kf_seconds >= time - 0.00001

    def get_reference(self, node_list: List[et.Element]) -> "KeyframeReference":
        # We itterate instead of an exact search because the "time" attribute can have a higher precision than what the user can provide.
        reference = None
        ref_index = 0
        for i, keyframe in enumerate(node_list):
            time = self._std_time(keyframe.get("time", 0.0))
            if self.is_reference_time(time):
                ref_index = i
                reference = Keyframe(
                    node=keyframe,
                    time=time,
                    valueX=keyframe_get(keyframe, "valueX"),
                    valueY=keyframe_get(keyframe, "valueY"),
                    valueZ=keyframe_get(keyframe, "valueZ"),
                )
                break

        if reference is None:
            raise PlapGenerator.ReferenceNotFoundError(self.ref_keyframe_time)
        else:
            # Once we found the reference keyframe, we check the next keyframe and calculate the difference between reference and next_keyframe.
            # The axis with the biggest difference will be our axis reference.
            # We also use the difference to determnine the direction of the pull out as 1 or -1.
            next_frame = None
            try:
                next_frame = node_list[ref_index + 1]
            except IndexError:
                raise IndexError("The reference keyframe cannot be the last keyframe.")

            x = keyframe_get(next_frame, "valueX") - reference.valueX
            y = keyframe_get(next_frame, "valueY") - reference.valueY
            z = keyframe_get(next_frame, "valueZ") - reference.valueZ

            if abs(z) < abs(x) > abs(y):
                axis = "valueX"
                out_direction = x / abs(x)
            elif abs(z) < abs(y) > abs(x):
                axis = "valueY"
                out_direction = y / abs(y)
            else:
                axis = "valueZ"
                out_direction = z / abs(z)

            # We then try and estimate the pull out distance by taking the biggest difference between the reference keyframe and (up too) the next 5 keyframes.
            estimated_pull_out = max(
                abs(keyframe_get(node_list[j], axis) - getattr(reference, axis))
                for j in range(ref_index, min(ref_index + 6, len(node_list)))
            )

        return KeyframeReference(
            node=reference.node,
            time=reference.time,
            valueX=reference.valueX,
            valueY=reference.valueY,
            valueZ=reference.valueZ,
            axis=axis,
            out_direction=out_direction,
            estimated_pull_out=estimated_pull_out,
        )

    def get_patterns(self) -> Dict[str, List[int]]:
        # fmt: off
        return {
            "W": [i for i in range(self.plap_count)] \
                + [i for i in range(self.plap_count - 2, int(math.ceil(self.plap_count / 2)) - 1, -1)] \
                + [i for i in range(int(math.ceil(self.plap_count / 2)) - 1, self.plap_count - 1)] \
                + [i for i in range(self.plap_count - 1, 0, -1)],
            "M": [i for i in range(self.plap_count - 1, -1, -1)] \
                + [i for i in range(1, int(math.ceil(self.plap_count / 2)) + 1)] \
                + [i for i in range(int(math.ceil(self.plap_count / 2)) - 1, 0, -1)] \
                + [i for i in range(self.plap_count - 1)],
            "V": [i for i in range(self.plap_count)] + [i for i in range(self.plap_count - 2, 0, -1)],
            "A": [i for i in range(self.plap_count - 1, 0, -1)] + [i for i in range(self.plap_count - 1)],
            "/": [i for i in range(self.plap_count - 1, -1, -1)],
            "\\": [i for i in range(self.plap_count)],
        }
        # fmt: on

    def _get_pattern_for_char(self, pattern_char: str) -> List[int]:
        return self.patterns[pattern_char]

    def _round(self, value: float) -> float:
        return round(value, 5)

    def _std_time(self, time: Union[str, int, float]) -> float:
        return self._round(float(time))


def keyframe_get(keyframe: et.Element, key: str) -> float:
    return float(cast(str, keyframe.get(key)))


@dataclass
class Keyframe:
    node: et.Element
    time: float
    valueX: float
    valueY: float
    valueZ: float


@dataclass
class KeyframeReference(Keyframe):
    axis: str
    out_direction: float
    estimated_pull_out: float

    @property
    def value(self):
        return getattr(self, self.axis)


notfound = et.Element("notfound")


class NodeNotFoundError(Exception):
    def __init__(
        self,
        node_name,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        *args,
        path: Optional[str] = None,
        xml_path: Optional[str] = None,
    ):
        self.node_name = node_name
        self.tag = tag
        self.value = value
        self.path = path
        self.xml_path = xml_path
        self.message = f"Node not found: {self.get_node_string()}"
        super().__init__(self.message, *args)

    def get_node_string(self):
        s = f"<{self.node_name}"
        s += (
            f" {self.tag}{("='" + self.value + "'") if self.value else ''}"
            if self.tag
            else ""
        )
        s += ">"
        return s


def deep_find_interpolable(node_list: List[et.Element], target: str):
    for node in node_list:
        if node.tag == "interpolable" and node.get("alias") == target:
            return node
        else:
            found = deep_find_interpolable(list(node), target)
            if found is not None:
                return found

    return None


def find_interpolable(root: et.Element, target: str) -> et.Element:
    node: et.Element = root
    tag, value, child = convert_string_to_nested_list(target)
    path = []
    while child is not None:
        path.append(value)
        node = node.find(f"""interpolableGroup[@{tag}='{value}']""") or notfound
        if node is notfound:
            raise NodeNotFoundError("interpolableGroup", tag, value, path=".".join(path))

        tag, value, child = child

    node = node.find(f"""interpolable[@{tag}='{value}']""") or notfound
    if node is notfound:
        raise NodeNotFoundError("interpolable", tag, value)

    return node


def convert_string_to_nested_list(s: str):
    parts = s.split(".")
    nested_list = None
    for part in reversed(parts):
        nested_list = ["alias" if nested_list is None else "name", part, nested_list]
    return nested_list


def convert_KKtime_to_seconds(time_str: str) -> float:
    """Convert a time string of format 'MM:SS.SS' to seconds in float"""
    minutes, seconds_fraction = time_str.split(":")
    seconds, fraction = seconds_fraction.split(".")
    total_seconds = int(minutes) * 60 + int(seconds) + float(f"0.{fraction}")
    return total_seconds
