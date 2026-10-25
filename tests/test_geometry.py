from pathlib import Path

from app.scene import load_scene
from app.semantics import (
    apply_labels,
    find_object_by_label,
    load_labels,
)
from app.tools.geometry import (
    can_pass_through_opening,
    distance_between_objects,
    surface_distance_between_objects,
)


SCENE_DIR = Path(
    "data/modelnet_eval_scenes"
)


def load_scene_number(
    number: int,
):

    scene_path = (
        SCENE_DIR
        / f"scene_{number}.ply"
    )

    labels_path = (
        SCENE_DIR
        / f"scene_{number}_labels.json"
    )

    scene = load_scene(
        scene_path
    )

    labels = load_labels(
        labels_path
    )

    return apply_labels(
        scene,
        labels,
    )


def get_id(
    scene,
    label,
):

    return find_object_by_label(
        scene,
        label,
    )


def test_centroid_distance_positive():

    scene = load_scene_number(
        1
    )

    table_id = get_id(
        scene,
        "table",
    )

    stool_id = get_id(
        scene,
        "stool",
    )

    result = (
        distance_between_objects(
            scene,
            table_id,
            stool_id,
        )
    )

    assert result > 0


def test_surface_distance_non_negative():

    scene = load_scene_number(
        1
    )

    table_id = get_id(
        scene,
        "table",
    )

    stool_id = get_id(
        scene,
        "stool",
    )

    result = (
        surface_distance_between_objects(
            scene,
            table_id,
            stool_id,
        )
    )

    assert result >= 0


def test_stool_passes_through_doorway():

    scene = load_scene_number(
        1
    )

    stool_id = get_id(
        scene,
        "stool",
    )

    doorway_id = get_id(
        scene,
        "doorway_opening",
    )

    result = (
        can_pass_through_opening(
            scene,
            stool_id,
            doorway_id,
        )
    )

    assert result["fits"] is True


def test_cabinet_fails_scene_1():

    scene = load_scene_number(
        1
    )

    cabinet_id = get_id(
        scene,
        "cabinet",
    )

    doorway_id = get_id(
        scene,
        "doorway_opening",
    )

    result = (
        can_pass_through_opening(
            scene,
            cabinet_id,
            doorway_id,
        )
    )

    assert result["fits"] is False


def test_cabinet_passes_scene_3():

    scene = load_scene_number(
        3
    )

    cabinet_id = get_id(
        scene,
        "cabinet",
    )

    doorway_id = get_id(
        scene,
        "doorway_opening",
    )

    result = (
        can_pass_through_opening(
            scene,
            cabinet_id,
            doorway_id,
        )
    )

    assert result["fits"] is True