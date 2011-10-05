from selenium import webdriver
import csv
import time
import unittest
import TestInit

class TestContent(unittest.TestCase):
    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.http.phishy-userpass-length', 255)
        self.driver = webdriver.Firefox(firefox_profile=profile)
        
    def tearDown(self):
        self.driver.save_screenshot(self.file_path + '.png')
        self.driver.close()

    def runTest(self):
        try:
            test_case_reader = csv.reader(open(self.file_path, 'rb'), delimiter=',')
            self.logger.info("Running test case %s" % self.file_path)
            for row in test_case_reader:
                if (len(row) > 1):
                    method_name, parameters = row[0], row[1:]
                    parameters = filter(None, parameters)
                    method = getattr(self, method_name)
                    self.logger.info("executing method %s parameters %s" % (method_name, parameters))
                    method(*parameters)
                    self.wait()
        except AssertionError, e:
            self.logger.error(e)
            self.fail("Test case failed: %s" % self.file_path)
                
    def wait(self):
        while (True):
            time.sleep(5)
            try:
                self.driver.find_element_by_xpath("//div[@id='wait_c'][contains(@style, 'visibility: visible')]")
            except:
                return
                
    def start_testing(self, mt_name):
        TestInit.TestInit(self, mt_name)
        
    def title(self, text):
        self.logger.info("Test Case: %s" % text)
        
    def input_text_by_name(self, name, value):
        while (True):
            try:
                test_client = self.driver.find_element_by_name(name);
                test_client.clear()
                test_client.send_keys(value)
                return test_client
            except:
                time.sleep(1)
    
    def click_by_text(self, text):
        while (True):
            try:
                test_client = self.driver.find_element_by_link_text(text)
                test_client.click()
                return
            except:
                time.sleep(1)
    
    def click_by_name(self, name):
        while (True):
            try:
                test_client = self.driver.find_element_by_name(name)
                test_client.click()
                return
            except:
                time.sleep(1)
    
    def click_by_id(self, id):
        test_client = self.driver.find_element_by_id(id)
        test_client.click()
        return test_client
    
    def click_continue(self):
        return self.click_by_id('continueTop')
        
    def click_check_product(self):
        return self.click_by_id('checkSystemTop')
    
    def click_check_system(self):    
        return self.click_by_id('checkSystem')
    
    def click_detail(self):
        test_client = self.driver.find_element_by_xpath("//em[.='Details']") 
        test_client.click()
        return test_client
        
    def click_feature(self, feature_code, group=None):
        if (group == None):
            test_client = self.driver.find_element_by_xpath("//label[contains(.,'%s')]" % feature_code) 
        else:
            test_client = self.driver.find_element_by_xpath("//span[contains(.,'%s')]/parent::*/parent::*/parent::*//.[contains(@value,'%s')]" % (group, feature_code))
        test_client.click()
        return test_client

    def select_feature_qty(self, feature_code, quantity, group=None):
        if (group == None):
            test_client = self.driver.find_element_by_xpath("//input[contains(@value,'%s')]/parent::*/parent::*//option[@value='%s']" % (feature_code, quantity))
        else:
            test_client = self.driver.find_element_by_xpath("//span[contains(.,'%s')]/parent::*/parent::*/parent::*//.[contains(@value,'%s')]/parent::*/parent::*//option[@value='%s']" % (group, feature_code, quantity))
        test_client.click()
        return test_client

    def select_feature_qty_dropdown(self, feature_code, quantity, group=None):
        try:
            if (group == None):
                test_client = self.driver.find_element_by_xpath("//option[contains(.,'%s')]" % (feature_code))
            else:
                test_client = self.driver.find_element_by_xpath("//span[contains(.,'%s')]/parent::*/parent::*/parent::*//option[contains(.,'%s')]" % (group, feature_code))
        except Exception as detail:
            self.assertTrue(False, detail)
        test_client.click()
        try:
            if (group == None):
                test_client = self.driver.find_element_by_xpath("//option[contains(.,'%s')]//parent::*//parent::*//parent::*//option[@value='%s']" % (feature_code, quantity))
            else:
                test_client = self.driver.find_element_by_xpath("//span[contains(.,'%s')]/parent::*/parent::*/parent::*//option[contains(.,'%s')]/parent::*/parent::*/parent::*//option[@value='%s']" % (group, feature_code, quantity))
        except Exception as detail:
            self.assertTrue(False, "%s is not a valid quantity" % quantity)
        test_client.click()
        return test_client
    
    def click_customize(self, mt_name):
        test_client = self.driver.find_element_by_xpath("//a[contains(@href,'%s')]/.[.='Customize']" % mt_name)
        test_client.click()
        return test_client
    
    def select_none(self, oc_name):
        try:
            test_client = self.driver.find_element_by_xpath("//span[contains(.,'%s')]/parent::*/parent::*/parent::*//label[contains(.,'None')]" % oc_name)
            test_client.click()
        except Exception, e:
            self.logger.exception(e)

    def verify_feature_code_present(self, feature_code, group=None):
        try:
            if (group == None):
                self.driver.find_element_by_xpath("//.[contains(@value,'%s')]" % feature_code)
            else:
                self.driver.find_element_by_xpath("//span[contains(.,'%s')]/parent::*/parent::*/parent::*//.[contains(@value,'%s')]" % (group, feature_code))
        except Exception:
            self.assertTrue(False, "%s is not present on UI page" % feature_code)
            
    def verify_feature_code_absent(self, feature_code, group=None):
        try:
            if (group == None):
                self.driver.find_element_by_xpath("//.[contains(@value,'%s')]" % feature_code)
            else:
                self.driver.find_element_by_xpath("//span[contains(.,'%s')]/parent::*/parent::*/parent::*//.[contains(@value,'%s')]" % (group, feature_code))
            self.assertTrue(False, "%s is present on UI page" % feature_code)
        except Exception:
            self.assertTrue(True, "%s is absent on UI page" % feature_code)
            
    def toXPathStringLiteral(self, s):
        if "'" not in s: return "'%s'" % s
        if '"' not in s: return '"%s"' % s
        return "concat('%s')" % s.replace("'", "',\"'\",'")

    def verify_feature_code_present_detail(self, feature_code, quantity):
        try:
            self.driver.find_element_by_xpath("//td[contains(.,'" + feature_code + "')]")
        except Exception:
            self.assertTrue(False, "%s is not present on detail page" % feature_code)
        try:
            self.driver.find_element_by_xpath("//tr[contains(.,'%s')]/td[4][contains(.,%s)]" % (feature_code, quantity))
        except Exception:
            self.assertTrue(False, "%d of %s is not present on detail page" % (quantity, feature_code))
            
    def verify_feature_code_absent_detail(self, feature_code):
        try:
            self.driver.find_element_by_xpath("//td[contains(.,'" + feature_code + "')]")
            self.assertTrue(False, "%s is present on detail page" % feature_code)
        except Exception:
            self.assertTrue(True, "%s is absent on detail page" % feature_code)
    
    def verify_configuration_valid(self):
        try:
            self.driver.find_element_by_xpath("//td[contains(.,'Your configuration is valid')]")
        except Exception:
            self.assertTrue(False, "unable to find message that configuration is valid")
         
    
    def verify_error_message_present(self, message):
        try:
            self.driver.find_element_by_xpath("//span[@class='error'][contains(.,%s)]" % self.toXPathStringLiteral(message))
        except Exception:
            self.assertTrue(False, "Error message not found: %s" % self.toXPathStringLiteral(message))
    
    def verify_oc_hidden(self, oc_name):
        try:
            self.driver.find_element_by_xpath("//label[contains(.,'%s')]" % oc_name)
            self.assertTrue(False, "%s is not hidden" % oc_name)
        except:
            self.assertTrue(True, "%s is hidden" % oc_name)

    def verify_oc_present(self, oc_name):
        try:
            self.driver.find_element_by_xpath("//label[contains(.,'%s')]" % oc_name)
        except Exception:
            self.assertTrue(False, "%s is not present" % oc_name)

    def verify_feature_qty(self, feature_code, quantity):
        try:
            self.driver.find_element_by_xpath("//input[contains(@value,'%s')]/parent::*/parent::*//option[@value='%s']/.[@selected='selected']" % (feature_code, quantity))
        except Exception:
            self.assertTrue(False, "%s is not the default value of %s" % (quantity, feature_code))
    
    def verify_feature_qty_dropdown(self, feature_code, quantity):
        try:
            self.driver.find_element_by_xpath("//option[contains(@value,'%s')]/parent::*/parent::*//parent::*//option[@value='%s']/.[@selected='selected']" % (feature_code, quantity))
        except Exception:
            self.assertTrue(False, "%s is not the default value of %s" % (quantity, feature_code))

    def verify_min_max_qty(self, feature_code, min_qty, max_qty, group=None):
        try:
            if (group == None):
                self.driver.find_element_by_xpath("//input[contains(@value,'%s')]/parent::*/parent::*/td[1]/select/option[1][@value='%s']/parent::*/option[last()][@value='%s']" % (feature_code, min_qty, max_qty))
            else:
                self.driver.find_element_by_xpath("//span[contains(.,'%s')]/parent::*/parent::*/parent::*//input[contains(@value,'%s')]/parent::*/parent::*/td[1]/select/option[1][@value='%s']/parent::*/option[last()][@value='%s']" % (group, feature_code, min_qty, max_qty))
        except Exception:
            self.assertTrue(False, "The minimum or maximum value of feature code %s is not valid" % feature_code)
            
    def verify_min_max_qty_dropdown(self, feature_code, min_qty, max_qty, group=None): 
        try:
            if (group == None):
                self.driver.find_element_by_xpath("//option[contains(.,'%s')]/parent::*/parent::*/parent::*/td[1]/select/option[1][@value='%s']/parent::*/option[last()][@value='%s']" % (feature_code, min_qty, max_qty))
            else:
                self.driver.find_element_by_xpath("//span[contains(.,'%s')]/parent::*/parent::*/parent::*//option[contains(.,'%s')]/parent::*/parent::*/parent::*/td[1]/select/option[1][@value='%s']/parent::*/option[last()][@value='%s']" % (group, feature_code, min_qty, max_qty))
        except Exception:
            self.assertTrue(False, "The minimum or maximum value of feature code %s is not valid " % feature_code)
