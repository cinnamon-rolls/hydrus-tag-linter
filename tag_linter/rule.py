from tag_linter.searches import load_search
import hydrus


# https://stackoverflow.com/a/8290508
def batch(iterable, batch_size=256):
    """
    Breaks a
    """

    if isinstance(iterable, set):
        iterable = list(iterable)

    l = len(iterable)
    for ndx in range(0, l, batch_size):
        yield iterable[ndx:min(ndx + batch_size, l)]


def ids2hashes(client: hydrus.BaseClient, file_ids):
    ret = []
    batch_size = 256

    batches = batch(file_ids, batch_size)

    for search_batch in batches:
        res = client.file_metadata(file_ids=search_batch)
        for val in res:
            ret.append(val.get('hash'))

    return ret


class Rule:
    def __init__(self, data: dict):
        self.search = load_search(data.get('search'))
        self.name = data.get('name', 'Unnamed Rule')
        self.note = data.get('note', None)
        self.disabled = data.get('disabled', False)
        self.cached_files = None

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'note': self.note
        }

    def is_enabled(self):
        return not self.disabled

    def get_files(self, client, inbox, archive, refresh: bool = False):
        if(not self.is_enabled()):
            return []

        if refresh == True:
            self.cached_files = None

        if self.cached_files is not None:
            return self.cached_files

        print("get files: " + self.name)

        ret = self.search.execute(client, inbox, archive)
        self.cached_files = ret
        return ret

    def get_hashes(self, client, inbox, archive, refresh=False):
        return ids2hashes(client, self.get_files(client=client, inbox=inbox, archive=archive, refresh=refresh))

    def get_name(self):
        return self.name if self.name is not None else "Unnamed Rule"

    def get_note(self):
        return self.note

    def has_note(self):
        return self.note is None

    def __repr__(self):
        return self.name
