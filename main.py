#!/usr/bin/env python3

import argparse

from dotenv import load_dotenv

from src.starter.hello import hello_world
from src.utils.loggging import setup_logging

load_dotenv()


def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Hello World - Prints a greeting message."
    )
    parser.add_argument(
        "--name",
        default="world",
        help="Name to greet (default: world)",
    )
    return parser.parse_args()


def main() -> None:
    logger = setup_logging("main")
    args = parser()
    logger.info("Starting the hello world script.")
    hello_world(args.name)
    logger.info("Finished the hello world script.")


if __name__ == "__main__":
    main()
