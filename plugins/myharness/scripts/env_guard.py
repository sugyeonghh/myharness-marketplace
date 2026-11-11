""".env 파일 읽기를 막는 PreToolUse Hook.

플러그인은 permissions.deny 를 실어 보낼 수 없어서,
원래 settings.json 의 "Read(./.env)" 거부를 Hook 으로 옮긴 것이다.

막는 것
  - .env, .env.local 처럼 .env 로 시작하는 파일
  - 단, .env.example / .env.sample / .env.template 은 허용
"""
import json
import sys
from pathlib import PurePath

ALLOWED_SUFFIXES = (".example", ".sample", ".template")


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    file_path = (data.get("tool_input") or {}).get("file_path", "")
    name = PurePath(file_path.replace("\\", "/")).name
    if (name == ".env" or name.startswith(".env.")) and not name.endswith(ALLOWED_SUFFIXES):
        print(f"[env_guard] 차단: {file_path}\n이유: .env 는 비밀값 파일이라 읽지 않습니다. "
              "필요한 키 이름은 사람에게 물어보세요.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
