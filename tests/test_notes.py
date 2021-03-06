import unittest
import datetime
from moonreader_tools.notes import PDFNote, FB2Note, AbstractNote

from tests.base import BaseTest, SAMPLE_SHORT_TIMESTAMP


class TestAbstractNotes(unittest.TestCase):

    @unittest.skip("Currently makes no sense")
    def test_str_repr_works(self):
        note_text = "Simple Note"
        note = AbstractNote(note_text=note_text)
        self.assertEqual(str(note), "<Note: {}>".format(note_text))


class TestPDFNotes(unittest.TestCase):

    def test_single_note_parses_correctly(self):
        note_text = "#A*#11#A1#1451497221825#A2#643#A3#646#A4#-11184811#A5#2#A6##A7#test_text#A@#"

        d = PDFNote._dict_from_text(note_text)

        self.assertEqual(d.get("page", ""), "11")
        self.assertEqual(d.get("timestamp", ""), "1451497221825")
        self.assertEqual(d.get("color", ""), "-11184811")
        self.assertEqual(d.get("style", ""), "2")
        self.assertEqual(d.get("text", ""), "test_text")

    def test_dumping_note_to_string_works(self):
        note_text = "#A*#11#A1#1451497221825#A2#643#A3#646#A4#-11184811#A5#2#A6##A7#test_text#A@#"

        d = PDFNote.from_text(note_text)
        dumped_text = d.to_string()
        dumped_note = PDFNote.from_text(dumped_text)

        self.assertEqual(dumped_note.text, "test_text")
        self.assertEqual(dumped_note._timestamp, "1451497221825")
        self.assertEqual(dumped_note._color, "-11184811")
        self.assertEqual(dumped_note.modifier, AbstractNote.CROSSED)

    def test_note_inited_from_text_correctly(self):
        note_text = "#A*#11#A1#1451497221825#A2#643#A3#646#A4#-11184811#A5#2#A6##A7#test_text#A@#"

        note = PDFNote.from_text(note_text)

        self.assertEqual(note.text, "test_text")
        self.assertEqual(note._timestamp, "1451497221825")
        self.assertEqual(note._color, "-11184811")
        self.assertEqual(note.modifier, AbstractNote.CROSSED)

    def test_binary_transform_int_list(self):
        seq1 = [0, 1, 0]
        bin_val = FB2Note.modifier_from_seq(seq1)
        self.assertEqual(bin_val, 0b010)

    def test_binary_transform_str_list(self):
        seq1 = ["0", "1", "0"]
        bin_val = FB2Note.modifier_from_seq(seq1)
        self.assertEqual(bin_val, 0b010)


class TestFB2Notes(BaseTest):

    def test_fb2_note_creation_from_str_list_works(self):
        note = FB2Note.from_str_list(self.sample_list)
        self.assertEqual(note.text, "Some Text")
        self.assertEqual(note.note_id, '1')
        self.assertEqual(note.time, datetime.datetime.fromtimestamp(int(SAMPLE_SHORT_TIMESTAMP)))

    def test_dumping_note_to_str_works(self):
        note = FB2Note.from_str_list(self.sample_list)
        t = note.to_string()
        dumped_note = FB2Note.from_text(t)
        self.assertEqual(dumped_note.text, "Some Text")
        self.assertEqual(dumped_note.note_id, '1')
        self.assertEqual(dumped_note.time, datetime.datetime.fromtimestamp(int(SAMPLE_SHORT_TIMESTAMP)))

    def test_fb2note_correctly_handles_DELETED_attr(self):
        note = FB2Note.from_str_list(self.deleted_note_list)
        self.assertEqual(note.is_deleted, True)

    def test_fb2_note_from_list_has_correct_modifier(self):
        note = FB2Note.from_str_list(self.sample_list)
        self.assertEqual(note.modifier, AbstractNote.WAVED)

    def test_binary_transform_int_list(self):
        seq1 = [0, 1, 0]
        bin_val = FB2Note.modifier_from_seq(seq1)
        self.assertEqual(bin_val, 0b010)

    def test_binary_transform_str_list(self):
        seq1 = ["0", "1", "0"]
        bin_val = FB2Note.modifier_from_seq(seq1)
        self.assertEqual(bin_val, 0b010)
