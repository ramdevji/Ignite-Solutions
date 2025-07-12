from flask_swagger_ui import get_swaggerui_blueprint
import yaml

SWAGGER_SPEC_YAML = """
openapi: 3.0.0
info:
  title: Project Gutenberg Books API
  description: API for querying and retrieving books from Project Gutenberg, with filtering, pagination, and sorting capabilities.
  version: 1.0.0
servers:
  - url: http://localhost:5000/api # API base path for Swagger UI to target
    description: Local API server

tags:
  - name: Books
    description: Operations related to books

paths:
  /books: # This path is relative to the server URL (http://localhost:5000/api)
    get:
      summary: Retrieve a list of books with optional filters, pagination, and sorting.
      tags:
        - Books
      parameters:
        - in: query
          name: gutenberg_id
          schema:
            type: string
          description: Comma-separated list of Project Gutenberg book IDs.
          example: 1342,11
        - in: query
          name: language
          schema:
            type: string
          description: Comma-separated list of language codes (e.g., 'en', 'fr').
          example: en,fr
        - in: query
          name: mime_type
          schema:
            type: string
          description: Comma-separated list of mime types (e.g., 'text/plain', 'application/pdf').
          example: text/plain,application/epub+zip
        - in: query
          name: topic
          schema:
            type: string
          description: Comma-separated list of topics (subjects or bookshelves). Case-insensitive, partial matches.
          example: fiction,history
        - in: query
          name: author
          schema:
            type: string
          description: Comma-separated list of author names. Case-insensitive, partial matches.
          example: mark twain,jane austen
        - in: query
          name: title
          schema:
            type: string
          description: Comma-separated list of book titles. Case-insensitive, partial matches.
          example: alice,pride and prejudice
        - in: query
          name: page
          schema:
            type: integer
            minimum: 1
            default: 1
          description: Page number for pagination. Each page returns up to 25 books.
        - in: query
          name: page_size
          schema:
            type: integer
            minimum: 1
            maximum: 25
            default: 25
          description: Number of books per page. Maximum is 25.
      responses:
        '200':
          description: A list of books matching the criteria.
          content:
            application/json:
              schema:
                type: object
                properties:
                  count:
                    type: integer
                    description: Total number of books matching the criteria.
                    example: 1234
                  results:
                    type: array
                    items:
                      $ref: '#/components/schemas/Book'
        '400':
          description: Invalid query parameters.
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
                    example: Invalid parameter value.

components:
  schemas:
    Author:
      type: object
      properties:
        name:
          type: string
          description: Name of the author.
          example: "Carroll, Lewis"
        birth_year:
          type: integer
          nullable: true
          description: Year of birth.
          example: 1832
        death_year:
          type: integer
          nullable: true
          description: Year of death.
          example: 1898
    Format:
      type: object
      properties:
        mime_type:
          type: string
          description: MIME type of the book format (e.g., text/plain, application/pdf).
          example: "text/html; charset=utf-8"
        url:
          type: string
          format: uri
          description: URL to download the book in this format.
          example: "http://www.gutenberg.org/files/11/11-h/11-h.htm"
    Book:
      type: object
      properties:
        id:
          type: integer
          description: Project Gutenberg ID of the book.
          example: 11
        title:
          type: string
          description: Title of the book.
          example: "Alice's Adventures in Wonderland"
        authors:
          type: array
          items:
            $ref: '#/components/schemas/Author'
          description: List of authors for the book.
        languages:
          type: array
          items:
            type: string
          description: List of language codes for the book (e.g., 'en').
          example: ["en"]
        subjects:
          type: array
          items:
            type: string
          description: List of subjects associated with the book.
          example: ["Children's stories", "Fantasy literature"]
        bookshelves:
          type: array
          items:
            type: string
          description: List of bookshelves the book belongs to.
          example: ["Children's Literature"]
        download_count:
          type: integer
          description: Number of times the book has been downloaded.
          example: 12345
        formats:
          type: array
          items:
            $ref: '#/components/schemas/Format'
          description: List of available download formats and their URLs.
"""

SWAGGER_JSON_DATA = yaml.safe_load(SWAGGER_SPEC_YAML)

SWAGGER_URL = '/swagger'
API_URL_FOR_SWAGGER_UI = '/openapi.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL_FOR_SWAGGER_UI,
    config={
        'app_name': "Project Gutenberg Books API"
    }
)

