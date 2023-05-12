import typing


import strawberry

from typing import Optional


def get_author_for_book(root) -> "Author":
    return Author(name="Michael Crichton")


@strawberry.type
class Book:
    title: str
    year: Optional[int]
    author: "Author" = strawberry.field(resolver=get_author_for_book)


def get_books_for_author(root):
    return [Book(title="Jurassic Park")]


@strawberry.type
class Author:
    name: str
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)


def get_authors(root) -> typing.List[Author]:
    return [Author(name="Michael Crichton")]


@strawberry.type
class Query:
    authors: typing.List[Author] = strawberry.field(resolver=get_authors)
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)


schema = strawberry.Schema(query=Query)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str) -> Book:
        return Book(title=title)


schema = strawberry.Schema(query=Query, mutation=Mutation)
