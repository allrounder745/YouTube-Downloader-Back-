@app.get("/download")
def download(video_url: str = Query(..., alias="url")):
    try:
        # 🧼 Clean URL
        if "youtube.com/shorts/" in video_url:
            video_id = video_url.split("/shorts/")[1].split("?")[0]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
        elif "youtu.be" in video_url:
            video_id = video_url.split("/")[-1].split("?")[0]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
        else:
            video_url = video_url.split("&")[0]

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forcejson': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])

            download_links = [
                {
                    "quality": f.get("format_note"),
                    "ext": f.get("ext"),
                    "url": f.get("url"),
                    "size": f.get("filesize")
                }
                for f in formats if f.get("url")
            ]

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "downloads": download_links
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
