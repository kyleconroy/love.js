from bs4 import BeautifulSoup
import urllib
import os
import logging

for d in ["wiki", "lib", "lib/love"]:
    try:
        os.mkdir(d)
    except:
        pass


logging.basicConfig(level=logging.INFO)

modules = [
    'love.audio',
    'love.event',
    'love.filesystem',
    'love.font',
    'love.graphics',
    'love.image',
    'love.joystick',
    'love.keyboard',
    'love.mouse',
    'love.physics',
    'love.sound',
    'love.thread',
    'love.timer',
]

def fetch(path):
    try:
        html = "wiki/{}.html".format(path)
    except UnicodeEncodeError:
        return

    if os.path.exists(html):
        return

    logging.info("https://love2d.org/wiki/{}".format(path))
    urllib.urlretrieve("https://love2d.org/wiki/{}".format(path), html)


for module in modules:
    fetch(module)


for module in modules:
    html = "wiki/{}.html".format(module)
    soup = BeautifulSoup(open(html))

    span = soup.find('span', id='Functions')

    if span is None:
        logging.error("No functions")

    table = span.parent.next_sibling.next_sibling

    for a in table.find_all('a'):
        func = a.text

        if module + '.' not in func:
            continue

        fetch(func)

for module in modules:

    javascript = ""

    for function in os.listdir('wiki'):
        if not function.startswith(module):
            continue

        if function == "{}.html".format(module):
            continue

        logging.info(function)

        html = "wiki/{}".format(function)
        soup = BeautifulSoup(open(html))

        deprecated = soup.find('table', bgcolor='#ff9090')

        for span in soup.find_all('span', id='Function'):
            code = span.parent.next_sibling.next_sibling.next_sibling.next_sibling

            if code is None or code.text is None:
                continue

            try:
                _, signature = code.text.split("=", 1)
            except ValueError:
                signature = code.text


            if not signature.strip().startswith("love"):
                continue

            logging.info(signature)

            signature = signature.replace(", ...", '')
            name, args = signature.split("(", 1)

            name = name.replace(module + ".", '').strip()

            try:
                body = "exports.{} = function({} {{\n".format(name, args)
                body += "  //{}\n".format("deprecated??" if deprecated else "implement me")
                body += "}\n"
            except UnicodeEncodeError:
                pass

            javascript += body

    with open("lib/love/{}.js".format(module.replace("love.", '')), 'w') as f:
        f.write(javascript)

