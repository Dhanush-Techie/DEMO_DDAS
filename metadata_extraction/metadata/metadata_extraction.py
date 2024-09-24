from PIL import Image
import os

def get_basic_video_attributes(video_path):
    """Extract metadata from video files."""
    media_info = MediaInfo.parse(video_path)
    for track in media_info.tracks:
        if track.track_type == "Video":
            return {
                "Filename": os.path.basename(video_path),
                "Duration (s)": track.duration / 1000 if track.duration else "Unknown",
                "Format": track.format,
                "Codec": track.codec_id if track.codec_id else "Unknown",
                "Bitrate (bps)": track.bit_rate if track.bit_rate else "Unknown",
                "Width": track.width,
                "Height": track.height,
                "Frame Rate": track.frame_rate,
                "Aspect Ratio": track.display_aspect_ratio,
                "Bit Depth": track.bit_depth if track.bit_depth else "Unknown",
                "Compression": track.compression_mode if track.compression_mode else "Unknown",
                "Audio Channels": track.channel_s if track.track_type == "Audio" else "N/A",
                "Sample Rate (Hz)": track.sample_rate if track.track_type == "Audio" else "N/A",
            }
    return None


def get_basic_image_attributes(image_path):
    try:
        with Image.open(image_path) as img:
            attributes = {
                "Filename": os.path.basename(image_path),
                "Filesize": os.path.getsize(image_path),  # File size in bytes
                "Format": img.format
                
                '''optional
                "Size": {"Width":img.size[0],"Height":img.size[1]},  # (width, height)
                "Color Mode": img.mode,  # RGB, CMYK, L (grayscale), etc.
                "Bit Depth": img.bits if hasattr(img, 'bits') else "Unknown",
                "Compression": img.info.get('compression', 'None'),  
                "Resolution": img.info.get('dpi', 'Unknown'), 
                "Info" : img.info
                '''
            }
            return attributes
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def get_file_metadata(file_path):
    file_stat = os.stat(file_path)
    return {
        "Filename": os.path.basename(file_path),
        "Filesize": file_stat.st_size,
        "Format": os.path.splitext(file_path)[1]
        
        '''optional
        "Creation Time": time.ctime(file_stat.st_ctime),
        "Modification Time": time.ctime(file_stat.st_mtime),
        "Access Time": time.ctime(file_stat.st_atime),
        "File Permissions": oct(file_stat.st_mode)[-3:]
        '''
    }


def process_images_in_directory(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_path = os.path.join(root, file)
                attributes = get_basic_image_attributes(image_path)
                if attributes:
                    print(attributes,"\n")

# Specify the directory containing the images
image_directory = 'D:/SIH'  # Replace with your image directory

# Process all images in the directory
process_images_in_directory(image_directory)