from typing import List, Tuple, TypedDict


class SoundComponentConfig(TypedDict):
    name: str
    offset: float
    cutoff: float


class PlapGroupConfig(TypedDict):
    sound_components: List[SoundComponentConfig]
    interpolable_path: str
    ref_keyframe_time: str
    offset: float
    min_pull_out: float
    min_push_in: float
    time_ranges: List[Tuple[str, str]]
    pattern_string: str
