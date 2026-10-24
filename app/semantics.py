import json
from pathlib import Path

from app.scene import Scene


def load_labels(path: str | Path) -> dict[str, str]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Label file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def apply_labels(
    scene: Scene,
    labels: dict[str, str],
) -> Scene:

    for obj in scene.objects:
        obj.label = labels.get(obj.object_id)

    return scene


def find_object_by_label(
    scene: Scene,
    label: str,
) -> str:

    def normalize(value: str) -> str:
        return (
            value.strip()
            .lower()
            .replace("_", " ")
            .replace("-", " ")
        )

    query = normalize(label)

    matches = [
        obj.object_id
        for obj in scene.objects
        if (
            obj.label is not None
            and normalize(obj.label) == query
        )
    ]

    if not matches:
        raise ValueError(
            f"No object with label '{label}' exists."
        )

    if len(matches) > 1:
        raise ValueError(
            f"Multiple objects have label '{label}'."
        )

    return matches[0]