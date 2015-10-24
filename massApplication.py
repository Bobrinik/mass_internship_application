import unittest
from selenium import webdriver
import pprint
import re
import time 

class MyCoursesInternship():
    def __init__(self):
        self.driver=webdriver.Firefox()
        self.driver.get("https://csm-caps.mcgill.ca/students/")


    def login(self, username, password):
        username_element=self.driver.find_element_by_xpath("id('username')")
        username_element.send_keys(username)
        password_element=self.driver.find_element_by_xpath("id('password')")
        password_element.send_keys(password)
        submit_element=self.driver.find_element_by_xpath("id('ui_module_modulecontent')/div/div/div[3]/div[1]/form/div[8]/input[1]")
        submit_element.click()

    def setSearchParameters(self):
        jobs=self.driver.find_element_by_xpath("id('yui-gen14')/a")#the xpath to this element is changing so you need to set it up manually
        jobs.click()
        advancedSearch=self.driver.find_element_by_xpath("id('ui_module_modulecontent')/div[1]/form/div/div[1]/a[1]")
        advancedSearch.click()
        self.driver.find_element_by_xpath("id('jobfilters_job_type___')/option[12]").click() #Industry

    def getLinksIDs(self):
        print "getLinksIds() executed"
        self.selector_ids=[]
        page=self.driver.page_source
        matches = re.findall('<.*?>', page)
        for match in matches:
            if "id=\"row_" in match:
                start=match.find('id="')+4
                end=len(match)-2
                self.selector_ids.append(match[start:end])

    def getJobDescription(self):
        try:
            jobDescription=self.driver.find_element_by_xpath("id('ui_module_modulecontent')")
            return jobDescription.text
        except:
            return "Nothing"

    def botLikesOffer(self,jobDescription):
        text=jobDescription.lower()
        search_terms=['java', 'c', 'python','ocaml']
        for term in search_terms:
            if term in jobDescription:
                return True
        return False

        #count how many times certain words are going to occur based on that return true or false
    def apply(self, row_id):
        try:
                apply_button=self.driver.find_element_by_xpath("id('job_send_docs')/a/span[2]")
                apply_button.click()
                cover_letter=self.driver.find_element_by_xpath("id('so_formfielddnf_class_values_non_ocr_job_resume__cover_letter_')/td[1]/div")
                if("*" not in cover_letter.text):
                    submit=self.driver.find_element_by_xpath("id('job_resume_form')/div/div/table/tbody/tr[2]/td/div/input")
                    time.sleep(5)
                    submit.click()
        except:
            print "Master I could not click Apply"
    def get_company_name(self, row_id):
        company_name=self.driver.find_element_by_xpath("id('%s')/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td[1]/a"%row_id)
        return company_name.text

    def get_location(self, row_id):
        location=self.driver.find_element_by_xpath("id('%s')/div[2]/div[2]/div/div[2]/table/tbody/tr[3]/td[1]"%row_id)
        return location.text

    def get_position(self, row_id):
        position=self.driver.find_element_by_xpath("id('%s')/div[2]/div[2]/h2/a"%row_id)
        return position.text

    def submit(self):
        submit_button=self.driver.find_element_by_xpath("id('job_resume_form')/div/div/table/tbody/tr[2]/td/div/input")
        submit_button.click()

    def go_back(self):
        go_back=self.driver.find_element_by_xpath("id('ui_module_modulecontent')/table/tbody/tr[3]/td/div/input[1]")
        go_back.click()

#Link ids are generated every time you visit a page
    def massApply(self):
        self.getLinksIDs()
        cache_of_row_numbers=[]
        for row_id in self.selector_ids:
            try:
                jobLink=self.driver.find_element_by_xpath("id('%s')/div[2]/div[2]/h2/a"%row_id)
            except:
                print "reloading row_ids"
                self.getLinksIDs()
                continue
            row_number=self.driver.find_element_by_xpath("id('%s')/div[1]"%row_id).text
            if not row_number in cache_of_row_numbers:
                cache_of_row_numbers.append(row_number)
                company=self.get_company_name(row_id)
                location=self.get_location(row_id)
                position=self.get_position(row_id)
                jobLink.click()
                jobDescription=self.getJobDescription()#someprocessing should be done on it and as result of the processing clicking should be decided
                if self.botLikesOffer(jobDescription):
                    print company+"---"+location+"---"+position
                    self.apply(row_id)
                self.go_back()



#    def searchContent(self, keywords): #this method is going to search texts from job_offers and is going to select the ones with matching words like computer science, undergrad
    def closeConnection(self):
        self.driver.close()


if __name__ == '__main__':
    myFuture=MyCoursesInternship()
    myFuture.login('test','test')
    myFuture.setSearchParameters()
    myFuture.massApply()
    myFuture.closeConnection()
