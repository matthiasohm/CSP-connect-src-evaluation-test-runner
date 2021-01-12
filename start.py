from csp_connect_src_test_run import handler
from multiprocessing import Process
import json


def f(event):
    retval = handler(event, "")
    print(retval)


if __name__ == '__main__':

    test_case_domain = "sourcedomain.test"
    # currently possible [1,2,3,4,5,6,7,8,9,10,11,12,13]
    different_main_test_cases_to_run = [1]
    # one range e.g. 0,1,2,3,4
    test_case_subnumberrange = 5
    test_case_start = 0

    # Initialize test cases on server and get amount of possible directives
    config = {"test_case_domain": test_case_domain,
            "test_case_number": "1",
            "test_case_subcount": "1",
            "test_case_start": "0",
            "test_case_subnumberrange": "0",
            "test_case_step": "init",
            "test_case_log": "false"}
    returnvalue = handler(config, "")
    returnvalue = returnvalue.replace("\'","\"")
    returnvalue = returnvalue.replace(":\"", "\":")
    returnvalue = json.loads(returnvalue)
    # Initialize DONE

    generation_successfull = returnvalue["generation successfull"]

    if generation_successfull == "true":
        test_case_subcount = int(returnvalue["cspcount"])

        #for testing purposes!!!!!
        test_case_subcount = 11

        process_amount = test_case_subcount//test_case_subnumberrange
        if test_case_subcount % test_case_subnumberrange > 0:
            process_amount = process_amount + 1

        proc = []

        for main_case in different_main_test_cases_to_run:

            for process_nbr in range(process_amount):

                config = {"test_case_domain": test_case_domain,
                        "test_case_number": str(main_case+1),
                        "test_case_subcount": str(test_case_subcount),
                        "test_case_start": str(test_case_start),
                        "test_case_subnumberrange": str(test_case_subnumberrange),
                        "test_case_step": "run",
                        "test_case_log": "false"}

                p = Process(target=f, args=(config,))
                p.start()
                proc.append(p)

                test_case_start = test_case_start+test_case_subnumberrange

        for p in proc:
            p.join()
    else:
        print("something went wrong initializing the test environment.")
