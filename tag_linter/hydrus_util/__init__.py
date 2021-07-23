import typing as T
from tag_linter.server import instance as server


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
    client = server.get_client()

    if not isinstance(file_ids, list):
        return [client.file_metadata(file_ids=[file_ids])[0].get('hash')]

    ret = []
    batch_size = 256

    batches = batch(file_ids, batch_size)

    for search_batch in batches:
        res = client.file_metadata(file_ids=search_batch)
        for val in res:
            ret.append(val.get('hash'))

    return ret


# The hydrus api library that I'm using doesn't implement everything that I wish it did :(

_DELETE_FILES_ROUTE = "/add_files/delete_files"
_UNDELETE_FILES_ROUTE = "/add_files/undelete_files"
_ARCHIVE_FILES_ROUTE = "/add_files/archive_files"
_UNARCHIVE_FILES_ROUTE = "/add_files/unarchive_files"

_GET_SERVICES_ROUTE = "/get_services"


def delete_files(file_ids):
    if(len(file_ids) < 1):
        return
    server.get_client()._api_request("POST", _DELETE_FILES_ROUTE, json={
        'hashes': ids2hashes(file_ids)
    })


def undelete_files(file_ids):
    if(len(file_ids) < 1):
        return
    server.get_client()._api_request("POST", _UNDELETE_FILES_ROUTE, json={
        'hashes': ids2hashes(file_ids)
    })


def archive_files(file_ids):
    if(len(file_ids) < 1):
        return
    server.get_client()._api_request("POST", _ARCHIVE_FILES_ROUTE, json={
        'hashes': ids2hashes(file_ids)
    })


def unarchive_files(file_ids):
    if(len(file_ids) < 1):
        return
    print(ids2hashes(file_ids))
    server.get_client()._api_request("POST", _UNARCHIVE_FILES_ROUTE, json={
        'hashes': ids2hashes(file_ids)
    })


def get_services():
    return server.get_client()._api_request("GET", _GET_SERVICES_ROUTE).json()
