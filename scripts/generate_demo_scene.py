from pathlib import Path

import open3d as o3d


OUTPUT = Path("data/demo_scene.ply")


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
        number_of_points=n_points
    )

    cloud.paint_uniform_color(color)

    return cloud


def main():
    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # object_0
    table = create_box(
        size=(1.6, 1.0, 0.8),
        position=(0.0, 0.0, 0.0),
        color=(0.8, 0.5, 0.2),
    )

    # object_1
    box = create_box(
        size=(0.6, 0.6, 0.6),
        position=(2.0, 0.2, 0.0),
        color=(1.0, 0.2, 0.2),
    )

    # object_2
    chair = create_box(
        size=(0.8, 0.8, 1.0),
        position=(3.8, 1.8, 0.0),
        color=(0.2, 0.4, 1.0),
    )

    # object_3
    cabinet = create_box(
        size=(1.2, 0.7, 1.8),
        position=(5.8, 0.2, 0.0),
        color=(0.2, 0.8, 0.3),
    )

    # object_4
    #
    # This represents the free volume of a doorway opening,
    # rather than the physical door frame.
    doorway_opening = create_box(
        size=(1.0, 0.35, 2.1),
        position=(7.8, 1.8, 0.0),
        color=(0.8, 0.8, 0.8),
    )

    scene = (
        table
        + box
        + chair
        + cabinet
        + doorway_opening
    )

    o3d.io.write_point_cloud(
        str(OUTPUT),
        scene,
    )

    print(f"Saved scene to: {OUTPUT}")
    print(
        f"Total points: {len(scene.points)}"
    )


if __name__ == "__main__":
    main()