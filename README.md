# Day 7 Project

D7 計畫，七天內生出一個酷酷的專案。我想做瀏覽器插件
### why 瀏覽器插件
比一般網頁的方式呈現還要新穎，泛用性更高，使用者不需要開另一個網頁去檢查，打開信箱就可以即時看到風險評估
### 執行
- 建立虛擬環境(第一次執行需要執行，並確保有 virtualenv 套件)
```
virtualenv env01
```
- 在專案跟目錄執行此命令進入虛擬環境
```
.\env01\Scripts\activate
```
- 安裝套件
```
pip install -r requirements.txt
```
- 安裝網頁顯示與LLM互動套件
```
pip install chainlit
pip install -U langchain-chroma
pip install -U langchain-openai
```

- 增加套件
```
pip freeze > requirements.txt
```

- 設定環境變數(.env)



### 參數範例
```json
{
    "data": {
        "status": "valid",
        "result": "deliverable",
        "_deprecation_notice": "Using result is deprecated, use status instead",
        "score": 100,
        "email": "service@ais3.org",
        "regexp": true,
        "gibberish": false,
        "disposable": false,
        "webmail": false,
        "mx_records": true,
        "smtp_server": true,
        "smtp_check": true,
        "accept_all": false,
        "block": false,
        "sources": [
            {
                "domain": "cc.stust.edu.tw",
                "uri": "http://cc.stust.edu.tw/tc/news/119-54390-n",
                "extracted_on": "2018-10-16",
                "last_seen_on": "2024-05-08",
                "still_on_page": true
            },
            {
                "domain": "cc.stust.edu.tw",
                "uri": "http://cc.stust.edu.tw/tc/news/119-56857-n",
                "extracted_on": "2018-12-24",
                "last_seen_on": "2024-05-29",
                "still_on_page": true
            },
            {
                "domain": "news.idea-show.com",
                "uri": "http://news.idea-show.com/post/%e6%95%99%e8%82%b2%e9%83%a8%e3%80%82109%ef%a6%8e%ef%a8%81%e8%b3%87%e5%ae%89%e5%88%9d%e5%ad%b8%e8%80%85%e6%8c%91%e6%88%b0%e6%b4%bb%e5%8b%95-myfirstctf",
                "extracted_on": "2020-07-03",
                "last_seen_on": "2024-05-31",
                "still_on_page": true
            },
            {
                "domain": "mis.stust.edu.tw",
                "uri": "http://mis.stust.edu.tw/tc/news/109-19409",
                "extracted_on": "2021-10-23",
                "last_seen_on": "2024-05-26",
                "still_on_page": true
            },
            {
                "domain": "sysh.tc.edu.tw",
                "uri": "http://sysh.tc.edu.tw/p/406-1064-165015,r2751.php",
                "extracted_on": "2022-05-30",
                "last_seen_on": "2024-05-30",
                "still_on_page": true
            },
            {
                "domain": "sysh.tc.edu.tw",
                "uri": "http://sysh.tc.edu.tw/p/16-1064-165015.php",
                "extracted_on": "2022-05-30",
                "last_seen_on": "2024-05-29",
                "still_on_page": true
            },
            {
                "domain": "tsvs.tc.edu.tw",
                "uri": "http://tsvs.tc.edu.tw/p/406-1083-165005,r1829.php",
                "extracted_on": "2022-06-12",
                "last_seen_on": "2024-05-31",
                "still_on_page": true
            },
            {
                "domain": "lic.tumt.edu.tw",
                "uri": "http://lic.tumt.edu.tw/p/406-1025-39934,r1422.php",
                "extracted_on": "2022-09-26",
                "last_seen_on": "2024-06-27",
                "still_on_page": true
            },
            {
                "domain": "lic.tumt.edu.tw",
                "uri": "http://lic.tumt.edu.tw/p/405-1025-39934,c3769.php",
                "extracted_on": "2022-09-26",
                "last_seen_on": "2024-07-14",
                "still_on_page": true
            },
            {
                "domain": "ais3.org",
                "uri": "http://ais3.org",
                "extracted_on": "2024-06-02",
                "last_seen_on": "2024-06-02",
                "still_on_page": true
            },
            {
                "domain": "ais3.org",
                "uri": "http://ais3.org/2018/accept.html",
                "extracted_on": "2024-05-31",
                "last_seen_on": "2024-06-02",
                "still_on_page": true
            },
            {
                "domain": "ais3.org",
                "uri": "http://ais3.org/home/en_us",
                "extracted_on": "2024-01-28",
                "last_seen_on": "2024-06-02",
                "still_on_page": true
            },
            {
                "domain": "ais3.org",
                "uri": "http://ais3.org/home/others",
                "extracted_on": "2024-01-28",
                "last_seen_on": "2024-06-02",
                "still_on_page": true
            },
            {
                "domain": "ais3.org",
                "uri": "http://ais3.org/account/register",
                "extracted_on": "2023-10-28",
                "last_seen_on": "2024-06-02",
                "still_on_page": true
            },
            {
                "domain": "olis.kmu.edu.tw",
                "uri": "http://olis.kmu.edu.tw/index.php/en-gb/notice/events/3004-myfirstctf2022",
                "extracted_on": "2023-04-07",
                "last_seen_on": "2024-07-10",
                "still_on_page": true
            },
            {
                "domain": "olis.kmu.edu.tw",
                "uri": "http://olis.kmu.edu.tw/index.php/zh-tw/notices/%e6%b4%bb%e5%8b%95%e5%85%ac%e5%91%8a/3004-myfirstctf2022",
                "extracted_on": "2023-04-07",
                "last_seen_on": "2024-07-21",
                "still_on_page": true
            },
            {
                "domain": "olis.kmu.edu.tw",
                "uri": "http://olis.kmu.edu.tw/index.php/zh-tw/notice/events/3004-myfirstctf2022",
                "extracted_on": "2022-10-07",
                "last_seen_on": "2024-07-09",
                "still_on_page": true
            },
            {
                "domain": "lic.tumt.edu.tw",
                "uri": "http://lic.tumt.edu.tw/p/16-1025-39934.php",
                "extracted_on": "2022-09-26",
                "last_seen_on": "2024-07-14",
                "still_on_page": true
            },
            {
                "domain": "tsvs.tc.edu.tw",
                "uri": "http://tsvs.tc.edu.tw/p/16-1083-165005.php",
                "extracted_on": "2022-06-12",
                "last_seen_on": "2024-03-23",
                "still_on_page": false
            },
            {
                "domain": "careercenter.ncu.edu.tw",
                "uri": "http://careercenter.ncu.edu.tw/extra-event/show/56",
                "extracted_on": "2022-07-03",
                "last_seen_on": "2024-02-02",
                "still_on_page": false
            },
            {
                "domain": "careercenter.ncu.edu.tw",
                "uri": "http://careercenter.ncu.edu.tw/extra-event/show/232",
                "extracted_on": "2021-09-17",
                "last_seen_on": "2024-02-01",
                "still_on_page": false
            },
            {
                "domain": "tsvs.tc.edu.tw",
                "uri": "http://tsvs.tc.edu.tw/p/406-1083-72930,r1636.php",
                "extracted_on": "2021-06-08",
                "last_seen_on": "2022-06-11",
                "still_on_page": false
            },
            {
                "domain": "saihs.edu.tw",
                "uri": "http://saihs.edu.tw/node/17514",
                "extracted_on": "2020-07-09",
                "last_seen_on": "2021-07-11",
                "still_on_page": false
            },
            {
                "domain": "saihs.edu.tw",
                "uri": "http://saihs.edu.tw/node/17515",
                "extracted_on": "2020-07-09",
                "last_seen_on": "2021-07-15",
                "still_on_page": false
            },
            {
                "domain": "cyber.ithome.com.tw",
                "uri": "http://cyber.ithome.com.tw/2022/exhibition-page/863",
                "extracted_on": "2022-09-12",
                "last_seen_on": "2023-09-23",
                "still_on_page": false
            },
            {
                "domain": "saihs.edu.tw",
                "uri": "http://saihs.edu.tw/node/17062",
                "extracted_on": "2020-01-07",
                "last_seen_on": "2021-07-09",
                "still_on_page": false
            },
            {
                "domain": "cc.ncku.edu.tw",
                "uri": "http://cc.ncku.edu.tw/p/16-1002-193079.php",
                "extracted_on": "2019-05-30",
                "last_seen_on": "2022-04-13",
                "still_on_page": false
            },
            {
                "domain": "cc.ncku.edu.tw",
                "uri": "http://cc.ncku.edu.tw/p/406-1002-193079,r391.php",
                "extracted_on": "2019-05-30",
                "last_seen_on": "2022-04-12",
                "still_on_page": false
            },
            {
                "domain": "cc.ncku.edu.tw",
                "uri": "http://cc.ncku.edu.tw/p/406-1002-193079,r804.php",
                "extracted_on": "2019-05-30",
                "last_seen_on": "2022-04-09",
                "still_on_page": false
            },
            {
                "domain": "saihs.edu.tw",
                "uri": "http://saihs.edu.tw/node/15578",
                "extracted_on": "2019-03-06",
                "last_seen_on": "2021-07-06",
                "still_on_page": false
            }
        ]
    },
    "meta": {
        "params": {
            "email": "service@ais3.org"
        }
    }
}
```