import unittest

import automation as A


class TestClassifyScope(unittest.TestCase):
    def test_block_image_gen(self):
        v, _ = A.classify_scope("Nano Banana Pro prompts for image generation", [], "Python", "prompts")
        self.assertEqual(v, "BLOCK")

    def test_block_framework(self):
        v, _ = A.classify_scope("cloud-native Go microservice framework", ["go"], "Go", "spec-driven")
        self.assertEqual(v, "BLOCK")

    def test_block_desktop_app(self):
        v, _ = A.classify_scope("all-in-one Desktop AI application with RAG", [], "JavaScript", "mcp")
        self.assertEqual(v, "BLOCK")

    def test_pass_mcp_server(self):
        v, _ = A.classify_scope("The official GitHub MCP server", ["mcp"], "Go", "mcp")
        self.assertEqual(v, "PASS")

    def test_pass_claude_md(self):
        v, _ = A.classify_scope("Claude Code starter template with CLAUDE.md memory bank", [], "Python", "claude-md")
        self.assertEqual(v, "PASS")

    def test_warn_no_generic_signal(self):
        v, _ = A.classify_scope("3D digital twin visualization toolkit", ["vue"], "Vue", "spec-driven")
        self.assertEqual(v, "WARN")

    def test_block_ad_audit(self):
        v, _ = A.classify_scope("Claude Code skill for paid ad auditing and marketing", [], "Python", "skills")
        # ad audit는 BLOCK 패턴이므로 BLOCK이 우선
        self.assertEqual(v, "BLOCK")

    def test_block_job_hunting(self):
        v, _ = A.classify_scope("Claude Code based job-hunting system with skill modes", [], "JavaScript", "skills")
        self.assertEqual(v, "BLOCK")  # "job-hunting"은 product-app 패턴


if __name__ == "__main__":
    unittest.main()
