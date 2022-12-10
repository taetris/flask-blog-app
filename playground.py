import requests
import webbrowser
def download(input_link):
    req = requests.get(input_link)
    filename = req.url[input_link.rfind("/")+1:]

    with open(filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                return

# download('https://filesamples.com/samples/document/txt/sample3.txt')
def openfile(filename):
    path = app.config['UPLOAD_FOLDER'] + filename
    webbrowser.open_new(path)
    return

openfile()
