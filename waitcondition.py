from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC


class wait_for_text_to_exist(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element_text = EC._find_element(driver, self.locator).get_attribute("innerHTML")
            if (len(element_text) > 0):
                return element_text
            else:
                return False
        except StaleElementReferenceException:
            return False
