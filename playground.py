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

# openfile()


def downimg():
    link = 'https://dcn6x9s7fzj11.cloudfront.net/monthly_2020_06/20200601_122514.jpg.9241a776371748ca0cec3e2151815f3c.jpg'
    req = requests.get(link)
    with open("static/files/tree2.jpg", 'wb') as f:
        f.write(req.content)
        print("image downloaded")
    return


downimg()
