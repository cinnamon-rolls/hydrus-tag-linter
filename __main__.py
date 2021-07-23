#!/usr/bin/env python3

import sys
import traceback
import os


def main(args) -> int:
    print("main")

    db_path = args.database

    if not isinstance(db_path, str):
        raise ValueError("database parameter is not a string")

    if not os.path.isabs(db_path):
        db_path = os.path.abspath(db_path)

    print("db_path: " + db_path)

    run_options = {"host": args.host, "port": args.port, "debug": args.debug}

    app_options = {
        "aggressive_static_caching": not args.debug,
        "db_path": db_path,
    }

    if args.ssl_adhoc == True:
        run_options["ssl_context"] = "adhoc"
        print("NOTE: Running on an an adhoc certificate")

    from tag_linter.flask_app import create_app

    app = create_app(args, app_options)

    print("running app...")
    app.run(**run_options)

    return 0


if __name__ == "__main__":
    import tag_linter.arg_config as arg_config

    args = arg_config.parse_args()

    try:
        sys.exit(main(args))
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print()
        print(e)
        print()
        traceback.print_exc()
        sys.exit(1)
