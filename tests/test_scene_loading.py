from pathlib import Path

from app.scene import load_scene
from app.semantics import (
    apply_labels,
    load_labels,
)


SCENE_PATH = Path(
    "data/modelnet_eval_scenes/scene_1.ply"
)

LABELS_PATH = Path(
    "data/modelnet_eval_scenes/scene_1_labels.json"
)


def load_test_scene():

    scene = load_scene(
        SCENE_PATH
    )

    labels = load_labels(
        LABELS_PATH
    )

    return apply_labels(
        scene,
        labels,
    )


def test_scene_has_five_objects():

    scene = load_test_scene()

    assert len(
        scene.objects
    ) == 5


def test_expected_labels_present():

    scene = load_test_scene()

    labels = {
        obj.label
        for obj in scene.objects
    }

    assert labels == {
        "table",
        "stool",
        "chair",
        "cabinet",
        "doorway_opening",
    }


def test_objects_have_points():

    scene = load_test_scene()

    for obj in scene.objects:

        assert obj.point_count > 0

        assert len(
            obj.points
        ) == obj.point_count


def test_object_dimensions_are_positive():

    scene = load_test_scene()

    for obj in scene.objects:

        assert (
            obj.dimensions > 0
        ).all()