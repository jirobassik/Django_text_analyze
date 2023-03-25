from requests import get

def handle_uploaded_file(f, path: str):
    with open(path + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def download_file_from_url(url: str):
    r = get(url)
    with open("role/static/saved/role.png", 'wb+') as f:
        f.write(r.content)
