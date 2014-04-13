from google.appengine.ext import db

# Create your models here.


class Article(db.Model):
    """Models an Article with an author, body and publish date"""

    author = db.StringProperty()
    title = db.StringProperty()
    body = db.TextProperty(multiline=True)
    publish_date = db.DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        """String representation of an Article."""

        return 'Article by %s, published the %s' %\
            (self.author, self.publish_date)
