class AuthorSchema:
    def to_dict(self, author):
        return {
            "name": author.name,
            "birth_year": author.birth_year,
            "death_year": author.death_year,
        }


class FormatSchema:
    def to_dict(self, format_obj):
        return {
            "mime_type": format_obj.mime_type,
            "url": format_obj.url,
        }


class BookSchema:
    def __init__(self):
        self.author_schema = AuthorSchema()
        self.format_schema = FormatSchema()

    def to_dict(self, book):
        return {
            "id": book.gutenberg_id,
            "title": book.title,
            "authors": [self.author_schema.to_dict(author) for author in book.authors],
            "languages": [lang.code for lang in book.languages],
            "subjects": [sub.name for sub in book.subjects],
            "bookshelves": [bs.name for bs in book.bookshelves],
            "download_count": book.download_count,
            "formats": [self.format_schema.to_dict(fmt) for fmt in book.formats],
        }


class BookListSchema:
    def __init__(self):
        self.book_schema = BookSchema()

    def to_dict(self, count, books):
        return {
            "count": count,
            "results": [self.book_schema.to_dict(book) for book in books],
        }
