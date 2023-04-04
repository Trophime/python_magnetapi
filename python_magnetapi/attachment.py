"""
create attachment
"""

import os
import requests
from . import utils


def create(
    api_server: str,
    headers: dict,
    data: str,
    verbose: bool = False,
    debug: bool = False,
):
    """
    create an attachment from a data dictionnary
    """
    print(f"attachment/create: data={data}")

    (basedir, basename) = os.path.split(data)
    cwd = os.getcwd()
    if basedir:
        os.chdir(basedir)

    files = {"file": open(basename, "rb")}

    # create an attachment
    response = utils.postfile(api_server, headers, files, "attachment", verbose, debug)
    if response is None:
        print(f"record {data['name']} failed to create attachment {data}")
        return None
    os.chdir(cwd)

    return response["id"]