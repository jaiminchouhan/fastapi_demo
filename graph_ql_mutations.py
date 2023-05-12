import typing

import strawberry


@strawberry.type
class Book:
    title: str
    author: str


@strawberry.type
class Query:
    books: typing.List[Book]


def get_books():
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        print(f"Adding {title} by {author}")

        return Book(title=title, author=author)


schema = strawberry.Schema(query=Query, mutation=Mutation)

# mutation to use in graphql editor
# mutation {
#   addBook(title: "The Little Prince", author: "Antoine de Saint-Exupéry") {
#     title
#   }
# }
