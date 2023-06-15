import tkinter as tk
from tkinter import messagebox
import requests
import time
import sys
import schedule
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup

NEWS_SITE1 = "https://www.philenews.com/"
NEWS_SITE2 = "https://www.sigmalive.com/"

dateTimeNow = datetime.now()


def printTimeDate():
    print("Time: " + dateTimeNow.strftime("%H:%M:%S"))
    print("Date: " + dateTimeNow.strftime("%d:%b:%Y"))


class News:
    def __init__(self, site):
        self.site = site
        self.response = None
        self.html = None
        self.soup = None
        self.titles = []

    def get_titles(self):
        self.response = requests.get(self.site)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.titles = self.soup.find_all(class_="card-wrapper")
        return self.titles

    def prepare_titles_for_gui(self):
        cards = self.get_titles()
        counter = 0
        master_list = []
        for single_card in cards:
            if counter > 50:
                break

            card = single_card.find_all("h3")
            a_tag = single_card.find_all("a")
            href = a_tag[0].get("href")

            if href.find(self.site) != -1:
                temp_dict = {}
                temp_dict["title_id"] = counter
                temp_dict["title_text"] = card[0].text.strip()
                temp_dict["title_url"] = href
                master_list.append(temp_dict)
            counter += 1
        return master_list


class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.news = News(NEWS_SITE1)

        self.setup_menu()
        self.setup_window()
        self.load_news()
        self.setup_refresh_button()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def setup_menu(self):
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.on_closing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Force Close", command=exit)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Settings", command=self.show_settings)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.show_about)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.editmenu, label="Edit")
        self.menubar.add_cascade(menu=self.helpmenu, label="Help")
        self.root.config(menu=self.menubar)

    def setup_window(self):
        self.root.geometry("500x900")
        self.root.title("List the News")

        self.label = tk.Label(self.root, text="List News", font=("Arial", 18))
        self.label.pack(padx=20, pady=20)

        self.label2 = tk.Label(self.root, text="Listing...", font=("Arial", 18))
        self.label2.pack(padx=20, pady=20)

    def load_news(self):
        news_list = self.news.prepare_titles_for_gui()
        label_widgets = []
        for item in news_list:
            title = item["title_text"]
            url = item["title_url"]
            self.label3 = tk.Label(self.root, text=title, fg="blue", cursor="hand2")
            self.label3.pack(anchor="w")
            self.label3.bind("<Button-1>", lambda event, url=url: self.open_link(url))

            label_widgets.append(self.label3)

    def setup_refresh_button(self):
        self.button = tk.Button(
            self.root, text="Refresh", font=("Arial", 12), command=self.refresh
        )
        self.button.pack(padx=10, pady=10)

    def refresh(self):
        print("refresh")
        if self.label2.cget("text") == "Listing...":
            print("must enter news")
            new_content = "content"
            self.label2.config(text=new_content)
        else:
            print("refresh news listing")

    def open_link(self, url):
        webbrowser.open(url)

    def show_settings(self):
        messagebox.showinfo(title="Settings", message="Setting window")

    def show_about(self):
        messagebox.showinfo(title="About", message="About window")

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()


MyGUI()
