from pprint import pprint

from app.scene import load_scene
from app.scene_graph import (
    build_scene_graph,
    scene_graph_summary,
)


def main():
    scene = load_scene(
        "data/demo_scene.ply"
    )

    graph = build_scene_graph(
        scene,
        near_threshold=1.5,
    )

    print("\nOBJECTS")
    pprint(graph.objects)

    print("\nRELATIONS")
    pprint(
        scene_graph_summary(graph)
    )


if __name__ == "__main__":
    main()