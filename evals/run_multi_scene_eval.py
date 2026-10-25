from collections import defaultdict
from statistics import mean

from app.agent import run_agent
from evals.multi_scene_cases import (
    MULTI_SCENE_CASES,
    get_scene_paths,
)
from evals.run_agent_eval import (
    answer_terms_match,
    subsequence_match,
)


def main():
    results = []

    for case in MULTI_SCENE_CASES:
        scene_path, labels_path = get_scene_paths(
            case["scene"]
        )

        print(
            f"\n{'=' * 70}\n"
            f"{case['id']}\n"
            f"Scene: {case['scene']}\n"
            f"Q: {case['question']}"
        )

        result = run_agent(
            case["question"],
            return_trace=True,
            scene_path=scene_path,
            labels_path=labels_path,
        )

        answer = result["answer"]

        actual_tools = [
            item["name"]
            for item in result["tool_trace"]
        ]

        tool_ok = subsequence_match(
            actual_tools,
            case["expected_tools"],
        )

        answer_ok = answer_terms_match(
            answer,
            case["expected_answer_terms"],
        )

        passed = (
            tool_ok
            and answer_ok
        )

        result_item = {
            "id": case["id"],
            "scene": case["scene"],
            "tool_ok": tool_ok,
            "answer_ok": answer_ok,
            "passed": passed,
            "tool_calls": len(actual_tools),
        }

        results.append(
            result_item
        )

        print(
            f"Tools: {actual_tools}"
        )

        print(
            f"Expected: "
            f"{case['expected_tools']}"
        )

        print(
            f"Answer: {answer}"
        )

        print(
            f"Tool check: {tool_ok}"
        )

        print(
            f"Answer check: {answer_ok}"
        )

        print(
            "PASS"
            if passed
            else "FAIL"
        )

    # ---------------------------------------------------------
    # Per-scene results
    # ---------------------------------------------------------

    grouped = defaultdict(list)

    for item in results:
        grouped[
            item["scene"]
        ].append(item)

    print(
        "\n"
        + "=" * 70
    )

    print(
        "PER-SCENE RESULTS"
    )

    print(
        "=" * 70
    )

    for scene_name, scene_results in grouped.items():
        passed = sum(
            item["passed"]
            for item in scene_results
        )

        total = len(
            scene_results
        )

        print(
            f"{scene_name}: "
            f"{passed}/{total} "
            f"({passed / total:.1%})"
        )

    # ---------------------------------------------------------
    # Aggregate results
    # ---------------------------------------------------------

    total = len(
        results
    )

    passed = sum(
        item["passed"]
        for item in results
    )

    tool_passed = sum(
        item["tool_ok"]
        for item in results
    )

    answer_passed = sum(
        item["answer_ok"]
        for item in results
    )

    avg_calls = mean(
        item["tool_calls"]
        for item in results
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "MULTI-SCENE SUMMARY"
    )

    print(
        "=" * 70
    )

    print(
        f"Overall: "
        f"{passed}/{total} "
        f"({passed / total:.1%})"
    )

    print(
        f"Tool selection: "
        f"{tool_passed}/{total} "
        f"({tool_passed / total:.1%})"
    )

    print(
        f"Answer checks: "
        f"{answer_passed}/{total} "
        f"({answer_passed / total:.1%})"
    )

    print(
        f"Average tool calls: "
        f"{avg_calls:.2f}"
    )

    failed = [
        item["id"]
        for item in results
        if not item["passed"]
    ]

    if failed:
        print(
            "\nFailed cases:"
        )

        for case_id in failed:
            print(
                f"- {case_id}"
            )


if __name__ == "__main__":
    main()