class TestInit(object):
    def __init__ (self, commonTester, mt_name):
        self.commonTester = commonTester
        environment = self.commonTester.config.get('main', 'test_environment')
        self.username = self.commonTester.config.get('main', 'username')
        self.password = self.commonTester.config.get('main', 'password')
        self.testkey = self.commonTester.config.get('main', 'testkey')
        if (environment == 'local'):
            self.__start_testing_local(mt_name)
        elif (environment == 't1vv'):
            self.__start_testing_t1vv(mt_name)
        elif (environment == 't1vv_ni'):
            self.__start_testing_t1vv_ni(mt_name)
        elif (environment == 't1fr_ni'):
            self.__start_testing_t1fr_ni(mt_name)
        elif (environment == 'production'):
            self.__start_testing_production(mt_name)
                    
    def __start_testing_local(self, mt_name):
        self.commonTester.driver.get('http://localhost:8080/products/hardware/configurator/americas/bhui/client/jsp/')
        self.commonTester.click_by_text('Application Test Client')
        self.commonTester.click_by_name('bhsubmit')
        self.commonTester.input_text_by_name('base', mt_name).submit()

    def __start_testing_t1vv(self, mt_name):
        self.commonTester.driver.get("https://%s:%s@c01z0016.pok.ibm.com/products/hardware/configurator/worldwide/bhui/client/jsp/#" % (self.username, self.password))
        self.commonTester.driver.get("https://c01z0016.pok.ibm.com/products/hardware/configurator/worldwide/bhui/client/jsp/#")
        self.commonTester.click_by_text('Application Test Client')
        self.commonTester.click_by_name('bhsubmit')
        self.commonTester.input_text_by_name('base', mt_name).submit()
        
    def __start_testing_t1vv_ni(self, mt_name):
        self.commonTester.driver.get("https://%s:%s@c01z0016.pok.ibm.com/products/hardware/configurator/worldwide/bhui/client/jsp/#" % (self.username, self.password))
        self.commonTester.driver.get("https://c01z0016.pok.ibm.com/products/hardware/configurator/worldwide/bhui/client/jsp/#")
        self.commonTester.click_by_text('T1VV beta')
        self.commonTester.input_text_by_name('CONTROL_Model_BasePN', mt_name)
        self.commonTester.click_by_name('submit')
        
    def __start_testing_t1fr_ni(self, mt_name):
        self.commonTester.driver.get("https://%s:%s@c01z0016.pok.ibm.com/products/hardware/configurator/worldwide/bhui/client/jsp/#" % (self.username, self.password))
        self.commonTester.driver.get("https://c01z0016.pok.ibm.com/products/hardware/configurator/worldwide/bhui/client/jsp/#")
        self.commonTester.click_by_text('T1FR beta')
        self.commonTester.input_text_by_name('CONTROL_Model_BasePN', mt_name)
        self.commonTester.click_by_name('submit')
        
    def __start_testing_production(self, mt_name):
        self.commonTester.driver.get("https://www-01.ibm.com/products/hardware/configurator/americas/bhui/launchNI.wss")
        self.commonTester.input_text_by_name('CONTROL_Model_BasePN', mt_name)
        self.commonTester.click_by_name('submit')
        
