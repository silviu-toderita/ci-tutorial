import json
import routes

functional_map = {
    key: getattr(routes, key)
    for key in dir(routes)
    if not key.startswith("__")
    and callable(getattr(routes, key))
    and getattr(routes, key).__module__ == "routes"
}


def handler(event, context):
    """Handler for the lambda function. You won't have to change any of this."""
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Origin": "*",
        },
        "multiValueHeaders": {},
    }
    try:
        if (
            event
            and "route" in (event.get("queryStringParameters", None) or {})
            and event["queryStringParameters"]["route"] in functional_map
        ):
            response["body"] = json.dumps(
                {
                    "response": functional_map[event["queryStringParameters"]["route"]](
                        json.loads(event["body"])["payload"]
                    )
                }
            )
        else:
            response["body"] = json.dumps(
                {
                    n: f.__doc__ if f.__doc__ else "No description."
                    for n, f in functional_map.items()
                }
            )
    except Exception as e:
        response["statusCode"] = 500
        response["body"] = json.dumps({"response": str(e)})
    return response


if __name__ == "__main__":
    print(
        "You shouldn't have to run this file directly, so instead I'll print debugging outputs."
    )
    print("Mapped Functions:")
    for func, desc in functional_map.items():
        print(func, " -- ", desc.__doc__)
