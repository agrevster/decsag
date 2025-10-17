import argparse
import src.config_reader as ConfigReader
import src.html_builder as HtmlBuilder


def main():
    arg_parser = argparse.ArgumentParser(
        prog="decag",
        usage="decsag --help",
        description="Generates a security audit document from a given .toml file.",
        epilog="~ DECAG (Dave's Extra Crappy Security Audit Generator)",
    )

    arg_parser.add_argument(
        "-i",
        "--input",
        metavar="file",
        required=False,
        help="The path of the TOML file to generate the report from.",
    )

    arg_parser.add_argument(
        "-o",
        "--output",
        metavar="file",
        required=False,
        help="The path of the generated HTML file.",
    )

    arg_parser.add_argument(
        "--generate-schema",
        required=False,
        action="store_true",
        help="Generates a Draft4 JSON schema used for the schema of the TOML file.",
    )

    args = arg_parser.parse_args()

    if args.generate_schema:
        print(ConfigReader.generate_schema())
    else:
        if args.input is None:
            arg_parser.error("You must specify an input file!")

        config = ConfigReader.load_config_from_file(args.input)


if __name__ == "__main__":
    main()
