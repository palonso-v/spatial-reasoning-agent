import json
from pathlib import Path

import h5py
import numpy as np
import open3d as o3d


MODELNET_DIR = Path(
    "data/modelnet40"
)

OUTPUT_SCENE = Path(
    "data/modelnet_scene.ply"
)

OUTPUT_LABELS = Path(
    "data/modelnet_scene_labels.json"
)


# Standard ModelNet40 class ordering commonly
# distributed with the HDF5 version.
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


SCENE_OBJECTS = [
    {
        "source_class": "table",
        "label": "table",
        "position": np.array(
            [0.0, 0.0, 0.0]
        ),
        "target_max_size": 1.6,
        "color": [0.8, 0.5, 0.2],
    },
    {
        "source_class": "stool",
        "label": "stool",
        "position": np.array(
            [2.5, 0.2, 0.0]
        ),
        "target_max_size": 0.8,
        "color": [1.0, 0.2, 0.2],
    },
    {
        "source_class": "chair",
        "label": "chair",
        "position": np.array(
            [4.5, 1.6, 0.0]
        ),
        "target_max_size": 1.1,
        "color": [0.2, 0.4, 1.0],
    },
    {
        "source_class": "dresser",
        "label": "cabinet",
        "position": np.array(
            [6.8, 0.2, 0.0]
        ),
        "target_max_size": 1.8,
        "color": [0.2, 0.8, 0.3],
    },
]


def load_h5_modelnet(
    path: str | Path,
):
    """
    Load a standard ModelNet40 HDF5 shard.

    Expected datasets:
        data  -> (N, num_points, 3)
        label -> (N, 1)
    """

    path = Path(path)

    with h5py.File(
        path,
        "r",
    ) as file:
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


def read_file_list(
    path: str | Path,
) -> list[str]:

    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def load_training_data():
    """
    Load the ModelNet40 training shards listed
    in train_files.txt.
    """

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

    points = np.concatenate(
        all_points,
        axis=0,
    )

    labels = np.concatenate(
        all_labels,
        axis=0,
    )

    return points, labels


def get_class_id(
    class_name: str,
) -> int:

    if (
        class_name
        not in MODELNET40_CLASSES
    ):
        raise ValueError(
            f"Unknown ModelNet40 class: "
            f"{class_name}"
        )

    return MODELNET40_CLASSES.index(
        class_name
    )


def select_example(
    all_points,
    all_labels,
    class_name: str,
):
    """
    Select the first available point cloud
    belonging to a requested class.
    """

    class_id = get_class_id(
        class_name
    )

    indices = np.where(
        all_labels == class_id
    )[0]

    if len(indices) == 0:
        raise ValueError(
            f"No samples found for "
            f"class '{class_name}'."
        )

    index = indices[0]

    return (
        all_points[index].copy(),
        index,
    )


def normalize_point_cloud(
    points: np.ndarray,
) -> np.ndarray:
    """
    Center the object and scale it so its
    largest bounding-box dimension is 1.
    """

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
        points - center
    )


    dimensions = (
        max_bound
        - min_bound
    )

    largest_dimension = (
        dimensions.max()
    )


    if largest_dimension <= 0:
        raise ValueError(
            "Degenerate point cloud."
        )


    points = (
        points
        / largest_dimension
    )

    return points


def place_object(
    points: np.ndarray,
    position: np.ndarray,
    target_max_size: float,
) -> np.ndarray:

    points = y_up_to_z_up(
        points
    )

    points = normalize_point_cloud(
        points
    )

    points = (
        points
        * target_max_size
    )

    # Put the lowest point on the floor.
    points[:, 2] -= (
        points[:, 2].min()
    )


    # Move x/y so the minimum corner begins at
    # the requested scene position.
    min_xy = points[:, :2].min(
        axis=0
    )

    points[:, 0] -= min_xy[0]
    points[:, 1] -= min_xy[1]


    points = (
        points
        + position
    )


    return points


def sample_box_surface(
    size,
    position,
    n_points=1200,
):
    """
    Create a point-cloud representation of the
    free-space doorway opening.

    This is an abstract spatial primitive rather
    than a physical ModelNet object.
    """

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


def create_open3d_cloud(
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


def y_up_to_z_up(
    points: np.ndarray,
) -> np.ndarray:
    """
    Convert ModelNet coordinates from Y-up to Z-up.

    Rotation:
        x' = x
        y' = -z
        z' = y
    """

    rotated = np.empty_like(
        points
    )

    rotated[:, 0] = points[:, 0]
    rotated[:, 1] = -points[:, 2]
    rotated[:, 2] = points[:, 1]

    return rotated


def main():

    print(
        "Loading ModelNet40..."
    )

    all_points, all_labels = (
        load_training_data()
    )


    scene_objects = []


    for config in SCENE_OBJECTS:

        points, sample_index = (
            select_example(
                all_points,
                all_labels,
                config[
                    "source_class"
                ],
            )
        )


        print(
            f"Using "
            f"{config['source_class']} "
            f"sample {sample_index}"
        )


        points = place_object(
            points,
            config["position"],
            config[
                "target_max_size"
            ],
        )


        scene_objects.append(
            {
                "label":
                    config["label"],

                "points":
                    points,

                "color":
                    config["color"],
            }
        )


    # ---------------------------------------------
    # Add doorway opening
    # ---------------------------------------------

    doorway_points = (
        sample_box_surface(
            size=(
                1.0,
                0.35,
                2.1,
            ),
            position=(
                9.2,
                1.5,
                0.0,
            ),
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
        }
    )


    # ---------------------------------------------
    # Sort by x position to match scene.py's
    # deterministic object ID assignment.
    # ---------------------------------------------

    scene_objects.sort(
        key=lambda item:
            item["points"][
                :, 0
            ].mean()
    )


    combined_cloud = (
        o3d.geometry.PointCloud()
    )


    label_mapping = {}


    for index, item in enumerate(
        scene_objects
    ):

        cloud = create_open3d_cloud(
            item["points"],
            item["color"],
        )


        combined_cloud += cloud


        object_id = (
            f"object_{index}"
        )


        label_mapping[
            object_id
        ] = item["label"]


        min_bound = (
            item["points"]
            .min(axis=0)
        )

        max_bound = (
            item["points"]
            .max(axis=0)
        )

        dimensions = (
            max_bound
            - min_bound
        )


        print(
            f"{object_id:10} "
            f"{item['label']:18} "
            f"points={len(item['points']):4} "
            f"dims="
            f"{np.round(dimensions, 3).tolist()}"
        )


    o3d.io.write_point_cloud(
        str(OUTPUT_SCENE),
        combined_cloud,
    )


    with OUTPUT_LABELS.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            label_mapping,
            file,
            indent=2,
        )


    print(
        f"\nSaved scene: "
        f"{OUTPUT_SCENE}"
    )

    print(
        f"Saved labels: "
        f"{OUTPUT_LABELS}"
    )


if __name__ == "__main__":
    main()