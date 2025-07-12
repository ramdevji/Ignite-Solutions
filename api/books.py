from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import func, or_, and_
from database import get_db_session
from models import Book, Author, Language, Subject, Bookshelf, Format
from schemas import BookListSchema
from utils.query_parser import parse_comma_separated_list, parse_int_list

books_bp = Blueprint('books_api', __name__, url_prefix='/api/books')


@books_bp.route('/', methods=['GET'])
def get_books():
    db_session_generator = get_db_session()
    db = next(db_session_generator)

    try:
        raw_gutenberg_ids = request.args.get('gutenberg_id')
        raw_languages = request.args.get('language')
        raw_mime_types = request.args.get('mime_type')
        raw_topics = request.args.get('topic')
        raw_authors = request.args.get('author')
        raw_titles = request.args.get('title')

        any_filter_provided = any([
            raw_gutenberg_ids,
            raw_languages,
            raw_mime_types,
            raw_topics,
            raw_authors,
            raw_titles
        ])

        if not any_filter_provided:
            print("API Debug: No filters provided, returning empty result.")
            return jsonify({"count": 0, "results": []})

        query = db.query(Book).options(
            joinedload(Book.authors),
            joinedload(Book.languages),
            joinedload(Book.subjects),
            joinedload(Book.bookshelves),
            joinedload(Book.formats)
        )

        filters_to_apply = []

        gutenberg_ids = parse_int_list(raw_gutenberg_ids)
        languages = parse_comma_separated_list(raw_languages)
        mime_types = parse_comma_separated_list(raw_mime_types)
        topics = parse_comma_separated_list(raw_topics)
        authors = parse_comma_separated_list(raw_authors)
        titles = parse_comma_separated_list(raw_titles)

        if gutenberg_ids:
            filters_to_apply.append(Book.gutenberg_id.in_(gutenberg_ids))

        if languages:
            query = query.join(Book.languages)
            filters_to_apply.append(Language.code.in_(languages))

        if mime_types:
            query = query.join(Book.formats)
            filters_to_apply.append(Format.mime_type.in_(mime_types))

        if topics:
            topic_conditions = []
            for t in topics:
                topic_conditions.append(func.lower(Subject.name).like(f'%{t}%'))
                topic_conditions.append(func.lower(Bookshelf.name).like(f'%{t}%'))

            query = query.outerjoin(Book.subjects) \
                .outerjoin(Book.bookshelves)
            if topic_conditions:
                if len(topic_conditions) == 1:
                    filters_to_apply.append(topic_conditions[0])
                else:
                    filters_to_apply.append(or_(*topic_conditions))

        if authors:
            author_conditions = []
            for a in authors:
                author_conditions.append(func.lower(Author.name).like(f'%{a}%'))
            query = query.join(Book.authors)
            if author_conditions:
                if len(author_conditions) == 1:
                    filters_to_apply.append(author_conditions[0])
                else:
                    filters_to_apply.append(or_(*author_conditions))

        if titles:
            title_conditions = []
            for t in titles:
                title_conditions.append(func.lower(Book.title).like(f'%{t}%'))
            if title_conditions:
                if len(title_conditions) == 1:
                    filters_to_apply.append(title_conditions[0])
                else:
                    filters_to_apply.append(or_(*title_conditions))

        if filters_to_apply:
            if len(filters_to_apply) == 1:
                query = query.filter(filters_to_apply[0])
            else:
                query = query.filter(and_(*filters_to_apply))
        else:
            print("API Debug: Filters_to_apply is empty after parsing, returning empty result as safeguard.")
            return jsonify({"count": 0, "results": []})

        total_books_count = query.distinct().count()
        print(f"API Debug: Total books count for current query: {total_books_count}")

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 25, type=int)
        page_size = min(page_size, 25)
        offset = (page - 1) * page_size
        if offset < 0:
            offset = 0

        books = query.order_by(Book.download_count.desc()).offset(offset).limit(page_size).distinct().all()

        response_data = BookListSchema().to_dict(total_books_count, books)

        return jsonify(response_data)

    except Exception as e:
        print(f"An error occurred during book retrieval: {e}")
        return jsonify({"detail": "An internal server error occurred. Please try again later."}), 500
    finally:
        db_session_generator.close()
