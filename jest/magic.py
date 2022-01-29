import json
import tqdm

from requests import request
from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError

try:
    import IPython
    from IPython.core import magic_arguments
    from IPython.core.getipython import get_ipython
except ImportError:
    raise ImportError("This module can only be loaded in IPython.")


@magic_arguments.magic_arguments()
@magic_arguments.argument(
    "--var",
    help=(
            "save the output to this variable."
    ),
)
@magic_arguments.argument(
    "--params",
    default=None,
    help=(
            "Parameters to feed the request body. If present, the --params "
            "flag should be followed by a list of string representation of "
            "a dictionary in the format [{'param_name': 'param_value'}] "
            "(ex. [{\"keyword\": \"iphone\"}]), or a reference to a list "
            " of dictionary/dictionaries in the same format. The key of "
            "a dictionary will be used in the requested body if exists. "
            "Body request must mention one or more key in the value section."
            "(ex. { \"date\": \"@keyword\" })."
    )
)
def _cell_magic(line, body):
    """Underlying function for jest cell magic

    Note:
        This function contains the underlying logic for the 'jest' cell
        magic. This function is not meant to be called directly.

    Args:
        line (str): "%%jest" followed by arguments as required
        body (str): a body providing the metadata of request options

        {
            'url': 'http://milvus.n11.local:80/collections',
            'request': 'GET',
            'body': null,
            'headers':{'accept: application/json'}
        }

    Returns:
        list: the request results.
    """

    args = magic_arguments.parse_argstring(_cell_magic, line)
    meta_data = json.loads(body.strip())

    assert meta_data.get('url', None) is not None, "url must be given"
    assert meta_data.get('request', None) is not None, "request must be given"

    params = args.params
    items = get_ipython().user_ns.get(params, [])

    responses = []
    if items:
        for item in tqdm.tqdm(items):
            assert isinstance(item, dict), "params must be a list of dictionary"

            body = meta_data.get("body", None).copy()
            update_request_body(body, item)

            response = return_response(meta_data, body)
            try:
                responses.append(response.json())
            except RequestsJSONDecodeError:
                responses.append(response)
    else:
        body = meta_data.get("body", None)
        responses.append(return_response(meta_data, body))

    print("Done.")
    IPython.get_ipython().push({args.var: responses})


def update_request_body(body, item):
    keys = item.keys()
    for k, v in body.items():
        for key in keys:
            if isinstance(body[k], dict):
                update_request_body(body[k], item)
            if v == "@" + key:
                body[k] = item[key]
                break


def return_response(meta_data, body):
    payload = meta_data.get("payload", None)
    headers = meta_data.get("headers", None)
    request_from_user = meta_data.get("request")

    return request(request_from_user, meta_data.get("url"), params=payload, headers=headers, json=body)
