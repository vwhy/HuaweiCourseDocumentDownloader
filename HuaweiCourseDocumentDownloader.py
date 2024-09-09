import datetime
import io
import os
import requests
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

''' 课件页面控制台执行以下代码：
var documentParams = new URLSearchParams(document.querySelector("#edmPage").src);
console.info('projectId: ', documentParams.get("appid"));
console.info('documentId: ', documentParams.get("docId"));
console.info('authorizationToken: ', documentParams.get("authToken"));
copy(`projectId = '${documentParams.get("appid")}'
documentId = '${documentParams.get("docId")}'
authorizationToken = '${documentParams.get("authToken")}'`);
console.info('----- Copied to clipboard! -----');
'''

#替换这里
projectId = '881715bf5fd14684a8e95f6a904f8...'
documentId = 'M1T9A107N1038113890187407...'
authorizationToken = 'security:...'
#替换这里

savePath = './课件/'

requestHeaders = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'EDM-Authorization': authorizationToken,
    'Pragma': 'no-cache',
    'Referer': 'https://cn.elearning.huawei.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0',
}

requestParams = {
    'docVersion': 'V1',
    'wmType': '',
    'renderDocType': '',
    'docFormat': '',
    'X-HW-ID': '',
    'X-HW-APPKEY': '',
}

def getDocumentParameters():
    url = f'https://cn.elearning.huawei.com/edm/projects/{projectId}/previewer/documents/{documentId}'
    response = requests.get(url, params=requestParams, headers=requestHeaders)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('getDocumentParameters failed: ' + response.text)

def getDocumentSpecifiedPage(pageNum, totalPage):
    url = f'https://cn.elearning.huawei.com/edm/projects/{projectId}/previewer/documents/{documentId}'
    
    dataToPost = {
        'docFormat': 'src',
        'docId': documentId,
        'docVersion': 'V1',
        'documentIndex': 1,
        'pageNum': pageNum,
        'type': 'doc',
        'totalPage': totalPage,
    }

    response = requests.post(url, params=requestParams, headers=requestHeaders, json=dataToPost)
    if response.status_code == 200:
        return response
    else:
        raise Exception(f'getDocumentSpecifiedPage failed for page {pageNum}: ' + response.text)

def convertPngToPdf(image_list, outputPdfFileName):
    if image_list:
        image_list[0].save(outputPdfFileName, save_all=True, append_images=image_list[1:])
    return outputPdfFileName

def process_page(currentPage, totalPage):
    try:
        pageResponse = getDocumentSpecifiedPage(currentPage, totalPage)
        suffixType = pageResponse.headers['Content-Disposition'].split('.')[-1]
        if suffixType == 'png':
            img = Image.open(io.BytesIO(pageResponse.content))
            if img.mode == "RGBA":
                img = img.convert("RGB") 
            return (currentPage, img)
        else:
            raise Exception(f'Unknown suffix type: {suffixType}')
    except Exception as e:
        print(f"Failed to process page {currentPage}: {e}")
        return None

if __name__ == '__main__':
    print('-------------- Download Started --------------')
    print('Project ID: ' + projectId)
    print('Document ID: ' + documentId)

    try:
        docParams = getDocumentParameters()
        totalPage = docParams['totalPage']
        print(f'totalPage: {totalPage}')

        containerDir = savePath + documentId + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '/'
        if not os.path.exists(containerDir):
            os.makedirs(containerDir)
        print('The document files will be saved to: ' + containerDir)

        pdfFileList = []
        image_list = []

        # 使用线程池并发下载页面
        with ThreadPoolExecutor(max_workers=50) as executor:  # 调整并发线程数
            futures = {executor.submit(process_page, page, totalPage): page for page in range(1, totalPage + 1)}
            for future in as_completed(futures):
                page = futures[future]
                try:
                    result = future.result()
                    if result: 
                        image_list.append(result)
                    print(f'Page {page} processed successfully.')
                except Exception as e:
                    print(f'Page {page} generated an exception: {e}')
        
        image_list.sort(key=lambda x: x[0])
        image_list = [img for _, img in image_list]

        if image_list:
            pngPdfFileName = containerDir + documentId + '_png.pdf'
            print(f'Converting PNGs to PDF: {pngPdfFileName}')
            convertPngToPdf(image_list, pngPdfFileName)
            pdfFileList.append(pngPdfFileName)

        print('-------------- Download Finished --------------')

    except Exception as e:
        print('-------------- Download Failed --------------')
        print(type(e))
        print(e)
