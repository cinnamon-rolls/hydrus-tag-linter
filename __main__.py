#!/usr/bin/env python3

from flask import Flask, render_template, jsonify, abort, request, make_response
from server import Server
import sys
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
    rule = server.get_lint_rule(rule_name)
    if rule is None:
        abort(404, "rule not found")
    return rule


def get_summary():
    return {
        'total_rules': len(server.get_lint_rules()),
        'total_issues': server.count_issues(),
        'rules_without_issues': server.count_rules_without_issues()
    }


@app.route('/', methods=['GET'])
def app_get_index():
    server.refresh_all()
    return render_template(
        'index.html',
        len=len,
        server=server,
        summary=get_summary(),
        rules=server.get_lint_rules())


@app.route('/api/rules/get_rules', methods=['GET'])
def api_get_rules():
    ret = list(map(lambda x: x.as_dict(), server.get_lint_rules()))
    return jsonify(ret)


@app.route('/api/rules/get_rule/', methods=['GET'])
def api_get_rule():
    rule = get_rule(request.args.get('name'))
    return jsonify(rule.as_dict())


@app.route('/api/rules/get_rule_names', methods=['GET'])
def api_get_rule_names():
    return jsonify(server.get_lint_rule_names())


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


def main(args):
    global server, app

    server = Server(args)

    app.run(host=args.host,
            port=args.port,
            debug=args.debug)

    #     out.write("<h1>Lint Results</h1>\n")
    #     out.write("<h2>Issues Detected</h2>\n")

    #     totalIssues = 0

    #     rules_ok = []

    #     # Provides a unique ID to each block of hashes
    #     hash_block_no = 0

    #     for rule in rules:

    #         if(len(fails) > 0):

    #             out.write("<h3>" + rule.get_name() + "</h3>\n")
    #             if(rule.has_note()):
    #                 out.write("<p>" + rule.get_note() + "</p>\n")

    #             out.write("<div class='hashes' id='hb_" + str(hash_block_no)
    #                       + "'><code id='hb_" + str(hash_block_no) + "_code'>\n")

    #             for fail in fails:
    #                 out.write(fail)
    #                 out.write("<br>\n")

    #             out.write("</code></div>\n")

    #             hash_block_no += 1

    #         else:
    #             rules_ok.append(rule.get_name())

    #     if totalIssues == 0:
    #         out.write("<p>No issues :)</p>\n")

    #     if len(rules_ok) > 0:
    #         out.write("<h2>Rules with no problems</h2>\n")
    #         out.write("<ul>")
    #         for rule_name in rules_ok:
    #             out.write("<li>" + rule_name + "</li>\n")
    #         out.write("</ul>")


if __name__ == "__main__":
    args = argp.parse_args()
    try:
        sys.exit(main(args))
    except KeyboardInterrupt:
        pass
