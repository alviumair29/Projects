#Imports
import requests
from plyer import notification
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

##Notes from November 21, 2023
# Got the news categories to work **GOTTA FIX THE LANGUAGE ISSUE
# Try the Weather API key again **Should work
##To-Do
#Make it more visually apealing
#Add Images


class NewsApp:
    def __init__(self, master):
        self.master = master
        self.master.title("News Notifier")
        
        self.news_articles = self.get_top_news()
        self.current_index = 0
        
        # Check if news_articles is not empty before setting variables
        if self.news_articles:
            self.title_var = tk.StringVar()
            self.title_var.set(self.news_articles[self.current_index]['title'])
        
            self.description_var = tk.StringVar()
            self.description_var.set(self.news_articles[self.current_index]['description'])
        else:
            # Handle the case when there are no news articles
            self.title_var = tk.StringVar(value="News Board")
            self.description_var = tk.StringVar(value="Cycle through the categories below to view news")
        
        self.create_widgets()

    
    def get_top_news(self, category = "general"):
        #BBC News API
        apiURL = "https://newsapi.org/v2/top-headlines"
        apiKey = "b5f644a56c824a2099ade16ee54698d9"

        #Parameters for API request
        param = {
            #'sources': 'bbc-news',
            'category' : category,
            'language' : 'en',
            'apiKey': apiKey
        }

        #Make API request
        response = requests.get(apiURL, params=param)
        data = response.json()

        #Extract news articles
        newsArticles = data.get('articles', [])

        # Print the raw API response for debugging
        print("Raw API Response:", data)
   
        return newsArticles

    def show_next_article(self):
        if self.current_index < len(self.news_articles) - 1:
            self.current_index += 1
            self.title_var.set(self.news_articles[self.current_index]['title'])
            self.description_var.set(self.news_articles[self.current_index]['description'])
        else:
            messagebox.showinfo("End of Articles", "No more articles available.")

    def create_widgets(self):
        title_label = tk.Label(self.master, textvariable=self.title_var, font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        description_label = tk.Label(self.master, textvariable=self.description_var, wraplength=400)
        description_label.pack(pady=20)

        next_button = tk.Button(self.master, text="Next", command=self.show_next_article)
        next_button.pack(pady=10)

        # Add a dropdown menu for news categories
        categories_label = tk.Label(self.master, text="Select News Category:")
        categories_label.pack(pady=5)

        # News categories dropdown
        categories = ["general", "business", "technology", "entertainment", "health", "science", "sports"]
        self.selected_category = tk.StringVar()
        category_dropdown = ttk.Combobox(self.master, textvariable=self.selected_category, values=categories)
        category_dropdown.pack(pady=5)
        category_dropdown.set(categories[0])  # Set the default category

        # Button to fetch news based on selected category
        fetch_button = tk.Button(self.master, text="Fetch News", command=self.fetch_news_by_category)
        fetch_button.pack(pady=10)

        #Add button to prompt weather information display in create_widgets
        weather_button = tk.Button(self.master, text = "Get Weather", command = self.display_weather)
        weather_button.pack(pady=10)
    
    #Method to fetch news based on the selected category
    def fetch_news_by_category(self):
        selected_category = self.selected_category.get()
        self.news_articles = self.get_top_news(category=selected_category)
        self.current_index = 0

        if self.news_articles:
            self.title_var.set(self.news_articles[self.current_index]['title'])
            self.description_var.set(self.news_articles[self.current_index]['description'])
        else:
            messagebox.showinfo("No News", f"No news available for the {selected_category} category.")

    def display_weather(self):
        api_key = "0ab7006df1d50f83008b0b01119144e6"
        city = "Mississauga"
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        

        try:
            response = requests.get(weather_url)
            weather_data = response.json()

            # Print the raw API response for debugging
            print("Raw Weather API Response:", weather_data)

            #Fetch weather information
            temperature = weather_data['main']['temp']
            weather_description = weather_data['weather'][0]['description']

            #Display weather
            weather_message = f"Today's weather in {city}: {temperature}°C, {weather_description.capitalize()}."
            notification.notify(
                title = "Weather Update",
                message = weather_message,
                timeout = 10
            )
        except Exception as e:
            messagebox.showwarning("Weather Error", f"Error displaying weather: {e}")


if __name__ == '__main__':
    root = tk.Tk()
    app = NewsApp(root)
    root.mainloop()


