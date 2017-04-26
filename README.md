# Twitch-clipper-skeleton
A skeleton-script in python for uploading a video on twitch.tv
<h1> How to </h1>
Update the file config.py with the required API keys from <a href="https://dev.twitch.tv">dev.twitch.tv</a>. Specify a filepath
and the name of the video. Consult <a href="https://dev.twitch.tv/docs/v5/guides/video-upload/"> the documentation </a> 
for accepted video formats/bitrates.

<h1> Workflow </h1> 
<ul>
<li> A Web OAuth2.0 authentication is performed first (see <a href="https://requests-oauthlib.readthedocs.io/en/latest/"> here </a>) </li>
<li> A POST request creates the video on twitch.tv. 
<li> Several PUT requests are performed for uploading the video in chunks.</li>
<li> A POST request alerts twitch.tv that the upload is finished. The video is available 
as soon as twitch.tv has finished encoding on its end
</li>
</ul>

<h1> Requirements </h1>
<ul>
<li> Python 3.x </li>
<li> requests and requests_oauthlib
<li> Install requirements with
```
python -m pip install requirements.txt
```</li>
</ul>

