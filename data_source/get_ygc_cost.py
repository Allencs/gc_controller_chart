import json
import re
from typing import List, Dict

import requests


def add_end_lf(string):
    return string + "\n"


class YGCDataCollector:

    def __init__(self):
        self.pageIndex = 1
        self.pageSize = 50
        self.totalCount = 2639
        # self.str_regx = "\[Times:\s+user=(.*?)\s+sys=(.*?),\s+real=(.*?)\s+secs\]"
        self.str_regx = "\[Parallel\s+Time:\s+(.+?)\s+ms,\s+GC\s+Workers:\s+\d+]"
        self.logUrl = "https://hlog-portal.hellobike.cn/api/gc/search"
        self.token = "bearer_e0fdfb16-a7c3-48d9-83ca-32e8563b9e81"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Content-Type": "application/json; charset=UTF-8", "token": self.token}
        self.play_load = {"machines": ["appphhitchcoreservice-pro-group1-77m2x"], "appId": "AppPHHitchCoreService",
                          "startTime": "2024-12-25 10:11:11.000", "endTime": "2024-12-26 10:11:11.000",
                          "timeType": "recently", "timeRegion": 86400000, "logType": "gc", "radio": "desc",
                          "content": "\"G1 Evacuation Pause\" AND \"young\"", "pageIndex": 1, "pageSize": self.pageSize}

    def get_ygc_log(self, request_body) -> List[Dict]:
        print("当前页-> " + str(request_body["pageIndex"]))
        response = requests.get(self.logUrl, headers=self.headers, data=json.dumps(request_body))
        try:
            logs = response.json()["data"]["logs"]
            self.totalCount = int(response.json()["data"]["page"]["totalCount"])
            return logs
        except Exception as e:
            print(response.text + "\n" + e.__str__())

    def get_ygc_cost(self, logs: List[Dict]) -> List[str]:
        costList = []
        for item in logs:
            content = item["content"]
            try:
                cost = re.search(self.str_regx, content).group(1)
                costList.append(cost)
            except Exception as e:
                print(item.__str__() + e.__str__())
        return costList

    def save_ygc_cost(self, costs: List[str]):
        costList = map(add_end_lf, costs)
        with open("ygc_cost.csv", "a+", encoding="utf-8") as f:
            f.writelines(costList)

    def main(self):
        for page_index in range(1, int(self.totalCount / self.pageIndex) + 1):
            self.play_load["pageIndex"] = page_index
            logs = self.get_ygc_log(self.play_load)
            costList = self.get_ygc_cost(logs)
            self.save_ygc_cost(costList)


if __name__ == "__main__":
    # strs = ["1.23", "423", "231.43", "343.3"]
    collector = YGCDataCollector()
    collector.main()
    # collector.save_ygc_cost(strs)
    # logs = collector.get_ygc_log()
    # collector.get_ygc_cost(logs)
