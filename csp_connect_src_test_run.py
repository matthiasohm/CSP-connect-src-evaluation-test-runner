import json
import boto3
from botocore.config import Config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Remote



# csp-connect-src-evaluation
from waitcondition import wait_for_text_to_exist


def handler(event, context):
    test_case_domain = event["test_case_domain"]
    # number of the testcase 1-13
    test_case_number = event["test_case_number"]

    # whole number of subtestcases
    test_case_subcount = event["test_case_subcount"]

    # which subtestcase to start with
    test_case_start = event["test_case_start"]

    # where did the lambda finish
    test_case_finish = ""

    # renge of subnumbers
    test_case_subnumberrange = event["test_case_subnumberrange"]

    # init or run
    test_case_step = event["test_case_step"]

    # true or false
    test_case_log = event["test_case_log"]

    # init driver -------------------------------------------------------------------------------
    my_config = Config(
        region_name='us-west-2'
    )

    devicefarm_client = boto3.client("devicefarm", config=my_config)

    testgrid_url_response = devicefarm_client.create_test_grid_url(
        projectArn="arn:aws:devicefarm:us-west-2:687448825126:testgrid-project:59c1f91a-d85b-4cf2-8631-c66bbb874a2c",
        expiresInSeconds=300
    )

    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["platform"] = "windows"
    driver = Remote(testgrid_url_response['url'], desired_capabilities)
    # init driver -------------------------------------------------------------------------------

    if test_case_step == "init":
        url = 'http://' + test_case_domain + '/initlocalcspobject'
        driver.get(url)
        text = driver.find_element_by_xpath("//body").get_attribute("innerHTML")
        return text
    elif test_case_step == "run":

        elements = {}
        range_end = int(test_case_start) + int(test_case_subnumberrange)

        if range_end > int(test_case_subcount):
            range_end = int(test_case_subcount) + 1

        # e.g. 0,0+10 --> test_case_finish = int(test_case_start)+int(test_case_subnumberrange)-1
        for i in range(int(test_case_start), range_end):
            url = 'http://' + test_case_domain + '/testcase?' \
                                                 'targethost=targetdomain.test' \
                                                 '&targetport=80' \
                                                 '&number=' + test_case_number + '' \
                                                 '&subnumber=' + str(i) + '' \
                                                 '&positivetest=false' \
                                                 '&logtoS3=' + test_case_log + ''

            driver.get(url)
            try:
                element = WebDriverWait(driver, 15).until(
                    wait_for_text_to_exist((By.ID, 'log'))
                )
            finally:
                result = str(element)
                result = result.replace("<h3>", "-")
                result = result.replace("</h3>", "-")
                elements[str(i)] = result
                test_case_finish = i

        returnval = {'test_case_domain': test_case_domain,
                     'test_case_number': test_case_number,
                     'test_case_subcount count': test_case_subcount,
                     'test_case_start': test_case_start,
                     'test_case_finish': test_case_finish,
                     'test_case_subnumberrange ': test_case_subnumberrange,
                     'test_case_step': test_case_step,
                     'test_case_log': test_case_log, 'test_case_url': url,
                     'log_element': json.dumps(elements)
                     }

        return json.dumps(returnval, indent=4)

    driver.quit()