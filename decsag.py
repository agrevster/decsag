import toml
import jinja2

def makeHtml(tomlFile, outputFile):
    jinja2_env = jinja2.Environment()
    builder = jinja2_env.from_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    {% for header in headers %}<h1>{{ header }}</h1>
    <h2>{{ tomlData[header] }}</h2>
    {% endfor %}
    </body>
    </html>
    """)
    with open(tomlFile) as f:
        tomlData = toml.load(f)
        htmlFile = open(outputFile, 'w')
        htmlFile.write(builder.render(headers=tomlData.keys(), tomlData=tomlData))


def main():
    makeHtml(tomlFile='sample.toml', outputFile='template.html')


if __name__ == "__main__":
    main()
