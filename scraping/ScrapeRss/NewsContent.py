from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import Any, List


class NewsContent:
    def __init__(
        self,
        news_url="",
        title="",
        author="",
        description="",
        published_at=None,
        seed_source=None,
    ):
        self.news_url = news_url
        self.title = title
        self.author = author
        self.description = description
        self.published_at = published_at
        self.seed_source = seed_source


class NewsIterator(Iterator):
    _position: int = None
    _reverse: bool = False

    def __init__(self, collection: NewsCollection, reverse: bool = False):
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()
        return value


class NewsCollection(Iterable):
    length = 0

    def __init__(self, news_collection: List[NewsContent] = []) -> None:
        self._collection = news_collection

    def __iter__(self) -> NewsIterator:
        return NewsIterator(self._collection)

    def get_reverse_iterator(self) -> NewsIterator:
        return NewsIterator(self._collection, True)

    def add_item(self, item: NewsContent):
        self._collection.append(item)
        self.length += 1
