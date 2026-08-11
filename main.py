from time import perf_counter
import httpx

def check_url(url):
    start_time = perf_counter()

    response = httpx.get(url)

    elapsed_time = perf_counter() - start_time

    return {
        "url": url,
        "status": response.status_code,
        "response_time": elapsed_time,
    }

def main():
    result = check_url("https://example.com")

    print("URL:", result["url"])
    print("Status:", result["status"])
    print("Response time:", result["response_time"])

if __name__ == "__main__":
    main()
