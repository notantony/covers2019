import argparse
import server.app

from server.app import app


parser = argparse.ArgumentParser(
    description='Run book covers generation server'
)
# Server settings
parser.add_argument(
    '--host',
    type=str,
    default='0.0.0.0',
    help='Host address'
)
parser.add_argument(
    '--port',
    type=int,
    default=5050,
    help='Listening port'
)
parser.add_argument(
    '--config',
    type=str,
    default='./config.yaml',
    help='Path to config'
)

def main():
    args = parser.parse_args()

    server.app.config = server.app.Сonfig(args.config)
 
    app.run(host=args.host, port=args.port)
