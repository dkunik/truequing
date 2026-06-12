from django.core.management.base import BaseCommand

from core.models import Coleccion, Pais, Figurita


PAISES = [
    ("Argentina", "ARG"),
    ("Alemania", "GER"),
    ("Argelia", "ALG"),
    ("Arabia Saudita", "KSA"),
    ("Australia", "AUS"),
    ("Austria", "AUT"),
    ("Bélgica", "BEL"),
    ("Bosnia y Herzegovina", "BIH"),
    ("Brasil", "BRA"),
    ("Canadá", "CAN"),
    ("Cabo Verde", "CPV"),
    ("Colombia", "COL"),
    ("Corea del Sur", "KOR"),
    ("Croacia", "CRO"),
    ("Curaçao", "CUW"),
    ("República Checa", "CZE"),
    ("República Democrática del Congo", "COD"),
    ("Ecuador", "ECU"),
    ("Egipto", "EGY"),
    ("España", "ESP"),
    ("Estados Unidos", "USA"),
    ("Francia", "FRA"),
    ("Ghana", "GHA"),
    ("Haití", "HAI"),
    ("Inglaterra", "ENG"),
    ("Irán", "IRN"),
    ("Iraq", "IRQ"),
    ("Japón", "JPN"),
    ("Jordania", "JOR"),
    ("Marruecos", "MAR"),
    ("México", "MEX"),
    ("Noruega", "NOR"),
    ("Nueva Zelanda", "NZL"),
    ("Países Bajos", "NED"),
    ("Panamá", "PAN"),
    ("Paraguay", "PAR"),
    ("Portugal", "POR"),
    ("Qatar", "QAT"),
    ("Escocia", "SCO"),
    ("Senegal", "SEN"),
    ("Sudáfrica", "RSA"),
    ("Suecia", "SWE"),
    ("Suiza", "SUI"),
    ("Túnez", "TUN"),
    ("Turquía", "TUR"),
    ("Uruguay", "URU"),
    ("Uzbekistán", "UZB"),
    ("Costa de Marfil", "CIV"),
]


class Command(BaseCommand):
    help = "Inicializa la colección Mundial 2026 con países y figuritas"

    def handle(self, *args, **options):
        figuritas_por_pais = 20

        coleccion, _ = Coleccion.objects.get_or_create(
            nombre="Mundial 2026",
            defaults={
                "descripcion": "Álbum de figuritas del Mundial 2026",
            },
        )

        for nombre_pais, codigo in PAISES:
            pais, _ = Pais.objects.get_or_create(
                coleccion=coleccion,
                codigo=codigo,
                defaults={
                    "nombre": nombre_pais,
                },
            )

            for numero in range(1, figuritas_por_pais + 1):
                Figurita.objects.get_or_create(
                    coleccion=coleccion,
                    pais=pais,
                    numero=numero,
                    defaults={
                        "nombre": None,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS("Colección Mundial 2026 inicializada correctamente")
        )
