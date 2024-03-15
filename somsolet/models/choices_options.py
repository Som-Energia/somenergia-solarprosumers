from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectStatus(models.TextChoices):
    EMPTY_STATUS = ("empty status", _("Initial"))
    PREREGISTERED = ("preregistered", _("Pre-Registered"))
    REGISTERED = ("registered", _("Registered"))
    DATA_DOWNLOADED = ("data downloaded", _("CCH data downloaded for analysis"))
    TECHINICAL_VISIT = ("technical visit", _("Technical visit scheduled"))
    PREREPORT_REVIEW = ("prereport review", _("Pre-Report review"))
    PREREPORT = ("prereport", _("Pre-Report uploaded"))
    REPORT_REVIEW = ("report review", _("Report review"))
    REPORT = ("report", _("Report uploaded"))
    OFFER = ("offer", _("Engineering offer"))
    OFFER_REVIEW = ("offer review", _("offer Review"))
    SIGNATURE = ("signature", _("Contract signature"))
    CONSTRUCTION_PERMIT = ("construction permit", _("Construction permit"))
    PENDING_INSTALLATION_DATE = (
        "pending installation date",
        _("Pending installation date"),
    )
    DATE_INSTALLATION_SET = ("date installation set", _("Date installation set"))
    INSTALLATION_IN_PROGRESS = (
        "installation in progress",
        _("Installation in progress"),
    )
    END_INSTALLATION = ("end installation", _("End installation"))
    LEGAL_REGISTRATION = ("legal registration", _("Legal Registration"))
    LEGALIZATION = ("legalization", _("Legalization"))
    FINAL_PAYMENT = ("final payment", _("Final payment"))
    WARRANTY_PAYMENT = ("warranty payment", _("Warranty payment"))
    DISCARDED = ("discarded", _("Discarded"))


ITEM_WARNINGS = (
    ("No Warn", _("---")),
    ("Not Payed", _("Warning: Not payed")),
    ("prereport", _("Warning: Waiting for prereport")),
    ("technical visit", _("Warning: Waiting for technical visit")),
    ("report", _("Warning: Waiting for report")),
    ("offer", _("Warning: Waiting for offer")),
    ("signature", _("Warning: Waiting for signature")),
    ("installation date", _("Warning: Waiting for installation date")),
    ("finish installation", _("Warning: Installation deadline has passed")),
    ("legal registration", _("Warning: Pending registration reciept")),
    ("legalization", _("Warning: Waiting for legalization certificates")),
    ("final payment", _("Warning: Pending engineering payment")),
    ("warranty payment", _("Warning: Pending warranty payment")),
)

ITEM_DISCARDED_TYPES = (
    ("Not discarded", _("---")),
    ("technical", _("technical")),
    ("voluntary", _("voluntary")),
)

ITEM_COMMUNITY = (
    ("empty", _("---")),
    ("And", _("Andalucía")),
    ("Ar", _("Aragón")),
    ("Ast", _("Principado Asturias")),
    ("Bal", _("Islas Baleares")),
    ("Can", _("Canarias")),
    ("Cantb", _("Cantabria")),
    ("Cast-Man", _("Castilla-La Mancha")),
    ("Cast Leo", _("Castila y León")),
    ("Cat", _("Cataluña")),
    ("Ceuta", _("Ceuta")),
    ("Ext", _("Extremadura")),
    ("Gal", _("Galicia")),
    ("Val", _("Comunidad Valenciana")),
    ("Mad", _("Communidad de Madrid")),
    ("Melilla", _("Melilla")),
    ("Mur", _("Región de Murcia")),
    ("Nav", _("Comunidad Foral de Navarra")),
    ("Rio", _("La Rioja")),
    ("Vasc", _("País Vasco")),
)

ITEM_ORIENTATION = (
    ("empty", _("---")),
    ("N", _("North")),
    ("NNE", _("North-northeast")),
    ("NE", _("Northeast")),
    ("ENE", _("East-northeast")),
    ("E", _("East")),
    ("ESE", _("East-southeast")),
    ("SE", _("Southeast")),
    ("SSE", _("South-southeast")),
    ("S", _("South")),
    ("SSW", _("South-southwest")),
    ("SW", _("Southwest")),
    ("WSW", _("West-southwest")),
    ("W", _("West")),
    ("WNW", _("West-northwest")),
    ("NW", _("Northwest")),
    ("NNW", _("North-northwest")),
)

ITEM_ANGLES = (
    (0, 0),
    (15, 15),
    (30, 30),
    (45, 45),
    (60, 60),
    (75, 75),
    (90, 90),
    (105, 105),
    (120, 120),
    (135, 135),
    (150, 150),
    (165, 165),
    (180, 180),
)

ITEM_VOLTAGE = (
    ("empty", _("---")),
    ("1P", _("single-phase")),
    ("2P", _("two-phase")),
    ("3P", _("three-phase")),
)

PANELS_BRAND = (
    ("empty", _("---")),
    ("REC", _("REC")),
    ("JA SOLAR", _("JA SOLAR")),
    ("JINKO", _("JINKO")),
    ("SOLARWATT", _("SOLARWATT")),
    ("PEIMAR", _("PEIMAR")),
    ("LUBI", _("LUBI")),
    ("ATERSA", _("ATERSA")),
    ("SUNPOWER", _("SUNPOWER")),
    ("C-SUN", _("C-SUN")),
    ("NOUSOL", _("NOUSOL")),
    ("SHARP", _("SHARP")),
    ("YINGLI", _("YINGLI")),
)

PANELS_TYPE = (
    ("empty", _("---")),
    ("CRISTAL", _("CRISTAL")),
    ("OTRO", _("OTRO")),
)

INVERSOR_BRAND = (
    ("empty", _("---")),
    ("SMA", _("SMA")),
    ("HUAWEI", _("HUAWEI")),
    ("FRONIUS", _("FRONIUS")),
    ("KOSTAL", _("KOSTAL")),
    ("VICTRON", _("VICTRON")),
    ("ENPHASE", _("ENPHASE")),
)

BATERY_BRAND = (
    ("empty", _("---")),
    ("SONNEN", _("SONNEN")),
    ("BYD", _("BYD")),
    ("AMPERE", _("AMPERE")),
    ("LG", _("LG")),
    ("TESLA", _("TESLA")),
)

LANGUAGES = (
    ("es", _("Spanish")),
    ("ca", _("Catalan")),
    ("gl", _("Galician")),
    ("eu", _("Euskara")),
)
