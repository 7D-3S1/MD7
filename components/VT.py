import aiohttp
import asyncio
import json
import dotenv
import os

async def VT_analyze_url(url_to_analyze, api_key):
    """
    Analyzes a URL using the VirusTotal API.

    Args:
        url_to_analyze (str): The URL to be analyzed.
        api_key (str): The API key for accessing the VirusTotal API.

    Returns:
        dict: The analysis report if successful, otherwise an error dictionary.

    Example of a successful report:

    {
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

    """

    url = "https://www.virustotal.com/api/v3/urls"
    payload = {"url": url_to_analyze}
    headers = {
        "accept": "application/json",
        "x-apikey": api_key,
        "content-type": "application/x-www-form-urlencoded"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                analysis_id = response_data["data"]["id"]
                print(f"URL submitted successfully. Analysis ID: {analysis_id}")

                await asyncio.sleep(3)

                report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
                async with session.get(report_url, headers=headers) as report_response:
                    if report_response.status == 200:
                        report = await report_response.json()
                        print(json.dumps(report, indent=4))
                        return report
                    else:
                        error_text = await report_response.text()
                        print(f"Failed to retrieve report: {report_response.status}")
                        print(error_text)
                        return {"error": f"Failed to retrieve report: {report_response.status}"}
            else:
                error_text = await response.text()
                print(f"Failed to submit URL: {response.status}")
                print(error_text)
                return {"error": f"Failed to submit URL: {response.status}"}
            
async def VT_analyze_file(api_key, file_path):
    """
    Uploads a file to VirusTotal for analysis and retrieves the analysis report.

    Args:
        api_key (str): The API key for accessing the VirusTotal API.
        file_path (str): The path to the file to be uploaded.

    Returns:
        dict: The analysis report as a dictionary.

    Raises:
        aiohttp.ClientError: If an error occurs during the HTTP request.
        Exception: If an unexpected error occurs.

    Example of a successful report:
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
    UPLOAD_URL = "https://www.virustotal.com/api/v3/files"

    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, "rb") as f:
                data = aiohttp.FormData()
                data.add_field('file', f)
                headers = {
                    "accept": "application/json",
                    "x-apikey": api_key
                }

                async with session.post(UPLOAD_URL, data=data, headers=headers) as response:
                    response.raise_for_status()
                    response_data = await response.json()
                    analysis_id = response_data["data"]["id"]
                    print(f"File uploaded successfully. Analysis ID: {analysis_id}")

                    await asyncio.sleep(3)

                    report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
                    async with session.get(report_url, headers=headers) as report_response:
                        report_response.raise_for_status()
                        report = await report_response.json()
                        print(json.dumps(report, indent=4))
                        return report

    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}

# 使用範例
async def main():
    # VT_analyze_url usage example
    url_to_analyze = "https://ais3.org/Home/Course"
    result = await VT_analyze_url(url_to_analyze, API_KEY)
    print("URL analysis result:")
    print(json.dumps(result, indent=4))

    # VT_analyze_file usage example
    file_path = "test_file.pdf"
    result = await VT_analyze_file(API_KEY, file_path)
    print("File upload result:")
    print(json.dumps(result, indent=4))

# 執行主函式
if __name__ == "__main__":
    # 載入環境變數
    dotenv.load_dotenv()
    # get the API key from the environment variable
    API_KEY = os.getenv("VT-API-KEY")
    asyncio.run(main())