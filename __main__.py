#!/usr/bin/env python3

from tag_linter.server import Server
from flask import Flask, render_template, jsonify, abort, request, make_response
import sys
import argparse
import json
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


argp = argparse.ArgumentParser()

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
    "--host", "-H",
    default="localhost",
    help="Defines the host to run the HTTP server on"
)

argp.add_argument(
    "--port", "-P",
    default=45868,
    help="Defines the port to run the HTTP server on"
)

app = Flask(__name__)

server = None


def get_rule(rule_name):
    rule = server.get_rule(rule_name)
    if rule is None:
        abort(404, "rule not found")
    return rule


def api_abort(status=400, message=None, err=None):
    if message is None and err is None:
        return make_response(status)
    response = make_response(message, status)
    response.mimetype = "text/plain"
    return response


@app.route('/', methods=['GET'])
def app_get_index():
    server.refresh_all()
    return render_template('index.html')


@app.route('/rules/<rule_name>', methods=['GET'])
def app_get_rule(rule_name):
    rule = get_rule(rule_name)
    # this will refresh the rule's cached list of files
    server.get_rule_files(rule, refresh=True)
    return render_template('rule.html', rule=rule)


@app.route('/api/rules/get_rules', methods=['GET'])
def api_get_rules():
    ret = list(map(lambda x: x.as_dict(), server.get_rules()))
    return jsonify(ret)


@app.route('/api/rules/get_rule/', methods=['GET'])
def api_get_rule():
    rule = get_rule(request.args.get('name'))
    return jsonify(rule.as_dict())


@app.route('/api/rules/get_rule_names', methods=['GET'])
def api_get_rule_names():
    return jsonify(server.get_rule_names())


@app.route('/api/rules/get_files', methods=['GET'])
def api_get_rule_files():
    rule = get_rule(request.args.get('name'))
    refresh = request.args.get('refresh', False)
    return jsonify(server.get_rule_files(rule=rule, refresh=refresh))


@app.route('/api/rules/get_hashes_as_text', methods=['GET'])
def api_get_rule_hashes_as_text():
    rule = get_rule(request.args.get('name'))
    refresh = request.args.get('refresh', False)
    text = "\n".join(server.get_rule_hashes(rule=rule, refresh=refresh))
    response = make_response(text, 200)
    response.mimetype = "text/plain"
    return response


@app.route('/api/rules/get_hashes', methods=['GET'])
def api_get_rule_hashes():
    rule = get_rule(request.args.get('name'))
    refresh = request.args.get('refresh', False)
    return jsonify(server.get_rule_hashes(rule=rule, refresh=refresh))


@app.route('/api/server/get_summary', methods=['GET'])
def api_server_get_summary():
    return jsonify(server.get_summary())


@app.route('/api/hydrus/add_tags/clean_tags', methods=['GET'])
def api_hydrus_clean_tags():
    tags_input = request.args.get('tags')
    tags = json.loads(tags_input)
    return jsonify(server.client.clean_tags(tags))


@app.before_first_request
def before_first_request():
    "set up globals here"
    global server
    server = Server(args)


@app.context_processor
def context_process():
    return {
        'len': len,
        'server': server
    }


def main(args) -> int:
    global app

    app.run(host=args.host,
            port=args.port,
            debug=args.debug)

    return 0


if __name__ == "__main__":
    global args

    args = argp.parse_args()
    try:
        sys.exit(main(args))
    except KeyboardInterrupt:
        pass
