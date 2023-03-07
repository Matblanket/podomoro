import subprocess

some = subprocess.getoutput('yt-dlp -f bestaudio -x -o temp https://www.youtube.com/watch?v=niqC3BT9gck')
print(some)
