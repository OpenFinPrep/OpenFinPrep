import argparse
import operator
import sys

from openfinprep.app import create_app
from openfinprep.default_values import DEFAULT_ARGUMENTS as DEFARGS

def get_args():
    parser = argparse.ArgumentParser(
        description="OpenFinPrep - Free and open source financial data hub and aggregation API"
    )
    parser.add_argument(
        "--host", type=str, help="Hostname (%(default)s)", default=DEFARGS['HOST']
    )
    parser.add_argument("--port", type=int, help="Port (%(default)s)", default=DEFARGS['PORT'])
    parser.add_argument(
        "--debug", default=DEFARGS['DEBUG'], action="store_true", help="Enable debug environment"
    )
    parser.add_argument(
        "--use-local-storage", default=DEFARGS['USE_LOCAL_STORAGE'], action="store_true", help="Enable local storage use"
    )
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    app = create_app(args)

    if '--wsgi' in sys.argv:
        return app
    else:
        if args.debug and args.host == "*":
            # '::' will listen on both ipv6 and ipv4
            args.host = "::"

        if args.debug:
            app.run(host=args.host, port=args.port, debug=True)
        else:
            from waitress import serve
            print(f"Running on http://{args.host}:{args.port}")

            serve(
                app,
                host=args.host,
                port=args.port,
                url_scheme="http",
                threads=4
            )


if __name__ == "__main__":
    main()