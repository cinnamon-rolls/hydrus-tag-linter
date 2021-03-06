import hydrus
import typing as T
from tag_linter.server import instance as server

TAG_ACTION_ADD_LOCAL = "0"
TAG_ACTION_DELETE_LOCAL = "1"

TAG_STATUS_STATUS_CURRENT = "0"
TAG_STATUS_STATUS_PENDING = "1"
TAG_STATUS_STATUS_DELETED = "2"
TAG_STATUS_STATUS_PETITIONED = "3"

NAME = "hydrus tag linter"
PERMISSIONS = [
    hydrus.Permission.SearchFiles,
    hydrus.Permission.AddTags,
    hydrus.Permission.ImportFiles
]

client = None


def create_hydrus_client(key, api_url) -> hydrus.BaseClient:
    global client
    import hydrus.utils

    if key is None:
        key = hydrus.utils.cli_request_api_key(
            NAME, PERMISSIONS)

    if key is None:
        raise ValueError("The API key could not be obtained.")

    # Try to log in
    client = hydrus.Client(key, api_url)
    if not hydrus.utils.verify_permissions(client, PERMISSIONS):
        raise ValueError(
            "The API key does not grant all required permissions:",
            PERMISSIONS)

    return client


def get_client() -> hydrus.BaseClient:
    if client is None:
        raise RuntimeError("Client is not instantiated yet")
    return client


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

    client = get_client()

    if not isinstance(file_ids, list):
        return [client.file_metadata(file_ids=[file_ids])[0].get("hash")]

    ret = []
    batch_size = 256

    batches = batch(file_ids, batch_size)

    for search_batch in batches:
        res = client.file_metadata(file_ids=search_batch)
        for val in res:
            ret.append(val.get("hash"))

    return ret


def search_by_tags(tags, inbox=True, archive=True, tag_service=None):
    # We currently just discard the tag_service because its not supported yet :(

    if inbox and archive:
        # neither are disabled
        return get_client().search_files(tags)
    elif not inbox and not archive:
        # both were disabled :(
        return []
    else:
        # one or the other was disabled
        return get_client().search_files(tags, inbox, archive)


def get_file_metadata(file_id: T.Union[T.List[int], int]) -> hydrus.FileMetadataResultType:
    if file_id is None:
        raise ValueError('file_id is None')

    if isinstance(file_id, str):
        file_id = int(file_id)

    if isinstance(file_id, int):
        return get_client().file_metadata(file_ids=[file_id])[0]

    if isinstance(file_id, list):
        return get_client().file_metadata(file_ids=file_id)

    raise ValueError('unexpected input: ' + str(file_id))


def change_tags(hashes=None, file_ids=None, add_tags=[], rm_tags=[], tag_service=None):
    if (hashes is None and file_ids is None) or (hashes is not None and file_ids is not None):
        raise ValueError("expected either hashes or file_ids, but not both")

    if tag_service is None:
        raise ValueError("tag service not specified")

    if hashes is None:
        hashes = ids2hashes(file_ids)

    if not isinstance(hashes, list):
        raise ValueError("Expected hashes as a list")
    if not isinstance(add_tags, list):
        raise ValueError("Expected add_tags as a list")
    if not isinstance(rm_tags, list):
        raise ValueError("Expected rm_tags as a list")
    if not isinstance(tag_service, str):
        raise ValueError(
            "Expected tag_service as a string, but got " + str(type(tag_service)))

    if len(hashes) < 1 or (len(add_tags) < 1 and len(rm_tags) < 1):
        # no-op, don't forward to hydrus
        return

    # TODO: check the type of the service and see if we are adding to a
    # repository, or check if the service accepts changes to begin with

    tag_action_add = TAG_ACTION_ADD_LOCAL
    tag_action_remove = TAG_ACTION_DELETE_LOCAL

    get_client().add_tags(
        hashes=hashes,
        service_to_action_to_tags={
            tag_service: {
                tag_action_add: add_tags,
                tag_action_remove: rm_tags,
            }
        },
    )


def get_file_tags(file_id, serviceName, status=TAG_STATUS_STATUS_CURRENT, display=True):
    metadata = get_file_metadata(file_id)
    if metadata is None:
        return []

    lookup = "service_names_to_statuses_to_display_tags" if display else "service_names_to_statuses_to_tags"

    serviceNamesToStatusesToTags = metadata.get(lookup)
    if serviceNamesToStatusesToTags is None:
        return []

    statusesToTags = serviceNamesToStatusesToTags.get(serviceName)
    if statusesToTags is None:
        return []

    tags = statusesToTags.get(status)
    if tags is None:
        return []

    return tags


