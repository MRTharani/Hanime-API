import os
import subprocess
import shlex
import time
import sys
import logging
import random




def generate_thumbnail(file_name, output_filename):
    """Generates a thumbnail for the provided video file."""
    command = [
        'vcsi',
        file_name,
        '-t',
        '-g', '2x2',
        '--metadata-position', 'hidden',
        '--start-delay-percent', '35',
        '-o', output_filename
    ] 
    try:
        logging.info(f"Running command: {' '.join(command)}")  # Log the command being run
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Thumbnail saved as {output_filename}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error generating thumbnail for {file_name}: {e.stderr.strip()}")
        logging.error(f"Command output: {e.stdout.strip()}")





def generate_thumb(file_name, output_filename, retry_interval=10, max_retries=10):
    retries = 0
    while retries < max_retries:
        if os.path.exists(file_name):
            video_duration = get_video_duration(file_name)
            if video_duration is None:
                logging.error("Could not retrieve video duration.")
                return False
            
            random_time = random.uniform(200, video_duration)
            random_time_str = time.strftime('%H:%M:%S', time.gmtime(random_time))
    
            command = ['ffmpeg', '-ss', random_time_str, '-i', file_name, '-vframes', '1', output_filename]
            try:
                subprocess.run(command, check=True, capture_output=True, text=True)
                logging.info(f"Thumbnail saved as {output_filename} at {random_time_str}")
                return True
            except subprocess.CalledProcessError as e:
                logging.error(f"Error: {e}")
                logging.error(f"Command output: {e.output.decode()}")
                return False
        else:
            logging.info(f"File {file_name} does not exist. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
            retries += 1

    logging.error(f"{max_retries} retries.")
    return False


def print_progress_bar(name, downloaded, total_size, length=20):
    if total_size <= 0:
        total_size = downloaded
    percent = ("{0:.1f}").format(100 * (downloaded / float(total_size)))
    filled_length = int(length * downloaded // total_size)
    bar = '#' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{name} - [{bar}] {percent}%')
    sys.stdout.flush()


def format_bytes(byte_count):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    index = 0
    while byte_count >= 1024 and index < len(suffixes) - 1:
        byte_count /= 1024
        index += 1
    return f"{byte_count:.2f} {suffixes[index]}"

def get_video_duration(file_name):
    command = ['ffmpeg', '-i', file_name, '-hide_banner']
    result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
    duration_line = [x for x in result.stderr.split('\n') if 'Duration' in x]
    if duration_line:
        duration = duration_line[0].split()[1]
        h, m, s = duration.split(':')
        total_seconds = int(h) * 3600 + int(m) * 60 + float(s[:-1])
        return total_seconds
    return None