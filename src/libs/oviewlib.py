# oviewlib.py

__author__ = 'Leonardo Oliveira (leonardo.ribeirooliv@rackspace.com)'

import random
import string
import time

import qetest.src.libs.sellib as sellib

def setup(driver, all_loggers, retrydict, sleepdict,):
    failed = overview_reset(driver, all_loggers, retrydict, sleepdict)

    return failed

def overview_reset(driver, all_loggers, retrydict, sleepdict):
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
        sellib.element_wait(driver.find_element_by_link_text, 'all nodes', element_action='click')
        sellib.sleeper(sleepdict)
        failed = False

    return failed

def add_server_button_top(driver):
    """
    Click on the top Add Server button.

    Args:
        driver: object - WebDriver instance.
    """

    path = '//div[@id="content_header"]/descendant::button[@class="add_server_button"]'
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='click')

def add_server_button_bottom(driver):
    """
    Click on the bottom Add Server button.

    Args:
        driver: object - WebDriver instance.
    """

    path = '//div[@class="buttons"]/descendant::button[@class="add_server_button"]'
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='click')

def get_server_name_list():

    return ['knucklehead', 'jughead', 'meathead']

def add_server_name(driver, name=None):
    """
    Input the new server's name.
    
    Args:
        driver: object - WebDriver object.
        name: string - Name to be assigned to node.  If None, a random name is generated.

    Returns:
        random_name: string - server's name if randomly generated
    """

    if not name:
        namelist = get_server_name_list()
        random_name = '%s-%s' % (random.choice(namelist),
                                 ''.join(random.sample(string.letters + string.digits, 8)))
        name = random_name
     
    path = '//input[@class="name1"]'
    sellib.element_wait(driver.find_element_by_xpath, path, element_action='send_keys',
                        action_arg=name)

    if random_name: return random_name

def add_server_os(driver):
    """
    Find the list of OS flavors and randomly select one.
    
    Args:
        driver: object - WebDriver object.

    Returns:
        server_os.text: string - text value associated with the OS element randomly selected.
    """

    path = ('//div[@class="rebuild_container"]/descendant::div[@class="ck-widgets-split-menuitem-'
            'section ck-widgets-split-menuitem-section-0"]')
    time.sleep(10)
    os_flavor_elements = sellib.elements_wait(driver, path)
    server_os = random.choice(os_flavor_elements)
    sellib.element_wait(server_os, element_action='click')

    return server_os.text

def add_server_size(driver):
    """
    Find the list of server sizes and randomly select one.
    
    Args:
        driver: object - WebDriver object.

    Returns:
        server_size.text: string - text value associated with the size element randomly selected.
    """

    path = ('//div[@class="resize-panel panel_menu"]/descendant::div[@class="ck-widgets-split-'
            'menuitem-section ck-widgets-split-menuitem-section-0"]')
    size_flavor_elements = sellib.elements_wait(driver, path)
    server_size = random.choice(size_flavor_elements)
    server_size.click()

    return server_size.text

def add_server(driver, all_loggers, sleepdict):
    logger = all_loggers[0]
    add_server_button_top(driver)
    logger.debug('Clicked on the top Add Server button')
    sellib.sleeper(sleepdict)
    # Assign a server name
    server_name = add_server_name(driver) 
    logger.debug('Added server name "%s"' % server_name)
    sellib.sleeper(sleepdict)
    # Pick a random OS
    os_flavor = add_server_os(driver)
    logger.debug('Picked "%s" for the OS flavor' % os_flavor)
    sellib.sleeper(sleepdict)
    # Pick a random size
    server_size = add_server_size(driver) 
    logger.debug('Picked "%s" for server size' % server_size)
    sellib.sleeper(sleepdict)
    #Submit it
    add_server_button_bottom(driver)
    logger.debug('Clicked the bottom Add Server button to submit') 
    sellib.sleeper(sleepdict)

    return server_name, os_flavor, server_size

def get_nodes(driver):
    """
    Find all nodes (servers) on a page.

    Args:
        driver: object - WebDriver instance.

    Returns:
        List of node elements
    """

    node_elements = sellib.elements_wait(driver, '//div[@class="node"]')

    return node_elements

def get_nodeid_list(driver):
    """
    Find all node (server) IDs on a page.

    Args:
        driver: object - WebDriver instance.

    Returns:
        List of node IDs
    """

    node_elements = get_nodes(driver)
    nodeid_list = [element.get_attribute('data-node_id') for element in node_elements]

    return nodeid_list

def find_nodeid_by_nodename(driver, nodename):
    """
    Find the node ID using the node (server) name.

    Args:
        driver: object - WebDriver instance.
        nodename: string - node (server) name

    Returns:
        A string which is the node's ID
    """

    path = ('//div[contains(text(), "%s")]/ancestor::div[@class="node"]' % nodename)
    node_element = sellib.element_wait(driver.find_element_by_xpath, path)
    nodeid = node_element.get_attribute('data-node_id')

    return nodeid

