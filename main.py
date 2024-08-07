import json
import re

def extract_locate(text):
    pattern = r'【(.*?)】'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


def save_text_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def data_formatting(report_data):
    result={}
    for data in report_data:
        date = data["report"]["routine_date"]
        locate = extract_locate(data["report"]["task_name"])
        if date not in result:
            result[date] = [locate]
        else:
            result[date].append(locate)
    return result


if __name__ == "__main__":
    file_name = "upload.txt"
    jso = file_to_json("/workspaces/dev/report.txt")
    result = data_formatting(jso)
    save_text_file(result, file_name)
