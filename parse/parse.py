# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
from gi.repository import PangoCairo
import cairo
import datetime
import math


def get_values():
    """Funkcja pobierajaca ze strony oraz zwracajaca ilosc ksiazek dla danego jezyka."""

    values = []  # pusta lista wartosci
    for link in soup.find_all('small'):  # wyszukanie w kodzie strony wzorca 'small'
        value = ""  # stworzenie pustego slowa
        for char in link.get_text():  # dla kazdego znaku w pobranym tekscie
            if char == " ":
                char = ""  # usuwanie znaku spacji
            if char != '+':  # dopoki nie natrafimy na znak '+'
                value += char  # dodanie znak do slowa
            else:  # jesli natrafimy na znak '+' to konczymy pobieranie slowa
                values.append(int(value))  # dodanie slowo do listy w reprezentacji liczbowy
                break
    return values  # zwrocenie listy wartosci


def get_names():
    """Funkcja pobierajaca ze strony oraz zwracajaca oryginalne nazwy jezykow."""

    count = 0  # ustawienie licznika na 0
    names = []  # stworzenie pustej listy nazw krajow
    for link in soup.find_all('strong'):  # szukanie w kodzie strony wzorca 'strong'
        if count < 10:  # pobieramy tylko 10 nazw krajow
            names.append(link.get_text())  # dodanie nazwy kraju do listy
            count += 1  # inkrementacja licznika
        else:
            return names  # zwrocenie listy
            break


def draw_graph():
    """Funkcja rysujaca wykres.

    Funkcja rysuje osie wykresu, slupki na osi OX dla zadanych wartosci
    a takze umieszcza jezyki na osi OY.
    """

    ctx.set_source_rgba(0, 0, 0, 1)  # ustawienie koloru
    ctx.set_line_width(2)  # ustawienie grubosci linii
    ctx.move_to(130, 600)
    ctx.line_to(130, 250)
    ctx.move_to(130, 600)
    ctx.line_to(580, 600)  # narysowanie osi wykresu
    ctx.stroke_preserve()

    count = 0  # ustawienie wartosci licznika na 0
    k = 125  # przyjeta skala, sluzy do rysowania slupkow na podstawie danej ilosci ksiazek
    for length in get_values():
        ctx.set_source_rgba(0, 0, 0, 1)  # ustawienie koloru
        ctx.set_line_width(2)  # ustawienie grubosci linii
        ctx.rectangle(132, 570 - 32 * count, length / k, 20)  # rysowanie slupka dla zadanej dlugosci
        ctx.stroke_preserve()
        ctx.set_source_rgba(0, 128, 128, 1)  # ustawienie koloru
        ctx.fill()  # wypelnienie slupka kolorem
        count += 1  # inkrementacja licznika
    count = 0  # wyzerowanie licznika
    for name in get_names():  # dla kazdej nazwy kraju
        ctx.set_source_rgba(0, 0, 255, 1)  # ustawienie koloru
        layout.set_text(name, -1)  # umieszczenie nazwy kraju na osi OY
        ctx.move_to(0, 570 - 32 * count)
        PangoCairo.show_layout(ctx, layout)  # wyswietlenie zmian
        count += 1


def set_list():
    """Funkcja generujaca liste jezykow oraz liczbe ksiazek dla kazdego z nich."""

    count = 0
    ctx.set_source_rgba(76, 0, 153, 1)
    for name in reversed(get_names()):  # dla kazdej nazwy kraju sposrod 10 wybranych
        layout.set_text(name, -1)  # umieszczenie nazwy kraju w raporcie
        ctx.move_to(0, 22 * count)
        PangoCairo.show_layout(ctx, layout)
        count += 1  # inkrementacja licznika

    count = 0
    for value in reversed(get_values()):  # dla kazej wartosci ilosci stron dla danego kraju
        layout.set_text(str(value), -1)  # umieszczenie wartosci w rapocie
        ctx.move_to(130, 22 * count)
        PangoCairo.show_layout(ctx, layout)
        count += 1


def set_date():
    """Funkcja umieszczajaca date wygenerowania raportu w jego lewym dolnym rogu."""

    ctx.set_source_rgba(0, 153, 0, 1)  # ustawienie koloru
    format = "%d.%m.%Y godz. %H:%M"  # ustawienie formatu wyswietlania daty
    current_time = datetime.datetime.now().strftime(format)  # pobranie i sformatowanie daty
    layout.set_text(current_time, -1)  # umieszczenie daty w raporcie
    ctx.move_to(20, 800)
    PangoCairo.show_layout(ctx, layout)


def get_image_link(soup):
    """Funkcja pobierajaca ze strony logo wikibooks."""

    for line in soup.find("style").string.split(";"):
        if "central-featured-logo" in line:
            start = line.index("(//") + 3
            end = line.index(")")
            return line[start:end]
            
                
        


def set_image():
    """Funkcja umieszczajaca logo wikibooks w prawym dolnym rogu raportu."""

    response2 = urllib2.urlopen('http://' + get_image_link(soup))  # pobranie adresu url loga wikibooks ze strony
    image = cairo.ImageSurface.create_from_png(response2)  # stworzenie obrazka na podstawie adresu url
    ctx.save()  # zapisanie stanu kontekstu
    ctx.scale(0.75, 0.75)  # przeskalowanie kontekstu
    ctx.set_source_surface(image, 590, 910)  # umieszczenie loga wikibooks w raporcie
    ctx.paint()
    ctx.restore()  # przywrocenie poprzedniej skali kontekstu


def set_units():
    """Funkcja umieszczajaca jednostki na osi OX wykresu."""

    count = 1
    ctx.set_line_width(0.01)  # ustawienie grubosci linii
    while count < 27:
        ctx.set_source_rgba(0, 0, 0, 1)  # ustawienie koloru
        k = 438 / 26  # skala wyliczona przez programiste
        if count % 2 == 1:  # dla czytelnosci tylko co druga linia jest rysowana
            ctx.move_to(132 + k * count, 610)
            ctx.line_to(132 + k * count, 270)  # rysowanie linii ulatwiajacych odczytanie wartosci z wykresu
        ctx.move_to(132 + k * count, 640)
        ctx.save()  # zapisanie stanu kontekstu
        ctx.rotate(math.pi * 3 / 2)  # obrocenie o 90 stopni
        unit = str(2000 * count)
        ctx.set_source_rgba(128, 0, 0, 1)
        ctx.show_text(unit)  # umieszczenie obroconych wartosci na osi OX
        ctx.restore()  # przywrocenie poprzedniego stanu
        count += 1
    ctx.stroke_preserve()

response = urllib2.urlopen('http://www.wikibooks.org//')
soup = BeautifulSoup(response.read())
surface = cairo.PDFSurface("plik.pdf", 595.44, 841.68)
ctx = cairo.Context(surface)
layout = PangoCairo.create_layout(ctx)

#draw_graph()
#set_units()
#set_list()
#set_date()
#set_image()
get_image_link(soup)
