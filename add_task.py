import PySimpleGUI as sg
import win32com.client
import datetime

def create_scheduled_task(task_name, trigger_time, action, arguments=""):
    """
    Windowsのタスクスケジューラーにタスクを登録する関数。

    Parameters:
    - task_name: タスクの名前 (str)
    - trigger_time: タスクの実行時間 (datetime.datetime)
    - action: 実行するプログラムのパス (str)
    - arguments: プログラムに渡す引数 (str, optional)
    """
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    root_folder = scheduler.GetFolder("\\")
    task_def = scheduler.NewTask(0)

    trigger = task_def.Triggers.Create(1)  # 1 = Time Trigger
    trigger.StartBoundary = trigger_time.isoformat()

    action_def = task_def.Actions.Create(0)  # 0 = Execute
    action_def.Path = action
    action_def.Arguments = arguments

    task_def.RegistrationInfo.Description = "My Scheduled Task"
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False

    root_folder.RegisterTaskDefinition(
        task_name,
        task_def,
        6,  # 6 = Task Create, or update if exists
        None,
        None,
        3,  # 3 = Logon interactively
    )

def main():
    # PySimpleGUIで入力画面を作成
    layout = [
        [sg.Text('タスクの時間 (HH:MM):'), sg.InputText(key='-TIME-', size=(10, 1))],
        [sg.Text('URL:'), sg.InputText(key='-URL-', size=(50, 1))],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('タスクスケジューラー設定', layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Cancel'):
            break
        if event == 'Submit':
            time_str = values['-TIME-']
            url = values['-URL-']

            # 入力された時間をパース
            try:
                task_time = datetime.datetime.strptime(time_str, "%H:%M").replace(
                    year=datetime.datetime.now().year,
                    month=datetime.datetime.now().month,
                    day=datetime.datetime.now().day
                )
                
                # 実行時間をUTCに変換
                task_time_utc = task_time - datetime.timedelta(hours=datetime.datetime.now().astimezone().utcoffset().total_seconds() / 3600)

                # タスクを作成
                create_scheduled_task(
                    task_name="OpenURLTask",
                    trigger_time=task_time_utc,
                    action="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                    arguments=url
                )
                
                sg.popup('タスクが正常に登録されました。')
            except ValueError:
                sg.popup('時間の形式が正しくありません。HH:MM形式で入力してください。')

    window.close()

if __name__ == "__main__":
    main()
