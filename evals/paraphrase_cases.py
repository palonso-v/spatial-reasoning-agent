PARAPHRASE_CASES = [
    {
        "id": "largest_object_paraphrase",
        "question": "What is the biggest thing in the scene?",
        "expected_tools": [
            "find_largest_object",
        ],
        "expected_answer_terms": [
            "cabinet",
        ],
    },
    {
        "id": "nearest_centroid_paraphrase",
        "question": "Which thing has its center closest to the center of the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_nearest_object",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "nearest_surface_paraphrase",
        "question": "What is sitting physically nearest to the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_nearest_object_by_surface",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "near_table_paraphrase",
        "question": "What things are close to the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_objects_by_relation",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "box_left_chair_paraphrase",
        "question": "If I look at the box and chair, is the box on the left side?",
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
        "id": "chair_right_box_paraphrase",
        "question": "Does the chair sit to the right of the box?",
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
        "id": "near_and_front_paraphrase",
        "question": "What is close to the table while also being in front of it?",
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
        "id": "chair_near_table_paraphrase",
        "question": "Would you consider the chair close to the table?",
        "expected_tools": [
            "find_object_by_label",
            "find_object_by_label",
            "find_objects_by_relation",
        ],
        "expected_answer_terms": [
            "no",
        ],
    },
    {
        "id": "box_inside_cabinet_paraphrase",
        "question": "Could I put the box completely inside the cabinet?",
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
        "id": "chair_inside_box_paraphrase",
        "question": "Is the box large enough to contain the chair?",
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
        "id": "box_doorway_paraphrase",
        "question": "Could the box get through the doorway?",
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
        "id": "cabinet_doorway_paraphrase",
        "question": "Would the cabinet make it through the doorway opening?",
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
        "id": "within_radius_paraphrase",
        "question": "What objects have their centers less than 2 units from the table?",
        "expected_tools": [
            "find_object_by_label",
            "objects_within_radius",
        ],
        "expected_answer_terms": [
            "box",
        ],
    },
    {
        "id": "overlap_paraphrase",
        "question": "Do the table and box occupy overlapping bounding-box space?",
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
        "id": "describe_table_paraphrase",
        "question": "Tell me how the table is positioned relative to everything else.",
        "expected_tools": [
            "find_object_by_label",
            "describe_object_relations",
        ],
        "expected_answer_terms": [
            "box",
            "chair",
            "cabinet",
        ],
    },
    {
        "id": "cabinet_right_chair_paraphrase",
        "question": "Is the cabinet positioned on the chair's right-hand side?",
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
        "id": "door_right_cabinet_paraphrase",
        "question": "From their positions, is the doorway farther right than the cabinet?",
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
        "id": "surface_distance_paraphrase",
        "question": "How much empty space separates the table's surface from the box's surface?",
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
        "id": "centroid_distance_paraphrase",
        "question": "How far apart are the centers of the table and the box?",
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
        "id": "multi_relation_paraphrase",
        "question": "Find the thing that is simultaneously close to and ahead of the table.",
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