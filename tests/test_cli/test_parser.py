from storage.cli.parser import ArgParser


def test_argparser_parses_console_args():
    parser = ArgParser()
    parser.setup_args()
    args = ['--gui']
    parsed_args: dict = parser.parse_args(args)
    assert len(parsed_args.keys()) > 0