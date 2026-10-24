import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.scene import load_scene
from app.scene_graph import (
    build_scene_graph,
    describe_object_relations,
    find_objects_by_relation,
)
from app.semantics import (
    apply_labels,
    find_object_by_label,
    load_labels,
)
from app.tools.geometry import (
    bounding_boxes_overlap,
    can_fit_inside,
    can_pass_through_opening,
    distance_between_objects,
    find_largest_object,
    find_nearest_object,
    find_nearest_object_by_surface,
    objects_within_radius,
    relative_position,
    scene_summary,
    surface_distance_between_objects,
)


load_dotenv()

client = OpenAI()

SCENE_PATH = Path("data/demo_scene.ply")
LABELS_PATH = Path("data/demo_labels.json")


AGENT_INSTRUCTIONS = (
    "You are a 3D spatial reasoning agent. "
    "Use the provided geometry tools whenever the answer depends on the scene. "
    "When the user refers to an object by a semantic name, resolve that name "
    "to its object ID using the available tool. "
    "Choose tools according to the geometric quantity requested. "
    "Centroid distance and physical surface distance are different concepts. "
    "Do not estimate geometric values yourself. "
    "You may call multiple tools in sequence. "
    "Base the final answer only on tool results. "
    "For questions about whether an object can pass through a doorway or opening, "
    "use can_pass_through_opening rather than can_fit_inside. "
    "Do not invent physical units. If the scene units are not explicitly defined, "
    "refer to measurements as units."
)


