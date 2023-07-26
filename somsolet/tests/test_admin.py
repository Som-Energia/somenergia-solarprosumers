import pytest
import tablib

from somsolet.admin import ProjectResource


@pytest.fixture
def raw_import_data():
    return {
        "Idioma": "es",
        "Data pagament 150 euros": "21/06/2023",
        "Número factura 150 euros": "2023/0611",
        "CCH passades?": "",
        "Codi Instal·lació": "SPP215",
        "Número de soci/a de Som Energia": "29112",
        "Nom i cognoms": "Sol Radiante Abrasador",
        "Número de DNI": "74483385R",
        "Correu electrònic": "solradianteabrasador@somenergia.coop",
        "Telèfon de contacte": "0010968711",
        "Municipi": "Girona",
        "Adreça": "Plaça de les olles 2, 3er 2a",
        "Número de contracte amb Som Energia": "no",
        "CUPS - Codi Unificat del Punt de Subministrament": "ES0390702063159022QF",
        "Tarifa d'accès": "2.0TD",
        "Selecciona l'ús anual d'electricitat d'aquest habitatge o local": "Entre 2.500 y 4.000 kWh/año",
        "Tipus d'instal·lació": "4,6",
        "Model monofàsic triat": "Monofásica Ampliada",
        "Model trifàsic triat": "",
        "Estic interessat en adquirir": "Medidor de energía inteligente, Optimizadores de sombras",
        "COMENTARIOS": "disponibilidad para recibir la visita técnica es a partir del 13 de julio. ",
        "Autorització cessió de dades": "Autorizo \u200b\u200bla cesión de mis datos de contacto a Ubora Autoconsumo SL por las gestiones y comunicaciones relacionadas con esta compra colectiva",
        "campanya": "Solaquen placa placa",
    }


@pytest.fixture
def project_import_data(raw_import_data):

    dataset = tablib.Dataset(headers=raw_import_data.keys())
    dataset.append(raw_import_data.items())
    return dataset


class TestProjectImport:
    @pytest.mark.django_db
    def test__full_project_import__ok(self, project_import_data, mailoutbox):
        result = ProjectResource().import_data(project_import_data, dry_run=False)

        assert not result.has_errors()
