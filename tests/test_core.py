import unittest

from html5_named_entity import decode, decode_one, NAMED_ENTITIES


class TestDecode(unittest.TestCase):
    def test_basic_semicolon(self):
        self.assertEqual(decode("&amp;"), "&")

    def test_basic_without_semicolon(self):
        self.assertEqual(decode("&amp"), "&")

    def test_multiple_entities(self):
        self.assertEqual(decode("&lt;tag&gt;"), "<tag>")

    def test_text_between_entities(self):
        self.assertEqual(decode("a&amp;b"), "a&b")

    def test_no_entities(self):
        self.assertEqual(decode("plain text"), "plain text")

    def test_empty_string(self):
        self.assertEqual(decode(""), "")

    def test_unknown_entity_left_as_is(self):
        self.assertEqual(decode("&notarealthing;"), "&notarealthing;")

    def test_ampersand_alone_left_as_is(self):
        self.assertEqual(decode("Tom & Jerry"), "Tom & Jerry")

    def test_apos_entity(self):
        self.assertEqual(decode("&apos;"), "'")

    def test_euro(self):
        self.assertEqual(decode("&euro;"), "\u20AC")

    def test_numeric_reference_not_decoded(self):
        self.assertEqual(decode("&#39;"), "&#39;")

    def test_numeric_reference_left_untouched(self):
        self.assertEqual(decode("&#x27;"), "&#x27;")

    def test_not_without_semicolon_is_legacy(self):
        self.assertEqual(decode("&not"), "\u00AC")

    def test_nbsp_followed_by_space(self):
        self.assertEqual(decode("&nbsp; "), "\u00A0 ")

    def test_nbsp_without_semicolon_followed_by_space(self):
        self.assertEqual(decode("&nbsp "), "\u00A0 ")

    def test_adjacent_entities(self):
        self.assertEqual(decode("&lt;&gt;"), "<>")

    def test_entity_at_end_of_string(self):
        self.assertEqual(decode("end&gt;"), "end>")

    def test_quoted_attributes(self):
        self.assertEqual(decode('name="a&quot;b"'), 'name="a\"b"')

    def test_cdata_not_special(self):
        self.assertEqual(decode("a &amp b"), "a & b")


class TestDecodeOne(unittest.TestCase):
    def test_amp_at_position_zero(self):
        self.assertEqual(decode_one("&amp;", 0), ("&", 5))

    def test_amp_without_semicolon(self):
        self.assertEqual(decode_one("&amp", 0), ("&", 4))

    def test_no_entity_at_position(self):
        self.assertEqual(decode_one("plain", 0), ("", 0))

    def test_ampersand_alone(self):
        self.assertEqual(decode_one("Tom & Jerry", 4), ("", 0))

    def test_euro(self):
        self.assertEqual(decode_one("&euro;", 0), ("\u20AC", 6))

    def test_pos_in_middle(self):
        self.assertEqual(decode_one("x&lt;y", 1), ("<", 4))

    def test_lt_without_semicolon(self):
        self.assertEqual(decode_one("&lt", 0), ("<", 3))

    def test_not_without_semicolon(self):
        self.assertEqual(decode_one("&not", 0), ("\u00AC", 4))

    def test_unknown_entity(self):
        self.assertEqual(decode_one("&foo;", 0), ("", 0))


class TestEntityTable(unittest.TestCase):
    def test_amp_with_semicolon_exists(self):
        self.assertIn("amp;", NAMED_ENTITIES)
        self.assertEqual(NAMED_ENTITIES["amp;"][0], "&")

    def test_amp_without_semicolon_exists(self):
        self.assertIn("amp", NAMED_ENTITIES)
        self.assertEqual(NAMED_ENTITIES["amp"][0], "&")

    def test_euro_only_with_semicolon(self):
        self.assertIn("euro;", NAMED_ENTITIES)
        self.assertNotIn("euro", NAMED_ENTITIES)

    def test_apos_only_with_semicolon(self):
        self.assertIn("apos;", NAMED_ENTITIES)
        self.assertEqual(NAMED_ENTITIES["apos;"][0], "'")

    def test_lt_both_forms(self):
        self.assertIn("lt;", NAMED_ENTITIES)
        self.assertIn("lt", NAMED_ENTITIES)
        self.assertEqual(NAMED_ENTITIES["lt;"][0], "<")
        self.assertEqual(NAMED_ENTITIES["lt"][0], "<")

    def test_value_is_tuple_with_bool(self):
        entry = NAMED_ENTITIES["amp;"]
        self.assertIsInstance(entry, tuple)
        self.assertEqual(len(entry), 2)
        self.assertIsInstance(entry[0], str)
        self.assertIsInstance(entry[1], bool)


if __name__ == "__main__":
    unittest.main()
