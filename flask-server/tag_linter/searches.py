from typing import Iterable
from tag_linter.server import Server

import hydrus


def search_op_union(x: set, y):
    return x.union(x, set(y))


def search_op_intersect(x: set, y):
    return x.intersection(y)


def get_search_op(op):
    op = op.strip().lower()
    if op == 'and' or op == 'intersect':
        return search_op_intersect
    elif op == 'or' or op == 'union':
        return search_op_union
    return None


class Search:
    "parent class for all search implementations"

    def __init__(self):
        pass

    def execute(self, server: Server):
        "Implementations should return an iterable collection of integer file IDs"
        raise NotImplementedError()

    def as_jsonifiable(self):
        """
        Creates some object that can be turned into a JSON object which
        represents this Search object
        """
        raise NotImplementedError()


class EmptySearch(Search):
    "Search implementation that returns no files"

    def __init__(self):
        super().__init__()

    def execute(self, server):
        return []

    def as_jsonifiable(self):
        return []


class AllSearch(Search):
    def __init__(self):
        super().__init__()

    def execute(self, server):
        return server.search_by_tags(tags=[])

    def as_jsonifiable(self):
        return True


class OpSearch(Search):
    def __init__(self, op_name, of):
        super().__init__()
        self.op_name = op_name
        self.op = get_search_op(op_name)
        self.of = of
        if(self.op is None):
            raise ValueError("Unknown op: " + str(op_name))
        if(not isinstance(of, Iterable) or of is None):
            raise ValueError("Expected Iterable, got " + str(of))

    def execute(self, server):
        initial_values = self.of[0].execute(server)
        if initial_values is None:
            return []

        ret = set(initial_values)

        for i in range(1, len(self.of)):
            other_search = self.of[i].execute(server)

            # print('before 1: ' + str(ret))
            # print('before 2: ' + str(other_search))
            # print('op: ' + str(self.op))

            ret = self.op(ret, other_search)

            # print('after: ' + str(ret))

        return list(ret)

    def as_jsonifiable(self):
        return {
            'op': self.op_name,
            'of': [i.as_jsonifiable() for i in self.of]
        }


class TagSearch(Search):
    "Search implementation that searches for a list of tags"

    def __init__(self, tags):
        super().__init__()
        self.tags = tags

    def execute(self, server):
        search = server.search_by_tags(self.tags)
        # print(str(search))
        return search

    def as_jsonifiable(self):
        if len(self.tags) == 1:
            return self.tags[0]
        return self.tags


def load_search(data):
    """
    Given recently parsed JSON, converts it into a Search object
    """

    if data is None:
        return EmptySearch()

    if isinstance(data, Search):
        return data

    if isinstance(data, bool):
        if data:
            return AllSearch()
        else:
            return EmptySearch()

    if isinstance(data, str):
        return TagSearch([data])

    if isinstance(data, list):
        return TagSearch(data)

    if isinstance(data, dict):
        op = data.get('op')
        of = data.get('of')

        if not isinstance(of, list):
            of = [of]

        of = [load_search(i) for i in of]

        return OpSearch(op, of)

    raise ValueError("Not sure how to convert to a search: " + str(data))
