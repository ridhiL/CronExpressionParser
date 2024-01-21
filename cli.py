import click

from parser.cron_parser import CronExpressionParser


@click.command()
@click.argument('expression')
def cli(expression):
    parser = CronExpressionParser(expression).cron_parse()
    output = parser.get_cron_output()
    click.echo(output)
    # to take care of Words range, L, #


if __name__ == '__main__':
    cli()
