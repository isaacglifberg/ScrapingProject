import requests
import sqlite3
from bs4 import BeautifulSoup as bs
from matplotlib import pyplot as plt


class ArticleFetcher:
    def __init__(self):
        self.default_urls = [
            "https://www.huffingtonpost.co.uk/", "https://www.thesun.co.uk/"]
        self.urls = []
        self.counts = {}
        self.connenction = sqlite3.connect('database')
        self.cursor = self.connenction.cursor()

    # Get all articles from the default urls and save them in list self.urls
    def fetch_articles(self):
        for url in self.default_urls:
            response = requests.get(url)
            soup = bs(response.content, "lxml")
            links = [link.get('href') for link in soup.find_all(
                'a') if "https://" in link.get('href')]
            self.urls.extend(links)

    # The articles that has been fetched are being inserted to a table if they are not already in there.
    def add_urls_to_db(self):
        for url in self.urls:
            self.cursor.execute(
                f"INSERT OR IGNORE INTO URL_table (url) VALUES ('{url}')")
        self.connenction.commit()

    # Check is category already exists, if so raise an error. If not insert to a table.
    def add_categories(self, category_to_add):
        for info in self.cursor.execute("PRAGMA table_info(phrases_table)"):
            if category_to_add.lower() in info[1]:
                raise Exception
            else:
                self.cursor.execute(
                    f"ALTER TABLE phrases_table ADD '{category_to_add}' text")
                self.connenction.commit()

    # Check if users choice of category exists, if not raise an error. If it exists insert users choice of phrase to table.
    def add_phrases(self, user_choice_category, user_choice_phrase):
        list_categorys = []
        for info in self.cursor.execute("PRAGMA table_info(phrases_table)"):
            list_categorys.append(info[1])
        if user_choice_category in list_categorys:
            self.cursor.execute(
                f"REPLACE INTO phrases_table ('{user_choice_category}') VALUES ('{user_choice_phrase}')")
            # Replace are being insted of an error handeling.
            self.connenction.commit()
        elif user_choice_category not in list_categorys:
            raise Exception

    # Print categorys from table.
    def list_of_categories_from_phrases(self):
        print("Categorys:")
        for info in self.cursor.execute("PRAGMA table_info(phrases_table)"):
            print(info[1])

    # Print URLs from the table.
    def print_urls_from_db(self):
        rows = self.cursor.execute("SELECT * FROM URL_table").fetchall()
        list_url = [item for t in rows for item in t]
        for url in list_url:
            print(url)

    # When the function fetch_articles() runs it saves the articles in a list called self.urls
    # After, this function comes in and counts all words saved in the databse and puts the word
    # as key and the count as value in a dictionary. But first of all it checks if the article
    # already has been analyzed.
    def count_word(self, list_words):
        list_of_tuples = self.cursor.execute(
            "SELECT * FROM URL_table").fetchall()
        list_url = [item for t in list_of_tuples for item in t]
        for url in self.urls:
            if url not in list_url:
                page = requests.get(url)
                soup = bs(page.text, "lxml")
                text = soup.get_text()
                for word in list_words:
                    count = text.count(word)
                    if word in self.counts:
                        self.counts[word] += count
                    else:
                        self.counts[word] = count

    def stored_phrases(self):
        list_of_tuples = self.cursor.execute(
            "SELECT * FROM phrases_table").fetchall()
        list_of_phrase = [
            item for t in list_of_tuples for item in t if item != None]
        for phrase in list_of_phrase:
            print(phrase)

    # The function count_word() saved the count in a dictionary called self.counts.
    # This function takes the values and insert it to a table.
    def update_table(self):
        for key, value in self.counts.items():
            self.cursor.execute(
                f"INSERT INTO update_table (word, update_nr) VALUES ('{key}', {value});")
        self.connenction.commit()

    # This function runs the scraper functions and insert functions.
    def fetch_articles_count_phrases(self):
        list_of_tuples = self.cursor.execute(
            "SELECT * FROM phrases_table").fetchall()
        list_of_phrase = [
            item for t in list_of_tuples for item in t if item != None]
        if list_of_phrase:
            self.fetch_articles()
            self.count_word(list_of_phrase)
            # self.word_counts_table()
            self.update_table()
            self.add_urls_to_db()
        else:
            raise Exception

    def monthly_statistics(self, phrase, number_of_months):
        # Get all timestamps from a word, count how many timestamps.
        dates = self.cursor.execute(
            f"SELECT timestamp FROM update_table WHERE word='{phrase}' and timestamp >= date('now', '-{number_of_months} months')").fetchall()
        count = len(dates)
        # Get the same amount as the count of timestamps
        # from a word from the bottom of the table, in other words the newest.
        test_list = self.cursor.execute(
            f"SELECT update_nr FROM update_table WHERE word = '{phrase}' ORDER BY word DESC LIMIT {count}").fetchall()
        # Map the count with sum.
        sum_of_phrase = sum(map(sum, test_list))
        # Print values.
        print(
            f"The word/phrase {phrase} was found {sum_of_phrase} times in the last {number_of_months} months")

    def chart(self, phrase):
        # Check if phrase exists in table, if not raise an error.
        list_of_tuples = self.cursor.execute(
            "SELECT * FROM phrases_table").fetchall()
        list_of_phrases = [
            item for x in list_of_tuples for item in x if item != None]
        if phrase not in list_of_phrases:
            raise Exception
        # If it exists find all counts from a phrase and all timestamps
        else:
            update_nr = self.cursor.execute(
                f"SELECT update_nr FROM update_table WHERE word = '{phrase}'").fetchall()
            timestamp = self.cursor.execute(
                f"SELECT timestamp FROM update_table WHERE word = '{phrase}'").fetchall()
        # Convert to a list
            count = [item for t in update_nr for item in t]
            time = [item for t in timestamp for item in t]
        # Create a chart.
            x_values = time
            y_values = count
            plt.plot(x_values, y_values, 's--', color='red',
                    label=(f"Phrase: {phrase}"))
            plt.tick_params(axis='x', labelsize=7)
            plt.xlabel("Date of count")
            plt.ylabel("Count of word")
            plt.title("Count on specific date")
            plt.show()
