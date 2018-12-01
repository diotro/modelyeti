#!/usr/bin/env python3

import argparse
from yetiserver import app_factory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--credentials", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=5000)
    parser.add_argument("--debug", default=False)

    args = parser.parse_args()
    run_server(args.credentials, args.host, args.port, args.debug)


def run_server(db_creds, host, port, debug):
    app = app_factory.create_app(db_creds)
    app.run(host, port, debug)


if __name__ == '__main__':
    main()
