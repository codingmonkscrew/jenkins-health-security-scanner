import json
import requests

def get_jenkins_info(jenkins_url, token):
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{jenkins_url}/api/json", headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {"error": str(e)}


def run_scanner():
    jenkins_url = "http://host.docker.internal:8080"  # your Jenkins container
    api_token = "dummy-token"  # will pass from Jenkins later

    print("[INFO] Collecting Jenkins data...")
    data = get_jenkins_info(jenkins_url, api_token)

    with open("report.json", "w") as f:
        json.dump(data, f, indent=4)

    print("[INFO] Basic scan completed. JSON saved as report.json")


if __name__ == "__main__":
    run_scanner()
