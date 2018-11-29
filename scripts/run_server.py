#!/usr/bin/env python3

import argparse
from yetiserver import app_factory


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-credentials-file", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=5000)
    parser.add_argument("--debug", default=False)

    args = parser.parse_args()
    db_creds, host, port, debug = args.database_credentials_file, args.host, args.port, args.debug
    app = app_factory.create_app(db_creds)
    app.run(host, port, debug)