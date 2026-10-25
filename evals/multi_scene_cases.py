from pathlib import Path


SCENE_DIR = Path("data/eval_scenes")


MULTI_SCENE_CASES = [
    # =========================================================
    # SCENE 1
    # =========================================================
    {
        "id": "scene1_largest",
        "scene": "scene_1",
        "question": "Which object is the largest?",
        "expected_tools": [
            "find_largest_object",
        ],
        "expected_answer_terms": [
            "cabinet",
        ],
    },
    {
        "id": "scene1_nearest_table",
        "scene": "scene_1",
        "question": "Which object is closest to the table by center distance?",
        "expected_tools": [
            "find_object_by_label",
            "find_nearest_object",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "scene1_near_table",
        "scene": "scene_1",
        "question": "Which objects are near the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_objects_by_relation",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "scene1_box_inside_cabinet",
        "scene": "scene_1",
        "question": "Can the box fit inside the cabinet?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_fit_inside",
        ],
        "expected_answer_terms": [
            "yes",
        ],
    },
    {
        "id": "scene1_box_doorway",
        "scene": "scene_1",
        "question": "Can the box pass through the doorway opening?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
        "expected_answer_terms": [
            "yes",
        ],
    },

    # =========================================================
    # SCENE 2
    # =========================================================
    {
        "id": "scene2_largest",
        "scene": "scene_2",
        "question": "Which object is the largest?",
        "expected_tools": [
            "find_largest_object",
        ],
        "expected_answer_terms": [
            "cabinet",
        ],
    },
    {
        "id": "scene2_nearest_table",
        "scene": "scene_2",
        "question": "Which object is closest to the table by center distance?",
        "expected_tools": [
            "find_object_by_label",
            "find_nearest_object",
        ],
        "expected_answer_terms": [
            "chair",
        ],
    },
    {
        "id": "scene2_chair_left_table",
        "scene": "scene_2",
        "question": "Is the chair to the left of the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "relative_position",
        ],
        "expected_answer_terms": [
            "yes",
        ],
    },
    {
        "id": "scene2_box_inside_cabinet",
        "scene": "scene_2",
        "question": "Can the box fit inside the cabinet?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_fit_inside",
        ],
        "expected_answer_terms": [
            "no",
        ],
    },
    {
        "id": "scene2_box_doorway",
        "scene": "scene_2",
        "question": "Can the box pass through the doorway opening?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
        "expected_answer_terms": [
            "no",
        ],
    },

    # =========================================================
    # SCENE 3
    # =========================================================
    {
        "id": "scene3_largest",
        "scene": "scene_3",
        "question": "Which object is the largest?",
        "expected_tools": [
            "find_largest_object",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "scene3_nearest_table",
        "scene": "scene_3",
        "question": "Which object is closest to the table by center distance?",
        "expected_tools": [
            "find_object_by_label",
            "find_nearest_object",
        ],
        "expected_answer_terms": [
            "chair",
        ],
    },
    {
        "id": "scene3_chair_right_table",
        "scene": "scene_3",
        "question": "Is the chair to the right of the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "relative_position",
        ],
        "expected_answer_terms": [
            "yes",
        ],
    },
    {
        "id": "scene3_box_inside_cabinet",
        "scene": "scene_3",
        "question": "Can the box fit inside the cabinet?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_fit_inside",
        ],
        "expected_answer_terms": [
            "no",
        ],
    },
    {
        "id": "scene3_box_doorway",
        "scene": "scene_3",
        "question": "Can the box pass through the doorway opening?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
        "expected_answer_terms": [
            "no",
        ],
    },
]


def get_scene_paths(scene_name: str):
    return (
        SCENE_DIR / f"{scene_name}.ply",
        SCENE_DIR / f"{scene_name}_labels.json",
    )