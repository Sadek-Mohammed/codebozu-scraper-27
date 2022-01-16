from utils import parse_wiki_multiple
from politico import parse_trump
from bbc import get_bbc_multi
from cnn import init
from fox_news import fox_news

if __name__ == '__main__':
    politicians_list: list = ['Donald Trump', 'Joe Biden', 'Barack Obama', 'George W. Bush', 'Bill Clinton']
    init(politicians_list)
