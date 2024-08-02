import requests
import time
import json

# API-KEY
API_KEY = "35acfa85c491f6be271de4934cfaafb4417593ecb3da890a9f67736517e3639e"

def analyze_url(url_to_analyze, api_key):
    # URL and payload
    url = "https://www.virustotal.com/api/v3/urls"
    payload = {"url": url_to_analyze}
    headers = {
        "accept": "application/json",
        "x-apikey": api_key,
        "content-type": "application/x-www-form-urlencoded"
    }

    # Send POST request
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        # Parse JSON data
        response_data = response.json()
        analysis_id = response_data["data"]["id"]
        print(f"URL submitted successfully. Analysis ID: {analysis_id}")

        time.sleep(3)

        # URL for the analysis report
        report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        report_response = requests.get(report_url, headers=headers)

        if report_response.status_code == 200:
            report = report_response.json()

            # Print the JSON report
            print(json.dumps(report, indent=4))

            # Return the JSON report
            return report
        else:
            print(f"Failed to retrieve report: {report_response.status_code}")
            print(report_response.text)
            return {"error": f"Failed to retrieve report: {report_response.status_code}"}
    else:
        print(f"Failed to submit URL: {response.status_code}")
        print(response.text)
        return {"error": f"Failed to submit URL: {response.status_code}"}

# Example usage
url_to_analyze = "https://ais3.org/Home/Course"
report = analyze_url(url_to_analyze, API_KEY)

"""{
    "data": {
        "id": "u-51749788b27b5e44ebac08c120ae5bb9208f3206870cb5c6c95520f9b8ad79f7-1722582595",
        "type": "analysis",
        "links": {
            "self": "https://www.virustotal.com/api/v3/analyses/u-51749788b27b5e44ebac08c120ae5bb9208f3206870cb5c6c95520f9b8ad79f7-1722582595",
            "item": "https://www.virustotal.com/api/v3/urls/51749788b27b5e44ebac08c120ae5bb9208f3206870cb5c6c95520f9b8ad79f7"
        },
        "attributes": {
            "results": {},
            "stats": {
                "malicious": 0,
                "suspicious": 0,
                "undetected": 0,
                "harmless": 0,
                "timeout": 0
            },
            "date": 1722582595,
            "status": "queued"
        }
    },
    "meta": {
        "url_info": {
            "id": "51749788b27b5e44ebac08c120ae5bb9208f3206870cb5c6c95520f9b8ad79f7",
            "url": "https://ais3.org/Home/Course"
        }
    }
}"""
def upload_file_to_virustotal(api_key, file_path):
    """
    Uploads a file to VirusTotal for analysis and returns the analysis report as JSON.

    Parameters:
    api_key (str): Your VirusTotal API key.
    file_path (str): The path to the file to be uploaded.

    Returns:
    dict: The analysis report as JSON, or an error message in case of failure.
    """
    upload_url = "https://www.virustotal.com/api/v3/files"

    try:
        # Read file
        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {
                "accept": "application/json",
                "x-apikey": api_key
            }

            # Upload file
            response = requests.post(upload_url, files=files, headers=headers)
            response.raise_for_status()  # Check if the request was successful

            # Parse JSON data
            response_data = response.json()
            analysis_id = response_data["data"]["id"]
            print(f"File uploaded successfully. Analysis ID: {analysis_id}")

            # Give some time for the analysis to be done
            time.sleep(3)

            # Get analysis report URL
            report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
            report_response = requests.get(report_url, headers=headers)
            report_response.raise_for_status()  # Check if the request was successful

            report = report_response.json()

            # Print the JSON report
            print(json.dumps(report, indent=4))

            return report

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}
"""
{
    "data": {
        "id": "MDA4ZGNmOWNhNmFhYjYyMWQzYjM4MzFkYjY4MTU4Njc6MTcyMjU4MzMzNQ==",
        "type": "analysis",
        "links": {
            "self": "https://www.virustotal.com/api/v3/analyses/MDA4ZGNmOWNhNmFhYjYyMWQzYjM4MzFkYjY4MTU4Njc6MTcyMjU4MzMzNQ==",
            "item": "https://www.virustotal.com/api/v3/files/440e6ea9fa825578abfdd7b7932ef8393d72ef86c0c33f64676705ce40b1dfc2"
        },
        "attributes": {
            "date": 1722583335,
            "stats": {
                "malicious": 0,
                "suspicious": 0,
                "undetected": 0,
                "harmless": 0,
                "timeout": 0,
                "confirmed-timeout": 0,
                "failure": 0,
                "type-unsupported": 0
            },
            "results": {},
            "status": "queued"
        }
    },
    "meta": {
        "file_info": {
            "sha256": "440e6ea9fa825578abfdd7b7932ef8393d72ef86c0c33f64676705ce40b1dfc2",
            "md5": "008dcf9ca6aab621d3b3831db6815867",
            "sha1": "24a49fea3c46cb86995d2e93a2188e9ba291747a",
            "size": 503663
        }
    }
}
"""

### Usage
API_KEY = "API-KEY"
FILE_PATH = "test_file.pdf"
upload_file_to_virustotal(API_KEY, FILE_PATH)

URL_TO_ANALYZE = "https://ais3.org/Home/Course"
analyze_url(URL_TO_ANALYZE, API_KEY)