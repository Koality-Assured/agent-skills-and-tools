"""Unit tests verifying skills against schemas."""

import json
import unittest
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

from tools.validator import extract_frontmatter, validate_skill_file


class TestSkillsAndSchemas(unittest.TestCase):
    def setUp(self):
        self.root = _ROOT
        self.schemas_dir = self.root / "schemas"
        self.skills_dir = self.root / "skills"

    def test_schemas_exist_and_are_valid_json(self):
        skill_schema = self.schemas_dir / "skill.schema.json"
        tool_schema = self.schemas_dir / "tool.schema.json"

        self.assertTrue(skill_schema.exists(), "skill.schema.json should exist")
        self.assertTrue(tool_schema.exists(), "tool.schema.json should exist")

        json.loads(skill_schema.read_text(encoding="utf-8"))
        json.loads(tool_schema.read_text(encoding="utf-8"))

    def test_bundled_skills_conform_to_schema(self):
        skill_schema = self.schemas_dir / "skill.schema.json"
        skill_files = list(self.skills_dir.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skill_files), 2, "Should have at least 2 bundled skills")

        for sf in skill_files:
            ok, errors = validate_skill_file(sf, skill_schema)
            self.assertTrue(ok, f"Skill {sf.name} failed validation: {errors}")

    def test_frontmatter_extraction(self):
        sample = """---
name: test-skill
description: This is a valid test skill description.
version: 1.0.0
tags: [test, sample]
---

# Content
"""
        fm = extract_frontmatter(sample)
        self.assertEqual(fm["name"], "test-skill")
        self.assertEqual(fm["version"], "1.0.0")
        self.assertEqual(fm["tags"], ["test", "sample"])


if __name__ == "__main__":
    unittest.main()
