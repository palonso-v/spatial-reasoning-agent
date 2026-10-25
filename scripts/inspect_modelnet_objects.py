from pathlib import Path

import h5py
import numpy as np
import open3d as o3d


MODELNET_DIR = Path(
    "data/modelnet40"
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


CLASSES_TO_INSPECT = [
    "table",
    "glass_box",
    "chair",
    "dresser",
]


def load_h5_modelnet(
    path,
):
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


def read_train_files():

    path = (
        MODELNET_DIR
        / "train_files.txt"
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def load_all_training_data():

    data_parts = []
    label_parts = []

    for filename in read_train_files():

        data, labels = (
            load_h5_modelnet(
                MODELNET_DIR
                / filename
            )
        )

        data_parts.append(
            data
        )

        label_parts.append(
            labels
        )

    return (
        np.concatenate(
            data_parts,
            axis=0,
        ),
        np.concatenate(
            label_parts,
            axis=0,
        ),
    )


def show_example(
    points,
    title,
):

    min_bound = points.min(
        axis=0
    )

    max_bound = points.max(
        axis=0
    )

    dimensions = (
        max_bound
        - min_bound
    )


    print(
        f"\n{title}"
    )

    print(
        "dimensions:",
        np.round(
            dimensions,
            3,
        ).tolist(),
    )


    cloud = (
        o3d.geometry.PointCloud()
    )

    cloud.points = (
        o3d.utility.Vector3dVector(
            points
        )
    )


    cloud.paint_uniform_color(
        [0.8, 0.8, 0.8]
    )


    axes = (
        o3d.geometry.TriangleMesh
        .create_coordinate_frame(
            size=0.8,
            origin=[
                0,
                0,
                0,
            ],
        )
    )


    o3d.visualization.draw_geometries(
        [
            cloud,
            axes,
        ],
        window_name=title,
        width=900,
        height=700,
    )


def main():

    data, labels = (
        load_all_training_data()
    )


    for class_name in (
        CLASSES_TO_INSPECT
    ):

        class_id = (
            MODELNET40_CLASSES.index(
                class_name
            )
        )


        indices = np.where(
            labels == class_id
        )[0]


        if len(indices) == 0:

            print(
                f"No samples for "
                f"{class_name}"
            )

            continue


        # Inspect the first three examples,
        # rather than blindly trusting sample 0.
        for local_index in range(
            min(
                3,
                len(indices),
            )
        ):

            dataset_index = (
                indices[
                    local_index
                ]
            )


            points = (
                data[
                    dataset_index
                ].copy()
            )


            show_example(
                points,
                (
                    f"{class_name} | "
                    f"dataset index "
                    f"{dataset_index}"
                ),
            )


if __name__ == "__main__":
    main()