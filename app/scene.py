from dataclasses import dataclass
from pathlib import Path

import numpy as np
import open3d as o3d


@dataclass
class SceneObject:
    object_id: str
    centroid: np.ndarray
    min_bound: np.ndarray
    max_bound: np.ndarray
    dimensions: np.ndarray
    point_count: int
    points: np.ndarray
    label: str | None = None

    @property
    def volume(self) -> float:
        return float(np.prod(self.dimensions))


@dataclass
class Scene:
    path: Path
    objects: list[SceneObject]


def load_point_cloud(
    path: str | Path,
) -> o3d.geometry.PointCloud:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Point cloud not found: {path}"
        )

    cloud = o3d.io.read_point_cloud(
        str(path)
    )

    if cloud.is_empty():
        raise ValueError(
            f"Point cloud is empty: {path}"
        )

    return cloud


def segment_objects(
    cloud: o3d.geometry.PointCloud,
    eps: float = 0.20,
    min_points: int = 10,
) -> list[SceneObject]:

    labels = np.asarray(
        cloud.cluster_dbscan(
            eps=eps,
            min_points=min_points,
            print_progress=False,
        )
    )

    points = np.asarray(
        cloud.points
    )

    cluster_ids = sorted(
        label
        for label in set(labels)
        if label != -1
    )

    raw_objects = []

    for cluster_id in cluster_ids:
        cluster_points = points[
            labels == cluster_id
        ]

        min_bound = (
            cluster_points.min(axis=0)
        )

        max_bound = (
            cluster_points.max(axis=0)
        )

        centroid = (
            cluster_points.mean(axis=0)
        )

        dimensions = (
            max_bound - min_bound
        )

        raw_objects.append(
            {
                "centroid": centroid,
                "min_bound": min_bound,
                "max_bound": max_bound,
                "dimensions": dimensions,
                "point_count": len(
                    cluster_points
                ),
                "points": cluster_points,
            }
        )

    # Keep object IDs deterministic across runs.
    # Objects are ordered from left to right
    # according to centroid x-coordinate.
    raw_objects.sort(
        key=lambda obj: (
            obj["centroid"][0]
        )
    )

    objects = []

    for index, obj in enumerate(
        raw_objects
    ):
        objects.append(
            SceneObject(
                object_id=(
                    f"object_{index}"
                ),
                centroid=obj[
                    "centroid"
                ],
                min_bound=obj[
                    "min_bound"
                ],
                max_bound=obj[
                    "max_bound"
                ],
                dimensions=obj[
                    "dimensions"
                ],
                point_count=obj[
                    "point_count"
                ],
                points=obj[
                    "points"
                ],
            )
        )

    return objects


def load_scene(
    path: str | Path,
    eps: float = 0.20,
    min_points: int = 10,
) -> Scene:

    cloud = load_point_cloud(
        path
    )

    objects = segment_objects(
        cloud,
        eps=eps,
        min_points=min_points,
    )

    return Scene(
        path=Path(path),
        objects=objects,
    )