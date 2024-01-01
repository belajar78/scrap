import requests

from bs4 import BeautifulSoup

async def getFolderDoodStream(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        data = []
        folderName = soup.find("div" > "h1" , {"class": "font-weight-bold text-center"})
        if (not folderName):
            return False, "Folder Tidak Ditemukan"
        folderName = folderName.text

        videos = soup.find_all("ul" > "li", {"class": "d-flex flex-wrap align-items-center justify-content-between mb-2"})
        if (not videos):
            return False, "Video Tidak Ditemukan"
        
        for video in videos:
            name = video.find("h4")
            if (name):
                name = name.text

            size = video.find("span", {"class": "d-inline-block mr-1"})
            if (size):
                size = size.text.strip()

            duration = video.find("span", {"class": "d-inline-block ml-1 mr-1"})
            if (duration):
                duration = duration.text.strip()

            date = video.find("span", {"class": "d-inline-block ml-1"})
            if (date):
                date = date.text.strip()

            link = video.find("a")
            if (link):
                link = link.get("href")
            
            data.append(
                {
                    "name": name,
                    "size": size,
                    "duration": duration,
                    "date": date,
                    "link": link,
                }
            )
        
        return folderName, data
    except Exception as e:
        print(e)
        return False, "Terjadi kesalahan atau URL tidak valid!"
    
async def getFolderPoopHD(url):
    try:
        baseURL = url.split("/f/")[0]
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers",
            "Referer": baseURL,
            "Origin": baseURL,
        }
        with requests.Session() as session:
            response = session.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        data = []
        folderName = soup.find("h3")
        if (not folderName):
            return False , "Folder Tidak Ditemukan"
        folderName = folderName.text
        
        videos = soup.find_all("div", {"class": "col-sm col-md-6 col-lg-4"})
        if (not videos):
            return False , "Video Tidak Ditemukan"
        
        for video in videos:
            name = video.find("a", {"class": "title_video"})
            link = name.get("href")
            if (name):
                name = name.text
                link = baseURL + link
            
            data.append({
                "name": name,
                "link": link
            })
        return folderName, data
    except Exception as e:
        print(e)
        return False, "Terjadi kesalahan atau URL tidak valid!"
