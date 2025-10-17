import jinja2
import src.config_reader as ConfigReader
import src.html_builder as HtmlBuilder


def main():
    print(ConfigReader.load_config_from_file("test.toml"))


if __name__ == "__main__":
    main()
