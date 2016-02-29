import numpy as np
import matplotlib.pyplot as plt
import math
import xml.etree.cElementTree as ET
import StringIO

def is_point_in(x, y, radius):
    """Funkcja sprawdzajaca, czy punkt o wspolrzednych (x,y) lezy w kole o promieniu radius."""
    
    distance = float(math.sqrt(x ** 2 + y ** 2))  # liczenie odleglosci punkty od srodka okregu
    if distance <= radius:  # jesli odleglosc punkt od srodka okregu jest mniejsza od dlugosci promienia zwroc prawde
        return True
    else:
        return False  # w przeciwnym wypadku zwroc falsz


def draw_graph1(points_number, graphs_number, radius):
    """Funkcja rysujaca wykres zbieznosci przebiegow funkcji dla stalego promienia rownego 1."""
    
    """Argumenty: points_number- liczba losowanych punktow dla kazdego przebiegu,
    graphs_number- liczba przebiegow funkcji estymujacych PI,
    radius- dlugosc promienia okregu.
    """
    
   # plt.figure(1)  # odwolanie do pierwszego wykresu dla stalego promienia
    plt.subplot(2,2,1)
    t1 = np.arange(0, points_number + 1, 1)  # tablica argumentow wykresu
    legend_list = []  # lista przechowujaca wartosci, ktore pozniej zostana wpisane do legendy
    legend_list.append("$\pi$")  # dodanie do listy znaku pi
    plt.plot(math.pi + 0 * t1, linewidth = 3.0)  # oznaczenie na wykresie wartosci pi
    points_count = 1  # ustawienia licznika punktow na wartosc poczatkowa
    for j in range(graphs_number):  # petla przebiegow funkcji estymujacych pi
        legend_list.append(str(j + 1))  # dodanie do listy kolejnych numerow przebiegow funkcji
        count = 0  # wyzerowanie licznika punktow znajdujacych sie w kole
        values_list = []  # puspta lista wartosci losowan
        while points_count <= (points_number + 1):
            x = np.random.uniform(-radius, radius + 0.001)  # losowanie wspolrzednej x
            y = np.random.uniform(-radius, radius + 0.001)  # llosowanie wspolrzednej y
            if x <= radius and y <= radius:  # sprawdzamy tylko zamknietych przedzial [-r,r]
                if is_point_in(x, y, radius):
                    count += 1  # jesli punkt znajduje sie w kole to inkrementujemy licznik
                result = 4 * float(count) / (points_count)  # obliczanie przyblizenia pi
                values_list.append(result)  # dodanie przyblizenia pi do listy
                points_count += 1  # inkrementacja licznika punktow
        plt.plot(t1, values_list)  # oznaczenie na wykresie wartosci przyblizen
        points_count = 1  # przywrocenie licznikowi punktow wartosci poczatkowej
    leg = plt.legend((legend_list), loc = 'lower center', title = 'Numer losowania, r=1', ncol = 5, prop={'size':6})  # stworzenie legendy
    plt.xlabel("Liczba wylosowanych punktow", fontsize = 20)  # podpisanie osi OX
    plt.ylabel("Estymacja $\pi$", fontsize = 20)  # podpisanie osi OX
    plt.grid(b=True, which='both', color=(0.8,0.8,1.0),linestyle='-')  # formatowanie siatki wykresu


def draw_graph2(points_number, graphs_number, radius):
    """Funkcja rysujaca wykres zbieznosci przebiegow funkcji dla rosnacego promienia."""
    
    """Argumenty: points_number- liczba losowanych punktow dla kazdego przebiegu,
    graphs_number- liczba przebiegow funkcji estymujacych PI,
    radius- dlugosc poczatkowego promienia okregu.
    """
    
    #plt.figure(2)  # odwolanie do pierwszego wykresu dla stalego promienia 
    plt.subplot(2,2,4)
    t1 = np.arange(0, points_number + 1, 1)  # tablica argumentow wykresu
    legend_list = []  # lista przechowujaca wartosci, ktore pozniej zostana wpisane do legendy
    legend_list.append("$\pi$")  # dodanie do listy znaku pi
    plt.plot(math.pi + 0 * t1, linewidth = 3.0)  # oznaczenie na wykresie wartosci pi
    points_count = 1  # ustawienia licznika punktow na wartosc poczatkowa
    for j in range(graphs_number):  # petla przebiegow funkcji estymujacych pi
        legend_list.append(str(j + 1))  # dodanie do listy kolejnych numerow przebiegow funkcji
        count = 0  # wyzerowanie licznika punktow znajdujacych sie w kole
        values_list = []  # puspta lista wartosci losowan
        while points_count <= (points_number + 1):
            x = np.random.uniform(-radius, radius + 0.001)  # losowanie wspolrzednej x
            y = np.random.uniform(-radius, radius + 0.001)  # llosowanie wspolrzednej y
            if x <= radius and y <= radius:  # sprawdzamy tylko zamknietych przedzial [-r,r]
                if is_point_in(x, y, radius):
                    count += 1  # jesli punkt znajduje sie w kole to inkrementujemy licznik
                result = 4 * float(count) / (points_count)  # obliczanie przyblizenia pi
                values_list.append(result)  # dodanie przyblizenia pi do listy
                points_count += 1  # inkrementacja licznika punktow
        plt.plot(t1, values_list)  # oznaczenie na wykresie wartosci przyblizen
        radius += 1  # inkrementacja dlugosci promienia
        points_count = 1  # przywrocenie licznikowi punktow wartosci poczatkowej
    leg = plt.legend((legend_list), loc = 'lower center', title = 'Kolejne r', ncol = 5, prop={'size':6})  # stworzenie legendy
    plt.xlabel("Liczba wylosowanych punktow", fontsize = 8)  # pospisanie osi OX
    plt.ylabel("Estymacja $\pi$", fontsize = 8)  # podpisanie oxi OY
    plt.grid(b=True, which='both', color=(0.8,0.8,1.0),linestyle='-')  # formatowanie siatki wykresu

def write_html():
    root = ET.Element("html")
    head = ET.SubElement(root, "head")
    title = ET.SubElement(head, "title")
    title.text = "Strona pierwsza"
    body = ET.SubElement(root, "body")
    paragraph = ET.SubElement(body, "p")
    paragraph.text = "Wykres:"
    imgdata = StringIO.StringIO()
    plt.savefig(imgdata, format="svg" )
    svg_txt = imgdata.getvalue()
    imgdata.close()
    ET.register_namespace("","http://www.w3.org/2000/svg")
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    svg_tree_root = ET.fromstring(svg_txt)
    paragraph = ET.SubElement(body, "p")
    paragraph.append(svg_tree_root)
    with open("b.html", "w") as f:
        f.write(ET.tostring(root))

draw_graph1(1000, 10, 1)  # wywolanie funkcji rysujacej wykresy dla r=1    
draw_graph2(1000, 10, 4)  # wywolanie funkcji rysujacej wykresy dla kolejnych wartosci r
#plt.show()  # wyswietlenie wykresow
write_html()





 