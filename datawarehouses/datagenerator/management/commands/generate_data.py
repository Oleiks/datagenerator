from django.core.management.base import BaseCommand
from faker import Faker
from datagenerator.models import (
    Pracownik,
    TrasaNarciarska,
    NadzorTrasy,
    ProblemNaStoku,
    PracaKonserwacyjna,
    Karnet,
    SprzedazKarnetow,
    KlientLoyalty,
    RejestrPrzejazdow,
)
import random

class Command(BaseCommand):
    help = 'Generate fake data'

    def handle(self, *args, **kwargs):
        fake = Faker('pl_PL')

        # Generate fake Pracownik (Employee) data
        for _ in range(50):
            Pracownik.objects.create(
                Imie=fake.first_name(),
                Nazwisko=fake.last_name(),
                Stanowisko=fake.job()
            )

        # Generate fake TrasaNarciarska (Ski Route) data
        for _ in range(30):
            TrasaNarciarska.objects.create(
                Poziom_trudnosci=random.choice(['Łatwa', 'Średnia', 'Trudna']),
                Dlugosc_trasy=fake.random_int(min=100, max=10000) / 100
            )

        # Generate fake NadzorTrasy (Route Supervision) data
        for _ in range(100):
            NadzorTrasy.objects.create(
                ID_pracownika=Pracownik.objects.order_by('?').first(),
                ID_trasy=TrasaNarciarska.objects.order_by('?').first(),
                Data_nadzoru=fake.date_this_decade()
            )

        # Generate fake ProblemNaStoku (Problem on the Slope) data
        for _ in range(50):
            ProblemNaStoku.objects.create(
                ID_trasy=TrasaNarciarska.objects.order_by('?').first(),
                opis_problemu=fake.text(max_nb_chars=200),
                data_zgloszenia=fake.date_this_decade(),
                data_rozwiazania_problemu=fake.date_this_decade()
            )

        # Generate fake PracaKonserwacyjna (Maintenance Work) data
        for _ in range(60):
            PracaKonserwacyjna.objects.create(
                ID_trasy=TrasaNarciarska.objects.order_by('?').first(),
                ID_konserwatora=Pracownik.objects.order_by('?').first(),
                opis_pracy=fake.text(max_nb_chars=200),
                data_rozpoczecia=fake.date_this_decade(),
                data_zakonczenia=fake.date_this_decade()
            )

        # Generate fake Karnet (Ticket) data
        for _ in range(5):
            Karnet.objects.create(
                rodzaj_karnetu=random.randint(1, 5),
                cena_karnetu=fake.random_int(min=50, max=300) / 100
            )

        # Generate fake SprzedazKarnetow (Ticket Sales) data
        for _ in range(100):
            SprzedazKarnetow.objects.create(
                PESEL_klienta=fake.unique.random_int(min=10000000000, max=99999999999),
                rodzaj_karnetu=Karnet.objects.order_by('?').first(),
                data_zakupu=fake.date_this_decade()
            )

        # Generate fake KlientLoyalty (Loyal Customers) data
        for _ in range(20):
            KlientLoyalty.objects.create(
                PESEL=str(fake.unique.random_int(min=10000000000, max=99999999999))
            )

        # Generate fake RejestrPrzejazdow (Ski Pass Register) data
        # Generate fake RejestrPrzejazdow (Ski Pass Register) data
        for _ in range(200):
            trasa = TrasaNarciarska.objects.order_by('?').first()
            karnet_sprzedaz = SprzedazKarnetow.objects.order_by('?').first()

            # Create a RejestrPrzejazdow instance with a valid Karnet instance
            RejestrPrzejazdow.objects.create(
                ID_trasy=trasa,
                ID_karnetu=karnet_sprzedaz.rodzaj_karnetu,  # Use the Karnet instance
                Data=fake.date_this_decade()
            )

