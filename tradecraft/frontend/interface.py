def get_html(path):
    with open('html/' + path) as html_file:
        html = path.read()
    return html


def homepage():
    return get_html('index.html')
