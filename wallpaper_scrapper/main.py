from bs4 import BeautifulSoup
import requests
import sys
from pathlib import Path


def getImagesSourceByPage(url: str, page: int):
    wallpapersListPage = requests.get(url % (page))
    wallpapersListSoup = BeautifulSoup(
        wallpapersListPage.content, 'html.parser')

    rawDivs = wallpapersListSoup.find('div', class_='wallpapers_container').find_all(
        'div', class_='wall-resp')

    cleanDivs = []
    for rawDiv in rawDivs:
        cleanDivs.append(rawDiv.find_all(
            'img', class_=['thumbnail', 'img-responsive']))

    imagesSrc = []
    for cleanDiv in cleanDivs:
        imagesSrc.append(cleanDiv[0]['src'])

    return imagesSrc


def dowloadImageWithSrc(ImgSrcUrl: str):
    global processedNumber

    if not ImgSrcUrl.find('/'):
        sys.exit('eeae')

    filename = ImgSrcUrl.rsplit('/', 1)[1]
    filenameParts = filename.rsplit('.', 1)
    sizedFilename = filenameParts[0] + '-2560x1440.' + filenameParts[1]

    dlUrl = downloadWallperUrl % sizedFilename

    r = requests.get(dlUrl, allow_redirects=True)

    open(folderName + '/' + filename, 'wb').write(r.content)

    processedNumber += 1

    print('Downloaded %d pictures' % (processedNumber), end="\r")


def main():
    global processedNumber
    processedNumber = 0
    global folderName
    folderName = 'dist/spaceWallpapers'
    global downloadWallperUrl
    downloadWallperUrl = 'https://images.hdqwalls.com/download/%s'

    wallpapersListUrl = 'https://hdqwalls.com/2560x1440/space-wallpapers/page/%d'

    Path(folderName).mkdir(parents=True, exist_ok=True)

    wallpapersListPage = requests.get(wallpapersListUrl % (1))
    wallpapersListSoup = BeautifulSoup(
        wallpapersListPage.content, 'html.parser')

    pagination = wallpapersListSoup.find('ul', class_='pagination')
    max_pages = int(pagination.contents[len(pagination.contents) - 2].string)

    for i in range(max_pages):
        # GET IMAGES SRC
        imagesSrc = getImagesSourceByPage(wallpapersListUrl, i)

        # DOWNLOAD PICTURE
        for imageSrc in imagesSrc:
            dowloadImageWithSrc(imageSrc)


if __name__ == "__main__":
    main()
