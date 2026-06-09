import json
import os
import re


def convert_hoppscotch_to_postman_collection_v21(hoppscotch_json_exported_file, output_file=None, output_dir=None):
    # Load Hoppscotch JSON file with UTF-8 encoding
    with open(hoppscotch_json_exported_file, 'r', encoding='utf-8') as hoppscotch_file:
        hoppscotch_data = json.load(hoppscotch_file)

    # Initialize Postman Collection structure
    postman_collection = {
        "info": {
            "name": hoppscotch_data["name"],
            "_postman_id": "",
            "description": "",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [],
        "auth": {},
        "event": [],
        "variable": [],
        "protocolProfileBehavior": {}
    }

    # Helper function to replace <<...>> with {{...}} for Postman variables
    def replace_placeholders(value):
        if isinstance(value, str):
            return re.sub(r"<<(.*?)>>", r"{{\1}}", value)
        return value

    # Helper function to convert auth details
    def convert_auth(hoppscotch_auth):
        if not hoppscotch_auth:
            return None

        auth_type = hoppscotch_auth.get("authType", "none")

        if auth_type == "bearer":
            return {
                "type": "bearer",
                "bearer": [
                    {"key": "token", "value": replace_placeholders(hoppscotch_auth.get("token", "")), "type": "string"}
                ]
            }
        elif auth_type == "api-key":
            key_name = hoppscotch_auth.get("key", "")
            key_value = replace_placeholders(hoppscotch_auth.get("value", ""))
            add_to = hoppscotch_auth.get("addTo", "HEADERS").upper()
            return {
                "type": "apikey",
                "apikey": [
                    {"key": "key", "value": key_name, "type": "string"},
                    {"key": "value", "value": key_value, "type": "string"},
                    {"key": "in", "value": "header" if add_to == "HEADERS" else "query", "type": "string"}
                ]
            }
        elif auth_type == "basic":
            return {
                "type": "basic",
                "basic": [
                    {"key": "username", "value": replace_placeholders(hoppscotch_auth.get("username", "")), "type": "string"},
                    {"key": "password", "value": replace_placeholders(hoppscotch_auth.get("password", "")), "type": "string"}
                ]
            }
        elif auth_type == "inherit":
            return {"type": "inherit"}
        elif auth_type == "none":
            return {"type": "noauth"}
        return None

    # Helper function to convert headers
    def convert_headers(hoppscotch_headers):
        return [
            {"key": replace_placeholders(header["key"]), "value": replace_placeholders(header["value"]), "type": "text"}
            for header in hoppscotch_headers if header["active"]]

    # Helper function to convert body
    def convert_body(hoppscotch_body):
        if not hoppscotch_body:
            return None

        content_type = hoppscotch_body.get("contentType") or ""
        body_content = hoppscotch_body.get("body", "")

        if content_type == "multipart/form-data":
            body_data = json.loads(body_content) if isinstance(body_content, str) else body_content
            return {
                "mode": "formdata",
                "formdata": [{"key": replace_placeholders(item["key"]), "value": replace_placeholders(item["value"]),
                              "type": "text"} for item in body_data]
            }
        elif content_type == "application/x-www-form-urlencoded":
            body_data = json.loads(body_content) if isinstance(body_content, str) else body_content
            return {
                "mode": "urlencoded",
                "urlencoded": [{"key": replace_placeholders(k), "value": replace_placeholders(v), "type": "text"}
                               for k, v in body_data.items()]
            }
        else:
            return {
                "mode": "raw",
                "raw": replace_placeholders(body_content) if isinstance(body_content, str) else json.dumps(body_content),
                "options": {"raw": {"language": "json" if "json" in content_type else "text"}}
            }

    # Helper function to convert query params
    def convert_params(hoppscotch_params):
        return [
            {"key": replace_placeholders(param["key"]), "value": replace_placeholders(param["value"]),
             "description": param.get("description", "")}
            for param in hoppscotch_params if param.get("active", True)
        ]

    # Helper function to convert individual requests
    def convert_request(hoppscotch_request):
        url = replace_placeholders(hoppscotch_request["endpoint"])
        query_params = convert_params(hoppscotch_request.get("params", []))

        url_object = {
            "raw": url,
            "host": url.split("/")[:1],
            "path": url.split("/")[1:]
        }
        if query_params:
            url_object["query"] = query_params

        # Convert request-level variables to pre-request script
        request_variables = hoppscotch_request.get("requestVariables", [])
        event = []
        if request_variables:
            var_assignments = "\n".join([
                f'pm.variables.set("{v["key"]}", "{replace_placeholders(v.get("value", ""))}");'
                for v in request_variables
            ])
            event.append({
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [var_assignments]
                }
            })

        # Add pre-request script if present
        pre_request_script = hoppscotch_request.get("preRequestScript", "")
        if pre_request_script:
            event.append({
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [pre_request_script]
                }
            })

        # Add test script if present
        test_script = hoppscotch_request.get("testScript", "")
        if test_script:
            event.append({
                "listen": "test",
                "script": {
                    "type": "text/javascript",
                    "exec": [test_script]
                }
            })

        result = {
            "name": hoppscotch_request["name"],
            "request": {
                "method": hoppscotch_request["method"],
                "header": convert_headers(hoppscotch_request.get("headers", [])),
                "body": convert_body(hoppscotch_request.get("body", None)),
                "url": url_object,
                "auth": convert_auth(hoppscotch_request["auth"]),
                "description": hoppscotch_request.get("description", "")
            }
        }
        if event:
            result["event"] = event

        return result

    # Recursively convert folders and requests
    def convert_folder(hoppscotch_folder):
        folder_item = {
            "name": hoppscotch_folder["name"],
            "item": []
        }

        for subfolder in hoppscotch_folder.get("folders", []):
            folder_item["item"].append(convert_folder(subfolder))

        for request in hoppscotch_folder.get("requests", []):
            folder_item["item"].append(convert_request(request))

        return folder_item

    # Convert folders and add to Postman collection
    for folder in hoppscotch_data.get("folders", []):
        postman_collection["item"].append(convert_folder(folder))

    # Add global auth if present
    if hoppscotch_data.get("auth"):
        auth = convert_auth(hoppscotch_data["auth"])
        if auth:
            postman_collection["auth"] = auth

    # Add collection headers if present
    for header in hoppscotch_data.get("headers", []):
        if header.get("active", True):
            postman_collection["event"].append({
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [f'pm.request.headers.add({{key: "{header["key"]}", value: "{replace_placeholders(header["value"])}"}});']
                }
            })

    # Add collection variables if present
    for variable in hoppscotch_data.get("variables", []):
        postman_collection["variable"].append({
            "key": variable.get("key", ""),
            "value": variable.get("initialValue") or variable.get("value") or "",
            "type": "text"
        })

    # Generate file name based on the collection name
    if not output_file:
        output_file = f'{hoppscotch_data["name"]}-Postman_v2.1.json'

    if output_dir:
        output_file = os.path.join(output_dir, output_file)

    # Save the Postman collection to a file with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as postman_file:
        json.dump(postman_collection, postman_file, indent=2, ensure_ascii=False)

    print(f"Conversion completed. Postman collection saved as {output_file}")

    return postman_collection