def get_tags_in_namespace(namespace, tag_service="all known tags", inbox=True, archive=True):
    if namespace is None:
        raise ValueError("namespace is not defined")
    if tag_service is None:
        raise ValueError("tag_service is not defined")

    files = search_by_tags(
        [namespace + ":*"], inbox=inbox, archive=archive, tag_service=tag_service)
    ret = []
    tag_prefix = namespace + ":"
    for file in files:
        tags = get_file_tags(file, serviceName=tag_service)
        for tag in tags:
            if tag.startswith(tag_prefix):
                ret.append(tag)

    return ret


def transpose_namespace(
        from_namespace,
        to_namespace,
        prefix = None,
        suffix = None,
        inbox = True,
        archive = True,
        tag_service = "my tags"):

    changes = {}

    if suffix is None:
        suffix = ""
    if prefix is None:
        prefix = ""
    if to_namespace is not None and to_namespace != "":
        prefix = to_namespace + ":" + prefix

    tags = get_tags_in_namespace(
        from_namespace, tag_service, inbox, archive)

    for tag in tags:
        substr_start = len(from_namespace) + 1
        new_tag = prefix + tag[substr_start:] + suffix
        changes[tag] = new_tag

    return changes


def search_and_destroy(tags, inbox, archive, read_tag_service, write_tag_service):
    removals = 0

    for tag in tags:
        if tag.endswith(":*"):
            namespace = tag[:-2]
            removals += search_and_destroy_namespace(
                namespace, inbox, archive, read_tag_service, write_tag_service)
        else:
            removals += search_and_destroy_tag(
                tag, inbox, archive, read_tag_service, write_tag_service)

    return removals


def search_and_destroy_namespace(namespace, inbox, archive, read_tag_service, write_tag_service):
    tags = get_tags_in_namespace(namespace, read_tag_service, inbox, archive)
    return search_and_destroy(
        tags, inbox, archive, read_tag_service, write_tag_service)


def search_and_destroy_tag(tag, inbox, archive, read_tag_service, write_tag_service):
    if read_tag_service is None:
        raise ValueError("read tag service not defined")
    if write_tag_service is None:
        raise ValueError("write tag service is not defined")

    rm_tags = [tag]
    files = search_by_tags(rm_tags, inbox, archive, read_tag_service)

    removals = len(files)

    change_tags(
        file_ids=files,
        rm_tags=rm_tags,
        tag_service=write_tag_service)

    return removals


def clean_tag(tag):
    client = get_client()

    if not isinstance(tag, str):
        raise ValueError("Expected a string, but got " + str(type(tag)))

    if isinstance(tag, list):
        client.clean_tags(tag)
    else:
        return client.clean_tags([tag])[0]


# The hydrus api library that I'm using doesn't implement everything that I wish
# it did, so I am implementing the missing features myself

_DELETE_FILES_ROUTE = "/add_files/delete_files"
_UNDELETE_FILES_ROUTE = "/add_files/undelete_files"
_ARCHIVE_FILES_ROUTE = "/add_files/archive_files"
_UNARCHIVE_FILES_ROUTE = "/add_files/unarchive_files"

_GET_SERVICES_ROUTE = "/get_services"


def delete_files(file_ids):
    if len(file_ids) < 1:
        return
    get_client()._api_request(
        "POST",
        _DELETE_FILES_ROUTE,
        json={"hashes": ids2hashes(file_ids)})


def undelete_files(file_ids):
    if len(file_ids) < 1:
        return
    get_client()._api_request(
        "POST",
        _UNDELETE_FILES_ROUTE,
        json={"hashes": ids2hashes(file_ids)})


def archive_files(file_ids):
    if len(file_ids) < 1:
        return
    get_client()._api_request(
        "POST",
        _ARCHIVE_FILES_ROUTE,
        json={"hashes": ids2hashes(file_ids)})


def unarchive_files(file_ids):
    if len(file_ids) < 1:
        return
    get_client()._api_request(
        "POST",
        _UNARCHIVE_FILES_ROUTE,
        json={"hashes": ids2hashes(file_ids)})


def get_services():
    return get_client()._api_request("GET", _GET_SERVICES_ROUTE).json()
