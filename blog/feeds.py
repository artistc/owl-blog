from django.contrib.syndication.views import Feed
from models import Article

class BlogFeed(Feed):
    title = "OranLooney.com"
    link = "http://oranlooney.com/"
    description = "quietly programming away: thoughts, tutorials, and vignettes"
    title_template = "blog/feeds/latest_title.html"
    description_template = "blog/feeds/latest_description.html"

    def items(self):
        return Article.objects.filter(published=True).order_by('-date_time_added')[:3]
    
    def item_link(self, item):
        return "http://oranlooney/" + item.slug + "/"
