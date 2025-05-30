import re

def main():
    update_urls_in_file("data/scrapelist.txt")

# Updates urls from archive to have `if_` after url so that they won't show the top bar
def update_urls_in_file(file_path):
    try:
        with open(file_path, 'r') as my_file:
            urls = my_file.readlines()

        timestamp_pattern = re.compile(r'(https://web.archive.org/web/(\d{14}))')

        updated_urls = []
        for url in urls:
            url = url.strip()
            if timestamp_pattern.match(url):
                updated_url = re.sub(r'(https://web.archive.org/web/(\d{14}))', r'\1if_', url)
                updated_urls.append(updated_url)
            else:
                updated_urls.append(url)

        # Write the updated URLs back to the file
        with open(file_path, 'w') as my_file:
            my_file.write("\n".join(updated_urls) + "\n")

        print("URLs successfully updated!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__=="__main__":
  main()