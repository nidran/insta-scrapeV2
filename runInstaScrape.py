
# getDetail dependencies

import argparse
# Importing getList & getInfo modules
import getList
import getInfo
from getList import InstagramCrawler
from getInfo import detailed_info
def main():
    #   Parsing Arguments  #
    parser = argparse.ArgumentParser(description='Instagram Crawler')
    parser.add_argument('-d', '--dir_prefix', type=str,
                        default='./data/', help=' directory to save results, default is ./data/')
    parser.add_argument('-q', '--query', type=str, default='instagram',
                        help=" Account to be followed.Default value will  use instagram's account for scraping")
    parser.add_argument('-t', '--crawl_type', type=str,
                        default='photos', help="Options: 'followers' | 'following'")
    parser.add_argument('-n', '--number', type=int, default=0,
                        help='Number of posts to scrape through')    
    parser.add_argument('-l', '--headless', action='store_true',
                        help='If set, will use PhantomJS driver to run script as headless')
    parser.add_argument('-a', '--authentication', type=str, default=None,
                        help='path to authentication json file')
    args = parser.parse_args()
    #  End Argparse #

    crawler = InstagramCrawler(headless=args.headless)
    crawler.crawl(dir_prefix=args.dir_prefix,
                  query=args.query,
                  crawl_type=args.crawl_type,
                  number=args.number,
                  caption=args.caption,
                  authentication=args.authentication)


if __name__ == "__main__":
    main()
    detailed_info()