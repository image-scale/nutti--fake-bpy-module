import re


def parse_log(log: str) -> dict[str, str]:
    """Parse test runner output into per-test results.

    Args:
        log: Full stdout+stderr output of `bash run_test.sh 2>&1`.

    Returns:
        Dict mapping test_id to status string: "PASSED", "FAILED", "SKIPPED", or "ERROR".
    """
    results = {}

    # Strip ANSI escape codes
    log = re.sub(r'\x1b\[[0-9;]*m', '', log)

    # Match inline pytest output: "path::Class::test_method STATUS [ XX%]"
    inline_pattern = re.compile(
        r'^(tests/\S+\.py::\S+)\s+(PASSED|FAILED|SKIPPED|ERROR)(?:\s.*?)?\s+\[\s*\d+%\]',
        re.MULTILINE
    )
    for m in inline_pattern.finditer(log):
        results.setdefault(m.group(1), m.group(2))

    # Match collection errors: "ERROR tests/path/file.py - ..."
    collection_error_pattern = re.compile(
        r'^ERROR (tests/\S+\.py)(?:\s|$)',
        re.MULTILINE
    )
    for m in collection_error_pattern.finditer(log):
        test_id = m.group(1)
        if test_id not in results:
            results[test_id] = "ERROR"

    return results

