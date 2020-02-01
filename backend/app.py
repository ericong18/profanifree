import json
import re
import urllib.request

from pytube import YouTube

from flask import Flask, request, url_for

app = Flask(__name__)
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS
import pandas as pd

import ast

from profanity_check import predict, predict_prob


@app.route('/', methods=['GET','POST'])
def main():



    if request.method == 'POST':
        print(request.form)
        print(request.json)
       
        video_id = request.form.get('video_id')
        if video_id == None:
            packet = dict(request.json)
            video_id = packet['video_id']



        print(video_id)

        data = YouTubeTranscriptApi.get_transcript(video_id)
        df = pd.DataFrame(data)
        print(df)

        ixs = df.loc[predict(df.text) == [1]]
        if ixs.empty:
            no_curse_words = True
        else:
            no_curse_words = False
        # print(ixs)
        ixs.start = ixs.start.round()
        ixs.duration = ixs.duration.round()
        offending_lines = [tuple(x) for x in ixs.to_numpy()]
        
        
        
        return json.dumps({"Message": "Hello chrome extension ppl", "no_curse_words":no_curse_words, "offending_lines":offending_lines})

@app.route('/test', methods=['GET','POST'])
def test():

    return json.dumps({"Message":"Eric"})


if __name__ == '__main__':
    app.run(debug=True)