from gi.repository import Gtk, GdkPixbuf
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
from gi.overrides.Pango import Pango
import random
import os


class Browser:
    """Klasa zawierajaca cala strukture dzialania aplikacji."""
    
    def create_bbox(self):
        """Funkcja tworzaca poszczegolne przyciski wykorzystywane w aplikacji."""
        
        self.frame = Gtk.Frame()
        self.bbox = Gtk.HButtonBox()
        self.frame.add(self.bbox)
        self.button = Gtk.Button('Poprzedni')  # stworzenie przycisku poprzedni
        self.button.connect("clicked", self.on_previous_clicked)  # polaczenie przycisku poprzedni z funkcja
        self.bbox.add(self.button)  # dodanie przycisku poprzedni do boxu
        self.button = Gtk.Button('Nastepny')   # stworzenie przycisku nastepny
        self.button.connect("clicked", self.on_next_clicked)  # polaczenie przycisku nastepny z funkcja
        self.bbox.add(self.button)
        self.button = Gtk.Button('Losowy')   # stworzenie przycisku losowy
        self.button.connect("clicked", self.on_random_clicked)  # polaczenie przycisku losowy z funkcja
        self.bbox.add(self.button)
        self.button = Gtk.Button('Najnowszy')   # stworzenie przycisku najnowszy
        self.button.connect("clicked", self.on_new_clicked)  # polaczenie przycisku najnowszy z funkcja
        self.bbox.add(self.button)  # dodanie przycisku do boxu
        self.entry1 = Gtk.Entry()  # stworzenie pola do wpisywania numeru obrazka
        self.entry1.connect("activate", self.checked)  # polaczenie pola z funkcja
        self.bbox.add(self.entry1)  # dodanie pola do boxu
        return self.frame  # zwrocenie obszaru roboczego

    def __init__(self):
        """Konstruktor klasy Browser.
        
        Ustawia wszystkie wartosci poczatkowe i wyglad aplikacji od razu po jej wlaczeniu.
        """
        
        if not os.path.exists(os.path.join(os.getcwd(), "cache")):
            os.makedirs(os.path.join(os.getcwd(), "cache"))  # stworzenie folderu cache jesli nie istnieje
        self.max_number = self.find_latest()  # ustawienie numeru najswiezszego obrazka
        self.actual_number = self.max_number  # numer aktualnie wyswietlanego obarzka
        self.value_list = [0 for i in range(1, self.max_number + 2)]  # lista do sprawdzenia, czy dany obrazek byl juz przegladany
        self.window = Gtk.Window()  # stworzenie glownego okna
        self.window.set_default_size(640, 480)
        self.window.set_title("Przegladarka komiksow")  # ustawienie tytulu aplikacji
        self.window.connect("destroy", lambda x: Gtk.main_quit())
        self.title_label = Gtk.Label()  # labelka przechowujaca tytul obrazka i jego numer
        self.main_vbox = Gtk.VBox(False, 0)  # stworzenie vboxa
        self.window.add(self.main_vbox)
        self.main_vbox.add(self.title_label)
        self.image = Gtk.Image()  # stworzenie obiektu do przechowywania obrazka
        self.vbox = Gtk.VBox(False, 0)
        self.main_vbox.set_size_request(10, 10)
        self.getset_images(self.max_number)  # wyswietlenie najswiezszego obrazka po otwarciu aplikacji
        self.main_vbox.add(self.image)
        self.main_vbox.add(self.vbox)
        self.vbox.pack_start(self.create_bbox(), True, True, 5)
        self.window.show_all()  # wyswietlenie wszystkich elementow okna

    def getset_images(self, number):
        """Funkcja pobierajaca obrazki oraz ich tytuly ze strony xkcd.com.
        
        Parametr number to numer aktualnego obrazka ktory jest pobierany i wyswietlany.
        """
        
        self.title = ""
        self.actual_number = number  # ustawienie aktualnego numeru obrazka
        self.url = 'http://www.xkcd.com/' + str(number) + '/'  # stworzenie adresu url na podstawie przekazanego numerb obrazka
        self.html = urlopen(self.url).read()
        self.soup = BeautifulSoup(self.html)
        for img in self.soup.findAll('title'):  # szukanie tytulu obrazka
            self.title += img.text[6:]  # ustawienie tytulu obrazka
        self.title_label.set_markup(self.title + ", " + str(number))  # wyswietlenie tytulu obrazka

        for img in self.soup.findAll('img'):  # szukanie obrazka w kodzie strony
            if img.get('src') != '//imgs.xkcd.com/static/terrible_small_logo.png':
                if img.get('src') != 'http://imgs.xkcd.com/store/te-news.png':
                    if img.get('src') != '//imgs.xkcd.com/s/a899e84.jpg':  # warunki do pominiecia innych obrazkow na stronie 
                        self.image_link = 'http:' + img.get('src')  # stworzenie linku do danego obarzka
                        self.filename = 'file_' + str(number) + '.png'  # ustawienie tytulu pliku w ktorym bedzie zapisany obrazek
                        if self.value_list[self.actual_number] == 0:  # jesli plik nie byl jeszcze przegladany
                            self.response = urllib.urlopen(self.image_link)
                            self.loader = GdkPixbuf.PixbufLoader()
                            self.loader.write(self.response.read())
                            self.loader.close()
                            self.image.set_from_pixbuf(self.loader.get_pixbuf())  # pobranie obrazka na podstawie adresu url
                            self.value_list[self.actual_number] = 1  # dzieki temu wiemy, ze przegladalismy juz dany obrazek
                            urllib.urlretrieve(self.image_link, os.path.join(os.getcwd(), "cache", self.filename))  # zapisanie w cachu
                        else:  # jesli obrazek byl przegladany to pobieramy go z folderu cache
                            self.image.set_from_file(os.path.join(os.getcwd(), "cache", self.filename))

    def on_previous_clicked(self, button):
        """Funkcja wykonujaca sie po wcisnieciu przycisku 'poprzedni'."""
        
        if self.actual_number > 1:  # warunek broniacy przed wybraniem zerowego obrazka- nie ma takiego
            self.getset_images(self.actual_number - 1)

    def on_next_clicked(self, button):
        """Funkcja wykonujaca sie po wcisnieciu przycisku 'nastepny'."""
        
        self.max_number = self.find_latest()  # pobranie numeru aktualnie najswiezszego obrazka
        if self.actual_number < self.max_number:  # warunek broniacy przed wybraniem numeru obrazka ktory nie istnieje
            self.getset_images(self.actual_number + 1)

    def on_random_clicked(self, button):
        """Funkcja wykonujaca sie po wcisnieciu przycisku 'losowy'."""
        
        self.max_number = self.find_latest()
        self.rand = random.randint(1, self.max_number + 1)  # losowanie numeru obrazka
        self.getset_images(self.rand)

    def on_new_clicked(self, button):
        """Funkcja wykonujaca sie po wcisnieciu przycisku 'najnowszy'."""
        
        self.max_number = self.find_latest()
        self.getset_images(self.max_number)  # wyswietlenie najnowszego obarzka

    def checked(self, liczba):
        """Funkcja wykonujaca sie po wpisaniu numeru obrazka w pole tekstowe."""
        
        self.max_number = self.find_latest()
        if int(self.entry1.get_text()) in range(1, self.max_number + 1):  # sprawdzenie poprawnosci numeru obarzka
            self.actual_number = int(self.entry1.get_text())
            self.getset_images(self.actual_number)

    def find_latest(self):
        """Funkcja znajdujaca najswiezszy obrazek i zwracajaca jego numer."""
        
        self.numbers_list = []
        self.url2 = 'http://www.xkcd.com/archive/'
        self.html2 = urlopen(self.url2).read()
        self.soup2 = BeautifulSoup(self.html2)
        for data in self.soup2.findAll('a'):
            number2 = data.get('href')[1:-1]
            if number2 < 'a':  # dzieki temu wyswietlane sa tylko numery
                self.numbers_list.append(number2)
        return int(self.numbers_list[1])  # zwrocenie numeru najswiezszego obrazka


Browser()
Gtk.main()
