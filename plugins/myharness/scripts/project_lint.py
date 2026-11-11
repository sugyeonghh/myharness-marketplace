"""Edit/Write 뒤에 프로젝트의 아키텍처 린터를 돌리는 PostToolUse Hook.

아키텍처 규칙은 프로젝트마다 다르므로 규칙 자체는 플러그인에 두지 않는다.
프로젝트에 `scripts/arch_lint.py` 가 있으면 실행하고, 없으면 아무것도 하지 않는다.

린터 작성 약속
  - 위반이 있으면 exit 2 로 끝내고, 수정 지침을 stderr 에 쓴다.
  - 그러면 이 Hook 이 그 지침을 그대로 에이전트에게 돌려준다.
"""
import os
import subprocess
import sys
from pathlib import Path

LINTER = Path("scripts") / "arch_lint.py"


def main() -> int:
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    linter = project / LINTER
    if not linter.is_file():
        return 0
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run(
        [sys.executable, str(linter)], cwd=project, env=env, capture_output=True
    )
    sys.stderr.buffer.write(result.stderr)
    sys.stderr.flush()
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
