import json
import tqdm

from requests import request

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
def _cell_magic(line, cell_body):
    """Underlying function for jest cell magic

    Note:
        This function contains the underlying logic for the 'jest' cell
        magic. This function is not meant to be called directly.

    Args:
        line (str): "%%jest" followed by arguments as required
        cell_body (json str): a body providing the metadata of request options

    Example: In Jupyter notebook we have two cells. First cell provides a list of
    dictionary to feed the body request. We will have two requests for each item in
    a give json_feed_dict list. Jest will request two requests and save the responses
    in to the "output" variable as list.

    If `--params` is not provided with the cell magic, we only request one call and
    jest saves the response to the `output` variable again.

    [1] json_feed_dict = [dict(placeholder='dvalue1'), dict(placeholder='dvalue2')]

    [2] %%jest --var output --params json_feed_dict

    {
        "url": "http://localhost:8080/request",
        "request": "post",
        "body": {
          "afield": "avalue",
          "bfield": "bvalue",
          "cfield": {
            "dfield": "@placeholder"
          },
          "efield": "evalue"
        },
        'payload': {"key1": "value1", "key2": "value2"},
        "headers":{"accept": "application/json"}
    }

    Returns:
        list: the request result(s) in json format.
    """

    args = magic_arguments.parse_argstring(_cell_magic, line)
    meta_data = json.loads(cell_body.strip())

    assert meta_data.get('url', None) is not None, "url must be given"
    assert meta_data.get('request', None) is not None, "request must be given"

    params = args.params
    items = get_ipython().user_ns.get(params, None)
    assert isinstance(items, list), "params must be a list"

    responses = []
    if items:
        for item in tqdm.tqdm(items):
            assert isinstance(item, dict), "item for the list must be a dictionary"

            request_body = meta_data.get("body", None).copy()
            valid_request_body = update_request_body(request_body, item)

            response = request_response(meta_data, valid_request_body)
            responses.append(response.json())
    else:
        valid_request_body = meta_data.get("body", None)
        responses.append(request_response(meta_data, valid_request_body).json())

    print("Done.")
    IPython.get_ipython().push({args.var: responses})


def update_request_body(_request_body, item):
    keys = {"@" + key: key for key in item.keys()}
    for k, v in _request_body.items():
        if isinstance(_request_body[k], dict):
            _request_body[k] = update_request_body(_request_body[k].copy(), item)
        elif v in keys:
            _request_body[k] = item[keys.get(v)]
    return _request_body


def request_response(meta_data, body):
    payload = meta_data.get("payload", None)
    headers = meta_data.get("headers", None)
    request_from_user = meta_data.get("request")

    return request(
        request_from_user,
        meta_data.get("url"),
        params=payload,
        headers=headers,
        json=body
    )
