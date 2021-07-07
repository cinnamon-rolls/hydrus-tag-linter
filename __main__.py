#!/usr/bin/env python3

import argparse
from typing import Iterable
import hydrus.utils
import hydrus
import json
import os


def str2bool(v):
    # We will use this function in argument parsing below
    # https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    if isinstance(v, bool):
        return v
    v = v.strip().lower()
    if v in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


NAME = "hydrus tag linter"
REQUIRED_PERMISSIONS = [
    hydrus.Permission.SearchFiles
]
ERROR_EXIT_CODE = 1
JSON_EXT = ".json"


argument_parser = argparse.ArgumentParser()

argument_parser.add_argument(
    "--api_key", "-k",
    help="The API Key used to connect to the API")

argument_parser.add_argument(
    "--api_url", "-a",
    default=hydrus.DEFAULT_API_URL,
    help="The URL the API is running on")

argument_parser.add_argument(
    "--rules", "-r",
    nargs='+', default=["default-rules"],
    help="The directory that the rule definitions are stored in")

argument_parser.add_argument(
    "--disable_archive",
    const=True, nargs='?', type=str2bool, default=False,
    help="Disables searching in the archive")

argument_parser.add_argument(
    "--disable_inbox",
    const=True, nargs='?', type=str2bool, default=False,
    help="Disables searching in the inbox")

argument_parser.add_argument(
    "--output_file_ids",
    const=True, nargs='?', type=str2bool, default=False,
    help="If enabled, the script will print offending file IDs rather than hashes"
)

argument_parser.add_argument(
    "--out", "-o",
    default="lint_results.html",
    help="File to write the lint results to"
)


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

    def execute(self, client, inbox, archive):
        "Implementations should return an iterable collection of integer file IDs"
        return None


class EmptySearch(Search):
    "Search implementation that returns no files"

    def __init__(self):
        super().__init__()

    def execute(self, client, inbox, archive):
        return []


class AllSearch(Search):
    def __init__(self):
        super().__init__()

    def execute(self, client, inbox, archive):
        return client.search_files(tags=[], inbox=inbox, archive=archive)


class OpSearch(Search):
    def __init__(self, op, of):
        super().__init__()
        self.op = get_search_op(op)
        self.of = of
        if(self.op is None):
            raise ValueError("Unknown op: " + str(op))
        if(not isinstance(of, Iterable)):
            raise ValueError("Expected Iterable, got " + str(of))

    def execute(self, client, inbox, archive):
        ret = set(self.of[0].execute(client, inbox, archive))

        for i in range(1, len(self.of)):
            other_search = self.of[i].execute(client, inbox, archive)

            # print('before 1: ' + str(ret))
            # print('before 2: ' + str(other_search))
            # print('op: ' + str(self.op))

            ret = self.op(ret, other_search)

            # print('after: ' + str(ret))

        return ret


class TagSearch(Search):
    "Search implementation that searches for a list of tags"

    def __init__(self, tags):
        super().__init__()
        self.tags = tags

    def execute(self, client, inbox, archive):
        return client.search_files(tags=self.tags, inbox=inbox, archive=archive)


def load_search(data):
    """
    Given recently parsed JSON, converts it into a JSON object
    """

    if data is None:
        return EmptySearch()

    if isinstance(data, Search):
        return data

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


class Rule:
    def __init__(self, data: dict):
        self.search = load_search(data.get('search'))
        self.name = data.get('name', 'Unnamed Rule')
        self.note = data.get('note', None)
        self.disabled = data.get('disabled', False)

    def is_enabled(self):
        return not self.disabled

    def runSearch(self, client, inbox, archive):
        return self.search.execute(client, inbox, archive)


def load_rule(rule_file_name):
    "Reads a rule and returns it, or returns None if the rule is otherwise disabled"
    json_len = len(JSON_EXT)

    print("Reading: " + rule_file_name)
    with open(rule_file_name) as rule_file:
        data = json.load(rule_file)

    return Rule(data)


def load_rules(rules_dir):
    ret = []
    for file in os.listdir(rules_dir):
        if file.endswith(JSON_EXT):
            rule = load_rule(rules_dir + '/' + file)
            if rule is not None and rule.is_enabled():
                ret.append(rule)
    return ret


