Script that automatically scrapes followers & following list from a public profile's account. 
Does not use Instagram API's

## Login to crawl followers/ following

To crawl followers or followings, you will need to login with your credentials by filling in 'auth.json' 

## Headless Browser
To use a headless browser like Phantom JS ,after installing phantomjs, add '-l' to the arguments

## Usage Format

 python runInstaScrape.py [-h] [-d DIR_PREFIX] [-q QUERY] [-t CRAWL_TYPE]  [-n NUMBER] [-l] [-a AUTHENTICATION]

 eg,

 python runInstaScrape.py -q instagram -t followers -n 200 -a auth.json

# Instagram Crawler

   Arg's details
   
  -h, --help            						show this help message and exit
  -d DIR_PREFIX, --dir_prefix DIR_PREFIX
                        						directory to save results, default is ./data/
  -q QUERY, --query QUERY
                       							 Account to be followed.Default value will use
                        						instagram's account for scraping
  -t CRAWL_TYPE, --crawl_type CRAWL_TYPE
                       							 Options: 'followers' | 'following'
  -n NUMBER, --number NUMBER
                        						Number of posts to scrape through
  -l, --headless        						If set, will use PhantomJS driver to run script as
                        						headless
  -a AUTHENTICATION, --authentication AUTHENTICATION
                        						path to authentication json file

