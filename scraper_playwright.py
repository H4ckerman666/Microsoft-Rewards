import asyncio
import random
import logging
import sys

from playwright.async_api import async_playwright

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("BingBot")

search_list = [
    "noticias de última hora",
    "cómo mejorar la memoria",
    "teoría de grafos aplicada",
    "ejercicios para fortalecer el core",
    "astronomía para principiantes",
    "novedades en inteligencia artificial",
    "mejor hardware para minar criptomonedas",
    "Sky-Watcher Explorer 130PDS opiniones",
    "mejor café del mundo",
    "historias de terror reales",
    "matemáticas avanzadas para análisis de datos",
    "cómo programar en Python",
    "ventajas y desventajas de una moto",
    "cómo dejar de procrastinar",
    "rutinas de gimnasio efectivas",
    "cómo hacer astrofotografía",
    "minería de Monero con GPU",
    "bancos de imágenes gratuitas",
    "últimos descubrimientos en astronomía",
    "qué telescopio comprar para astrofotografía",
    "cómo optimizar macros en Excel",
    "analista de datos freelance",
    "cursos gratuitos de ciencia de datos",
    "recomendaciones de series de ciencia ficción",
    "mejor música para concentración",
    "cuál es el mejor procesador para gaming",
    "cómo mejorar mi condición física",
    "técnicas para aprender inglés más rápido",
    "cómo configurar una GPU para minería",
    "los mejores ejercicios para espalda",
    "cuánto cuesta un telescopio para principiantes",
]
search_random_list = random.sample(search_list, len(search_list))


async def debug_page(page):
    await page.wait_for_timeout(5000)
    await page.screenshot(path="screenshot.png")


async def edge_search_bot_unique(page, search_list: list):
    logger.info("Iniciando el bot de búsqueda de Bing...")
    await page.goto("https://www.bing.com/")
    logger.info("Esperando a que se cargue la página...")
    await page.wait_for_load_state("networkidle")
    # await debug_page(page)
    logger.info("Esperando a que se cargue el cuadro de búsqueda...")
    await page.wait_for_selector("#sb_form_q", state="visible")
    search_bar = page.locator("#sb_form_q")

    for search in search_list:
        logger.info(f"Buscando: {search}")
        typed = search[random.randint(0, len(search) - 1) :]
        await search_bar.fill(typed)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(8000)


async def edge_reward_cards(page, xpath: str):
    await page.goto("https://rewards.bing.com/?ref=rewardspanel")
    await page.wait_for_timeout(5000)

    cards = await page.query_selector(xpath)
    if not cards:
        print(f"No se encontró el contenedor: {xpath}")
        return

    children = await cards.query_selector_all(":scope > *")
    for child in children:
        try:
            print(await child.inner_text())
            await child.click()
            await page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Error al hacer clic: {e}")


async def main():
    async with async_playwright() as p:

        logger.info("Configurando el navegador...")
        browser = await p.chromium.launch_persistent_context(
            channel="msedge",
            # user_data_dir="/home/yisus/.config/microsoft-edge-automation",
            user_data_dir="microsoft-edge-automation",
            headless=True,
            viewport={"width": 1920, "height": 1080},
        )  # O True para oculto

        page = browser.pages[0]
        await page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => false })"
        )
        await edge_search_bot_unique(page, search_random_list)
        await edge_reward_cards(page, '//*[@id="daily-sets"]/mee-card-group[1]/div')
        await edge_reward_cards(page, '//*[@id="more-activities"]/div')

        # await browser.close()


if __name__ == "__main__":
    logger.info("Iniciando el bot de Bing...")
    asyncio.run(main())
