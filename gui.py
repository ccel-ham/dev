import customtkinter as ctk
import PySimpleGUI as sg
import win32com.client
import datetime

class GUI_ctk(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Task Scheduler")
        self.geometry("400x250")

        ctk.CTkLabel(self, text="Enter Task Details", font=("Helvetica", 16)).pack(pady=20)

        self.time_entry = ctk.CTkEntry(self, placeholder_text="Time (HH:MM)")
        self.time_entry.pack(pady=10)

        self.url_entry = ctk.CTkEntry(self, placeholder_text="URL")
        self.url_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text="Create Task", command=self.create_task)
        self.submit_button.pack(pady=20)

    def create_task(self):
        task_time = self.time_entry.get()
        url = self.url_entry.get()

        try:
            task_datetime = datetime.datetime.combine(
                datetime.date.today(),
                datetime.datetime.strptime(task_time, '%H:%M').time()
            )

            task_name = "OpenURLTask"
            browser_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

            create_scheduled_task(
                task_name=task_name,
                trigger_time=task_datetime,
                action=browser_path,
                arguments=url
            )

            ctk.CTkLabel(self, text="Task Created Successfully!", text_color="green").pack(pady=10)
        except Exception as e:
            ctk.CTkLabel(self, text=f"Error: {str(e)}", text_color="red").pack(pady=10)


class GUI_simple:
    def __init__(self):
        self.layout = [
            [sg.Text('タスクの時間 (HH:MM):'), sg.InputText(key='-TIME-', size=(10, 1))],
            [sg.Text('URL:'), sg.InputText(key='-URL-', size=(50, 1))],
            [sg.Submit(), sg.Cancel()]
        ]
        self.window = sg.Window('タスクスケジューラー設定', self.layout)

    def read_input(self):
        while True:
            event, values = self.window.read()
            if event in (sg.WINDOW_CLOSED, 'Cancel'):
                break
            if event == 'Submit':
                time_str = values['-TIME-']
                url = values['-URL-']
                return time_str, url
        self.window.close()
        return None, None
    
def ctk_main():
    app = GUI_ctk()
    app.mainloop()

def simple_main():
    gui = GUI_simple()
    time_str, url = gui.read_input()

    if time_str and url:
        task_scheduler = TaskScheduler(time_str, url)
        task_scheduler.schedule_task()


if __name__ == "__main__":
    pass