from typing import List
from xml.etree import ElementTree as et

import pytest

from kk_plap_generator.generator.plap_generator import (
    KeyframeReference,
    PlapGenerator,
    keyframe_get,
)


@pytest.fixture
def plap_generator():
    return PlapGenerator(
        interpolable_path="path/to/interpolable",
        ref_keyframe_time="00:01.00",
        offset=0.0,
        min_pull_out=0.2,
        min_push_in=0.2,
        time_ranges=[("00:00.00", "00:10.00")],
        pattern_string="V",
        plap_folder_names=["Plap1", "Plap2", "Plap3", "Plap4"],
        template_path="path/to/template.xml",
    )


@pytest.fixture
def keyframes_sets():
    r = {
        "simple": [
            et.Element("keyframe", time="0.0", valueX="0", valueY="0.2", valueZ="0"),
            et.Element(
                "keyframe", time="0.2", valueX="0", valueY="0.1", valueZ="0"  # reference
            ),  
            et.Element("keyframe", time="0.4", valueX="0", valueY="0.2", valueZ="0"),
            et.Element("keyframe", time="0.6", valueX="0", valueY="0.1", valueZ="0"),
            et.Element("keyframe", time="0.8", valueX="0", valueY="0.2", valueZ="0"),
        ],
        "under_push": [
            et.Element("keyframe", time="0.0", valueX="0", valueY="0.2", valueZ="0"),
            et.Element(
                "keyframe", time="0.2", valueX="0", valueY="0.1", valueZ="0"  # reference
            ),  
            et.Element("keyframe", time="0.4", valueX="0", valueY="0.2", valueZ="0"),
            et.Element("keyframe", time="0.6", valueX="0", valueY="0.12", valueZ="0"),
            et.Element("keyframe", time="0.8", valueX="0", valueY="0.2", valueZ="0"),
            et.Element("keyframe", time="1.0", valueX="0", valueY="0.15", valueZ="0"),
            et.Element("keyframe", time="1.2", valueX="0", valueY="0.2", valueZ="0"),
            et.Element("keyframe", time="1.4", valueX="0", valueY="0.18", valueZ="0"),
            et.Element("keyframe", time="1.6", valueX="0", valueY="0.2", valueZ="0"),
            et.Element("keyframe", time="1.8", valueX="0", valueY="0.19", valueZ="0"),
        ],
        "over_push": [
            et.Element("keyframe", time="0.0", valueX="0", valueY="0.2", valueZ="0"),
            et.Element("keyframe", time="0.2", valueX="0", valueY="0.1", valueZ="0"),
            et.Element("keyframe", time="0.4", valueX="0", valueY="0.2", valueZ="0"),
            et.Element("keyframe", time="0.6", valueX="0", valueY="0.08", valueZ="0"),
            et.Element("keyframe", time="0.8", valueX="0", valueY="0.2", valueZ="0"),
        ],
        "under_pull": [
            et.Element("keyframe", time="0.0", valueX="0", valueY="0.1", valueZ="0"),
            et.Element("keyframe", time="0.2", valueX="0", valueY="0.0", valueZ="0"),
            et.Element("keyframe", time="0.3", valueX="0", valueY="0.1", valueZ="0"),
            et.Element("keyframe", time="0.35", valueX="0", valueY="0.0", valueZ="0"),
            et.Element("keyframe", time="0.4", valueX="0", valueY="0.08", valueZ="0"),
            et.Element("keyframe", time="0.6", valueX="0", valueY="0.0", valueZ="0"),
            et.Element("keyframe", time="0.8", valueX="0", valueY="0.05", valueZ="0"),
            et.Element("keyframe", time="1.0", valueX="0", valueY="0.0", valueZ="0"),
            et.Element("keyframe", time="1.2", valueX="0", valueY="0.02", valueZ="0"),
            et.Element("keyframe", time="1.4", valueX="0", valueY="0.0", valueZ="0"),
            et.Element("keyframe", time="1.6", valueX="0", valueY="0.01", valueZ="0"),
            et.Element("keyframe", time="1.8", valueX="0", valueY="0.0", valueZ="0"),
        ],
        "over_pull": [
            et.Element("keyframe", time="0.0", valueX="0", valueY="0.1", valueZ="0"),
            et.Element("keyframe", time="0.2", valueX="0", valueY="0.0", valueZ="0"),
            et.Element("keyframe", time="0.4", valueX="0", valueY="0.1", valueZ="0"),
            et.Element("keyframe", time="0.6", valueX="0", valueY="0.0", valueZ="0"),
            et.Element("keyframe", time="0.8", valueX="0", valueY="0.12", valueZ="0"),
            et.Element("keyframe", time="1.0", valueX="0", valueY="0.0", valueZ="0"),
        ],
    }
    return r


