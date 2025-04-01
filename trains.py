import re

import unidecode
from playwright.async_api import async_playwright, expect
import asyncio


async def main():
    browsers = ['chromium']
    async with async_playwright() as p:
        for browser_type in browsers:
            browser = await p[browser_type].launch(headless=False)
            page = await browser.new_page()
            await page.goto('https://wolnelektury.pl/katalog/nowe/')
            await refuse_help(page)

            for position in range(99, -1, -1):
                book = await page.query_selector(new_book_titles[position])
                result = dict()
                title_el = await book.query_selector('h2  a')
                result['title'] = await title_el.inner_text() if title_el else None
                author_el = await book.query_selector('h3  a')
                result['author'] = await author_el.inner_text() if author_el else None
                author_name = await author_el.inner_text() if author_el else None
                author_last_name = author_name.split()[-1].lower() if author_name else None
                title = await title_el.inner_text()
                title_ascii = unidecode.unidecode(title)
                title_clean = re.sub(r'[^a-zA-Z0-9 ]+', '', title_ascii)
                title_slug = title_clean.replace(" ", "-").lower()
                book_url = 'https://wolnelektury.pl/katalog/lektura/' + f'{author_last_name}' + '-' + f'{title_slug}' + '.html'
                with open('read_books.txt', 'r') as f:
                    content = f.read()
                    cover = await book.query_selector('figure a img')
                    if f'{title_clean}, {author_last_name}' not in content:
                        print(result)
                        print(book_url)
                        try:
                            await cover.click(timeout=2000)
                            await refuse_help(page)
                            await cover.click(timeout=2000)
                            with open('read_books.txt', 'a') as file:
                                file.write(
                                    f'{title_clean}, {author_last_name}\n'
                                )
                        except Exception as error:
                            print(error.__class__)
                    else:
                        print('Book read')

            translator_el = await page.query_selector(
                '.l-header__translators')
            translator = dict()
            translator['translator'] = await translator_el.inner_text() if translator_el else None
            print(translator)
            await refuse_help(page)
            read_all = await page.query_selector(
                'body > main > section.l-section.lay-s-col-rev > div > article > div.c-media > div.lay-row.lay-l-block.lay-spread > div > div.c-media__actions.lay-col.lay-l-row > div:nth-child(3) > a'
            )
            await read_all.click()
            await refuse_help(page)
            found_phrases = []
            for rail_phrase in train_phrases_iterator():
                result = dict()
                await refuse_help(page)
                train_phrase_paragraphs = await page.query_selector_all('.paragraph')
                for paragraph in train_phrase_paragraphs:
                    if rail_phrase in await paragraph.inner_text():
                        await refuse_help(page)
                        found_phrases.append(rail_phrase)
                result['train_phrase'] = found_phrases
                print(result)
            with open(f'{title}.txt', 'w') as file:
                file.write(
                    f'{title}, ' f'{author_name}, ' f'{translator}\n' f'Cała książka na: {book_url}\n'
                    f'{found_phrases}')


