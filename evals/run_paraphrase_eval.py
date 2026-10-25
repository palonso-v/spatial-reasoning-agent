from statistics import mean

from app.agent import run_agent
from evals.paraphrase_cases import PARAPHRASE_CASES
from evals.run_agent_eval import (
    answer_terms_match,
    subsequence_match,
)


def main():
    results = []

    for case in PARAPHRASE_CASES:
        print(
            f"\n{'=' * 70}\n"
            f"{case['id']}\n"
            f"Q: {case['question']}"
        )

        result = run_agent(
            case["question"],
            return_trace=True,
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

        passed = tool_ok and answer_ok

        results.append(
            {
                "id": case["id"],
                "tool_ok": tool_ok,
                "answer_ok": answer_ok,
                "passed": passed,
                "tool_calls": len(actual_tools),
            }
        )

        print(f"Tools: {actual_tools}")
        print(
            f"Expected: {case['expected_tools']}"
        )
        print(f"Answer: {answer}")
        print(f"Tool check: {tool_ok}")
        print(f"Answer check: {answer_ok}")
        print(
            "PASS" if passed else "FAIL"
        )

    total = len(results)

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

    print("\n" + "=" * 70)
    print("PARAPHRASE ROBUSTNESS SUMMARY")
    print("=" * 70)

    print(
        f"Overall: {passed}/{total} "
        f"({passed / total:.1%})"
    )

    print(
        f"Tool selection: {tool_passed}/{total} "
        f"({tool_passed / total:.1%})"
    )

    print(
        f"Answer checks: {answer_passed}/{total} "
        f"({answer_passed / total:.1%})"
    )

    print(
        f"Average tool calls: {avg_calls:.2f}"
    )

    failed = [
        item["id"]
        for item in results
        if not item["passed"]
    ]

    if failed:
        print("\nFailed cases:")

        for case_id in failed:
            print(f"- {case_id}")


if __name__ == "__main__":
    main()