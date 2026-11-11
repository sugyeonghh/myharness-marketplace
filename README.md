# myharness-marketplace

practice-m3 하네스에서 프로젝트 전용 내용을 뺀 플러그인 마켓플레이스.

## 설치

```
/plugin marketplace add sugyeonghh/myharness-marketplace
/plugin install myharness@myharness-marketplace
```

## 들어 있는 것

| 종류 | 이름 | 하는 일 |
|---|---|---|
| agent | `verifier` | spec 기준으로 검증하고 문제만 보고한다 (코드 수정 안 함) |
| agent | `cleaner` | 라운드 끝에 죽은 코드 · 중복 · 어긋난 문서를 정리한다 |
| hook (PreToolUse, Bash/PowerShell) | `guard.py` | `rm -rf`, `Remove-Item -Recurse -Force`, `rmdir /s`, `git push --force` 차단 |
| hook (PreToolUse, Read) | `env_guard.py` | `.env` 계열 파일 읽기 차단 (`.env.example` 등은 허용) |
| hook (PostToolUse, Edit/Write) | `project_lint.py` | 프로젝트에 `scripts/arch_lint.py` 가 있으면 실행, 위반 시 에이전트에게 전달 |

## 프로젝트 쪽에서 준비할 것

- `CLAUDE.md`: 테스트 · 린트 명령, 코드 규칙, 라운드 종료 조건 (에이전트가 여기를 기준으로 삼는다)
- `docs/roundNN/spec.md` · `plan.md` · `review.md`, `docs/SSOT.md` (라운드 방식을 쓸 때)
- `scripts/arch_lint.py` (선택): 위반 시 exit 2 + stderr 에 수정 지침

## practice-m3 에서 뺀 것

- pip / `python -m venv` 차단 규칙 (uv 전용 프로젝트 규칙)
- `app/routes` → `app/db` import 금지, `print()` 금지 린트 규칙 (프로젝트 구조 전용)
- Todo API · uv 명령 등 CLAUDE.md 의 프로젝트 설명

Hook 은 `python` 으로 실행되므로 PATH 에 Python 3 이 있어야 한다.
