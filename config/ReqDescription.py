class RequestDescription:
    def _url(self, tail = None):
        return "https://lihkg.com/api_v2/thread" + tail
    
    def _headers(self, referer = None):
        return {
            "Accept": "application/json, text/plain, */*",
            "x-li-device": "c96ccbfcd0a9cd4f6a1f5456b9a2bc3a396fe6b9",
            "x-li-deivce-type": "browser",
            "x-li-load-time": "4.367764",
            "Referer": referer
        }

    def generate(self, type, page, thread_id = -1):
        """
        type: category or thread
        """
        if type == "category":
            url = self._url(tail = f"/category?cat_id=15&page={page}&count=60&type=now")
            headers = self._headers(referer = "https://lihkg.com/category/15")

        else:
            url = self._url(tail = f"/{thread_id}/page/{page}")
            headers = self._headers(referer = f"https://lihkg.com/thread/{thread_id}/page/{page}")

        return url, headers

RD = RequestDescription()