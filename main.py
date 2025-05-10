#!/usr/bin/env python3

import argparse

from dotenv import load_dotenv

from src.llm.service import LLMService
from src.starter.hello import hello_world
from src.utils.logging import setup_logging

load_dotenv()
logger = setup_logging("main")


def parser() -> argparse.Namespace:
    """
    Parses command-line arguments for the greeting script.

    Returns:
        An argparse.Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Hello World - Prints a greeting message."
    )
    parser.add_argument(
        "--name",
        default="world",
        help="Name to greet (default: world)",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate a random pet name using the LLM service.",
    )
    return parser.parse_args()


def handle_name_generation() -> str:
    """
    Handles the generation of a name using the LLM service.

    Args:
        name: The name to generate.

    Returns:
        The generated name.
    """
    logger.info("Generating a name using LLM service.")
    llm_service = LLMService()
    prompt = "Give me a random pet English nameReturn only the name, nothing else."
    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    generated_name = llm_service.send_llm_request(
        model_name="gemini-flash-2.5", messages=messages
    )
    if generated_name:
        # Clean up the generated name, remove quotes or extra text
        name_to_greet = generated_name.strip().strip('"')
        logger.info(f"Generated name: {name_to_greet}")
    else:
        logger.warning("Failed to generate name, using default.")
    return name_to_greet


def main() -> None:
    """
    Main function to set up logging, parse arguments, and print a greeting.
    """

    args = parser()
    logger.info("Starting the greeting script.")

    name_to_greet = args.name

    if args.generate:
        name_to_greet = handle_name_generation() or name_to_greet

    hello_world(name_to_greet)
    logger.info("Finished the greeting script.")


if __name__ == "__main__":
    main()
