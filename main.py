import click
from stocks_spider import StockSpider


@click.command()
@click.option('--email', prompt='email', help='Type your email')
@click.option(
    '--password',
    prompt='password',
    help='Type your password',
    hide_input=True,
)
@click.option('--save/--no-save', default=True, help='Save data at database')
@click.option('--mongo-url', default='mongodb://localhost:27017/', help='Mongo endpoint ')
@click.option('--db-name', default='stocks', help='Database name')
def run(email, password, save, mongo_url, db_name):

    spider = StockSpider(
        email, password, mongo_url=mongo_url, db_name=db_name,
    )
    spider.extract_data_for_all_stocks(save=save)


if __name__ == '__main__':
    run()
