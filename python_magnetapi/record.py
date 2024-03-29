"""
create record
"""

from . import utils
from .attachment import create as attach_create


def create(
    session,
    api_server: str,
    headers: dict,
    data: dict,
    verbose: bool = False,
    debug: bool = False,
):
    """
    create a record from a data dictionnary
    """

    _ids = utils.get_list(
        session, api_server, headers=headers, mtype="record", debug=debug
    )
    if data["name"] in _ids:
        print(f"record with name={data['name']} already exists")
        return None

    else:
        # look for site
        _ids = utils.get_list(
            session, api_server, headers=headers, mtype="site", debug=debug
        )
        if data["site"] not in _ids:
            print(
                f"create(record, name={data['name']}): site with name={data['site']} does not exist - must be created first"
            )
            return None
        else:
            _id = _ids[data["site"]]
            data["site_id"] = _id
            del data["site"]

            data["attachment_id"] = attach_create(
                session, api_server, headers, data["file"], verbose, debug
            )
            del data["file"]
            print(f"data:{data}")

            # process record data: remove empty columns, rename columns, add Hoopstress data
            response = utils.post_json(
                session, api_server, headers, data, "clirecord", verbose, debug=True
            )
            if response is None:
                print(f"record {data['name']} failed to be created")
                return None

            print(f"record {data['name']} created with id={response['id']}")
            return response["id"]