def convert_hoppscotch_env_to_postman_env(hoppscotch_json_env, output_dir=None):
    import uuid
    from datetime import datetime, timezone

    # Load Hoppscotch environment JSON file
    with open(hoppscotch_json_env, 'r', encoding='utf-8') as hoppscotch_file:
        hoppscotch_env_data = json.load(hoppscotch_file)

    # Initialize Postman Environment structure
    postman_env = {
        "id": str(uuid.uuid4()),
        "name": hoppscotch_env_data["name"],
        "values": [],
        "_postman_variable_scope": "environment",
        "_postman_exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "_postman_exported_using": "Hoppscotch to Postman Converter"
    }

    # Convert variables from Hoppscotch to Postman format
    for variable in hoppscotch_env_data["variables"]:
        postman_env["values"].append({
            "key": variable["key"],
            "value": variable.get("initialValue") or variable.get("currentValue") or "",
            "enabled": True,
            "type": "text"
        })

    # Generate file name based on the environment name
    postman_env_file_name = f'{hoppscotch_env_data["name"]}-postman_environment.json'

    if output_dir:
        postman_env_file_name = os.path.join(output_dir, postman_env_file_name)

    # Save the Postman environment to a file with UTF-8 encoding
    with open(postman_env_file_name, 'w', encoding='utf-8') as postman_env_file:
        json.dump(postman_env, postman_env_file, indent=2, ensure_ascii=False)

    print(f"Environment conversion completed. Saved as {postman_env_file_name}")

    return postman_env