TOOLS = [
    {
        "type": "function",
        "name": "scene_summary",
        "description": (
            "Return the objects detected in the 3D scene, including semantic labels, "
            "centroids, dimensions, volume, and point counts."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "find_largest_object",
        "description": (
            "Find the object with the largest axis-aligned bounding-box volume."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "find_nearest_object",
        "description": (
            "Find the object whose centroid is nearest to a reference object."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "reference_object": {
                    "type": "string",
                    "description": "Object ID such as object_0.",
                }
            },
            "required": ["reference_object"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "distance_between_objects",
        "description": (
            "Compute Euclidean distance between the centroids of two objects."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "object_a": {"type": "string"},
                "object_b": {"type": "string"},
            },
            "required": ["object_a", "object_b"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "surface_distance_between_objects",
        "description": (
            "Compute the minimum separation between the axis-aligned bounding boxes "
            "of two objects."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "object_a": {"type": "string"},
                "object_b": {"type": "string"},
            },
            "required": ["object_a", "object_b"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "relative_position",
        "description": (
            "Describe object A relative to object B using left/right, "
            "front/behind, and above/below relations."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "object_a": {"type": "string"},
                "object_b": {"type": "string"},
            },
            "required": ["object_a", "object_b"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "bounding_boxes_overlap",
        "description": (
            "Check whether the axis-aligned bounding boxes of two objects overlap."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "object_a": {"type": "string"},
                "object_b": {"type": "string"},
            },
            "required": ["object_a", "object_b"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "find_nearest_object_by_surface",
        "description": (
            "Find the object with the smallest physical surface separation "
            "from a reference object."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "reference_object": {
                    "type": "string",
                }
            },
            "required": ["reference_object"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "objects_within_radius",
        "description": (
            "Return all objects whose centroids are within a given radius "
            "of a reference object."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "reference_object": {
                    "type": "string",
                },
                "radius": {
                    "type": "number",
                },
            },
            "required": [
                "reference_object",
                "radius",
            ],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "can_fit_inside",
        "description": (
            "Check whether one object's bounding-box dimensions can fit inside "
            "another object's bounding-box dimensions, allowing axis reordering."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "object_a": {
                    "type": "string",
                },
                "object_b": {
                    "type": "string",
                },
            },
            "required": [
                "object_a",
                "object_b",
            ],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "describe_object_relations",
        "description": (
            "Return all known spatial relationships from a given object "
            "to other objects in the scene graph."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "object_id": {
                    "type": "string",
                    "description": "Object ID such as object_0.",
                }
            },
            "required": ["object_id"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "find_objects_by_relation",
        "description": (
            "Find objects related to a reference object by a spatial relation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "reference_object": {
                    "type": "string",
                },
                "relation": {
                    "type": "string",
                    "enum": [
                        "NEAR",
                        "LEFT_OF",
                        "RIGHT_OF",
                        "IN_FRONT_OF",
                        "BEHIND",
                        "ABOVE",
                        "BELOW",
                        "OVERLAPS",
                    ],
                },
            },
            "required": [
                "reference_object",
                "relation",
            ],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "find_object_by_label",
        "description": (
            "Resolve a semantic object label such as table, chair, "
            "or box to its internal object ID."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "description": (
                        "Semantic object name such as table."
                    ),
                }
            },
            "required": ["label"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "can_pass_through_opening",
        "description": (
            "Check whether an object can physically pass through an opening such as "
            "a doorway. Use this for passage, doorway, opening, or clearance questions. "
            "Do not use can_fit_inside for doorway passage."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "object_id": {
                    "type": "string",
                    "description": (
                        "The object that must pass through the opening."
                    ),
                },
                "opening_id": {
                    "type": "string",
                    "description": (
                        "The doorway or opening object ID."
                    ),
                },
            },
            "required": [
                "object_id",
                "opening_id",
            ],
            "additionalProperties": False,
        },
    },
]


def get_object_label(
    scene,
    object_id: str,
) -> str | None:
    obj = next(
        (
            obj
            for obj in scene.objects
            if obj.object_id == object_id
        ),
        None,
    )

    return obj.label if obj else None


def enrich_object_result(
    scene,
    result: dict,
    object_key: str = "object_id",
) -> dict:
    object_id = result.get(object_key)

    if object_id is None:
        return result

    return {
        **result,
        "label": get_object_label(
            scene,
            object_id,
        ),
    }


def enrich_object_list(
    scene,
    results: list[dict],
) -> list[dict]:
    return [
        enrich_object_result(
            scene,
            item,
        )
        for item in results
    ]


def execute_tool(
    scene,
    graph,
    name: str,
    arguments: dict,
):
    if name == "scene_summary":
        return scene_summary(scene)

    if name == "find_largest_object":
        object_id, volume = find_largest_object(
            scene
        )

        return {
            "object_id": object_id,
            "label": get_object_label(
                scene,
                object_id,
            ),
            "volume": volume,
        }

    if name == "find_nearest_object":
        object_id, distance = find_nearest_object(
            scene,
            arguments["reference_object"],
        )

        return {
            "object_id": object_id,
            "label": get_object_label(
                scene,
                object_id,
            ),
            "centroid_distance": distance,
        }

    if name == "distance_between_objects":
        return {
            "distance": distance_between_objects(
                scene,
                arguments["object_a"],
                arguments["object_b"],
            )
        }

    if name == "surface_distance_between_objects":
        return {
            "surface_distance": surface_distance_between_objects(
                scene,
                arguments["object_a"],
                arguments["object_b"],
            )
        }

    if name == "relative_position":
        return {
            "relations": relative_position(
                scene,
                arguments["object_a"],
                arguments["object_b"],
            )
        }

    if name == "bounding_boxes_overlap":
        return {
            "overlap": bounding_boxes_overlap(
                scene,
                arguments["object_a"],
                arguments["object_b"],
            )
        }

    if name == "find_nearest_object_by_surface":
        object_id, distance = (
            find_nearest_object_by_surface(
                scene,
                arguments["reference_object"],
            )
        )

        return {
            "object_id": object_id,
            "label": get_object_label(
                scene,
                object_id,
            ),
            "surface_distance": distance,
        }

    if name == "objects_within_radius":
        results = objects_within_radius(
            scene,
            arguments["reference_object"],
            arguments["radius"],
        )

        return {
            "objects": enrich_object_list(
                scene,
                results,
            )
        }

    if name == "can_fit_inside":
        return can_fit_inside(
            scene,
            arguments["object_a"],
            arguments["object_b"],
        )

    if name == "describe_object_relations":
        results = describe_object_relations(
            graph,
            arguments["object_id"],
        )

        return {
            "relations": [
                {
                    **item,
                    "target_label": get_object_label(
                        scene,
                        item["target"],
                    ),
                }
                for item in results
            ]
        }

    if name == "find_objects_by_relation":
        results = find_objects_by_relation(
            graph,
            arguments["reference_object"],
            arguments["relation"],
        )

        return {
            "objects": enrich_object_list(
                scene,
                results,
            )
        }

    if name == "find_object_by_label":
        object_id = find_object_by_label(
            scene,
            arguments["label"],
        )

        return {
            "object_id": object_id,
            "label": get_object_label(
                scene,
                object_id,
            ),
        }

    if name == "can_pass_through_opening":
        return can_pass_through_opening(
            scene,
            arguments["object_id"],
            arguments["opening_id"],
        )

    raise ValueError(
        f"Unknown tool: {name}"
    )


def run_agent(
    question: str,
    return_trace: bool = False,
):
    scene = load_scene(
        SCENE_PATH
    )

    labels = load_labels(
        LABELS_PATH
    )

    scene = apply_labels(
        scene,
        labels,
    )

    graph = build_scene_graph(
        scene
    )

    input_items = [
        {
            "role": "user",
            "content": question,
        }
    ]

    tool_trace = []

    response = client.responses.create(
        model="gpt-5.6",
        instructions=AGENT_INSTRUCTIONS,
        input=input_items,
        tools=TOOLS,
    )

    max_steps = 8

    for _ in range(max_steps):
        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            if return_trace:
                return {
                    "answer": response.output_text,
                    "tool_trace": tool_trace,
                }

            return response.output_text

        input_items.extend(
            response.output
        )

        for call in tool_calls:
            arguments = json.loads(
                call.arguments
            )

            tool_trace.append(
                {
                    "name": call.name,
                    "arguments": arguments,
                }
            )

            print(
                f"TOOL: {call.name} "
                f"{arguments}"
            )

            try:
                result = execute_tool(
                    scene,
                    graph,
                    call.name,
                    arguments,
                )
            except Exception as exc:
                result = {
                    "error": str(exc)
                }

            print(
                f"RESULT: {result}"
            )

            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(
                        result
                    ),
                }
            )

        response = client.responses.create(
            model="gpt-5.6",
            instructions=AGENT_INSTRUCTIONS,
            input=input_items,
            tools=TOOLS,
        )

    raise RuntimeError(
        "Agent exceeded maximum number of tool steps."
    )


def main():
    question = (
        "Can the box fit inside the cabinet?"
    )

    answer = run_agent(
        question
    )

    print(
        "\nFINAL ANSWER"
    )

    print(
        answer
    )


if __name__ == "__main__":
    main()