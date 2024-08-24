import customtkinter as ctk
from googleapiclient.discovery import build
import os
from tkinter import filedialog

API_KEY = "AIzaSyBFw8ofrocPB-CZrI04o08e3MGGtwLASmY"
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_video_tags(video_id):
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    tags = response["items"][0]["snippet"].get("tags", [])
    return tags

def search_videos_by_keyword(keyword):
    request = youtube.search().list(
        q=keyword,
        part="id",
        type="video",
        maxResults=10
    )
    response = request.execute()
    video_ids = [item["id"]["videoId"] for item in response["items"]]
    return video_ids

def get_tags_by_keyword(keyword):
    video_ids = search_videos_by_keyword(keyword)
    all_tags = []
    for video_id in video_ids:
        tags = get_video_tags(video_id)
        all_tags.extend(tags)
    unique_tags = list(set(all_tags))
    return unique_tags

def save_tags_to_file(tags, folder_path):
    file_name = "etiketler.txt"
    full_path = os.path.join(folder_path, file_name)
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(tags))

def show_and_save_tags():
    keyword = entry.get()
    folder_path = filedialog.askdirectory()
    if not folder_path:
        result_label.configure(text="Klasör seçilmedi.")
        return
    tags = get_tags_by_keyword(keyword)
    if tags:
        save_tags_to_file(tags, folder_path)
        result_label.configure(text=f"Etiketler bulundu ve '{folder_path}/etiketler.txt' dosyasına kaydedildi.")
    else:
        result_label.configure(text="Etiket bulunamadı")

app = ctk.CTk()
app.geometry("600x500")
app.title("YTSeo @Ogehan")
app.configure(fg_color="#000000")
app.attributes("-alpha", 0.9)


title_label = ctk.CTkLabel(app, text="YTSeo ", text_color="green", font=("Helvetica", 24))
title_label.pack(pady=20)

entry = ctk.CTkEntry(app, placeholder_text="Anahtar kelime girin örnek (hack,tht)", width=300)
entry.pack(pady=10)

search_button = ctk.CTkButton(app, text="Bul ve etiketleri Kaydet", command=show_and_save_tags, text_color="white", fg_color="green")
search_button.pack(pady=10)

result_label = ctk.CTkLabel(app, text="", text_color="white", justify="left")
result_label.pack(pady=20)

app.mainloop()
