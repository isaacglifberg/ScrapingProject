from scraping import ArticleFetcher


class Menu:
    def __init__(self):
        self.articles = ArticleFetcher()
        self.main_menu()

    def main_menu(self):
        while True:
            print("[1] - See the list of stored URLs ")
            print("[2] - See the list of all categories")
            print("[3] - See the list of all phrases saved in the database")
            print("[4] - Add category")
            print("[5] - Add search words/phrases")
            print(
                "[6] - See monthly statistics about a word tha has been saved in the databse")
            print(
                "[7] - See a chart that depicts the occurrence of a specific search phrase/word tha has been saved in the databse")
            print("[q] - Quit")

            user_input = input("What would you like to do? \n")
            if user_input == "1":
                self.articles.print_urls_from_db()
            elif user_input == "2":
                self.articles.list_of_categories_from_phrases()
            elif user_input == "3":
                self.articles.stored_phrases()
            elif user_input == "4":
                self.add_category()
            elif user_input == "5":
                self.add_word_phrases()
            elif user_input == "6":
                self.monthly_statistics_menu()
            elif user_input == "7":
                self.see_chart()
            elif user_input == "q":
                quit()
            else:
                print("Enter a number between 1-5 or enter q to quit program.")

    def add_word_phrases(self):
        try:
            choice_of_category = input(
                "What category do you want to add a word to?\n")
            choice_of_phrase = input("What word/phrase do you want to add?\n")
            self.articles.add_phrases(choice_of_category, choice_of_phrase)
        except Exception:
            print("No category with that name")

    def add_category(self):
        try:
            choice_of_category = input(
                "What category do you want to add?\n")
            self.articles.add_categories(choice_of_category)
        except Exception:
            print("Category already exists")

    def monthly_statistics_menu(self):
        try:
            print("If you don't no what word/phrase is stored in the database, press 3 in the menu to see list of phrases.")
            choice_of_word = input(
                "What word/phrase that is stored in the databse do you want monthly statistics on?\n")
            choice_number_of_months = input(
                "For how many months do you want statistics on?\n")
            self.articles.monthly_statistics(
                choice_of_word, int(choice_number_of_months))
        except ValueError:
            print("Invalid input, need a number")
        except Exception:
            print("Word/phrase does not exists in database")

    def fetch_and_count_phrase(self):
        try:
            self.articles.fetch_articles_count_phrases()
        except Exception:
            print("No phrases stored in the database")

    def see_chart(self):
        try:
            print("If you don't no what word/phrase is stored in the database, press 3 in the menu to see list of phrases.")
            choice_of_phrase = input(
                "What phrase/word do you want a chart on? \n")
            self.articles.chart(choice_of_phrase)
        except Exception:
            print("Phrase does not exists in the database")


if __name__ == "__main__":
    menu = Menu()