def get_nodename(driver, nodeid):

    namepath = ('//div[@class="node" and @data-node_id="%s"]/descendant::div[@class='
                '"goog-control ck_widgets_glance_name"]' % nodeid)
    nodename = sellib.element_wait(driver.find_element_by_xpath(namepath).text)

    return nodename

def get_pmn(nodeid):
    """
    Assemble XPath for the first part of the panel menu node that includes the provided nodeid.

    Args:
        nodeid: string - the node's numeric ID as a string value

    Returns:
        pmn: string - XPath part that includes nodeid, used later to ensure work done using the
                      panel menu uses the correct node (stands for "panel menu node").
    """
    
    return '//div[@id="panel-menu-node-%s"]/descendant::' % nodeid

def get_sprocket_path(nodeid):
    """Assemble XPath for the sprocket associated with the provided nodeid.

    Args:
        nodeid: string - the node's numeric ID as a string value

    Returns:
        sprocket_path: string - XPath for panel menu 'sprocket' associated with the nodeid
    """

    return '//div[@data-node_id="%s"]/descendant::span[@class="panel_button_box"]' % nodeid

def find_sprocket(driver, nodeid):

    sellib.element_wait(driver.find_element_by_xpath, get_sprocket_path(nodeid), 'click')

def delete_node(driver, nodeid, sleepdict):
    """
    Deletes node (server) by using the Power >> Destroy feature.

    Args:
        driver: object - WebDriver instance.
        nodeid: string - Unique ID of node to be deleted. 
        sleepdict: dictionary - Universal sleep value (float) and "fast" on/off (boolean).
    """

    find_sprocket(driver, nodeid)
    sellib.sleeper(sleepdict)
    pmn = get_pmn(nodeid)
    powerpath = ('%sdiv[attribute::class="panel-menuitem power-panel-menuitem"]' % pmn)
    sellib.element_wait(driver.find_element_by_xpath, powerpath, 'click')
    sellib.sleeper(sleepdict)
    sellib.element_wait(driver.find_element_by_xpath, '//button[@class="destroy_button"]', 'click')
    sellib.sleeper(sleepdict)
    sellib.element_wait(driver.find_element_by_xpath, '//button[@name="ok"]', 'click')

def close_panel_menu(driver, all_loggers, retrydict, sleepdict, path_prepend):
    """
    Close the panel menu by clicking on the "X" in the upper right corner.
    
    Args:
        driver: object - WebDriver instance.
        all_loggers: tuple - Contains all logging objects.
        retrydict: dictionary - Contains current retry count and max retry count.
        sleepdict: dictionary - Universal sleep value (float) and "fast" on/off (boolean).
        path_prepend: string - Portion of XPath needed to isolate the correct panel-menu-close.

    Returns:
        Boolean "failed" (if True, test failed).
    """
    failed = True
    logger = all_loggers[0]
    with sellib.error_handler(driver, all_loggers, retrydict,
                              'Unable to close the panel menu using the "X"'):
        closepath = '%sdiv[attribute::class="panel-menu-close"]' % path_prepend
        sellib.element_wait(driver.find_element_by_xpath, closepath, 'click')
        sellib.sleeper(sleepdict)
        logger.debug('Closed the panel menu')
        failed = False

    return failed

def custom_colors(driver, logger, custompath, sleepdict):
    custom = driver.find_element_by_xpath(custompath)
    custom.clear()
    custom.send_keys("#FF0000\n")
    logger.debug('Changed to custom color (red) with #HEXVAL')
    sellib.sleeper(sleepdict)
    custom.clear()
    custom.send_keys("00FF00\n")
    logger.debug('Changed to custom color (lime green) with HEXVAL '
                  '(no # symbol)')
    sellib.sleeper(sleepdict)
    custom.clear()
    custom.send_keys("#ff00ff\n")
    logger.debug('Changed to custom color (fuschia) with lowercase '
                  'letters in #HEXVAL')
    sellib.sleeper(sleepdict)
    custom.clear()
    custom.send_keys("ffffff\n")
    logger.debug('Changed to custom color (white) with lowercase '
                  'letters in HEXVAL (no # symbol)')
    sellib.sleeper(sleepdict)

def panel_colors():
    panel_colors = (
        '(225, 117, 96)',
        '(255, 153, 106)',
        '(255, 222, 117)',
        '(189, 230, 108)',
        '(138, 191, 196)',
        '(153, 153, 153)',
        '(228, 135, 116)',
        '(255, 166, 125)',
        '(255, 226, 134)',
        '(198, 233, 126)',
        '(153, 199, 203)',
        '(178, 178, 178)',
        '(232, 152, 136)',
        '(255, 179, 143)',
        '(255, 230, 151)',
        '(206, 236, 145)',
        '(167, 207, 211)',
        '(204, 204, 204)',
        '(236, 169, 155)',
        '(255, 191, 162)',
        '(255, 234, 168)',
        '(214, 239, 163)',
        '(182, 215, 218)',
        '(229, 229, 229)',
        '(240, 186, 175)',
        '(255, 204, 181)',
        '(255, 239, 186)',
        '(222, 243, 181)',
        '(197, 223, 225)',
        '(255, 255, 255)')

    return panel_colors
