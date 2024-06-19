LRE = "\u202A"
PDF = "\u202C"
SKIP_SEQUENCE = "xxxx"

LETTERS = "־אבגדהוזחטיכלמנסעפצקרשתךםןףץ"
TAAMIM_SYMBOLS_TO_NAMES = {
    "\u0591": "atnah",
    "\u0592": "segolta",
    "\u0593": "shalshelet",
    "\u0594": "zaqef_qaton",
    "\u0595": "zaqef_gadol",
    "\u0596": "tarha",
    "\u0597": "ravia",
    "\u0598": "zarqa",
    "\u0599": "pashta",
    "\u059A": "yetiv",
    "\u059B": "tevir",
    "\u059C": "gerish",
    "\u059E": "shene_gerishin",
    "\u059F": "karne_farah",
    "\u05A0": "tarsa",
    "\u05A1": "pazer_gadol",
    "\u05A2": "yareah_ben_yomo",
    "\u05A3": "shofar_holekh",
    "\u05A4": "shofar_mehupakh",
    "\u05A5": "maarikh",
    "\u05A6": "tere_taame",
    "\u05A7": "darga",
    "\u05A8": "qadma",
    "\u0599\u0599": "tere_qadmin",
    "\u05A9": "talsha",
    "\u05AA": "yareah_ben_yomo",
    "\u05AE": "zarqa",
    "\u05BD": "maamid",
    "\u05C0": "paseq",
    "\u05C3": "sof_passuq",
}
TAAMIM_NAMES_TO_SYMBOLS = {v: k for k, v in TAAMIM_SYMBOLS_TO_NAMES.items()}
TAAMIM_SYMBOLS = set(TAAMIM_SYMBOLS_TO_NAMES.keys())
TAAMIM_NAMES = set(TAAMIM_NAMES_TO_SYMBOLS.keys())
TAAME_MESHARET = {
    "maamid",
    "shofar_holekh",
    "shofar_mehupakh",
    "talsha",
    "maarikh",
    "darga",
    "qadma",
    "azla",
}
TAAM_ENGLISH_TO_HEBREW_NAMES = {
    "atnah": "אתנח",
    "segolta": "סגולתא",
    "shalshelet": "שלשלת",
    "zaqef_qaton": "זקף קטון",
    "zaqef_gadol": "זקף גדול",
    "tarha": "טרחא",
    "ravia": "רביע",
    "zarqa": "זרקא",
    "pashta": "פשתא",
    "yetiv": "יתיב",
    "tevir": "תביר",
    "gerish": "גריש",
    "shene_gerishin": "שני גרשין",
    "karne_farah": "קרני פרה",
    "tarsa": "תרסא",
    "pazer_gadol": "פזר גדול",
    "yareah_ben_yomo": "ירח בן יומו",
    "shofar_holekh": "שופר הולך",
    "shofar_mehupakh": "שופר מהופך",
    "maarikh": "מאריך",
    "tere_taame": "תרי טעמי",
    "darga": "דרגא",
    "qadma": "קדמא",
    "tere_qadmin": "תרי קדמין",
    "talsha": "טלשא",
    "sof_passuq": "סוף פסוק",
    "maamid": "מעמיד",
    "paseq": "פסק",
    "azla": "אזלא",
}
TAAM_HEBREW_TO_ENGLISH_NAMES = {v: k for k, v in TAAM_ENGLISH_TO_HEBREW_NAMES.items()}

NEQUDOT_SYMBOLS_TO_NAMES = {
    "\u05B0": "shva",
    "\u05B1": "hataf_segol",
    "\u05B2": "hataf_patah",
    "\u05B3": "hataf_qamats",
    "\u05B4": "hiriq",
    "\u05B5": "tsere",
    "\u05B6": "segol",
    "\u05B7": "patah",
    "\u05B8": "qamats",
    "\u05B9": "holam_haser",
    "\u05BB": "qubuts",
    "\u05BC": "dagesh",
    "\u05C1": "shin_dot",
    "\u05C2": "sin_dot",
    "\u05C4": "upper_dot",
}
NEQUDOT_NAMES_TO_SYMBOLS = {v: k for k, v in NEQUDOT_SYMBOLS_TO_NAMES.items()}
NEQUDOT_NAMES = set(NEQUDOT_NAMES_TO_SYMBOLS.keys())
NEQUDOT_SYMBOLS = set(NEQUDOT_SYMBOLS_TO_NAMES.keys())
