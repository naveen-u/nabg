import click
import nabg.bullshit_generator as bullshit_generator


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-n", default=1, help="Number of sentences to generate.")
@click.option(
    "--topic", "-t", default=None, help="Topic on which to generate bullshit."
)
@click.option(
    "--list-topics", "-l", is_flag=True, default=False, help="List available topics."
)
def main(n: int, topic: str, list_topics: bool):
    """
    Generate new-age bullshit.
    """
    if list_topics:
        for topic in bullshit_generator.list_topics():
            print(topic)
        return
    print(bullshit_generator.ionize(n, topic))


main()