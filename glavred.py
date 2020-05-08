from collections import OrderedDict
from pprint import pprint

PAGES = 104
MIN_PAGES_AMOUNT = 4

POPULATION = OrderedDict({
    'Дун-Дук': 35000,
    'Мунь-Чунь': 25000,

    'Шакиш-Ма': 10000,
    'Йопт': 5000,
    'Дерде-Кефир': 5000,
    'Анан-Ус': 5000,
    'Хали-Гали': 10000
})


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
            {'rubric': 'Внекомпьютерные игры',
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
        'Самоубийство':
            {'rubric': 'Игрострой',
             'region': 'Хали-Гали'},
        'Жаркое заседание':
            {'rubric': 'Внекомпьютерные игры',
             'region': 'Йопт'},
    }
    priority = variants.get(query_string)
    return priority


def calc_rubriс_distribution(news_priority):
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

    if sum(distribution.values()) < PAGES:
        min_rubric = min(distribution, key=distribution.get)
        distribution[min_rubric] += PAGES - sum(distribution.values())

    assert sum(distribution.values()) == PAGES, \
        f'Something went wrong with rubric distribution, {sum(distribution.values())} != {PAGES}'
    return distribution


def calc_circulation(news_priority, amount, pr_credits, artist_rate):
    pr_koeff = {
        0: 1,
        500: 1,
        1000: 1.2,
        2000: 1.5,
        3000: 2.0
    }.get(pr_credits)

    initial_koeff = 0.143  # tweak this in case circulation went wrong
    city_initial_koeff = initial_koeff * pr_koeff if artist_rate >= 3 else 0.0
    town_initial_koeff = initial_koeff * pr_koeff

    max_circulation_per_city = OrderedDict({
        'Дун-Дук': int(POPULATION['Дун-Дук'] * city_initial_koeff),
        'Мунь-Чунь': int(POPULATION['Мунь-Чунь'] * city_initial_koeff),

        'Шакиш-Ма': int(POPULATION['Шакиш-Ма'] * town_initial_koeff),
        'Йопт': int(POPULATION['Йопт'] * town_initial_koeff),
        'Дерде-Кефир': int(POPULATION['Дерде-Кефир'] * town_initial_koeff),
        'Анан-Ус': int(POPULATION['Анан-Ус'] * town_initial_koeff),
        'Хали-Гали': int(POPULATION['Хали-Гали'] * town_initial_koeff),
    })

    max_circulation_per_city[news_priority['region']] *= 2.5

    circulation = OrderedDict({})
    circulation_left = amount
    for city, city_max_circulation in max_circulation_per_city.items():
        if circulation_left <= 0:
            break

        circulation_chunk = city_max_circulation
        circulation_left -= circulation_chunk

        if circulation_left < 0:
            delta = circulation_left
            circulation_chunk += delta

        circulation.update({city: circulation_chunk})

    assert sum(circulation.values()) == amount, \
        f'Something wrong with circulation: {sum(circulation.values())} != {amount}'
    return circulation


# todo use click to write a CLI instead
news_headline = 'Слухи о враждебных'
artist_rate = 7
amount = 31000
pr_credits = 3000

news_priority = _get_news_priority(news_headline)

rubric_distribution_suggest = calc_rubriс_distribution(news_priority)
pprint(rubric_distribution_suggest)

circulation_suggest = calc_circulation(news_priority, amount=amount,
                                       pr_credits=pr_credits, artist_rate=artist_rate)
pprint(circulation_suggest)
