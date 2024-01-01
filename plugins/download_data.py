import requests
import shutil
import time, math, os

from bs4 import BeautifulSoup

async def getDetailsDoodStreamDownload(url):
    try:
        session = requests.Session()
        url = url.replace('/e/', '/d/')
        baseURL = url.split("/d/")[0]

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        soup = BeautifulSoup(response.text, "html.parser")
        
        urlThumb = soup.find("iframe")
        if (urlThumb):
            urlThumbCek = urlThumb.get("src").startswith("https://") or urlThumb.get("src").startswith("http://")
            urlThumb = urlThumb.get("src")
            urlThumb = urlThumb if urlThumbCek else baseURL + urlThumb
            urlThumb = await getThumb(urlThumb)

        
        info = soup.find("div", {"class": "info"})
        
        if not info:
            return False, "Video Tidak Ditemukan"

        name = info.find("h4")
        if name:
            name = name.text.strip()

        duration = info.find("div", class_="length")
        if duration:
            duration = duration.text.strip()

        size = info.find("div", class_="size")
        if size:
            size = size.text.strip()

        date = info.find("div", class_="uploadate")
        if date:
            date = date.text.strip()

        downloadLink = soup.find("div", {"class": "download-content"})
        if not downloadLink:
            return False, "Button download tidak ditemukan."

        downloadLink = downloadLink.find("a")
        if not downloadLink:
            return False, "URL tersebut tidak mengizinkan untuk didownload"
        downloadLink = downloadLink.get("href")

        # downloads(url.split("/d/")[0] + downloadLink, session)
        data = {
            "name": name,
            "duration": duration,
            "size": size,
            "date": date,
            "thumb": urlThumb,
            "url": baseURL + downloadLink,
            "session": session
        }

        return True, data
    except Exception as e:
        print(e)
        return False, "Terjadi kesalahan atau URL tidak valid!"

async def getThumb(url):
    try:

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        urlThumb = soup.find('video', {"class": "video-js vjs-big-play-centered"})
        if (urlThumb):
            urlThumb = urlThumb.get("poster")
        
        response = requests.get(urlThumb, headers={"User-Agent": "Mozilla/5.0"})
        nama_folder = 'img'
        if not os.path.exists(nama_folder):
            os.mkdir(nama_folder)
            
        urlThumb = f"{nama_folder}/thumb_{str(time.time()).replace('.', '_')}.jpg"
        with open(urlThumb, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
            # shutil.copyfileobj(response.raw, file)

        return urlThumb
    except Exception as e:
        return None

async def downloads(message, url, session, name_file, text_progress):
    nama_folder = 'videos'
    try:
        response = session.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        link = soup.find('a', {"class": "btn btn-primary d-flex align-items-center justify-content-between"})
        
        if (not link):
            return False, "Video Tidak Ditemukan, coba kembali."
        link = link.get('href')

        response = session.get(link, headers={"User-Agent": "Mozilla/5.0", "Referer": url.split('/download')[0]}, stream=True)
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            chunk_size = 1024

            start_time = time.time()
            a = 0
            if not os.path.exists(nama_folder):
                os.mkdir(nama_folder)
            name_file = f"{nama_folder}/{name_file}"
            with open(name_file, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    await progress_for_pyrogram(a+len(data), total_size, text_progress, message, start_time)
                    a += len(data)
            
            data = {
                "url": "",
                "namefile": name_file
            }
            return True, data
        else:
            return False, f"Error {response.status_code}: Gagal mengunduh video."
    except:
        name_file = f"{nama_folder}/{name_file}"
        if os.path.exists(name_file):
            os.remove(name_file)
        return False, "Terjadi kesalahan atau URL tidak valid!"

async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        
        percentage = round(percentage, 2)

        progress = f"[ {percentage:.2f}% ]"

        tmp = f"<b>{humanbytes(current)} of {humanbytes(total)} {progress}</b>\nSpeed: {humanbytes(speed)}/s\nETA: {estimated_total_time if estimated_total_time != '' else '0 s'}\n"
        
        try:
            await message.edit(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

async def convert_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    total_seconds = minutes * 60 + seconds
    return total_seconds