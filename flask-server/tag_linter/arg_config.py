# This file is responsible for adding commands to the argparser

import hydrus
import argparse


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


def add_args(argp: argparse.ArgumentParser):
    argp.add_argument(
        "--api_key", "-k",
        help="The API Key used to connect to the API")

    argp.add_argument(
        "--api_url", "-a",
        default=hydrus.DEFAULT_API_URL,
        help="The URL the API is running on")

    argp.add_argument(
        "--rules", "-r",
        nargs='+', default=["default-rules"],
        help="The directory that the rule definitions are stored in")

    argp.add_argument(
        "--disable_archive",
        const=True, nargs='?', type=str2bool, default=False,
        help="Disables searching in the archive")

    argp.add_argument(
        "--disable_inbox",
        const=True, nargs='?', type=str2bool, default=False,
        help="Disables searching in the inbox")

    argp.add_argument(
        "--out", "-o",
        default="lint_results.html",
        help="File to write the lint results to"
    )

    argp.add_argument(
        "--debug", "-d",
        const=True, nargs='?', type=str2bool, default=True,
        help="Enables debug mode, which will give more info if things fail"
    )

    argp.add_argument(
        "--tag_service",
        default="my tags",
        help="The name of the tag service to operate on"
    )

    argp.add_argument(
        "--host", "-H",
        default="localhost",
        help="Defines the host to run the HTTP server on"
    )

    argp.add_argument(
        "--port", "-P",
        default=45868,
        help="Defines the port to run the HTTP server on"
    )

    argp.add_argument(
        "--ssl_adhoc",
        const=True, nargs='?', type=str2bool, default=False,
        help="Automatically creates a self-signed HTTPS certificate, good for at-home setups"
    )

    argp.add_argument(
        "--password",
        default=None,
        help="Requires people to enter a password before they get access to anything"
    )


def get_argp() -> argparse.ArgumentParser:
    argp = argparse.ArgumentParser()
    add_args(argp)
    return argp


def parse_args():
    argp = get_argp()
    return argp.parse_args()
