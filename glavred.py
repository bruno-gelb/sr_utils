from collections import OrderedDict
from pprint import pprint

PAGES = 104
MIN_PAGES_AMOUNT = 4


def get_lit_rate(beginning):
    variants = {
        'Я ждал этой': '3. Очень плохо',
        'После того, как': '4. Плохо',
        'В игру': '5. Терпимо',
        'Привет, девочки': '6. Удовлетворительно',
        'В нашей загадочной': '7. Неплохо',
        'Едва мы проглотили': '8. Хорошо',
        'Такого не мог': '9. Отлично',
        'Тяжело': '10. Великолепно! Полный отпад!!!',
    }

    rate = variants.get(beginning)
    return rate


def _get_news_priority(query_string):
    variants = {
        'Смешно выглядела':
            {'rubric': 'Юмор',
             'region': 'Дун-Дук'},
        'Слухи о враждебных':
            {'rubric': 'Железо',
             'region': 'Шакиш-Ма'},
        'О чём спорят в':
            {'rubric': 'Новости',
             'region': 'Дун-Дук'},
        'Разнообразие в провинции':
            {'rubric': 'Внекомпьютерные Игры',
             'region': 'Йопт'},
        'Функционер заставил задуматься':
            {'rubric': 'Новости',
             'region': 'Хали-Гали'},
        'В Анан-Усе':
            {'rubric': 'Новости',
             'region': 'Анан-Ус'},
        'Поэма из':
            {'rubric': 'Игрострой',
             'region': 'Хали-Гали'},
        'Разборки в компьютерном':
            {'rubric': 'Рецензии',
             'region': 'Дерде-Кефир'},
        'Новости из Дун-Дука':
            {'rubric': 'Новости',
             'region': 'Дун-Дук'},
        'Самоубийство на почве':
            {'rubric': 'Игрострой',
             'region': 'Хали-Гали'},
    }
    priority = variants.get(query_string)
    return priority


def calc_rubriс_distribution(news_priority, artist_rate):
    NEWS_PRIORITY_RUBRIC_PAGES = 8 * MIN_PAGES_AMOUNT

    def _get_complementary_rubric(rubric):
        return {
            'Новости': 'Железо',
            'Железо': 'Новости',

            'Рецензии': 'Внекомпьютерные игры',
            'Внекомпьютерные игры': 'Рецензии'
        }.get(rubric, None)

    distribution = OrderedDict({
        'Новости': MIN_PAGES_AMOUNT,
        'Железо': MIN_PAGES_AMOUNT,
        'Рецензии': MIN_PAGES_AMOUNT,
        'Внекомпьютерные игры': MIN_PAGES_AMOUNT,
        'Игрострой': MIN_PAGES_AMOUNT,
        'Юмор': MIN_PAGES_AMOUNT
    })

    complementary_rubric = _get_complementary_rubric(news_priority['rubric'])

    distribution['Юмор'] = 6 * MIN_PAGES_AMOUNT

    distribution.pop(news_priority['rubric'], None)
    distribution.pop(complementary_rubric, None)

    rubrics_to_iterate = list(
        filter(lambda x: x not in [news_priority['rubric'], complementary_rubric], distribution.keys()))

    while sum(distribution.values()) != PAGES - NEWS_PRIORITY_RUBRIC_PAGES - MIN_PAGES_AMOUNT:
        min_rubric = min(distribution, key=distribution.get)
        distribution[min_rubric] += MIN_PAGES_AMOUNT

    if news_priority['rubric'] == 'Юмор':  # ¯\_(ツ)_/¯
        min_rubric = min(distribution, key=distribution.get)
        distribution[min_rubric] += MIN_PAGES_AMOUNT

    distribution[news_priority['rubric']] = NEWS_PRIORITY_RUBRIC_PAGES
    if complementary_rubric:
        distribution[complementary_rubric] = MIN_PAGES_AMOUNT

    # assert sum(distribution.values()) == PAGES, 'Something wrong with rubriс distribution'
    return distribution


def calc_circulation(news_priority, amount, pr_credits, artist_rate):
    # todo first of all, distribute 10% per population to each city / town
    POPULATION = OrderedDict({
        'Дун-Дук': 35000,
        'Мунь-Чунь': 25000,

        'Шакиш-Ма': 10000,
        'Йопт': 5000,
        'Дерде-Кефир': 5000,
        'Анан-Ус': 5000,
        'Хали-Гали': 10000
    })

    pr = {
        0: 1,
        500: 1,
        1000: 1.2,
        2000: 1.5,
        3000: 2.0
    }.get(pr_credits)

    city_koeff = 0.22 if artist_rate >= 3 else 0.0
    town_koeff = 0.2

    max_circulation_per_city = OrderedDict({
        'Дун-Дук': int(POPULATION['Дун-Дук'] * city_koeff * pr),
        'Мунь-Чунь': int(POPULATION['Мунь-Чунь'] * city_koeff * pr),

        'Шакиш-Ма': int(POPULATION['Шакиш-Ма'] * town_koeff * pr),
        'Йопт': int(POPULATION['Йопт'] * town_koeff * pr),
        'Дерде-Кефир': int(POPULATION['Дерде-Кефир'] * town_koeff * pr),
        'Анан-Ус': int(POPULATION['Анан-Ус'] * town_koeff * pr),
        'Хали-Гали': int(POPULATION['Хали-Гали'] * town_koeff * pr),
    })

    max_circulation_per_city[news_priority['region']] *= 2.5

    circulation = OrderedDict({})
    circulation_left = amount
    for city, max_circulation in max_circulation_per_city.items():
        if circulation_left < 0:
            break

        if not circulation_left:
            break

        circulation_chunk = max_circulation
        circulation_left -= circulation_chunk

        if circulation_left < 0:
            delta = circulation_left
            circulation_chunk += delta

        circulation.update({city: circulation_chunk})

    # assert sum(circulation.values()) == amount, 'Something wrong with circulation'
    return circulation


# todo use click to write a CLI instead
news_priority = _get_news_priority('Разнообразие в провинции')
artist_rate = 10
amount = 4000
pr_credits = 1000

rubric_distribution = calc_rubriс_distribution(news_priority, artist_rate)
pprint(rubric_distribution)

circulation = calc_circulation(news_priority, amount=amount,
                               pr_credits=pr_credits, artist_rate=artist_rate)
pprint(circulation)
