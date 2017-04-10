## client_id client_secret are obtained from
## dev.twitch.tv
client_id = ""
client_secret= ''
redirect_uri = 'https://example.com'
## channel_editor is required for uploading.
## channel_read is required for obtaining a channel_id
scope = ["channel_editor","channel_read"]
auth_url= "https://api.twitch.tv/kraken/oauth2/authorize?response_type=code"
filepath = "path/to/your/file.mp4"
title ="You will not believe what happened to this guy!"
## TODO add a skeleton for published/unpublished/scheduled,
## thumbnail, keywords.
