import os
import re
from typing import Optional, Tuple
from xml.etree import ElementTree as et


def int_to_bytes(number: int) -> bytes:
    # Calculate the minimum number of bytes required to represent the integer
    min_bytes = (number.bit_length() + 7) // 8
    # Convert the integer to a big-endian byte string of the minimum length
    return number.to_bytes(min_bytes, byteorder="big")


def flag_to_int_array(flag: bytes) -> Tuple[int, int]:
    return int.from_bytes(flag[0:1], byteorder="big"), int.from_bytes(
        flag[1:], byteorder="big"
    )


IS_ANIMATION_PATTERN = re.compile(rb'guideObjectPath="(.+)"')


class SceneDataException(Exception):
    pass


class SceneData:

    class ContentError(SceneDataException):
        pass

    class TimelineDoesNotExist(SceneDataException):
        pass

    class MemoryError(SceneDataException):
        pass

    class ValueError(SceneDataException):
        pass

    file_path: str
    timeline_regex: "re.Pattern"
    timeline_status: str
    image_type: Optional[str]

    _duration_pattern = re.compile(rb'duration="([\d\.]+)"')
    _animation_pattern = re.compile(rb'guideObjectPath="([^"]+)"')

    # Timeline data starts with b'timeline[somebytes_I_dont_know]sceneInfo[bytes(length_flag + bit_length_of_data_lenght)][bytes(data_lenght)]'
    # right before the xml data, the known flags must be updated on every change.
    _timeline_length_flag: int = 216

    def __init__(self, file_path: str, timeline_regex: Optional[str] = None):
        self.file_path = file_path
        self.timeline_regex = re.compile(
            timeline_regex
            or rb"timeline.+?sceneInfo(?P<flag>.*?)(?P<data><root\b[^>]*?>.*?</root>)",
            re.DOTALL,
        )
        try:
            with open(file_path, "rb") as filekk:
                self._content = filekk.read()
        except MemoryError:
            raise SceneData.MemoryError(f"File is to big, file.read() failed")

        if not self._is_scene_data():
            raise SceneData.ContentError("Not a scene data file")

        self._cached_timeline: Optional[bytes] = None
        self._timeline_changed = False

        self.timeline_status, self.image_type, self._duration = self._check_timeline()

    @property
    def content_str(self) -> str:
        try:
            return self._content.decode("utf-8", errors="ignore")
        except MemoryError:
            raise SceneData.MemoryError(
                f"File is to big, content.decode('utf-8', errors='ignore') failed"
            )

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def duration(self) -> Optional[float]:
        return self._duration

    @duration.setter
    def duration(self, value: float):

        raise NotImplementedError("Modification of the timeline is not supported (yet)")

        if not self.has_timeline():
            raise SceneData.ValueError("Scene data does not have a timeline")
        elif self.image_type == "static":
            raise SceneData.ValueError(
                "Scene data is Static and does not have a duration"
            )
        elif value <= 0:
            raise SceneData.ValueError("Duration must be greater than 0")
        elif value == self._duration:
            return
        else:
            # replace "duration={value}" by value in the timeline string
            modified_timeline = re.sub(
                self._duration_pattern,
                f'duration="{value}"'.encode("utf-8"),
                self.get_timeline_xml(),
            )
            self.replace_timeline(modified_timeline)
            self._duration = value
        return self

    def get_timeline_info(self) -> Tuple[str, Optional[str], Optional[float]]:
        return self.timeline_status, self.image_type, self.duration

    def get_timeline_xml(self, raise_exception: bool = False) -> Optional[bytes]:
        """
        Raises
        ------
        SceneData.TimelineDoesNotExist
            If raise_exception is True and the timeline data is not found.
        """
        if self._cached_timeline:
            return self._cached_timeline
        else:
            match = self.timeline_regex.search(self._content)
            if match and b"</root>" in match.group("data"):
                self._cached_timeline = match.group("data")
                return self._cached_timeline
            elif raise_exception:
                raise SceneData.TimelineDoesNotExist("Timeline data not found")
            else:
                return None

    def get_timeline_xml_tree(
        self, raise_exception: bool = False
    ) -> Optional[et.ElementTree]:
        xml_str = self.get_timeline_xml(raise_exception=raise_exception)
        return et.ElementTree(et.fromstring(xml_str)) if xml_str else None

    def replace_timeline(self, new_timeline: str):
        """Replace the timeline data with a new one"""

        raise NotImplementedError("Modification of the timeline is not supported (yet)")

        length_flag, timeline_byte_legth = self._get_timeline_byte_vars(new_timeline)

        def replace(match):
            return (
                match.group(0)
                .replace(match.group("data"), new_timeline)
                .replace(match.group("flag"), length_flag + timeline_byte_legth)
            )

        self._content = re.sub(self.timeline_regex, replace, self._content)
        self._cached_timeline = new_timeline

    def has_timeline(self) -> bool:
        return self.timeline_status == "has_timeline"

    def save(self, overwrite: bool = False):
        filename, ext = os.path.splitext(self.file_path)
        if not overwrite and os.path.exists(self.file_path):
            filename = filename + "_new"

        file_path = os.path.join(os.path.dirname(self.file_path), f"{filename}{ext}")
        with open(file_path, "wb") as filekk:
            filekk.write(self._content)

        self.file_path = file_path

    def _get_timeline_byte_vars(self, timeline) -> Tuple[bytes, bytes]:
        """Return the length flag and the timeline byte length"""
        num_bytes = (len(timeline).bit_length() + 7) // 8
        length_flag = (
            self._timeline_length_flag + (num_bytes if num_bytes <= 3 else 3)
        ).to_bytes(1, byteorder="big")
        timeline_byte_length = len(timeline).to_bytes(num_bytes, byteorder="big")
        return length_flag, timeline_byte_length

    def _is_scene_data(self) -> bool:
        """檢查是否為scene data :: Check if the file is a scene data"""
        return (
            os.path.splitext(self.file_path)[1] == ".png" and b"KStudio" in self._content
        )

    def _check_timeline(self) -> Tuple[str, Optional[str], Optional[float]]:
        """
        Returns:
            tuple (timeline_status, image_type, duration)
            timeline_status: "has_timeline", "no_timeline"
            image_type: "animation", "dynamic", "static", None
            duration: float, None
        """
        timeline_xml = self.get_timeline_xml()
        if not timeline_xml:  # Check if there is a timeline
            return "no_timeline", None, None
        elif b"Timeline" not in timeline_xml:
            return "has_timeline", "static", None
        elif match := re.search(self._duration_pattern, timeline_xml):
            if self._animation_pattern.search(timeline_xml):
                # A timeline with a guideObject interpolable is most likely an animation.
                return "has_timeline", "animation", float(match.group(1))
            else:
                # Without a guideObject, it's most likely camera movement, sound effects or alpha/color changes.
                return "has_timeline", "dynamic", float(match.group(1))
        else:
            return "has_timeline", "dynamic", None