def make_reference(keyframes):
    return KeyframeReference(
        node=keyframes[1],
        time=keyframes[1].get("time"),
        valueX=keyframe_get(keyframes[1], "valueX"),
        valueY=keyframe_get(keyframes[1], "valueY"),
        valueZ=keyframe_get(keyframes[1], "valueZ"),
        axis="valueY",
        out_direction=1,
        estimated_pull_out=abs(
            keyframe_get(keyframes[1], "valueY") - keyframe_get(keyframes[2], "valueY")
        ),
    )


def test_get_keyframe_times_with_empty_keyframes(plap_generator):
    keyframe_times = plap_generator.get_keyframe_times([], None)
    expected_times: List[float] = []
    assert keyframe_times == expected_times


@pytest.mark.parametrize(
    "min_pull_out, min_push_in",
    [
        (0.0, 0.0),
        (0.2, 0.0),
        (0.0, 0.2),
        (0.2, 0.2),
        (0.5, 0.0),
        (0.0, 0.5),
        (0.5, 0.5),
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 0.5),
        (0.5, 1.0),
        (1.0, 1.0),
    ],
)
def test_simple(min_pull_out, min_push_in, plap_generator, keyframes_sets):
    plap_generator.min_pull_out = min_pull_out
    plap_generator.min_push_in = min_push_in
    keyframe_times = plap_generator.get_keyframe_times(
        keyframes_sets["simple"], make_reference(keyframes_sets["simple"])
    )
    expected_times = [0.2, 0.6]
    assert keyframe_times == expected_times


@pytest.mark.parametrize(
    "min_push_in, expected_times",
    [
        (1.0, [0.2]),
        (0.8, [0.2, 0.6]),
        (0.5, [0.2, 0.6, 1.0]),
        (0.2, [0.2, 0.6, 1.0, 1.4]),
        (0.0, [0.2, 0.6, 1.0, 1.4, 1.8]),
    ],
)
def test_under_push(plap_generator, keyframes_sets, min_push_in, expected_times):
    plap_generator.min_push_in = min_push_in
    keyframe_times = plap_generator.get_keyframe_times(
        keyframes_sets["under_push"], make_reference(keyframes_sets["under_push"])
    )
    assert keyframe_times == expected_times


@pytest.mark.parametrize(
    "min_pull_out, min_push_in",
    [
        (0.0, 0.0),
        (0.2, 0.0),
        (0.0, 0.2),
        (0.2, 0.2),
        (0.5, 0.0),
        (0.0, 0.5),
        (0.5, 0.5),
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 0.5),
        (0.5, 1.0),
        (1.0, 1.0),
    ],
)
def test_over_push(plap_generator, keyframes_sets, min_pull_out, min_push_in):
    plap_generator.min_push_in = min_push_in
    plap_generator.min_pull_out = min_pull_out
    keyframe_times = plap_generator.get_keyframe_times(
        keyframes_sets["over_push"], make_reference(keyframes_sets["over_push"])
    )
    expected_times = [0.2, 0.6]
    assert keyframe_times == expected_times


@pytest.mark.parametrize(
    "min_pull_out, expected_times",
    [
        (1.0, [0.2, 0.35]),
        (0.8, [0.2, 0.35, 0.6]),
        (0.5, [0.2, 0.35, 0.6, 1.0]),
        (0.2, [0.2, 0.35, 0.6, 1.0, 1.4]),
        (0.0, [0.2, 0.35, 0.6, 1.0, 1.4, 1.8]),
    ],
)
def test_under_pull(plap_generator, keyframes_sets, min_pull_out, expected_times):
    plap_generator.min_pull_out = min_pull_out
    plap_generator.min_push_in = 0.0
    keyframe_times = plap_generator.get_keyframe_times(
        keyframes_sets["under_pull"], make_reference(keyframes_sets["under_pull"])
    )
    assert keyframe_times == expected_times


@pytest.mark.parametrize(
    "min_pull_out, min_push_in",
    [
        (0.0, 0.0),
        (0.2, 0.0),
        (0.0, 0.2),
        (0.2, 0.2),
        (0.5, 0.0),
        (0.0, 0.5),
        (0.5, 0.5),
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 0.5),
        (0.5, 1.0),
        (1.0, 1.0),
    ],
)
def test_over_pull(plap_generator, keyframes_sets, min_pull_out, min_push_in):
    plap_generator.min_pull_out = min_pull_out
    plap_generator.min_push_in = min_push_in
    keyframe_times = plap_generator.get_keyframe_times(
        keyframes_sets["over_pull"], make_reference(keyframes_sets["over_pull"])
    )
    expected_times = [0.2, 0.6, 1.0]
    assert keyframe_times == expected_times
