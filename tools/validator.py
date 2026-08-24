"""CLI and library tool to validate agent skills and JSON schemas.

tags: [validator, skills, schemas]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import jsonschema
except ImportError:
    jsonschema = None  # type: ignore

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from a Markdown document."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError("Missing YAML frontmatter block (enclosed in '---')")
    raw_yaml = match.group(1)
    if yaml is not None:
        data = yaml.safe_load(raw_yaml)
    else:
        # Fallback simple parser if PyYAML is not installed
        data = {}
        for line in raw_yaml.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip()
                if v.startswith("[") and v.endswith("]"):
                    items = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
                    data[k] = items
                else:
                    data[k] = v.strip("'\"")
    if not isinstance(data, dict):
        raise ValueError(f"Frontmatter did not parse to dictionary: {raw_yaml}")
    return data


def validate_skill_file(skill_md_path: Path, schema_path: Path) -> Tuple[bool, List[str]]:
    """Validate a SKILL.md file against skill.schema.json."""
    errors: List[str] = []
    if not skill_md_path.exists():
        return False, [f"File not found: {skill_md_path}"]

    try:
        content = skill_md_path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
    except Exception as exc:
        return False, [f"Frontmatter parsing error in {skill_md_path}: {exc}"]

    if not schema_path.exists():
        return False, [f"Schema file not found: {schema_path}"]

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, [f"Schema JSON parsing error in {schema_path}: {exc}"]

    if jsonschema is not None:
        validator = jsonschema.Draft202012Validator(schema)
        for err in validator.iter_errors(frontmatter):
            errors.append(f"Validation error at '{err.json_path}': {err.message}")
    else:
        # Fallback manual validation for core required fields
        required = schema.get("required", [])
        for req in required:
            if req not in frontmatter:
                errors.append(f"Missing required frontmatter field: '{req}'")

    return len(errors) == 0, errors


def validate_all_skills(base_dir: Path) -> Tuple[int, int]:
    """Validate all skills under the skills directory."""
    skills_dir = base_dir / "skills"
    schema_path = base_dir / "schemas" / "skill.schema.json"

    if not skills_dir.exists():
        print(f"Error: skills directory not found at {skills_dir}", file=sys.stderr)
        return 0, 1

    skill_files = list(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        print(f"No skills found in {skills_dir}")
        return 0, 0

    passed = 0
    failed = 0

    print(f"Validating {len(skill_files)} skill(s) against {schema_path.name}...")
    for sf in skill_files:
        ok, errors = validate_skill_file(sf, schema_path)
        rel_path = sf.relative_to(base_dir)
        if ok:
            print(f"  [PASS] {rel_path}")
            passed += 1
        else:
            print(f"  [FAIL] {rel_path}")
            for e in errors:
                print(f"         - {e}")
            failed += 1

    return passed, failed


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Validate all skills in skills/")
    parser.add_argument("--skill", type=str, help="Path to a specific skill directory or SKILL.md")
    parser.add_argument("--tool-schema", type=str, help="Validate a tool schema JSON file")
    parser.add_argument("--base-dir", type=str, default=".", help="Base directory of repository")
    args = parser.parse_args(argv)

    base = Path(args.base_dir).resolve()

    if args.tool_schema:
        target = Path(args.tool_schema).resolve()
        if not target.exists():
            print(f"Error: Tool schema not found at {target}", file=sys.stderr)
            return 2
        try:
            data = json.loads(target.read_text(encoding="utf-8"))
            if jsonschema is not None:
                jsonschema.Draft202012Validator.check_schema(data)
            print(f"[PASS] Tool schema is valid JSON Schema: {target}")
            return 0
        except Exception as exc:
            print(f"[FAIL] Tool schema error: {exc}", file=sys.stderr)
            return 1

    if args.skill:
        target = Path(args.skill).resolve()
        if target.is_dir():
            target = target / "SKILL.md"
        schema_path = base / "schemas" / "skill.schema.json"
        ok, errors = validate_skill_file(target, schema_path)
        if ok:
            print(f"[PASS] {target}")
            return 0
        else:
            print(f"[FAIL] {target}", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            return 1

    # Default to validating all
    passed, failed = validate_all_skills(base)
    print(f"Result: {passed} passed, {failed} failed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
