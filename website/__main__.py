import argparse
import os.path
import sys

def main():
    parser = argparse.ArgumentParser(description='webpage app')
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port to run app on (default 5000)'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help=('Run the application in debug mode (reloads when the source '
              'changes and gives more detailed error messages)')
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Print the version number and exit'
    )

    args = vars(parser.parse_args())

    from . import version, webapp

    if args['version']:
        print (version.__version__)
        sys.exit()

    webapp.app.run(port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()