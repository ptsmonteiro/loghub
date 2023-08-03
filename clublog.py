import http.client, urllib.parse

clublog_url = 'clublog.org'
clublog_apikey = 'refh34o8th9384rt98'

def realtime_api(email, password, callsign, adif):
    print("Sending to ClubLog the following ADIF:\n")
    print(adif)
    conn = http.client.HTTPSConnection(clublog_url)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.parse.urlencode({
        '@email': email, 
        '@password': password, 
        '@callsign': callsign,
        '@adif': adif,
        '@api': clublog_apikey
        })
    print(params)
    conn.request("POST", "/realtime.php", params, headers)
    response = conn.getresponse()
    print(response)
