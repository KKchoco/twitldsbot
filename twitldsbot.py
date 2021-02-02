from urllib import request
import json
import discord
import re

client = discord.Client()
regex = "twitter.com\/(.*)\/status\/(\d*)"
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if re.search(regex, message.content):
        tweetid = re.search(regex, message.content)
        try:
            opener = request.build_opener()
            opener.addheaders = [
                                ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'),
                                ('x-twitter-client-language', 'en'),
                                ('x-csrf-token', 'yourtoken'),
                                ('authorization', 'yourtoken'),
                                ('Cookie', 'auth_token=yourtoken;ct0=yourtoken'),
                                ]
            f = opener.open("https://twitter.com/i/api/1.1/strato/column/None/tweetId=" + str(tweetid.group(2)) + ",destinationLanguage=None,translationSource=Some(Google),feature=None,timeout=None,onlyCached=None/translation/service/translateTweet")
        except HTTPError as e:
            print('[ERROR] The server couldn\'t fulfill the request.')
            print('[ERROR] Error code: ', e.code)
        except URLError as e:
            print('[ERROR] We failed to reach a server.')
            print('[ERROR] Reason: ', e.reason)
        else:
            html_text = f.read().decode('utf-8')
            a = json.loads(html_text)
            await message.channel.send('```' + a['translation'] + '```')

client.run('yourbottoken')