def lint(client, rule: Rule, inbox: bool, archive: bool):
    """
    Searches for noncompliant files, returns a list of failed file IDs
    Or, returns an empty list if all files are OK
    """

    print("Checking rule '{}', inbox={}, archive={}".format(
        rule.name, inbox, archive))

    return rule.runSearch(client, inbox, archive)


# https://stackoverflow.com/a/8290508
def batch(iterable, n=1):
    if isinstance(iterable, set):
        iterable = list(iterable)

    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def ids2hashes(client: hydrus.BaseClient, file_ids):
    ret = []
    batch_size = 256

    batches = batch(file_ids, batch_size)

    for search_batch in batches:
        res = client.file_metadata(file_ids=search_batch)
        for val in res:
            ret.append(val.get('hash'))

    return ret


def get_key(args, permissions):
    "Gets the API key supplied in the args, or read from input if its not specified"
    if(args.api_key is not None):
        return args.api_key
    else:
        return hydrus.utils.cli_request_api_key(NAME, permissions)


def main(args):
    archive_enabled = not args.disable_archive
    inbox_enabled = not args.disable_inbox

    permissions = REQUIRED_PERMISSIONS

    # Get the key
    key = str(get_key(args, permissions))
    if(not key):
        print("The API key could not be obtained.")
        return ERROR_EXIT_CODE

    # Try to log in
    client = hydrus.Client(key, args.api_url)
    if not hydrus.utils.verify_permissions(client, permissions):
        print(
            "The API key does not grant all required permissions:",
            permissions)
        return ERROR_EXIT_CODE

    rules = []
    # Load rules for linting
    for rule_dir in args.rules:
        rules_loaded = load_rules(rule_dir)
        for rule in rules_loaded:
            rules.append(rule)

    print("got " + str(len(rules)) + " rules")

    # Generate results :)
    with open(args.out, "w") as out:

        out.write("<html>")

        out.write("<head>")

        with(open('assets/head.html')) as head_file:
            out.writelines(head_file.readlines())

        out.write("<style>")
        with(open('assets/style.css')) as style_file:
            out.writelines(style_file.readlines())
        out.write("</style>")

        out.write("</head>")

        out.write("<body>")

        out.write("<h1>Lint Results</h1>\n\n")
        out.write("\n<h2>Issues Detected</h2>\n\n")

        totalIssues = 0

        rules_ok = []

        # Provides a unique ID to each block of hashes
        hash_block_no = 0

        for rule in rules:

            fails = lint(client, rule, inbox_enabled, archive_enabled)

            totalIssues += len(fails)

            rule_name = rule.name
            rule_note = rule.note

            if(len(fails) > 0):

                out.write("\n<h3>" + rule_name + "</h3>\n\n")
                if(rule_note is not None):
                    out.write("<p>" + rule.note + "</p>\n")

                if(not args.output_file_ids):
                    fails = ids2hashes(client, fails)

                out.write("\n<div class='hashes' id='hb_" + str(hash_block_no)
                          + "'><code id='hb_" + str(hash_block_no) + "_code'>\n")

                for fail in fails:
                    out.write(fail)
                    out.write("<br>\n")

                out.write("</code></div>\n")

                hash_block_no += 1

            else:
                rules_ok.append(rule_name)

        if totalIssues == 0:
            out.write("<p>No issues :)</p>\n")

        if len(rules_ok) > 0:
            out.write("\n<h2>Rules with no problems</h2>\n\n")
            out.write("<ul>")
            for rule_name in rules_ok:
                out.write("<li>" + rule_name + "</li>\n")
            out.write("</ul>")

        out.write("\n<h2>Summary</h2>\n\n")
        out.write("<ul>")
        out.write("<li>Total issues: <code>" +
                  str(totalIssues) + "</code></li>\n")
        out.write("<li>Rules checked: <code>" +
                  str(len(rules)) + "</code></li>\n")
        out.write("<li>Rules without issues: <code>" +
                  str(len(rules_ok)) + "</code></li>\n")
        out.write("</ul>")

        out.write("</body>")

        out.write("</html>")

        print("Done")


if __name__ == "__main__":
    args = argument_parser.parse_args()
    try:
        argument_parser.exit(main(args))
    except KeyboardInterrupt:
        pass
