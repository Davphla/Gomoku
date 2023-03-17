#!/usr/bin/env python3

import argparse
import asyncio

from Client import Client


def get_flags():
    """
    Get the flags from the command line
    :return: options from the command line
    """
    parser = argparse.ArgumentParser()
    return parser.parse_args()


def create_client():
    try:
        client = Client()
        asyncio.run(client.loop_client())
    except IOError as e:
        raise e("Connection closed.")


def entrypoint():
    opts = get_flags()
    try:
        create_client()
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")


if __name__ == '__main__':
    entrypoint()
