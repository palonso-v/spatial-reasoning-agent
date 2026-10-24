EVAL_CASES = [
    {
        "id": "largest_object",
        "question": "Which object is the largest?",
        "expected_tools": [
            "find_largest_object",
        ],
        "expected_answer_terms": [
            "cabinet",
        ],
    },
    {
        "id": "nearest_to_table_centroid",
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
        "id": "nearest_to_table_surface",
        "question": "Which object is physically closest to the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_nearest_object_by_surface",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "near_table",
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
        "id": "box_left_of_chair",
        "question": "Is the box left of the chair?",
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
        "id": "chair_right_of_box",
        "question": "Is the chair right of the box?",
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
        "id": "box_near_table_and_front",
        "question": "Which objects are near the table and in front of it?",
        "expected_tools": [
            "find_object_by_label",
            "find_objects_by_relation",
            "find_objects_by_relation",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "chair_near_table",
        "question": "Is the chair near the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
        ],
        "expected_answer_terms": [
            "no",
        ],
    },
    {
        "id": "box_inside_cabinet",
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
        "id": "chair_inside_box",
        "question": "Can the chair fit inside the box?",
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
        "id": "box_through_door",
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
    {
        "id": "cabinet_through_door",
        "question": "Can the cabinet pass through the doorway opening?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "can_pass_through_opening",
        ],
        "expected_answer_terms": [
            "no",
        ],
    },
    {
        "id": "objects_within_2_table",
        "question": "Which objects are within 2 units of the table?",
        "expected_tools": [
            "find_object_by_label",
            "objects_within_radius",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "table_box_overlap",
        "question": "Do the table and the box overlap?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "bounding_boxes_overlap",
        ],
        "expected_answer_terms": [
            "no",
        ],
    },
    {
        "id": "describe_table",
        "question": "Describe the spatial relationships around the table.",
        "expected_tools": [
            "find_object_by_label",
            "describe_object_relations",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "cabinet_vs_chair",
        "question": "Is the cabinet to the right of the chair?",
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
        "id": "doorway_vs_cabinet",
        "question": "Is the doorway opening to the right of the cabinet?",
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
        "id": "surface_distance_table_box",
        "question": "What is the physical surface distance between the table and the box?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "surface_distance_between_objects",
        ],
        "expected_answer_terms": [
            "0.4",
        ],
    },
    {
        "id": "centroid_distance_table_box",
        "question": "What is the centroid distance between the table and the box?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "distance_between_objects",
        ],
        "expected_answer_terms": [
            "1.48",
        ],
    },
    {
        "id": "near_and_front_table",
        "question": "Which object is both near the table and in front of the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_objects_by_relation",
            "find_objects_by_relation",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
]