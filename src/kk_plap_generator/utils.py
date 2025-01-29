from typing import Dict, List, Tuple, TypedDict

import toml


class PlapGroupConfig(TypedDict):
    plap_folder_names: List[str]
    interpolable_path: str
    ref_keyframe_time: str
    offset: float
    min_pull_out: float
    min_push_in: float
    time_ranges: List[Tuple[str, str]]
    pattern_string: str


def load_config_file(path: str) -> Dict[str, List[PlapGroupConfig]]:
    with open(path, "r", encoding="UTF-8") as f:
        return toml.load(f)
