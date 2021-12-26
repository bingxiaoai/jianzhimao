# Scrapy settings for mao project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'mao'

SPIDER_MODULES = ['mao.spiders']
NEWSPIDER_MODULE = 'mao.spiders'

# 设置重复过滤器的模块
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 设置调度器，scrap_redis中的调度器具备与数据库交互的功能
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 设置当爬虫结束的时候是否保持redis数据库中的去重集合与任务队列
SCHEDULER_PERSIST = True
#SCHEDULER_QUEUE_CLASS ='scrapy_redis.queue.PriorityQueue' #默认队列，优先级队列 ,备用队列
#SCHEDULER_QUEUE_CLASS ='scrapy_redis.queue.FifoQueue' #先进先出队列
#SCHEDULER_QUEUE_CLASS ='scrapy_redis.queue.LifoQueue' #后进先出队列

# 导出时强制为'utf-8'
# FEED_EXPORT_ENCODING = 'utf-8'
# # 数据库设置
# MYSQL_DB_HOST='127.0.0.1'
# MYSQL_DB_PORT=3306
# MYSQL_DB_NAME='text'
# MYSQL_DB_USER='root'
# MYSQL_DB_PASSWORD=''

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mao (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
USER_AGENT_LIST = {
   "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0;.NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC6.0)",
   "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64;Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
   "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
   "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
   "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
   "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
   "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
   "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
}

PROXY_LIST = [
   {"ip_port":"58.47.159.147:8001"},
   {"ip_port":"203.189.199.18:8888"}
    ]
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'mao.middlewares.MaoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'mao.middlewares.MaoDownloaderMiddleware': 543,
   'mao.middlewares.RandomUserAgent': 542,
   'mao.middlewares.RandomProxy': 543,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'mao.pipelines.MaoPipeline': 300,
#}
ITEM_PIPELINES = {
   # 'mao.pipelines.MYSQLPipeline': 300,
   'mao.pipelines.JsonPipeline': 299,
   'mao.pipelines.CSVPipeline': 298,
   # 'scrapy_redis.pipelines.RedisPipeline':400,
}
# 设置redis数据库
REDIS_URL = 'redis://192.168.238.1'
# redis的默认encoding是utf-8，如果你想用其他编码可以进行如下设置：
REDIS_ENCODING = 'utf-8'
# LOG_LEVEL = 'DEBUG'
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
