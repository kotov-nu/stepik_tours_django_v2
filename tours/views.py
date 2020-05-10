from django.shortcuts import render
from django.views import View
from random import shuffle

from .data import tours, title, subtitle, description, departures

info = {'tours': tours, 'title': title, 'subtitle': subtitle, 'description': description, 'departures': departures}


class MainView(View):
    """ Главная. """

    def get(self, request):

        rand_tours_ids = []
        for tour in info['tours']:
            rand_tours_ids.append(tour)
        shuffle(rand_tours_ids)
        rand_tours_ids = rand_tours_ids[:6]

        main_tours = {}
        for num, tour in info['tours'].items():
            if num in rand_tours_ids:
                main_tours[num] = tour

        info['main_tours'] = main_tours

        return render(
            request, 'index.html', context=info
        )


class DepartureView(View):
    """ Направления. """

    def get(self, request, departure):

        suitable_tours = {}
        for num, tour in info['tours'].items():
            if tour['departure'] == departure:
                suitable_tours[num] = tour
        info['suitable_tours'] = suitable_tours

        info['min_price'] = min(suitable_tours.values(), key=lambda tour: tour['price'])['price']
        info['max_price'] = max(suitable_tours.values(), key=lambda tour: tour['price'])['price']
        info['nights_from'] = min(suitable_tours.values(), key=lambda tour: tour['nights'])['nights']
        info['nights_to'] = max(suitable_tours.values(), key=lambda tour: tour['nights'])['nights']

        return render(
            request, 'departure.html', context=info
        )


class TourView(View):
    """ Тур. """

    def get(self, request, tour_id):

        info['tour'] = info['tours'][tour_id]
        info['departure'] = info['departures'][info['tour']['departure']]

        return render(
            request, 'tour.html', context=info
        )
