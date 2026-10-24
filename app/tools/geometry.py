import numpy as np

from app.scene import Scene, SceneObject


def get_object(scene: Scene, object_id: str) -> SceneObject:
    for obj in scene.objects:
        if obj.object_id == object_id:
            return obj

    raise ValueError(f"Unknown object: {object_id}")


def scene_summary(scene: Scene) -> list[dict]:
    return [
        {
            "object_id": obj.object_id,
            "label": obj.label,
            "centroid": obj.centroid.round(3).tolist(),
            "dimensions": obj.dimensions.round(3).tolist(),
            "volume": round(obj.volume, 3),
            "point_count": obj.point_count,
        }
        for obj in scene.objects
    ]


def distance_between_objects(
    scene: Scene,
    object_a: str,
    object_b: str,
) -> float:

    a = get_object(scene, object_a)
    b = get_object(scene, object_b)

    return float(
        np.linalg.norm(a.centroid - b.centroid)
    )


def find_nearest_object(
    scene: Scene,
    reference_object: str,
) -> tuple[str, float]:

    reference = get_object(scene, reference_object)

    candidates = [
        obj
        for obj in scene.objects
        if obj.object_id != reference_object
    ]

    if not candidates:
        raise ValueError("Scene contains no other objects.")

    distances = [
        (
            obj.object_id,
            float(
                np.linalg.norm(
                    reference.centroid - obj.centroid
                )
            ),
        )
        for obj in candidates
    ]

    return min(distances, key=lambda item: item[1])


def find_largest_object(
    scene: Scene,
) -> tuple[str, float]:

    if not scene.objects:
        raise ValueError("Scene contains no objects.")

    largest = max(
        scene.objects,
        key=lambda obj: obj.volume,
    )

    return largest.object_id, largest.volume


def surface_distance_between_objects(
    scene: Scene,
    object_a: str,
    object_b: str,
) -> float:
    a = get_object(scene, object_a)
    b = get_object(scene, object_b)

    separation = np.maximum(
        0.0,
        np.maximum(
            a.min_bound - b.max_bound,
            b.min_bound - a.max_bound,
        ),
    )

    return float(np.linalg.norm(separation))


def relative_position(
    scene: Scene,
    object_a: str,
    object_b: str,
) -> list[str]:
    a = get_object(scene, object_a)
    b = get_object(scene, object_b)

    delta = a.centroid - b.centroid

    relations = []

    if delta[0] < 0:
        relations.append("left")
    elif delta[0] > 0:
        relations.append("right")

    if delta[1] < 0:
        relations.append("behind")
    elif delta[1] > 0:
        relations.append("in front")

    if delta[2] < 0:
        relations.append("below")
    elif delta[2] > 0:
        relations.append("above")

    return relations


def bounding_boxes_overlap(
    scene: Scene,
    object_a: str,
    object_b: str,
) -> bool:
    a = get_object(scene, object_a)
    b = get_object(scene, object_b)

    overlap = np.all(
        (a.min_bound <= b.max_bound)
        & (b.min_bound <= a.max_bound)
    )

    return bool(overlap)


def find_nearest_object_by_surface(
    scene: Scene,
    reference_object: str,
) -> tuple[str, float]:
    reference = get_object(scene, reference_object)

    candidates = [
        obj
        for obj in scene.objects
        if obj.object_id != reference_object
    ]

    if not candidates:
        raise ValueError("Scene contains no other objects.")

    distances = [
        (
            obj.object_id,
            surface_distance_between_objects(
                scene,
                reference_object,
                obj.object_id,
            ),
        )
        for obj in candidates
    ]

    return min(distances, key=lambda item: item[1])


def objects_within_radius(
    scene: Scene,
    reference_object: str,
    radius: float,
) -> list[dict]:
    reference = get_object(scene, reference_object)

    results = []

    for obj in scene.objects:
        if obj.object_id == reference_object:
            continue

        distance = float(
            np.linalg.norm(
                reference.centroid - obj.centroid
            )
        )

        if distance <= radius:
            results.append(
                {
                    "object_id": obj.object_id,
                    "centroid_distance": distance,
                }
            )

    return sorted(
        results,
        key=lambda item: item["centroid_distance"],
    )


def can_fit_inside(
    scene: Scene,
    object_a: str,
    object_b: str,
) -> dict:
    a = get_object(scene, object_a)
    b = get_object(scene, object_b)

    a_dims = np.sort(a.dimensions)
    b_dims = np.sort(b.dimensions)

    fits = bool(np.all(a_dims <= b_dims))

    clearance = b_dims - a_dims

    return {
        "fits": fits,
        "object_dimensions": a_dims.round(3).tolist(),
        "container_dimensions": b_dims.round(3).tolist(),
        "clearance": clearance.round(3).tolist(),
    }

def can_pass_through_opening(
    scene: Scene,
    object_id: str,
    opening_id: str,
    passage_axis: int = 1,
) -> dict:
    obj = get_object(scene, object_id)
    opening = get_object(scene, opening_id)

    object_dims = np.asarray(obj.dimensions)
    opening_dims = np.asarray(opening.dimensions)

    # Remove the dimension along the direction of travel.
    object_cross_section = np.delete(
        object_dims,
        passage_axis,
    )

    opening_cross_section = np.delete(
        opening_dims,
        passage_axis,
    )

    object_cross_section = np.sort(
        object_cross_section
    )

    opening_cross_section = np.sort(
        opening_cross_section
    )

    fits = bool(
        np.all(
            object_cross_section
            <= opening_cross_section
        )
    )

    clearance = (
        opening_cross_section
        - object_cross_section
    )

    return {
        "fits": fits,
        "object_cross_section": (
            object_cross_section
            .round(3)
            .tolist()
        ),
        "opening_cross_section": (
            opening_cross_section
            .round(3)
            .tolist()
        ),
        "clearance": (
            clearance
            .round(3)
            .tolist()
        ),
    }