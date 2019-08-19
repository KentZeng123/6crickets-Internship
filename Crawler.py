import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, provider_websites):
        ''' Pass in one provider website main page for the constructor argument '''
        self.provider_website_main_page = [provider_websites]
        self.properly_installed_register_buttons = {}
        self.visited_links = []
        self.clicks = 0

    def start_crawl(self):
        ''' Starts crawling the desired provider website for registration buttons '''
        self.visited_links.append(self.provider_website_main_page)
        self.clicks += 1
        self.crawl(self.provider_website_main_page)

    def crawl(self, list_of_urls):
        ''' Recursive function that crawls through every unique page in a website '''
        self.clicks += 1
        links_in_level = []
        for url in list_of_urls:
            list_of_links = self.parse_page(url)
            for link in list_of_links:
                links_in_level.append(link)
        self.visited_links.append(links_in_level)
        if len(links_in_level) > 0:
            self.crawl(links_in_level)

    def parse_page(self, url):
        ''' Parses a web page and finds all the unvisited links and registration buttons on that page '''
        links_to_follow = []
        results = requests.get(url)
        source = results.content
        soup_object = BeautifulSoup(source, 'lxml')
        for a_tag in soup_object.find_all("a"):
            found_link = self.search_visited_links(str(a_tag.attrs["href"]))
            if found_link or "pdf" in str(a_tag.attrs["href"]) or "jpg" in str(a_tag.attrs["href"]):
                continue
            else:
                main_page = str(self.provider_website_main_page)
                if main_page[2:len(main_page) - 2] in str(a_tag.attrs["href"]):
                    links_to_follow.append(str(a_tag.attrs["href"]))
                if "https://www.6crickets.com/providerDirectory" in str(a_tag.attrs["href"]):
                    self.properly_installed_register_buttons.update({str(a_tag.attrs["href"]): self.clicks})
        return links_to_follow

    def search_visited_links(self, url):
        ''' Searches self.visited_links for the url that is passed into this function '''
        found_link = False
        for level in self.visited_links:
            for link in level:
                if link == url or link == (url + "/"):
                    found_link = True
                    break
        return found_link

    def get_properly_installed_register_buttons(self):
        return self.properly_installed_register_buttons

    def register_button_position(self, register_button):
        ''' Takes in a register button you would like to know the location of and returns a list of urls
        that are in order of the sequence of clicks to get to that register button. '''
        path = [register_button]
        return path


crickets_Crawler = Crawler("https://firecrackermath.org")
crickets_Crawler.start_crawl()
print(crickets_Crawler.get_properly_installed_register_buttons())
