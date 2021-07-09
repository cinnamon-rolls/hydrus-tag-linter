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


TAG_ACTION_ADD_LOCAL = "0"
TAG_ACTION_DELETE_LOCAL = "1"

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

app = Flask(__name__)

server = None


def get_rule(rule_name):
    if rule_name is None:
        abort(400, "rule name not specified")
    rule = server.get_rule(rule_name)
    if rule is None:
        abort(400, "rule not found: '" + rule_name + "'")
    return rule


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


@app.route('/api/rules/apply_linter_tag', methods=['GET'])
def api_rules_apply_linter_tag():
    preview = request.args.get('preview', 'true') == 'true'
    rule = get_rule(request.args.get('name'))
    tag_raw = request.args.get('tag', rule.get_linter_rule_tag())
    tag_service = server.tag_service

    enable_add = request.args.get('add', 'true') == 'true'
    enable_remove = request.args.get('remove', 'true') == 'true'

    tag = server.client.clean_tags([tag_raw])[0]

    files_tagged_now = server.search_by_tags(tags=[tag])
    files_that_need_tag = server.get_rule_files(rule, refresh=True)

    files_to_untag = [
        i for i in files_tagged_now if i not in files_that_need_tag]

    files_to_tag = [
        i for i in files_that_need_tag if i not in files_tagged_now]

    if not preview:
        # Add
        if(len(files_to_tag) > 0):
            print('add...')
            server.get_client().add_tags(
                hashes=server.ids2hashes(files_to_tag),
                service_to_action_to_tags={
                    server.tag_service: {
                        TAG_ACTION_ADD_LOCAL: [tag]
                    }
                }
            )

        # Remove
        if(len(files_to_untag) > 0):
            print('remove...')
            server.get_client().add_tags(
                hashes=server.ids2hashes(files_to_untag),
                service_to_action_to_tags={
                    server.tag_service: {
                        TAG_ACTION_DELETE_LOCAL: [tag]
                    }
                }
            )

    return jsonify({
        'preview': preview,
        'tag': tag,
        'added': len(files_to_tag),
        'removed': len(files_to_untag),
        'tag_service': tag_service
    })


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
