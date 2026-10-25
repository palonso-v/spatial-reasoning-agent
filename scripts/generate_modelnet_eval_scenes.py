import json
from pathlib import Path

import h5py
import numpy as np
import open3d as o3d


MODELNET_DIR = Path(
    "data/ModelNet40"
)

OUTPUT_DIR = Path(
    "data/modelnet_eval_scenes"
)


MODELNET40_CLASSES = [
    "airplane",
    "bathtub",
    "bed",
    "bench",
    "bookshelf",
    "bottle",
    "bowl",
    "car",
    "chair",
    "cone",
    "cup",
    "curtain",
    "desk",
    "door",
    "dresser",
    "flower_pot",
    "glass_box",
    "guitar",
    "keyboard",
    "lamp",
    "laptop",
    "mantel",
    "monitor",
    "night_stand",
    "person",
    "piano",
    "plant",
    "radio",
    "range_hood",
    "sink",
    "sofa",
    "stairs",
    "stool",
    "table",
    "tent",
    "toilet",
    "tv_stand",
    "vase",
    "wardrobe",
    "xbox",
]


SCENE_CONFIGS = [
    {
        "name": "scene_1",
        "sample_offset": 0,
        "objects": [
            {
                "source_class": "table",
                "label": "table",
                "position": [0.0, 0.0, 0.0],
                "target_max_size": 1.6,
                "color": [0.8, 0.5, 0.2],
            },
            {
                "source_class": "stool",
                "label": "stool",
                "position": [2.3, 0.2, 0.0],
                "target_max_size": 0.8,
                "color": [1.0, 0.2, 0.2],
            },
            {
                "source_class": "chair",
                "label": "chair",
                "position": [4.4, 1.6, 0.0],
                "target_max_size": 1.1,
                "color": [0.2, 0.4, 1.0],
            },
            {
                "source_class": "dresser",
                "label": "cabinet",
                "position": [6.7, 0.2, 0.0],
                "target_max_size": 1.8,
                "color": [0.2, 0.8, 0.3],
            },
        ],
        "doorway_position": [9.2, 1.5, 0.0],
    },

    {
        "name": "scene_2",
        "sample_offset": 1,
        "objects": [
            {
                "source_class": "chair",
                "label": "chair",
                "position": [0.0, 0.2, 0.0],
                "target_max_size": 1.1,
                "color": [0.2, 0.4, 1.0],
            },
            {
                "source_class": "table",
                "label": "table",
                "position": [2.0, 1.0, 0.0],
                "target_max_size": 1.6,
                "color": [0.8, 0.5, 0.2],
            },
            {
                "source_class": "dresser",
                "label": "cabinet",
                "position": [5.0, 0.0, 0.0],
                "target_max_size": 1.8,
                "color": [0.2, 0.8, 0.3],
            },
            {
                "source_class": "stool",
                "label": "stool",
                "position": [7.6, 1.7, 0.0],
                "target_max_size": 0.8,
                "color": [1.0, 0.2, 0.2],
            },
        ],
        "doorway_position": [9.5, 0.4, 0.0],
    },

    {
        "name": "scene_3",
        "sample_offset": 2,
        "objects": [
            {
                "source_class": "dresser",
                "label": "cabinet",
                "position": [0.0, 0.0, 0.0],
                "target_max_size": 1.8,
                "color": [0.2, 0.8, 0.3],
            },
            {
                "source_class": "stool",
                "label": "stool",
                "position": [2.6, 1.7, 0.0],
                "target_max_size": 0.8,
                "color": [1.0, 0.2, 0.2],
            },
            {
                "source_class": "table",
                "label": "table",
                "position": [4.5, 0.2, 0.0],
                "target_max_size": 1.6,
                "color": [0.8, 0.5, 0.2],
            },
            {
                "source_class": "chair",
                "label": "chair",
                "position": [7.1, 1.2, 0.0],
                "target_max_size": 1.1,
                "color": [0.2, 0.4, 1.0],
            },
        ],
        "doorway_position": [9.2, 0.2, 0.0],
    },
]


def load_h5_modelnet(path):
    with h5py.File(path, "r") as file:
        data = (
            file["data"][:]
            .astype(np.float32)
        )

        labels = (
            file["label"][:]
            .astype(np.int64)
            .reshape(-1)
        )

    return data, labels


def read_file_list(path):
    with Path(path).open(
        "r",
        encoding="utf-8",
    ) as file:

        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def load_training_data():
    train_files = read_file_list(
        MODELNET_DIR
        / "train_files.txt"
    )

    all_points = []
    all_labels = []

    for filename in train_files:
        path = (
            MODELNET_DIR
            / filename
        )

        print(
            f"Loading {path}"
        )

        data, labels = (
            load_h5_modelnet(
                path
            )
        )

        all_points.append(
            data
        )

        all_labels.append(
            labels
        )

    return (
        np.concatenate(
            all_points,
            axis=0,
        ),
        np.concatenate(
            all_labels,
            axis=0,
        ),
    )


def class_id(class_name):
    return MODELNET40_CLASSES.index(
        class_name
    )


