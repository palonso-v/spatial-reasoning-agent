import json
from pathlib import Path

import open3d as o3d


OUTPUT_DIR = Path("data/eval_scenes")


SCENES = {
    "scene_1": [
        {
            "label": "table",
            "size": (1.6, 1.0, 0.8),
            "position": (0.0, 0.0, 0.0),
            "color": (0.8, 0.5, 0.2),
        },
        {
            "label": "box",
            "size": (0.6, 0.6, 0.6),
            "position": (2.0, 0.2, 0.0),
            "color": (1.0, 0.2, 0.2),
        },
        {
            "label": "chair",
            "size": (0.8, 0.8, 1.0),
            "position": (3.8, 1.8, 0.0),
            "color": (0.2, 0.4, 1.0),
        },
        {
            "label": "cabinet",
            "size": (1.2, 0.7, 1.8),
            "position": (5.8, 0.2, 0.0),
            "color": (0.2, 0.8, 0.3),
        },
        {
            "label": "doorway_opening",
            "size": (1.0, 0.35, 2.1),
            "position": (7.8, 1.8, 0.0),
            "color": (0.8, 0.8, 0.8),
        },
    ],

    "scene_2": [
        {
            "label": "chair",
            "size": (0.8, 0.8, 1.0),
            "position": (0.0, 0.2, 0.0),
            "color": (0.2, 0.4, 1.0),
        },
        {
            "label": "table",
            "size": (1.6, 1.0, 0.8),
            "position": (2.0, 0.0, 0.0),
            "color": (0.8, 0.5, 0.2),
        },
        {
            "label": "box",
            "size": (0.9, 0.9, 0.9),
            "position": (5.0, 1.5, 0.0),
            "color": (1.0, 0.2, 0.2),
        },
        {
            "label": "doorway_opening",
            "size": (0.8, 0.35, 2.0),
            "position": (7.5, 0.2, 0.0),
            "color": (0.8, 0.8, 0.8),
        },
        {
            "label": "cabinet",
            "size": (1.4, 0.8, 1.8),
            "position": (9.5, 1.5, 0.0),
            "color": (0.2, 0.8, 0.3),
        },
    ],

    "scene_3": [
        {
            "label": "box",
            "size": (1.2, 1.2, 1.2),
            "position": (0.0, 1.5, 0.0),
            "color": (1.0, 0.2, 0.2),
        },
        {
            "label": "cabinet",
            "size": (1.0, 0.8, 1.5),
            "position": (2.5, 0.0, 0.0),
            "color": (0.2, 0.8, 0.3),
        },
        {
            "label": "table",
            "size": (1.6, 1.0, 0.8),
            "position": (5.0, 0.0, 0.0),
            "color": (0.8, 0.5, 0.2),
        },
        {
            "label": "chair",
            "size": (0.8, 0.8, 1.0),
            "position": (7.0, 0.2, 0.0),
            "color": (0.2, 0.4, 1.0),
        },
        {
            "label": "doorway_opening",
            "size": (1.0, 0.35, 2.1),
            "position": (9.5, 1.5, 0.0),
            "color": (0.8, 0.8, 0.8),
        },
    ],
}


def create_box(
    size,
    position,
    color,
    n_points=1200,
):
    mesh = o3d.geometry.TriangleMesh.create_box(
        width=size[0],
        height=size[1],
        depth=size[2],
    )

    mesh.translate(position)

    cloud = mesh.sample_points_uniformly(
        number_of_points=n_points,
    )

    cloud.paint_uniform_color(
        color
    )

    return cloud


def expected_center_x(item):
    return (
        item["position"][0]
        + item["size"][0] / 2
    )


def generate_scene(
    scene_name,
    objects,
):
    cloud = None

    for item in objects:
        object_cloud = create_box(
            item["size"],
            item["position"],
            item["color"],
        )

        if cloud is None:
            cloud = object_cloud
        else:
            cloud += object_cloud

    ply_path = (
        OUTPUT_DIR
        / f"{scene_name}.ply"
    )

    o3d.io.write_point_cloud(
        str(ply_path),
        cloud,
    )

    # scene.py assigns object IDs after sorting
    # clusters by centroid X. Reproduce that ordering
    # here so labels remain correct even when objects
    # move around.
    ordered = sorted(
        objects,
        key=expected_center_x,
    )

    labels = {
        f"object_{i}": item["label"]
        for i, item in enumerate(ordered)
    }

    label_path = (
        OUTPUT_DIR
        / f"{scene_name}_labels.json"
    )

    with label_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            labels,
            file,
            indent=2,
        )

    print(
        f"{scene_name}: "
        f"{len(cloud.points)} points"
    )

    print(
        f"  labels: {labels}"
    )


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for scene_name, objects in SCENES.items():
        generate_scene(
            scene_name,
            objects,
        )


if __name__ == "__main__":
    main()