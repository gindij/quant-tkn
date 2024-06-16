VERSE_LINE_START_SYMBOL = "\u202B"


class TextParsingUtils:
    """
    Utility functions for parsing text. These functions are used to parse the text files containing the Tanakh.
    """

    @staticmethod
    def is_line_start_of_verse(line: str) -> bool:
        """
        Check if a line is the start of a verse.

        :param line: The line to check.
        :return: True if the line is the start of a verse, False otherwise.
        """
        return line.startswith(VERSE_LINE_START_SYMBOL)

    @staticmethod
    def is_line_start_of_chapter(line: str) -> bool:
        """
        Check if a line is the start of a chapter.

        :param line: The line to check.
        :return: True if the line is the start of a chapter, False otherwise.
        """
        return "Chapter" in line

    @staticmethod
    def is_line_start_of_book(line: str) -> bool:
        """
        Check if a line is the start of a book.

        :param line: The line to check.
        :return: True if the line is the start of a book, False otherwise.
        """
        return "chapters" in line and "verses" in line and "End of" not in line

    @staticmethod
    def extract_chapter_idx(line: str) -> int:
        """
        Extract the chapter index from a line.

        :param line: The chapter specification line.
        :return: The chapter index.
        """
        return int(line.split()[2])

    @staticmethod
    def extract_verse_idx(line: str) -> int:
        """
        Extract the verse index from a line.

        :param line: The verse specification line.
        :return: The verse index.
        """
        return int(line.split()[1])

    @staticmethod
    def extract_book_name(line: str) -> str:
        """
        Extract the book name from a line.

        :param line: The verse specification line.
        :return: The book name.
        """
        return line.split()[1]
