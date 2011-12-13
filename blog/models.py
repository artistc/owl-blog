from django.db import models
from thumbs import ImageWithThumbsField

THUMBNAIL_SIZE = (50,50)

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    date_time_added = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    content = models.TextField()
    lead_photo = ImageWithThumbsField(
        upload_to="images/lead", 
        blank=True,
        sizes=( (75,75), )
    )
    lead_photo_link = models.URLField(blank=True)
    published = models.BooleanField()

    def __unicode__(self):
        return self.title

    def get_expanded_content(self):
        "expands the markdown content in full HTML and adds links."
        import links
        import markdown
        markdown_content = markdown.markdown(self.content)
        le = links.getLinkExpander()
        return le(markdown_content)
    
##    def create_thumbnail(self):
##        from PIL import Image
##        from cStringIO import StringIO
##        import os
##        if not self.lead_photo:
##            return
##        image = Image.open(self.lead_photo.path)
##        if image.mode not in ('L', 'RGB'):
##            image = image.convert('RGB')
##        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
##        buffer = StringIO()
##        image.save(buffer, image.format)
##        content = ContentFile(buffer.getvalue())
##        self.thumbnail.save(self.lead_photo.name, content, save=False)

    class Meta:
        get_latest_by = 'date_time_added'

    
class Link(models.Model):
    link_id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=20)
    url = models.URLField()

    def __unicode__(self):
        address = self.url.replace('http://','')
        return "%s -> %s" % (self.keyword, address)

    class Meta:
        pass
     
class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    slug = models.SlugField()
    articles = models.ManyToManyField(Article)
    
    def __unicode__(self):
        count = self.articles.count()
        if count == 0:
            return self.title
        else:
            return self.title + '(' + str(count) + ')'


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article)
    user_name = models.CharField(max_length=12)
    date_time_added = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=800)

    def __unicode__(self):
        c = self.content
        if len(c) < 20: said = c
        else: said = ( c[0:22] + '...')

        d = self.date_time_added
        when = '%d-%dT%02d:%02d' % (d.month, d.day, d.hour, d.minute)
        return '%s@%s: %s said "%s"' % (
            self.article.slug,
            when,
            self.user_name,
            said
        )

    class Meta:
        order_with_respect_to = 'article'
        get_latest_by = 'date_time_added'



