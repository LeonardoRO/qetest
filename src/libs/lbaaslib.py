# lbaaslib.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import random
import time
import string

import qetest.src.libs.sellib as sellib

def setup(driver, all_loggers, retrydict, sleepdict,):
    failed = load_balancers_reset(driver, all_loggers, retrydict, sleepdict)

    return failed

def load_balancers_reset(driver, all_loggers, retrydict, sleepdict):
    """
    Reset by reloading the page and clicking on the 'all nodes' link.
    
    Args:
        driver: object - WebDriver instance.
        all_loggers: tuple - Contains all logging objects.
        retrydict: dictionary - Contains current retry count and max retry count.
        sleepdict: dictionary - Universal sleep value (float) and "fast" on/off (boolean).

    Returns:
        Boolean "failed" (if True, test failed).
    """

    failed = True
    with sellib.error_handler(driver, all_loggers, retrydict,
                              'Unable to reset Overview page'):
        driver.refresh()
        sellib.element_wait(driver.find_element_by_link_text, 'Load Balancers', element_action='click')
        sellib.sleeper(sleepdict)
        failed = False

    return failed

def go_to_lbaas(driver):
    """
    Click on the top Add Server button.

    Args:
        driver: object - WebDriver instance.
    """

    path = '//div[@id="nav"]/descendant::li[@class="load_balancers"]'
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='click')

def sort_by_name_asc(driver):
    """
    Click on the Name header and sort load balancers by name

    Args:
        driver: object - WebDriver instance.
    """

    path = '//div[@class="data_table_header"]/descendant::div[@class="data_table_cell name"]'
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='click')

def sort_by_name_desc(driver):
    """
    Click on the Name header and sort load balancers by name

    Args:
        driver: object - WebDriver instance.
    """
    path = '//div[@class="data_table_header"]/descendant::div[@class="data_table_cell name sorted_asc"]'
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='click')

def sort_by_protocol_port_asc(driver):
    """
    Click on the Name header and sort load balancers by Protocol/Port

    Args:
        driver: object - WebDriver instance.
    """

    path = '//div[@class="data_table_header"]/descendant::div[@class="data_table_cell protocol_port"]'
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='click')

def sort_by_protocol_port_desc(driver):
    """
    Click on the Name header and sort load balancers by Protocol/Port

    Args:
        driver: object - WebDriver instance.
    """

    path = '//div[@class="data_table_header"]/descendant::div[@class="data_table_cell protocol_port sorted_asc"]'
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='click')


def add_load_balancer_top(driver):
    """
    Click on the top Add Load Balancer button.

    Args:
        driver: object - WebDriver instance.
    """

    path = '//div[@id="content_header"]/descendant::button[@class="add_load_balancer_button"]'
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='click')

def get_load_balancers(driver):
    """
    Find all load balancers on a page.

    Args:
        driver: object - WebDriver instance.

    Returns:
        List of node elements
    """

    load_balancer_elements = sellib.elements_wait(driver, '//div[@class="data_table_row"]')

    return load_balancer_elements

def get_loadbalancersid_list(driver):
    """
    Find all load balancers IDs on a page.

    Args:
        driver: object - WebDriver instance.

    Returns:
        List of node IDs
    """

    loadbalancers_elements = get_load_balancers(driver)
    loadbalancersid_list = [element.get_attribute('data-model_id') for element in loadbalancers_elements]

    return loadbalancersid_list

def find_load_balancers_id_by_nodename(driver, loadbalancer_name):
    """
    Find the load balancer ID using the load balancer name.

    Args:
        driver: object - WebDriver instance.
        nodename: string - node (server) name

    Returns:
        A string which is the node's ID
    """

    path = ('//div[contains(text(), "%s")]/ancestor::div[@class="data_table_row"]' % loadbalancer_name)
    loadbalancer_element = sellib.element_wait(driver.find_element_by_xpath, path)
    loadbalancerid = loadbalancer_element.get_attribute('data-model_id')

    return loadbalancerid

def get_load_balancer_name(driver, loadbalancerid):

    namepath = ('//div[@class="data_table_row" and @data-model_id="%s"]/descendant::div[@class='
                '"data_table_cell name"]' % loadbalancerid)
    loadbalancername = sellib.element_wait(driver.find_element_by_xpath(namepath).text)

    return loadbalancername

def random_load_balancer(driver):

    path = ('//div[@class="data_table_body"]/descendant::div[@class="data_table_cell name"]')

    time.sleep(10)
    lbaas_elements = sellib.elements_wait(driver, path)
    lbaas = random.choice(lbaas_elements)
    sellib.element_wait(lbaas, element_action='click')
    #TODO: use this return to make sure the correct page is displayed
    #return lbaas.text

def get_random_name():
    namelist = ['thunderstruck', 'moneytalks', 'hellsbells', 'ballbreaker', 'heatseeker']
    random_name = '%s-%s' % (random.choice(namelist),
                             ''.join(random.sample(string.letters + string.digits, 8)))
    return random_name

def click_load_balancer_by_name(driver, loadbalancer_name):

    path = ('//div[contains(text(), "%s")]/ancestor::div[@class="data_table_row"]' % loadbalancer_name)
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='click')