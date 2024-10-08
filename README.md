# HuaweiCourseDocumentDownloader
Dump document from `cn.elearning.huawei.com` 

### 1.更新适配最新华为培训
### 2.合并生成pdf文件

## Installation
```bash
git clone https://github.com/penguin806/HuaweiCourseDocumentDownloader.git
pip install requests svglib PyPDF2
```

## Getting Started
1. Login to `learning.huaweils.com`, navigate to the course  page you want to download, and press `F12` to open DevTools.
    ![GettingStarted1.png](img/GettingStarted1.png)
2. Switch to `Console` tab.
3. Paste the following code into the console and press `Enter`:
    ```javascript
    var documentParams = new URLSearchParams(document.querySelector("#edmPage").src);
    console.info('projectId: ', documentParams.get("appid"));
    console.info('documentId: ', documentParams.get("docId"));
    console.info('authorizationToken: ', documentParams.get("authToken"));
    copy(`projectId = '${documentParams.get("appid")}'
    documentId = '${documentParams.get("docId")}'
    authorizationToken = '${documentParams.get("authToken")}'
    savePath = './snow_downloads/'`);
    console.info('----- Copied to clipboard! Now you can paste it into HuaweiCourseDocumentDownloader.py -----');
    ```
4. This will print out the `projectId`, `documentId` and `authorizationToken` of the document you'd like to download. And it will also copy the necessary code to your clipboard.
    ![GettingStarted2.png](img/GettingStarted2.png)
5. Paste the code into `HuaweiCourseDocumentDownloader.py` and replace the corresponding variables **(Line 16 ~ 19)**.
    ![GettingStarted3.png](img/GettingStarted3.png)
6. Run `HuaweiCourseDocumentDownloader.py`, wait for the download to finish.
    ![GettingStarted4.png](img/GettingStarted4.png)
7. The downloaded files will be saved in the directory you specified in `savePath` variable.

## Helpful Projects Made by Other People or Companies
- [https://tools.pdf24.org/en/merge-pdf](https://tools.pdf24.org/en/merge-pdf) - Combine multiple files into a single PDF.
