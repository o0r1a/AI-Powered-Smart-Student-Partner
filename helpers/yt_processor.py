from youtube_transcript_api import YouTubeTranscriptApi

def process_yt(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([entry['text'] for entry in transcript])
    return text
