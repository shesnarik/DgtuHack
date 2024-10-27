import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def lemmatize(text):
    words = text.split()
    return [morph.parse(word)[0].normal_form for word in words]

my_list_str = {
    "тариф": ["изменение тарифа", "поменять тариф", "сменить тариф","изменить тариф","смена тарифа"],
    "услуга": ["подключить услугу","подключение услуги", "добавить услугу","добавление услуги", "услуга"],
    "договор": ["заключить договор", "оформить договор", "договор", "расторгнуть договор"]
}

def detect_intent(text, intents):
    lemmas = lemmatize(text)
    for intent, keywords in my_list_str.items():
        if any(keyword in lemmas for keyword in keywords):
            return intent
    return "неопределено"