new_book_titles = ["#book-list article:nth-child(1)", "#book-list article:nth-child(2)",
                   "#book-list article:nth-child(3)",
                   "#book-list article:nth-child(4)", "#book-list article:nth-child(5)",
                   "#book-list article:nth-child(6)",
                   "#book-list article:nth-child(7)", "#book-list article:nth-child(8)",
                   "#book-list article:nth-child(9)",
                   "#book-list article:nth-child(10)", "#book-list article:nth-child(11)",
                   "#book-list article:nth-child(12)",
                   "#book-list article:nth-child(13)", "#book-list article:nth-child(14)",
                   "#book-list article:nth-child(15)",
                   "#book-list article:nth-child(16)", "#book-list article:nth-child(17)",
                   "#book-list article:nth-child(18)",
                   "#book-list article:nth-child(19)", "#book-list article:nth-child(20)",
                   "#book-list article:nth-child(21)",
                   "#book-list article:nth-child(22)", "#book-list article:nth-child(23)",
                   "#book-list article:nth-child(24)",
                   "#book-list article:nth-child(25)", "#book-list article:nth-child(26)",
                   "#book-list article:nth-child(27)",
                   "#book-list article:nth-child(28)", "#book-list article:nth-child(29)",
                   "#book-list article:nth-child(30)",
                   "#book-list article:nth-child(31)", "#book-list article:nth-child(32)",
                   "#book-list article:nth-child(33)",
                   "#book-list article:nth-child(34)", "#book-list article:nth-child(35)",
                   "#book-list article:nth-child(36)",
                   "#book-list article:nth-child(37)", "#book-list article:nth-child(38)",
                   "#book-list article:nth-child(39)",
                   "#book-list article:nth-child(40)", "#book-list article:nth-child(41)",
                   "#book-list article:nth-child(42)",
                   "#book-list article:nth-child(43)", "#book-list article:nth-child(44)",
                   "#book-list article:nth-child(45)",
                   "#book-list article:nth-child(46)", "#book-list article:nth-child(47)",
                   "#book-list article:nth-child(48)",
                   "#book-list article:nth-child(49)", "#book-list article:nth-child(50)",
                   "#book-list article:nth-child(51)",
                   "#book-list article:nth-child(52)", "#book-list article:nth-child(53)",
                   "#book-list article:nth-child(54)",
                   "#book-list article:nth-child(55)", "#book-list article:nth-child(56)",
                   "#book-list article:nth-child(57)",
                   "#book-list article:nth-child(58)", "#book-list article:nth-child(59)",
                   "#book-list article:nth-child(60)",
                   "#book-list article:nth-child(61)", "#book-list article:nth-child(62)",
                   "#book-list article:nth-child(63)",
                   "#book-list article:nth-child(64)", "#book-list article:nth-child(65)",
                   "#book-list article:nth-child(66)",
                   "#book-list article:nth-child(67)", "#book-list article:nth-child(68)",
                   "#book-list article:nth-child(69)",
                   "#book-list article:nth-child(70)", "#book-list article:nth-child(71)",
                   "#book-list article:nth-child(72)",
                   "#book-list article:nth-child(73)", "#book-list article:nth-child(74)",
                   "#book-list article:nth-child(75)",
                   "#book-list article:nth-child(76)", "#book-list article:nth-child(77)",
                   "#book-list article:nth-child(78)",
                   "#book-list article:nth-child(79)", "#book-list article:nth-child(80)",
                   "#book-list article:nth-child(81)",
                   "#book-list article:nth-child(82)", "#book-list article:nth-child(83)",
                   "#book-list article:nth-child(84)",
                   "#book-list article:nth-child(85)", "#book-list article:nth-child(86)",
                   "#book-list article:nth-child(87)",
                   "#book-list article:nth-child(88)", "#book-list article:nth-child(89)",
                   "#book-list article:nth-child(90)",
                   "#book-list article:nth-child(91)", "#book-list article:nth-child(92)",
                   "#book-list article:nth-child(93)",
                   "#book-list article:nth-child(94)", "#book-list article:nth-child(95)",
                   "#book-list article:nth-child(96)",
                   "#book-list article:nth-child(97)", "#book-list article:nth-child(98)",
                   "#book-list article:nth-child(99)",
                   "#book-list article:nth-child(100)"]


def train_phrases() -> list[str]:
    return [" pociąg", " kolej", " stacj", " dworzec", " dworcu", " przedział", " przedziale",
            " lokomotywa", " szyn", " konduktor", " maszynista", " tor", " żelazn", " nasyp",
            " przejazd", " wagon", " dróżnik", " dużurny ruchu", " dużurn",
            " tabor", " rozkład", " opóźnion", " opóźnien", " kuszetk", " sypialn", " osobow",
            " towarow", " pośpieszn",
            " ekspres", " przesiadk", " przesiad"]


def train_phrases_iterator() -> list[str]:
    for train_phrase in train_phrases():
        yield train_phrase


async def refuse_help(page):
    result = dict()
    decline_el = await page.query_selector(
        'a.annoy-banner-off'
    )
    if decline_el and await decline_el.is_visible():
        result['decline'] = await decline_el.inner_text() if decline_el else None
        await decline_el.click()
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
