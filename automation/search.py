import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO)


class AutomationSearchProduct:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome(service=self.service)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def search_product(self, specific_product, site_domain="https://www.ikesaki.com.br/"):
        """
        Objective:
        Search the domain website for the specific product
        through automation, and click on the first corresponding product.

        Parameters:
        site_domain = "https://www.ikesaki.com.br/"
        product = "Esmalte Vermelho"
        """
        self.start_driver()

        self.driver.get(site_domain)
        time.sleep(2)
        search_box = self.driver.find_element('xpath', '//*[@id="downshift-0-input"]')
        search_box.send_keys(specific_product, Keys.ENTER)
        time.sleep(5)

        html_content = self.driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        gallery_div = soup.find('div', {'id': 'gallery-layout-container'})
        if gallery_div:
            first_img = gallery_div.find('img')
            if first_img:
                img_element = self.driver.find_element('xpath',
                                                       '//*[@id="gallery-layout-container"]/div/section/a/article'
                                                       '/div[1]/div[1]/div/div/img')

                img_element.click()

                time.sleep(3)

                if self.driver.current_url != site_domain:
                    print("Redirecionado para:", self.driver.current_url)
                else:
                    print("Não houve redirecionamento após clicar na imagem.")

        time.sleep(5)
        current_url = self.driver.current_url

        self.stop_driver()

        return current_url

    def search_product_all(self, generic_product, site_domain="https://www.ikesaki.com.br/"):
        self.start_driver()

        try:
            self.driver.get(site_domain)
            time.sleep(2)

            # Run the search
            search_box = self.driver.find_element(By.XPATH, '//*[@id="downshift-0-input"]')
            search_box.send_keys(generic_product, Keys.ENTER)
            time.sleep(5)

            current_url_all = []
            while True:
                html_content = self.driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                gallery_div = soup.find('div', {'id': 'gallery-layout-container'})

                if not gallery_div:
                    break

                # Retrieves all and entire search results
                img_elements = gallery_div.find_all('img')
                for i, img in enumerate(img_elements, start=1):
                    img_xpath = (f'//*[@id="gallery-layout-container"]/div[{i}]/section/a/article/div[1]/div['
                                 f'1]/div/div/img')

                    # Find and click on each result
                    try:
                        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, img_xpath)))
                        img_element = self.driver.find_element(By.XPATH, img_xpath)
                        self.driver.execute_script("arguments[0].click();", img_element)  # Solving problem of
                        # intercepted elements
                        time.sleep(3)
                    except TimeoutException as e:
                        print(f"Erro ao clicar na imagem: Tempo de execução limite {e}")
                        logging.error("O elemento foi encontrado, mas não se tornou visivel dentro do tempo limite.")
                        continue
                    except NoSuchElementException as e:
                        print(f"Erro ao clicar na imagem: Imagem não encontrada {e}.")
                        logging.error("O elemento não foi encontrado.")
                        continue

                    # Checking redirection to each specific result page
                    if self.driver.current_url != site_domain:
                        print("Redirecionado para:", self.driver.current_url)
                        current_url_all.append(self.driver.current_url)
                    else:
                        print("Não houve redirecionamento após clicar na imagem.")

                    # Returning to the page that lists the image of all products
                    self.driver.back()
                    time.sleep(2)

                # Proceed with the results on the next page if they exist
                try:
                    next_page_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div['
                                                                          '2]/div/div[2]/section/div[2]/div/div['
                                                                          '2]/div/div[2]/div/div['
                                                                          '7]/div/div/div/div/div/a/div')
                    if next_page_button.get_attribute('aria-disabled') == 'true':
                        break
                    else:
                        next_page_button.click()
                        time.sleep(5)
                except NoSuchElementException:
                    print("Não há mais páginas para percorrer.")
                    break

        finally:
            self.stop_driver()

        return current_url_all
