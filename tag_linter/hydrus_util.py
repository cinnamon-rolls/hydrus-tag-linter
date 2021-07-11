import typing as T


def batch(iterable: T.Iterable, batch_size: int = 256) -> list:
    """
    Breaks a large list into batches of a predetermined size
    https://stackoverflow.com/a/8290508
    """

    if isinstance(iterable, set):
        iterable = list(iterable)

    l = len(iterable)
    for ndx in range(0, l, batch_size):
        yield iterable[ndx:min(ndx + batch_size, l)]


def ids2hashes(file_ids):
    """
    Converts an arbitrary amount of file IDs into hashes as strings
    """
    from tag_linter.server import instance as server
    ret = []
    batch_size = 256

    batches = batch(file_ids, batch_size)

    for search_batch in batches:
        res = server.get_client().file_metadata(file_ids=search_batch)
        for val in res:
            ret.append(val.get('hash'))

    return ret
