from dataclasses import dataclass

from app.scene import Scene
from app.tools.geometry import (
    bounding_boxes_overlap,
    relative_position,
    surface_distance_between_objects,
)


RELATION_NAMES = {
    "left": "LEFT_OF",
    "right": "RIGHT_OF",
    "in front": "IN_FRONT_OF",
    "behind": "BEHIND",
    "above": "ABOVE",
    "below": "BELOW",
}


@dataclass
class SceneRelation:
    source: str
    relation: str
    target: str
    value: float | None = None


@dataclass
class SceneGraph:
    objects: list[str]
    relations: list[SceneRelation]


def build_scene_graph(
    scene: Scene,
    near_threshold: float = 1.5,
) -> SceneGraph:

    object_ids = [
        obj.object_id
        for obj in scene.objects
    ]

    relations = []

    for i, object_a in enumerate(object_ids):
        for object_b in object_ids[i + 1:]:

            # Directional relations from A to B.
            directions_a_to_b = relative_position(
                scene,
                object_a,
                object_b,
            )

            for relation in directions_a_to_b:
                relations.append(
                    SceneRelation(
                        source=object_a,
                        relation=RELATION_NAMES[relation],
                        target=object_b,
                    )
                )

            # Directional relations from B to A.
            directions_b_to_a = relative_position(
                scene,
                object_b,
                object_a,
            )

            for relation in directions_b_to_a:
                relations.append(
                    SceneRelation(
                        source=object_b,
                        relation=RELATION_NAMES[relation],
                        target=object_a,
                    )
                )

            # Physical proximity.
            surface_distance = surface_distance_between_objects(
                scene,
                object_a,
                object_b,
            )

            if surface_distance <= near_threshold:
                relations.append(
                    SceneRelation(
                        source=object_a,
                        relation="NEAR",
                        target=object_b,
                        value=surface_distance,
                    )
                )

                relations.append(
                    SceneRelation(
                        source=object_b,
                        relation="NEAR",
                        target=object_a,
                        value=surface_distance,
                    )
                )

            # Bounding-box overlap.
            if bounding_boxes_overlap(
                scene,
                object_a,
                object_b,
            ):
                relations.append(
                    SceneRelation(
                        source=object_a,
                        relation="OVERLAPS",
                        target=object_b,
                    )
                )

                relations.append(
                    SceneRelation(
                        source=object_b,
                        relation="OVERLAPS",
                        target=object_a,
                    )
                )

    return SceneGraph(
        objects=object_ids,
        relations=relations,
    )


def scene_graph_summary(
    graph: SceneGraph,
) -> list[dict]:

    return [
        {
            "source": relation.source,
            "relation": relation.relation,
            "target": relation.target,
            "value": relation.value,
        }
        for relation in graph.relations
    ]


def describe_object_relations(
    graph: SceneGraph,
    object_id: str,
) -> list[dict]:

    if object_id not in graph.objects:
        raise ValueError(
            f"Unknown object: {object_id}"
        )

    return [
        {
            "relation": relation.relation,
            "target": relation.target,
            "value": relation.value,
        }
        for relation in graph.relations
        if relation.source == object_id
    ]


def find_objects_by_relation(
    graph: SceneGraph,
    reference_object: str,
    relation: str,
) -> list[dict]:

    if reference_object not in graph.objects:
        raise ValueError(
            f"Unknown object: {reference_object}"
        )

    relation = relation.upper()

    return [
        {
            "object_id": item.target,
            "value": item.value,
        }
        for item in graph.relations
        if (
            item.source == reference_object
            and item.relation == relation
        )
    ]