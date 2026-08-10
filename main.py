from time import perf_counter
import httpx

def check_url(url):
    start_time = perf_counter()

    response = httpx.get(url)

    elapsed_time = perf_counter() - start_time

    print("URL:", url)
    print("Status:", response.status_code)
    print("Reponse time:", elapsed_time)

def main():
    check_url("https://example.com")



if __name__ == "__main__":
    main()
