import json
from django.conf import settings
from django.http import HttpResponse
import facebook
import requests

app_id = "2310735412324019"
app_secret = "ba377ec43ccabf958d5eafa77930ac70"
access_token = 'EAAg1mgNr5rMBABrx6sG1yTsFCvqv2rs5KgOyc10sDUmsKmTiu3b2RoJYea8hAJi6UZAmW0wymvdmFAY3IbBbP5IAeuxNrJm5SQccLuFgfVzwj35st11zNAiChNij5SVgTG854Vaypxr00KpRmNi6eRcOqqjQZD'


class FacebookFeed:

    #TODO - fix method
    def get_posts(cls, user, count=6):
        try:
            graph = facebook.GraphAPI(access_token)
            profile = graph.get_object('me')
            query_string = 'posts?limit={}'.format(count)
            posts = graph.get_connections(profile['id'], query_string)
            return posts
        except facebook.GraphAPIError:
            return None

if __name__ == '__main__':
    posts = FacebookFeed().get_posts(user="")
    if not posts:
        http_res = HttpResponse(status=500, content="Can't get posts for user", content_type="application/json")
    else:
        http_res = HttpResponse(json.dumps(posts), content_type="application/json")