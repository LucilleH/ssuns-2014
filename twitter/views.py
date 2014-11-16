import codecs
import datetime
import json
import os

from django.shortcuts import render
from django.http import HttpResponse

import twilio.twiml
from twitter.models import Tweet


def reply(message):
    resp = twilio.twiml.Response()
    resp.sms(message)
    return HttpResponse(str(resp))


def forum_approve(request):
    message = request.GET.get('Body')
    if not message:
        return reply("You sent an empty message")

    try:
        tweet_id = int(message)
    except ValueError:
        return reply("You must send a tweet ID")

    try:
        tweet_file = codecs.open("forum/data/%d" % tweet_id, 'r',
            encoding='utf-8')
    except IOError:
        return reply("Tweet ID not found")

    tweet_text = tweet_file.read()

    # Save it to the DB
    tweet, created = Tweet.objects.get_or_create(text=tweet_text, id=tweet_id)
    if created:
        return reply('Approved %d' % tweet_id)
    else:
        return reply("You already approved this tweet.")


def forum(request):
    return render(request, 'twitter/forum.html')


def forum_json(request):
    tweets = Tweet.objects.all()[:5]
    data = []
    for tweet in tweets:
        timestamp = (tweet.timestamp - datetime.timedelta(hours=5)).strftime("%H:%M:%S")
        data.append({
            'text': tweet.text,
            'timestamp': timestamp,
            'id': tweet.id,
        })

    return HttpResponse(json.dumps(data), mimetype='application/json')
