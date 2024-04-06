from googleapiclient.discovery import build
import json

api_key = 'AIzaSyDgWWxgNb_2-x5stWsI14xUujW8qIYP_n4'

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.search().list(
    part="snippet",
    q="south korea",
    type="video",
    videoDuration="medium",
    publishedAfter="2024-03-01T00:00:00Z",
    maxResults=50
)

nextPageToken = ""
videos = []
for page in range(5):
    request = youtube.search().list(
        part="snippet",
        q="north korea",
        type="video",
        videoDuration="medium",
        publishedAfter="2024-04-01T00:00:00Z",
        maxResults=50,
        pageToken=nextPageToken
    )

    response = request.execute()

    if page != 5:
        nextPageToken = response['nextPageToken']

    if 'items' in response:
        for item in response['items']:
            video = {
                'title': item['snippet']['title'],
                'publishTime': item['snippet']['publishTime']
            }
            videos.append(video)

    print(str(page) + "...")


# Save the data to a new JSON file
json_file_path = 'youtube_data.json'
with open(json_file_path, 'w') as json_file:
    json.dump(videos, json_file, indent=2)

print("JSON file done!")
