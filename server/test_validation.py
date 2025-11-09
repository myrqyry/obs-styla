import unittest
from validation import validate_theme_content

class TestThemeValidation(unittest.TestCase):

    def test_invalid_theme_with_hyphen(self):
        """Test that a theme with a hyphen in a variable name fails validation."""
        invalid_content = """
@OBSThemeMeta {
    id: "com.obsproject.Yami.Invalid-Theme";
    name: "Invalid Theme";
    dark: "true";
}
@OBSThemeVars {
    --invalid-variable: "#FF0000";
}
        """
        report = validate_theme_content(invalid_content)
        self.assertGreater(report.summary.errors, 0, "Should have errors")
        self.assertTrue(
            any("Could not parse line" in e.message for e in report.errors),
            "Should have a parse error for the invalid variable"
        )

    def test_valid_theme(self):
        """Test that a valid theme passes validation."""
        valid_content = """
@OBSThemeMeta {
    id: "com.obsproject.Yami.Valid-Theme";
    name: "Valid Theme";
    dark: "true";
}
@OBSThemeVars {
    --valid_variable: "#00FF00";
}
        """
        report = validate_theme_content(valid_content)
        self.assertEqual(report.summary.errors, 0, "Should have no errors")

    def test_invalid_variable_reference(self):
        """Test that a theme with a hyphen in a variable reference fails validation."""
        invalid_content = """
@OBSThemeMeta {
    id: "com.obsproject.Yami.Invalid-Reference";
    name: "Invalid Reference";
    dark: "true";
}
@OBSThemeVars {
    --valid_variable: var(--invalid-reference);
}
        """
        report = validate_theme_content(invalid_content)
        self.assertGreater(report.summary.errors, 0, "Should have errors")
        self.assertTrue(
            any("contains invalid characters" in e.message for e in report.errors),
            "Should have a parse error for the invalid variable reference"
        )


if __name__ == '__main__':
    unittest.main()
