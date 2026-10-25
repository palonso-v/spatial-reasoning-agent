from pathlib import Path

from app.agent import run_agent
from evals.modelnet_multi_scene_cases import (
    MODELNET_MULTI_SCENE_CASES,
)


SCENE_DIR = Path(
    "data/modelnet_eval_scenes"
)


def normalize_text(
    value: str,
) -> str:

    return (
        value
        .strip()
        .lower()
    )


def tool_names(
    trace,
):

    return [
        item["name"]
        for item in trace
    ]


def answer_passes(
    answer,
    expected_terms,
):

    normalized = normalize_text(
        answer
    )

    return all(
        normalize_text(term)
        in normalized
        for term in expected_terms
    )


def tools_pass(
    actual,
    expected,
):

    if len(actual) < len(expected):
        return False

    expected_index = 0

    for name in actual:

        if (
            name
            == expected[
                expected_index
            ]
        ):
            expected_index += 1

            if (
                expected_index
                == len(expected)
            ):
                return True

    return False


def main():

    total = len(
        MODELNET_MULTI_SCENE_CASES
    )

    answer_score = 0
    tool_score = 0
    overall_score = 0

    total_tool_calls = 0

    scene_scores = {}


    for index, case in enumerate(
        MODELNET_MULTI_SCENE_CASES,
        start=1,
    ):

        scene_name = case[
            "scene"
        ]

        scene_path = (
            SCENE_DIR
            / f"{scene_name}.ply"
        )

        labels_path = (
            SCENE_DIR
            / (
                f"{scene_name}"
                "_labels.json"
            )
        )


        print(
            "\n"
            + "=" * 70
        )

        print(
            f"CASE {index}/{total}"
        )

        print(
            f"Scene: {scene_name}"
        )

        print(
            f"Question: "
            f"{case['question']}"
        )


        result = run_agent(
            case["question"],
            return_trace=True,
            scene_path=scene_path,
            labels_path=labels_path,
        )


        answer = result[
            "answer"
        ]

        trace = result[
            "tool_trace"
        ]

        actual_tools = (
            tool_names(
                trace
            )
        )


        answer_ok = (
            answer_passes(
                answer,
                case[
                    "expected_answer_contains"
                ],
            )
        )

        tools_ok = (
            tools_pass(
                actual_tools,
                case[
                    "expected_tools"
                ],
            )
        )

        overall_ok = (
            answer_ok
            and tools_ok
        )


        total_tool_calls += len(
            actual_tools
        )


        if answer_ok:
            answer_score += 1

        if tools_ok:
            tool_score += 1

        if overall_ok:
            overall_score += 1


        if scene_name not in scene_scores:
            scene_scores[
                scene_name
            ] = {
                "passed": 0,
                "total": 0,
            }


        scene_scores[
            scene_name
        ][
            "total"
        ] += 1


        if overall_ok:
            scene_scores[
                scene_name
            ][
                "passed"
            ] += 1


        print(
            f"Answer: {answer}"
        )

        print(
            f"Tools: {actual_tools}"
        )

        print(
            "Answer check:",
            "PASS"
            if answer_ok
            else "FAIL",
        )

        print(
            "Tool check:",
            "PASS"
            if tools_ok
            else "FAIL",
        )

        print(
            "Overall:",
            "PASS"
            if overall_ok
            else "FAIL",
        )


    average_calls = (
        total_tool_calls
        / total
    )


    print(
        "\n"
        + "=" * 70
    )

    print(
        "MODELNET MULTI-SCENE RESULTS"
    )

    print(
        "=" * 70
    )


    for scene_name, result in (
        scene_scores.items()
    ):

        print(
            f"{scene_name}: "
            f"{result['passed']}/"
            f"{result['total']}"
        )


    print()

    print(
        f"Overall: "
        f"{overall_score}/{total}"
    )

    print(
        f"Tool selection: "
        f"{tool_score}/{total}"
    )

    print(
        f"Answer checks: "
        f"{answer_score}/{total}"
    )

    print(
        f"Average tool calls: "
        f"{average_calls:.2f}"
    )


if __name__ == "__main__":
    main()