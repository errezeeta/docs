import json
import os

def generate_mdx_from_openapi(openapi_path, output_dir):
    with open(openapi_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    
    paths = spec.get("paths", {})
    os.makedirs(output_dir, exist_ok=True)
    
    for endpoint, methods in paths.items():
        for method, details in methods.items():
            title = details.get("summary", method.upper() + " " + endpoint)
            description = details.get("description", "No description available.")
            mdx_filename = f"{method}_{endpoint.strip('/').replace('/', '_')}.mdx"
            mdx_path = os.path.join(output_dir, mdx_filename)
            
            mdx_content = f"""---
title: '{title}'
description: '{description}'
api: '{method.upper()} {endpoint}'
---

### Body

<Warning>
    Review the body parameters before sending the request.
</Warning>

"""
            if "requestBody" in details:
                for content_type, content in details["requestBody"].get("content", {}).items():
                    if "schema" in content:
                        mdx_content += f"<ParamField body='body' type='{content_type}' required>
    {json.dumps(content['schema'], indent=2)}
</ParamField>

"
            
            mdx_content += "### Response\n"
            if "responses" in details:
                for status, response in details["responses"].items():
                    mdx_content += f"<ResponseField name='status' type='integer'>
  HTTP status code: {status}.
</ResponseField>\n"
                    
                    if "content" in response:
                        for content_type, content in response["content"].items():
                            if "schema" in content:
                                mdx_content += f"<ResponseField name='response_body' type='{content_type}'>
  {json.dumps(content['schema'], indent=2)}
</ResponseField>\n"
            
            with open(mdx_path, "w", encoding="utf-8") as f:
                f.write(mdx_content)
            print(f"Generated: {mdx_filename}")

# Uso del script
generate_mdx_from_openapi("openapi.json", "mdx_output")
