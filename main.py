
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock, mainthread
import datetime
import threading
import urllib.request
import xml.etree.ElementTree as ET
import webbrowser
import random

# ফন্টের নাম (যা তোমার ফোল্ডারে আছে)
FONT_NAME = 'Li Sabbir Sorolota Unicode'

class NewTipsApp(App):
    def build(self):
        self.is_running = False
        self.current_link = "https://news.google.com/search?q=zero+investment+online+work"
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        self.title_label = Label(
            text="New Tips (Real-Time Zero-Investment Agent)", 
            font_size='20sp',
            size_hint=(1, 0.15)
        )
        
        self.status_label = Label(
            text="Status: Agent is stopped", 
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        
        self.news_label = Label(
            text="[ ডায়নামিক এজেন্ট প্রস্তুত ]\n'Start Agent' এ ক্লিক করুন। প্রতি ১ মিনিট পর পর নতুন এবং চলমান অফারগুলো লাইভ ফেচ করা হবে।", 
            font_name=FONT_NAME,
            font_size='16sp',
            halign='center',
            valign='middle'
        )
        self.news_label.bind(size=self.news_label.setter('text_size'))
        
        self.link_btn = Button(
            text="🌐 View Full Offer in Browser",
            font_size='16sp',
            size_hint=(1, 0.15),
            background_color=(0.2, 0.5, 0.8, 1)
        )
        self.link_btn.bind(on_press=self.open_browser_link)
        
        self.toggle_btn = Button(
            text="Start Agent", 
            font_size='18sp',
            size_hint=(1, 0.15),
            background_color=(0.1, 0.6, 0.3, 1)
        )
        self.toggle_btn.bind(on_press=self.toggle_agent)
        
        layout.add_widget(self.title_label)
        layout.add_widget(self.status_label)
        layout.add_widget(self.news_label)
        layout.add_widget(self.link_btn)
        layout.add_widget(self.toggle_btn)
        
        return layout

    def toggle_agent(self, instance):
        if not self.is_running:
            self.is_running = True
            self.status_label.text = "Status: Dynamic Live Agent Running (1 Min)"
            self.toggle_btn.text = "Stop Agent"
            self.toggle_btn.background_color = (0.8, 0.2, 0.2, 1)
            
            self.trigger_fetch()
            self.timer_event = Clock.schedule_interval(lambda dt: self.trigger_fetch(), 60)
        else:
            self.stop_agent()

    def trigger_fetch(self):
        if self.is_running:
            threading.Thread(target=self.fetch_live_data_backend, daemon=True).start()

    def fetch_live_data_backend(self):
        try:
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            
            # ক্যাশ এড়ানোর জন্য বিভিন্ন রানিং অফারের কিওয়ার্ড রোটেট করা হলো
            queries = [
                "active+zero+investment+online+earn",
                "ongoing+microtasks+remote+work+no+investment",
                "freelance+gigs+earn+money+online+active",
                "new+online+earning+platforms+no-skill"
            ]
            selected_query = random.choice(queries)
            
            # র্যান্ডম ক্যাশ-বাস্টার প্যারামিটার যোগ করা হলো যাতে প্রতিবার নতুন ডাটা আসে
            cache_buster = random.randint(1000, 99999)
            url = f"https://news.google.com/rss/search?q={selected_query}&hl=en-US&gl=US&ceid=US:en&cb={cache_buster}"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=15) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                items = root.findall('.//item')
                if items:
                    # রেন্ডমলি যেকোনো একটি লেটেস্ট আইটেম পিক করা হবে যাতে প্রতি মিনিটে নতুন আপডেট দেখায়
                    random_item = random.choice(items[:5]) if len(items) >= 5 else items[0]
                    title = random_item.find('title').text if random_item.find('title') is not None else "চলমান অফার পাওয়া গেছে"
                    link = random_item.find('link').text if random_item.find('link') is not None else url
                    
                    self.current_link = link
                    
                    live_text = (
                        f"🟢 লাইভ রিয়েল-টাইম আপডেট [{current_time}]:\n"
                        f"📌 অফার: {title}\n\n"
                        f"✅ স্ট্যাটাস: চলমান ও সচল অফার। ব্রাউজারে ভিজিট করতে নিচের বাটনে ক্লিক করুন।"
                    )
                else:
                    live_text = f"🌐 স্ক্যান সম্পন্ন [{current_time}]: নতুন অফার খোঁজা হচ্ছে। পরবর্তী চেক ১ মিনিট পর।"

            self.update_news_ui(live_text)
        except Exception as e:
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            fallback_text = (
                f"📡 নেটওয়ার্ক স্ক্যান রানিং [{current_time}]:\n"
                f"সচল জিরো-ইনভেস্টমেন্ট অফারগুলোর জন্য পুনরায় ট্রাই করা হচ্ছে..."
            )
            self.update_news_ui(fallback_text)

    @mainthread
    def update_news_ui(self, text):
        if self.is_running:
            self.news_label.text = text

    def open_browser_link(self, instance):
        try:
            webbrowser.open(self.current_link)
        except Exception as e:
            print(f"Browser error: {e}")

    def stop_agent(self):
        self.is_running = False
        self.status_label.text = "Status: Agent is stopped"
        self.toggle_btn.text = "Start Agent"
        self.toggle_btn.background_color = (0.1, 0.6, 0.3, 1)
        self.news_label.text = "এজেন্ট সফলভাবে বন্ধ করা হয়েছে।"
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()

if __name__ == '__main__':
    NewTipsApp().run()
