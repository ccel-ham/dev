import re
import json

class DataFormatter:
    def __init__(self) -> None:
        pass

    def extract_locate(self, text):
        pattern = r'【(.*?)】'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None


    def data_formatting(self, report_data):
        result={}
        for data in report_data:
            date = data["report"]["routine_date"]
            locate = self.extract_locate(data["report"]["task_name"])
            if date not in result:
                result[date] = [locate]
            else:
                result[date].append(locate)
        return json.dumps(result)


if __name__ == "__main__":
    pass
