import os
import json
import requests

def find_json_files(path):
    """Recursively finds all JSON files in a given path."""
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".json"):
                yield os.path.join(root, file)

def get_model_info(model_id):
    """Fetches model information from the Civitai API."""
    url = f"https://civitai.com/api/v1/models/{model_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching model info for modelId {model_id}: {e}")
        return None

def main():
    """Main function to find download links and write them to a file."""
    output_file = "download_links.txt"
    download_links = []

    for json_file in find_json_files("."):
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
                if "modelId" in data:
                    model_id = data["modelId"]
                    model_info = get_model_info(model_id)
                    if model_info:
                        model_type = model_info.get("type", "").lower()
                        if model_type in ["illustrious", "noobai"]:
                            if model_info.get("modelVersions"):
                                latest_version = model_info["modelVersions"][0]
                                if latest_version.get("files"):
                                    download_url = latest_version["files"][0].get("downloadUrl")
                                    if download_url:
                                        download_links.append(download_url)
                                        print(f"Found download link for modelId {model_id}: {download_url}")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing {json_file}: {e}")

    with open(output_file, "w") as f:
        for link in download_links:
            f.write(f"{link}\n")

    print(f"Download links saved to {output_file}")

if __name__ == "__main__":
    main()
