from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint

from futbol.models import *
 
faker = Faker(["es_CA","es_ES"])
 
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
 
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
 
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(nom=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
 
        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga( nom=titol_lliga, temporada="temporada" )
        lliga.save()
 
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            equip = Equip(ciutat=ciutat,nom=nom,lliga=lliga)
            #print(equip)
            equip.save()
            lliga.equips.add(equip)
 
            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.name()
                posicio = "jugador"
                data_naixement = "1989-11-01"
                jugador = Jugador(nom=nom,posicio=posicio,
                    data_naixement=data_naixement,equip=equip)
                #print(jugador)
                jugador.save()
 
        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local!=visitant:
                    partit = Partit(local=local,visitant=visitant)
                    partit.local = local
                    partit.visitant = visitant
                    partit.data = timezone.now()
                    partit.lliga = lliga
                    partit.save()

                    #creem gols locals
                    for i in range(randint (0,6)):
                        gol = Event(partit=partit, temps=timezone.now(),
                            tipus="GOL",equip=local,
                            jugador=local.jugadors.all()[randint(0,20)])
                        #partit.events.add(gol)

                    #creem gols visitants
                    for i in range(randint (0,6)):
                        gol = Event(partit=partit, temps=timezone.now(),
                            tipus="GOL",equip=visitant,
                            jugador=visitant.jugadors.all()[randint(0,20)])
                        gol.save()
                        #partit.events.add(gol)