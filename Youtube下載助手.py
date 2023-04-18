import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube, Playlist

#-------------下載function-------------

def download_file(link, resolution, download_type, save_path):
    YT=YouTube(link)
    if download_type == "影片":
        if YT.streams.filter().get_by_resolution(resolution) is None:
            list_box.insert(tk.END, f'{YT.title} 不支援{resolution}!')
            return
        YT.streams.filter().get_by_resolution(resolution).download(output_path=save_path, filename=f'{YT.title}_{resolution}.mp4')
    if download_type == "純聲音":
        YT.streams.filter(type="audio").first().download(output_path=save_path, filename=f'{YT.title}.mp3')
    list_box.insert(tk.END, f'{YT.title} 下載完成!')

def check():
    video_link = link_entry.get()
    download_path = path_entry.get()
    download_type = download_type_menu.get()
    resolution = resolution_menu.get()
    if video_link == "":
        messagebox.showwarning('錯誤','請輸入下載連結')
        return
    if download_path == "":
        messagebox.showwarning('錯誤','請選擇下載路徑')
        return
    if download_type == "":
        messagebox.showwarning('錯誤','請輸入下載形式')
        return
    if resolution == "" and download_type != "純聲音":
        messagebox.showwarning('錯誤','請選擇解析度')
        return
    try:
        if "list=" in video_link and "watch?" not in video_link:
            YT=Playlist(video_link)
            for video in YT.video_urls:
                list_box.insert(tk.END,f'{YouTube(video).title} 開始下載...')
                threading.Thread(target=download_file,args=(video, resolution, download_type, download_path)).start()
        else:
            YT=YouTube(video_link)
            list_box.insert(tk.END,f'{YT.title} 開始下載...')
            threading.Thread(target=download_file,args=(video_link, resolution, download_type, download_path)).start()
    #顯示錯誤訊息
    except Exception as error_message:
        messagebox.showwarning("錯誤",str(error_message))
        link_entry.delete(0, tk.END)

#-------------介面設置-------------

#主視窗設定
window = tk.Tk()                                                      #建立主視窗
window.title('Youtube下載助手')                                        #標題
window.iconbitmap('youtube.ico')                                      #icon
window.geometry('640x480')                                            #主視窗尺寸
window.resizable(False,False)                                         #限制不可縮放

#提示"本助手可下載Youtube影片或音樂"
hint = tk.Label(window, text='本助手可下載Youtube影片或音樂，歡迎多加利用。', fg='red', font=('微軟正黑體',16))
hint.place(relx=0.12, rely=0)

#提示"請輸入影片或播放清單連結"
link_label = tk.Label(window, text='請輸入影片或播放清單連結', fg='#F3844D', font=('微軟正黑體',12))
link_label.place(relx=0.01, rely=0.06)

#網址輸入框
link_entry = tk.Entry(window, width=50)
link_entry.place(relx=0.32, rely=0.068)

#下載按鈕
download_button = tk.Button(window, text="下載", command=check, fg='black', bg='#9591DA')
download_button.place(relx=0.88, rely=0.06)

#提示"請選擇下載路徑"
path_label = tk.Label(window, text='請選擇下載路徑', fg='#F3844D', font=('微軟正黑體',12))
path_label.place(relx=0.01, rely=0.13)

#下載路徑輸入框與按鈕
path_entry = tk.Entry(window, width=50)
path_entry.place(relx=0.32, rely=0.138)
def path_select():
    path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)
path_change = tk.Button(window, text='選擇路徑', command=path_select, fg='black', bg='#9591DA')
path_change.place(relx=0.88, rely=0.13)

#下載形式
download_type_label = tk.Label(window, text="下載形式", fg='#F3844D', font=('微軟正黑體',12))
download_type_label.place(relx=0.01, rely=0.2)
download_types = ["影片", "純聲音"]
download_type_menu = ttk.Combobox(window, values=download_types, state='readonly', width=30)
download_type_menu.place(relx=0.135, rely=0.208)

#解析度選擇
resolution_label = tk.Label(window, text="解析度", fg='#F3844D', font=('微軟正黑體',12))
resolution_label.place(relx=0.51, rely=0.2)
resolutions = ["720p", "480p", "360p", "240p", "144p"]
resolution_menu = ttk.Combobox(window, values=resolutions, state='readonly', width=30)
resolution_menu.place(relx=0.6, rely=0.208)

#下載清單
list_box = tk.Listbox(window, width=88, height=20)
list_box.place(relx=0.01, rely=0.3)

#下載清單捲軸
list_bary = tk.Scrollbar(list_box)
list_barx = tk.Scrollbar(list_box, orient='horizontal')
list_bary.place(relx=0.98, rely=0, relheight=0.95)
list_barx.place(relx=0, rely=0.95, relwidth=1)

#連結清單和卷軸
list_box.config(yscrollcommand=list_bary.set, xscrollcommand=list_barx.set)
list_bary.config(command=list_box.yview)
list_barx.config(command=list_box.xview)

#執行
window.mainloop()
