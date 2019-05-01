import pdftotext
from unsplashScrapper import UnsplashScrapper
import markovify
from random_word import RandomWords
import csv


class PdfToCsv:
    def __init__(self, filename, pdf_start=None):
        self.filename = filename
        self.pdf_start = pdf_start

        self.pdf = self.__get_pdf_pages()
        self.images_bot = UnsplashScrapper(self.get_random_word)
        self.photos_urls = self.images_bot.photos_urls
        self.convert_pdf_to_csv()


    def __get_pdf_pages(self):
        with open(f"{self.filename}.pdf", "rb") as pdf_file:
            pdf = pdftotext.PDF(pdf_file)
            pdf = [page for page in pdf]
            # pdf = [self.__return_asci_characters(page) for page in pdf]
        return pdf
    
    def get_pdf_end_page(self):
        pdf_length = len(self.pdf)
        if not self.pdf_start:
            self.pdf_start = int(pdf_length/10)-1
        pdf_end = pdf_length - self.pdf_start
        return pdf_end
    
    def convert_pdf_to_csv(self):
        pdf_end = self.get_pdf_end_page()
        with open(f'{self.filename}.csv', mode='w') as csv_file:
            file_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['title', 'content', 'image'])
            
            for page in self.pdf[self.pdf_start:pdf_end]:
                title = self.generate_title(page)
                if title is None:
                    continue
                image = self.generate_image(title)
                file_writer.writerow([title, page, image])
    
    def generate_image(self, title):
        if len(self.photos_urls) < 1:
            splitted_title = title.split()
            for i in range(len(splitted_title)):
                self.photos_urls = self.images_bot.get_photos_urls_by_keyword(splitted_title[i])
                if len(self.photos_urls) > 0:
                    break
        image = self.photos_urls[0]
        self.photos_urls.pop(0)
        return image

    
    def generate_title(self, page):
        title_model = markovify.NewlineText(page, state_size=2)
        title = title_model.make_sentence()
        count = 0
        while title is None:
            title = title_model.make_sentence()
            count += 1
            if count > 15:
                break
        return title

    @staticmethod
    def __return_asci_characters(text):
        return ''.join([i if ord(i) < 128 else ' ' for i in text])

    @staticmethod
    def get_random_word():
        r = RandomWords()
        word = r.get_random_word()
        return word

pdf_to_csv = PdfToCsv('193lt')