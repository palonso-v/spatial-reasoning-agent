from pathlib import Path

from app.scene import load_scene
from app.semantics import (
    apply_labels,
    load_labels,
)


SCENE_DIR = Path(
    "data/eval_scenes"
)


def main():
    for scene_number in range(
        1,
        4,
    ):
        name = (
            f"scene_{scene_number}"
        )

        scene_path = (
            SCENE_DIR
            / f"{name}.ply"
        )

        labels_path = (
            SCENE_DIR
            / f"{name}_labels.json"
        )

        scene = load_scene(
            scene_path
        )

        labels = load_labels(
            labels_path
        )

        scene = apply_labels(
            scene,
            labels,
        )

        print(
            "\n"
            + "=" * 60
        )

        print(
            name.upper()
        )

        print(
            "=" * 60
        )

        print(
            f"Objects detected: "
            f"{len(scene.objects)}"
        )

        for obj in scene.objects:
            print(
                f"{obj.object_id:10} "
                f"{str(obj.label):18} "
                f"centroid="
                f"{obj.centroid.round(2).tolist()} "
                f"dims="
                f"{obj.dimensions.round(2).tolist()}"
            )


if __name__ == "__main__":
    main()