def select_example(
    all_points,
    all_labels,
    class_name,
    offset,
):
    target_id = class_id(
        class_name
    )

    indices = np.where(
        all_labels == target_id
    )[0]

    if len(indices) <= offset:
        raise ValueError(
            f"Not enough samples for "
            f"{class_name}"
        )

    index = indices[offset]

    return (
        all_points[index].copy(),
        int(index),
    )


def y_up_to_z_up(points):
    rotated = np.empty_like(
        points
    )

    rotated[:, 0] = points[:, 0]
    rotated[:, 1] = -points[:, 2]
    rotated[:, 2] = points[:, 1]

    return rotated


def normalize_point_cloud(points):
    min_bound = points.min(
        axis=0
    )

    max_bound = points.max(
        axis=0
    )

    center = (
        min_bound
        + max_bound
    ) / 2

    points = (
        points
        - center
    )

    dimensions = (
        max_bound
        - min_bound
    )

    max_dimension = (
        dimensions.max()
    )

    if max_dimension <= 0:
        raise ValueError(
            "Degenerate point cloud."
        )

    return (
        points
        / max_dimension
    )


def place_object(
    points,
    position,
    target_max_size,
):
    points = y_up_to_z_up(
        points
    )

    points = normalize_point_cloud(
        points
    )

    points *= (
        target_max_size
    )

    points[:, 2] -= (
        points[:, 2].min()
    )

    min_xy = points[
        :, :2
    ].min(
        axis=0
    )

    points[:, 0] -= min_xy[0]
    points[:, 1] -= min_xy[1]

    return (
        points
        + np.asarray(
            position,
            dtype=np.float32,
        )
    )


def sample_box_surface(
    size,
    position,
    n_points=1200,
):
    mesh = (
        o3d.geometry.TriangleMesh
        .create_box(
            width=size[0],
            height=size[1],
            depth=size[2],
        )
    )

    mesh.translate(
        position
    )

    cloud = (
        mesh.sample_points_uniformly(
            number_of_points=n_points
        )
    )

    return np.asarray(
        cloud.points
    )


def create_cloud(
    points,
    color,
):
    cloud = (
        o3d.geometry.PointCloud()
    )

    cloud.points = (
        o3d.utility.Vector3dVector(
            points
        )
    )

    colors = np.tile(
        np.asarray(
            color,
            dtype=float,
        ),
        (
            len(points),
            1,
        ),
    )

    cloud.colors = (
        o3d.utility.Vector3dVector(
            colors
        )
    )

    return cloud


def generate_scene(
    config,
    all_points,
    all_labels,
):
    scene_objects = []

    offset = config[
        "sample_offset"
    ]

    print(
        "\n"
        + "=" * 70
    )

    print(
        f"Generating "
        f"{config['name']}"
    )

    print(
        "=" * 70
    )

    for obj_config in config[
        "objects"
    ]:

        points, sample_index = (
            select_example(
                all_points,
                all_labels,
                obj_config[
                    "source_class"
                ],
                offset,
            )
        )

        points = place_object(
            points,
            obj_config[
                "position"
            ],
            obj_config[
                "target_max_size"
            ],
        )

        scene_objects.append(
            {
                "label":
                    obj_config[
                        "label"
                    ],

                "points":
                    points,

                "color":
                    obj_config[
                        "color"
                    ],

                "sample_index":
                    sample_index,
            }
        )

        print(
            f"{obj_config['label']:10} "
            f"sample={sample_index}"
        )


    doorway_points = (
        sample_box_surface(
            size=(
                1.0,
                0.35,
                2.1,
            ),
            position=config[
                "doorway_position"
            ],
        )
    )

    scene_objects.append(
        {
            "label":
                "doorway_opening",

            "points":
                doorway_points,

            "color":
                [0.8, 0.8, 0.8],

            "sample_index":
                None,
        }
    )


    scene_objects.sort(
        key=lambda item:
            item["points"][
                :, 0
            ].mean()
    )


    combined_cloud = (
        o3d.geometry.PointCloud()
    )

    labels = {}


    for index, item in enumerate(
        scene_objects
    ):

        cloud = create_cloud(
            item["points"],
            item["color"],
        )

        combined_cloud += cloud


        object_id = (
            f"object_{index}"
        )

        labels[
            object_id
        ] = item[
            "label"
        ]


        dimensions = (
            item["points"].max(
                axis=0
            )
            -
            item["points"].min(
                axis=0
            )
        )


        print(
            f"{object_id:10} "
            f"{item['label']:18} "
            f"dims="
            f"{np.round(dimensions, 3).tolist()}"
        )


    scene_path = (
        OUTPUT_DIR
        / f"{config['name']}.ply"
    )

    labels_path = (
        OUTPUT_DIR
        / f"{config['name']}_labels.json"
    )


    o3d.io.write_point_cloud(
        str(
            scene_path
        ),
        combined_cloud,
    )


    with labels_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            labels,
            file,
            indent=2,
        )


    print(
        f"Saved {scene_path}"
    )

    print(
        f"Saved {labels_path}"
    )


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    all_points, all_labels = (
        load_training_data()
    )

    for config in SCENE_CONFIGS:
        generate_scene(
            config,
            all_points,
            all_labels,
        )


if __name__ == "__main__":
    main()