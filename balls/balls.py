from gi.repository import Gtk
from gi.repository import GdkPixbuf
import random


class Plansza(Gtk.Table):
    """Klasa reprezentujaca plansze, na ktorej toczy sie gra."""

    def __init__(self):
        """Konstruktor, inicjalizujacy plansze.

        Inicjalizacja odbywa sie poprzez stworzenie listy przyciskow
        oraz podlaczenie ich pod tablice.
        """

        Gtk.Table.__init__(self, 10, 10, True)
        self.button_list = []
        for i in range(10):
            self.button_list.append([])
            for j in range(10):
                self.button_list[i].append(Gtk.ToggleButton())  # lista przyciskow ToggleButton
                self.button_list[i][j].set_size_request(40, 40)  # ustawienie rozmiaru przycisku
                self.attach(self.button_list[i][j], i, i + 1, j, j + 1)  # ustawienie przyciskow na tablicy

    def reset(self):
        """Metoda resetujaca plansze po zakonczonej grze."""

        for i in range(10):
            for j in range(10):
                self.button_list[i][j].set_image(Gtk.Image())  # usuwanie obrazka z przycisku


class Game():
    """Klasa zawierajaca mechanike gry oraz informacje o jej przebiegu."""

    def __init__(self):
        """Inicjalizacja wsystkich pol potrzebnych do gry."""

        self.window = Gtk.Window(title="Kulki")  # nadanie tytulu okienka
        self.window.set_default_size(480, 440)  # ustawienie rozmiaru okienka
        self.window.connect("delete-event", Gtk.main_quit)  # zapewnia zamkniecie aplikacji po nacisnieciu krzyzyka
        self.image1 = GdkPixbuf.Pixbuf.new_from_file_at_size("kulka1.svg", 35, 35)  # zaladowanie obarzka kulki
        self.image2 = GdkPixbuf.Pixbuf.new_from_file_at_size("kulka2.svg", 35, 35)
        self.image3 = GdkPixbuf.Pixbuf.new_from_file_at_size("kulka3.svg", 35, 35)
        self.image4 = GdkPixbuf.Pixbuf.new_from_file_at_size("kulka4.svg", 35, 35)
        self.image5 = GdkPixbuf.Pixbuf.new_from_file_at_size("kulka5.svg", 35, 35)
        self.moves = 0  # zmienna zwiekszana zawsze, gdy zostanie dodana nowa kulka
        self.points = 0  # zmienna liczaca ile razy uzytkownik przesunal kulke
        self.ranking_count = 0  # zmienna, dzieki ktorej wyswietlane jest tylko 5 najlepszych wynikow
        self.ranking_list = list()  # lista przechowujaca najlepsze wyniki
        self.ranking = ""  # string przechowujacy wpis do rankingu w odpowiedniej formie
        self.play_again = Gtk.Button(label="Graj od poczatku")  # przycisk zerujacy stan rozgrywki
        self.ranking_label = Gtk.Label()  # labelka, w ktorej wyswietlany jest wynik
        self.points_label = Gtk.Label()  # labelka, w ktorej wyswietlane sa punkty
        self.table = Gtk.Table(12, 11, True)  # stworzenie calego okienka
        self.area = Plansza()  # zmienna typu plansza, przechowuje przyciski
        self.table.attach(self.play_again, 0, 11, 11, 12)
        self.table.attach(self.ranking_label, 0, 1, 1, 6)
        self.table.attach(self.points_label, 0, 3, 0, 1)
        self.table.attach(self.area, 1, 11, 1, 11)
        self.window.add(self.table)
        self.new_game(self)  # wywolanie nowej rozgrywki
        self.play_again.connect("clicked", self.new_game)  # reakcja na kilkniecie przycisku nowej gry
        self.window.show_all()

        for i in range(10):
            for j in range(10):
                self.area.button_list[i][j].connect("clicked", self.player_move)  # reakcja na klikniecie przycisku

    def new_game(self, _):
        """Metoda przywracajaca ustawienia poczatkowe i zerujaca wszystkie wartosci.

        Odbywa sie w niej takze wywolanie metody losujacej 50 poczatkowych kulek.
        """

        self.ranking_label.set_text("Ranking:\n" + self.ranking)  # wyswietlenie rankinu w labelce
        self.area.reset()  # usuniecie wszystkich obrazkow z przyciskow
        self.moves = 0  # wyzerowanie wartosci ruchow
        self.points = 0  # wyzerowanie punktow
        self.ranking_count += 1  
        if self.ranking_count > 5:
            self.ranking_count = 5
        self.ranking = ""
        for i in range(10):
            for j in range(10):
                self.area.button_list[i][j].set_active(False)  # odklikniecie wszystkich przyciskow
        self.tab = []
        for i in range(10):
            self.tab.append([])
            for j in range(10):
                self.tab[i].append(0)  # zerowanie wartosci listy

        while self.moves < 50:
            self.rand_balls()  # losowanie 50 poczatkowych kulek
        self.delete_balls()  # sprawdzenie, czy w tym momencie trzeba usunac jakies kulki
        self.points_label.set_text("Liczba punktow: 0")  # na poczatku rozgrywki liczba punktow wynosi 0

    def player_move(self, which_button):
        """Metoda reagujaca na klikniecie przycisku.

        Argument wchich_button sluzy do rozpoznania, ktory przycisk zostal nacisniety.
        """

        for i in range(10):
            for j in range(10):
                if id(which_button) == id(self.area.button_list[i][j]):  # sprawdzenie, ktory przycisk zostal klikniety
                    if self.tab[i][j] != 0:  # jesli pole jest wolne
                        self.x, self.y = i, j  # pomocnicze zmienne przecohwujace wspolrzedne
                    elif self.x != -1:
                        if self.tab[self.x][self.y] == 1:  # wstawienie na wolne pola takiego obrazka, jaki przenosimy
                            self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image1))
                        elif self.tab[self.x][self.y] == 2:
                            self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image2))
                        elif self.tab[self.x][self.y] == 3:
                            self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image3))
                        elif self.tab[self.x][self.y] == 4:
                            self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image4))
                        elif self.tab[self.x][self.y] == 5:
                            self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image5))

                        self.area.button_list[self.x][self.y].set_image(Gtk.Image())  # usuniecie obrazka z poprzedniego pola
                        self.tab[i][j], self.tab[self.x][self.y] = self.tab[self.x][self.y], self.tab[i][j]  # zamiana wartosci
                        self.x, self.y = -1, -1
                        self.points += 1  # zwiekszenie liczy punktow
                        self.points_label.set_text("Liczba punktow: {}".format(self.points))  # wyswietlenie liczy punktow
                        self.delete_balls()  # sprawdzenie, czy trzeba usunac kulki
                        self.rand_balls()  # losowanie nowych kulek
                        self.delete_balls()  # sprawdzeniem czy trzeba usunac kulki
                        if self.moves >= 100:  # jesli nie ma zadnego pustego pola
                            self.ranking_list.append(str(self.points))  # dodanie punktow do listy
                            self.ranking_list.sort(reverse=True)  # sortowanie wynikow
                            for i in range(self.ranking_count):
                                self.ranking += str(i + 1) + ". " + self.ranking_list[i] + "\n"
                                self.ranking_label.set_text("Ranking:\n" + self.ranking)  # wyswietlenie rankingu

    def rand_balls(self):
        """Metoda losujaca wspolrzedne kulki i ustawiajaca jej obrazek na przycisku."""

        self.count = 0  # zerowanie wartosci licznika
        while self.count < 3:  # losujemy tylko 3 kulki za kazdym razem
            if self.moves < 100:  # jesli istnieje wolne pole
                self.ball = random.randint(1, 5)  # losowanie koloru kulki
                i = random.randint(0, 9)  # losowanie wspolrzednych
                j = random.randint(0, 9)

                if self.tab[i][j] == 0:
                    if self.ball == 1:
                        self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image1))  # wstawienie obrazka
                        self.tab[i][j] = 1  # nadanie wartosci
                    elif self.ball == 2:
                        self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image2))
                        self.tab[i][j] = 2
                    elif self.ball == 3:
                        self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image3))
                        self.tab[i][j] = 3
                    elif self.ball == 4:
                        self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image4))
                        self.tab[i][j] = 4
                    else:
                        self.area.button_list[i][j].set_image(Gtk.Image.new_from_pixbuf(self.image5))
                        self.tab[i][j] = 5
                    self.moves += 1
                    self.count += 1
            else:
                break  # jesli nie ma pustego pola, to petla zostaje przerwana

    def delete_balls(self):
        """Metoda usuwajaca odpowiednie kulki.

        Metoda sprawdza czy w danym rzedzie, kolumnie lub przekatnej
        nie ma 5 takich samych kulek. Jesli warunek jest spelniony, to
        usuwa je poprzez wyzerowanie wartosci pola oraz usuniecie obrazka.
        """

        for i in range(10):  # petla usuwajaca kulki w kolumnach i wierszach
            self.count1 = 1
            self.count2 = 1
            for j in range(9):
                if self.tab[i][j] == self.tab[i][j + 1] and self.tab[i][j] != 0:  # sprawdzanie kolumn
                    self.count1 += 1
                    if self.count1 == 5:  # jesli jest 5 takich samych kulek
                        self.moves -= 5  # zmniejszenie ilosci ruchow o 5
                        self.count1 = 1  # wyzerowanie licznika
                        for k in range(5):
                            self.tab[i][j + 1 - k] = 0
                            self.area.button_list[i][j + 1 - k].set_image(Gtk.Image())  # usuniecie obrazkow z przyciskow

                else:
                    self.count1 = 1  

                if self.tab[j][i] == self.tab[j + 1][i] and self.tab[j][i] != 0:  
                    self.count2 += 1
                    if self.count2 == 5:  # jesli jest 5 takich samych kulek
                        self.moves -= 5  # zmniejszenie ilosci ruchow o 5
                        self.count2 = 1  # wyzerowanie licznika
                        for k in range(5):
                            self.tab[j + 1 - k][i] = 0
                            self.area.button_list[j + 1 - k][i].set_image(Gtk.Image())  # usuniecie obrazkow z przyciskow
                else:
                    self.count2 = 1  # jeœli jakakolwiek kulka na drodze jest inna niz poprzednia, to licznik jest zerowany

        for i in range(6):  # petla sprawdzajacy przekatne
            self.count1 = 1
            self.count2 = 1
            for j in range(9 - i):
                if self.tab[i + j][j] == self.tab[i + j + 1][j + 1] and self.tab[i + j][j] != 0:
                    self.count1 += 1
                    if self.count1 == 5:
                        self.moves -= 5
                        self.count1 = 1
                        for k in range(5):
                            self.tab[i + j + 1 - k][j + 1 - k] = 0
                            self.area.button_list[i + j + 1 - k][j + 1 - k].set_image(Gtk.Image())
                else:
                    self.count1 = 1

                if self.tab[j][i + j] == self.tab[j + 1][i + j + 1] and self.tab[j][i + j] != 0:
                    self.count2 += 1
                    if self.count2 == 5:
                        self.moves -= 5
                        self.count2 = 1
                        for k in range(5):
                            self.tab[j + 1 - k][i + j + 1 - k] = 0
                            self.area.button_list[j + 1 - k][i + j + 1 - k].set_image(Gtk.Image())
                else:
                    self.count2 = 1

        for i in range(4, 10):
            self.count1 = 1
            self.count2 = 1
            for j in range(i):
                if self.tab[j][i - j] == self.tab[j + 1][i - j - 1] and self.tab[j][i - j] != 0:
                    self.count1 += 1
                    if self.count1 == 5:
                        self.moves -= 5
                        self.count1 = 1
                        for k in range(5):
                            self.tab[j + 1 - k][i - j - 1 + k] = 0
                            self.area.button_list[j + 1 - k][i - j - 1 + k].set_image(Gtk.Image())
                else:
                    self.count1 = 1

                if self.tab[9 - i + j][9 - j] == self.tab[9 - i + j + 1][9 - j - 1] and self.tab[9 - i + j][9 - j] != 0:
                    self.count2 += 1
                    if self.count2 == 5:
                        self.moves -= 5
                        self.count2 = 1
                        for k in range(5):
                            self.tab[9 - i + j + 1 - k][9 - j - 1 + k] = 0
                            self.area.button_list[9 - i + j + 1 - k][9 - j - 1 + k].set_image(Gtk.Image())
                else:
                    self.count2 = 1


Game()
Gtk.main()