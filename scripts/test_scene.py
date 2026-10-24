from pprint import pprint

from app.scene import load_scene
from app.tools.geometry import (
    bounding_boxes_overlap,
    distance_between_objects,
    find_largest_object,
    find_nearest_object,
    relative_position,
    scene_summary,
    surface_distance_between_objects,
)


def main():
    scene = load_scene("data/demo_scene.ply")

    print("\nSCENE OBJECTS")
    pprint(scene_summary(scene))

    print("\nLARGEST OBJECT")
    print(find_largest_object(scene))

    print("\nNEAREST TO OBJECT_0")
    print(find_nearest_object(scene, "object_0"))

    print("\nDISTANCE OBJECT_0 -> OBJECT_1")
    print(
        distance_between_objects(
            scene,
            "object_0",
            "object_1",
        )
    )

    print("\nSURFACE DISTANCE OBJECT_0 -> OBJECT_1")
    print(
        surface_distance_between_objects(
            scene,
            "object_0",
            "object_1",
        )
    )

    print("\nRELATIVE POSITION OBJECT_1 TO OBJECT_0")
    print(
        relative_position(
            scene,
            "object_1",
            "object_0",
        )
    )

    print("\nOBJECT_0 / OBJECT_1 OVERLAP")
    print(
        bounding_boxes_overlap(
            scene,
            "object_0",
            "object_1",
        )
    )

if __name__ == "__main__":
    main()