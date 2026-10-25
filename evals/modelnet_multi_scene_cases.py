MODELNET_MULTI_SCENE_CASES = [
    # -------------------------------------------------
    # Scene 1
    # -------------------------------------------------
    {
        "scene": "scene_1",
        "question": "Which object is the largest?",
        "expected_answer_contains": [
            "cabinet",
        ],
        "expected_tools": [
            "find_largest_object",
        ],
    },
    {
        "scene": "scene_1",
        "question": "Which object is closest to the table by center distance?",
        "expected_answer_contains": [
            "stool",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_nearest_object",
        ],
    },
    {
        "scene": "scene_1",
        "question": "Is the chair to the right of the table?",
        "expected_answer_contains": [
            "yes",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "relative_position",
        ],
    },
    {
        "scene": "scene_1",
        "question": "Can the stool pass through the doorway opening?",
        "expected_answer_contains": [
            "yes",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
    },
    {
        "scene": "scene_1",
        "question": "Can the cabinet pass through the doorway opening?",
        "expected_answer_contains": [
            "no",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
    },

    # -------------------------------------------------
    # Scene 2
    # -------------------------------------------------
    {
        "scene": "scene_2",
        "question": "Which object is the largest?",
        "expected_answer_contains": [
            "cabinet",
        ],
        "expected_tools": [
            "find_largest_object",
        ],
    },
    {
        "scene": "scene_2",
        "question": "Which object is closest to the table by center distance?",
        "expected_answer_contains": [
            "chair",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_nearest_object",
        ],
    },
    {
        "scene": "scene_2",
        "question": "Is the chair to the right of the table?",
        "expected_answer_contains": [
            "no",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "relative_position",
        ],
    },
    {
        "scene": "scene_2",
        "question": "Can the stool pass through the doorway opening?",
        "expected_answer_contains": [
            "yes",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
    },
    {
        "scene": "scene_2",
        "question": "Can the cabinet pass through the doorway opening?",
        "expected_answer_contains": [
            "no",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
    },

    # -------------------------------------------------
    # Scene 3
    # -------------------------------------------------
    {
        "scene": "scene_3",
        "question": "Which object is the largest?",
        "expected_answer_contains": [
            "cabinet",
        ],
        "expected_tools": [
            "find_largest_object",
        ],
    },
    {
        "scene": "scene_3",
        "question": "Which object is closest to the table by center distance?",
        "expected_answer_contains": [
            "stool",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_nearest_object",
        ],
    },
    {
        "scene": "scene_3",
        "question": "Is the chair to the right of the table?",
        "expected_answer_contains": [
            "yes",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "relative_position",
        ],
    },
    {
        "scene": "scene_3",
        "question": "Can the stool pass through the doorway opening?",
        "expected_answer_contains": [
            "yes",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
    },
    {
        "scene": "scene_3",
        "question": "Can the cabinet pass through the doorway opening?",
        "expected_answer_contains": [
            "yes",
        ],
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
    },
]