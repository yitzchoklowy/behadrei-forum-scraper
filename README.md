# behadrei-forum-scraper
Scraper for Bechadrei Charedim Forums - Based on Scrapy

There are 2 spiders meanwhile in this project: A post spider and an index spider.

#Post Spider

name is bechadrei_post_spider

This Scrapy spider will scrape all posts in the forum, outputting for each post: 

*Cluster title: The title of the cluster post belongs to
*Cluster ID: The ID of the cluster post belongs to (From bechadrei ID)
*Datetime: Date and time of post
*Author : Author of post
*Author ID: Post Author's ID (From bechadrei ID)
*Post Title: Title of post (if available, otherwise will be empty string)
*Post Content: Content of post (cleaned up somewhat, ideally this should only have p tags and quote tags, but the messiness of bechadrei code and people's different ways of formatting for understanding made this too hard to acheive for now, so I left some html tags in it rather than losing content)
*Signature : Post signature (if available, otherwise empty string)


To reconstruct clusters from this you would have to select by cluster ID and order by datetime. You can also select any other way you want.


#Index Spider

name is bechadrei_index_spider

This will fetch the entire index of the forum, outputting a list of clusters with:

*Title
*Author
*Replies Number
*Views Number
*Last Reply Author
*Last Reply Time
*Cluster URL
*Cluster ID


# To run

from project directory: scrapy crawl [spider_name] -o filename.csv # You can also specify .xml or .json to get output in this way. csv is not reccomended for this project as the many commas in the post_content text will mess it up. 

# Requirements
*Python 3.6.2
*Scrapy 1.4.0
*BeautifulSoup 4.6.0
