from pathlib import Path

from app.scene import load_scene
from app.semantics import (
    apply_labels,
    load_labels,
)


SCENE_DIR = Path(
    "data/modelnet_eval_scenes"
)


def main():

    all_passed = True

    for scene_number in range(
        1,
        4,
    ):

        scene_path = (
            SCENE_DIR
            / f"scene_{scene_number}.ply"
        )

        labels_path = (
            SCENE_DIR
            / (
                f"scene_{scene_number}"
                "_labels.json"
            )
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
            + "=" * 70
        )

        print(
            f"MODELNET SCENE "
            f"{scene_number}"
        )

        print(
            "=" * 70
        )


        print(
            f"Detected objects: "
            f"{len(scene.objects)}"
        )


        for obj in scene.objects:

            print(
                f"{obj.object_id:10} "
                f"{str(obj.label):18} "
                f"points={obj.point_count:4} "
                f"dims="
                f"{obj.dimensions.round(3).tolist()}"
            )


        if len(
            scene.objects
        ) != 5:

            all_passed = False

            print(
                "FAIL: expected 5 objects."
            )

        else:

            print(
                "PASS: detected "
                "5 objects."
            )


    print(
        "\n"
        + "=" * 70
    )

    if all_passed:

        print(
            "ALL MODELNET SCENES PASSED"
        )

    else:

        print(
            "ONE OR MORE SCENES FAILED"
        )


if __name__ == "__main__":
    main()