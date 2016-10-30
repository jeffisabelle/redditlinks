import click


@click.command()
@click.option('--input_file', default="input.html", help='input filename')
@click.option('--output_file', default="output.html", help='output filename')
def beautify_mjml(input_file, output_file):
    """

    Arguments:
    - `input_file`:
    - `output_file`:
    """
    with open(input_file, "r") as inp:
        input_text = inp.read()

    output_text = input_text.replace(">", ">\n")
    with open(output_file, "w") as out:
        out.write(output_text)

if __name__ == '__main__':
    beautify_mjml()
