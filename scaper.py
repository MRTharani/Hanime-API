import subprocess

def fetch_video_links(command):
    try:
        links = []
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        data = result.stdout
        
        # Split data once
        video_lines = data.split('\n')
        
        # Extract video links
        for i in range(1, len(video_lines)):
            video = video_lines[i]
            if video.endswith('.m3u8'):
                # Use the previous line for the first part of the link
                links.append([video_lines[i - 1].split(":")[0], "https:" + video.split(":")[-1]])
        
        return links

    except subprocess.CalledProcessError as e:
        # Print the error message if the command fails
        print("Error:")
        print(e.stderr)
        return []  # Return an empty list on error


