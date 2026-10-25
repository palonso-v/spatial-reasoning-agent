from pathlib import Path

from app.scene import load_scene
from app.semantics import (
    apply_labels,
    load_labels,
)


SCENE_PATH = Path(
    "data/modelnet_scene.ply"
)

LABELS_PATH = Path(
    "data/modelnet_scene_labels.json"
)


def main():

    scene = load_scene(
        SCENE_PATH
    )

    labels = load_labels(
        LABELS_PATH
    )

    scene = apply_labels(
        scene,
        labels,
    )


    print(
        "=" * 70
    )

    print(
        "MODELNET SCENE SEGMENTATION CHECK"
    )

    print(
        "=" * 70
    )


    print(
        f"Objects detected: "
        f"{len(scene.objects)}"
    )


    for obj in scene.objects:

        print(
            f"\n{obj.object_id}"
        )

        print(
            f"  label: "
            f"{obj.label}"
        )

        print(
            f"  points: "
            f"{obj.point_count}"
        )

        print(
            f"  centroid: "
            f"{obj.centroid.round(3).tolist()}"
        )

        print(
            f"  dimensions: "
            f"{obj.dimensions.round(3).tolist()}"
        )

        print(
            f"  min_bound: "
            f"{obj.min_bound.round(3).tolist()}"
        )

        print(
            f"  max_bound: "
            f"{obj.max_bound.round(3).tolist()}"
        )


    print(
        "\n"
        + "=" * 70
    )


    if len(scene.objects) == 5:

        print(
            "PASS: "
            "DBSCAN detected exactly "
            "5 objects."
        )

    else:

        print(
            "WARNING: "
            f"Expected 5 objects, "
            f"but DBSCAN detected "
            f"{len(scene.objects)}."
        )


if __name__ == "__main__":
    main()