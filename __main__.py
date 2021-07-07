#!/usr/bin/env python3

from rules import Rule, load_rules
import argparse
import hydrus.utils
import hydrus


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

            if args.output_file_ids:
                fails = rule.get_files(client, inbox_enabled, archive_enabled)
            else:
                fails = rule.get_hashes(client, inbox_enabled, archive_enabled)


            totalIssues += len(fails)

            rule_name = rule.name
            rule_note = rule.note

            if(len(fails) > 0):

                out.write("\n<h3>" + rule_name + "</h3>\n\n")
                if(rule_note is not None):
                    out.write("<p>" + rule.note + "</p>\n")

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
