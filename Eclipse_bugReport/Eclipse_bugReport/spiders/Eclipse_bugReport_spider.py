#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-


import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BugReportSpider(scrapy.Spider):
    name = "Eclipse_bugReport"
    
    def start_requests(self):
        url_1 = "https://bugs.eclipse.org/bugs/show_bug.cgi?id="
        url_2 = "https://bugs.eclipse.org/bugs/show_activity.cgi?id="
        
        #yield scrapy.Request(url=url_1+'403467', callback=self.parse)
        #yield scrapy.Request(url=url_2+'403467', callback=self.parse_history)
        with open("/home/carrie/scrapyCrawe/mySpider/Eclipse_Tools_reopen_urls.csv") as f:
            #the first line is the headline
            line_1 = f.readline()
            #the second line contains all bug ids, which are seperated by delimiter comma
            line_2 = f.readline().replace('"', '')
            bug_ids = line_2.split(',')
            for i in range(len(bug_ids)):
                yield scrapy.Request(url=url_1+bug_ids[i], callback=self.parse)
                yield scrapy.Request(url=url_2+bug_ids[i], callback=self.parse_history)
    def parse_history(self, response):
        page = response.url.split("?")[-1]
        filename = '/home/carrie/scrapyCrawe/Eclipse_bugReport/reopen_Eclipse_Tools_2.txt'
        change_times = response.xpath('count(//*[@id="bugzilla-body"]/table/tr)').extract()[0]
        changes = int(round(float(change_times)))
        with open(filename, 'a') as of:
            #bug_ids
            of.write(page)
            of.write('\t')
            #total times for fixing the bug
            if changes == 0 or changes == 1:
                of.write('0')
            else:
                of.write(str(changes - 1))
            of.write('\t')
            priority_changed = False
            severity_changed = False
            change_item = response.xpath('//*[@id="bugzilla-body"]/table//td[last()-2]/text()').extract()
            for item in change_item:
                item = item.strip()
                if item == "Severity":
                    severity_changed = True
                elif item == "Priority":
                    priority_changed = True
            #priority_changed
            of.write(str(priority_changed))
            of.write('\t')
            #severity_changed
            of.write(str(severity_changed))
            of.write('\t')
            #fixer
            fixer = response.xpath('//*[@id="bugzilla-body"]/table/tr[2]/td[1]/text()').extract()
            if len(fixer) == 0:
                of.write('None')
            else:
                for fix in fixer:
                    tmp = fix.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #remod, if the bug will reopen, the remod = '1', else remod = '0'
            of.write('1')
            of.write('\n')

    def parse(self, response):
        page = response.url.split("?")[-1]
        filename_1 = '/home/carrie/scrapyCrawe/Eclipse_bugReport/reopen_Eclipse_Tools_1.txt'
        with open(filename_1, 'a') as of:
            #bug_ids
            of.write(page)
            of.write('\t')
            #status
            status = response.xpath('//*[@id="static_bug_status"]/text()').extract()
            if len(status) == 0:
                of.write('None')
            else:
                for sta in status:
                    tmp = sta.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #product
            product = response.xpath('//*[@id="field_container_product"]/text()').extract()
            if len(product) == 0:
                of.write('None')
            else:
                for pro in product:
                    tmp = pro.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #component
            component = response.xpath('//*[@id="field_container_component"]/text()[1]').extract()
            if len(component) == 0:
                of.write('None')
            else:
                for com in component:
                    tmp = com.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #version
            version = response.xpath('//*[@id="bz_show_bug_column_1"]/table/tr[6]/td/text()').extract()
            if len(version) == 0:
                of.write('None')
            else:
                for ver in version:
                    tmp = ver.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #hardware
            hardware = response.xpath('//*[@id="bz_show_bug_column_1"]/table/tr[7]/td/text()').extract()
            if len(hardware) == 0:
                of.write('None')
            else:
                for hard in hardware:
                    tmp = hard.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #importance
            importance = response.xpath('//*[@id="bz_show_bug_column_1"]/table/tr[9]/td/text()').extract()
            if len(importance) == 0:
                of.write('None')
            else:
                for imp in importance:
                    tmp = imp.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #Assignee
            assigned = response.xpath('//*[@id="bz_show_bug_column_1"]/table/tr[11]/td/span/span/text()').extract()
            if len(assigned) == 0:
                of.write('None')
            else:
                for ass in assigned:
                    tmp = ass.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #Reported
            reported = response.xpath('//*[@id="bz_show_bug_column_2"]/table/tr[1]/td/text()').extract()
            if len(reported) == 0:
                of.write('None')
            else:
                for rep in reported:
                    tmp = rep.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #reporter
            reporter = response.xpath('//*[@id="bz_show_bug_column_2"]/table/tr[1]/td/span/span/text()').extract()
            if len(reporter) == 0:
                of.write('None')
            else:
                for repo in reporter:
                    tmp = repo.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #Modified
            modified = response.xpath('//*[@id="bz_show_bug_column_2"]/table/tr[2]/td/text()[1]').extract()
            if len(modified) == 0:
                of.write('None')
            else:
                for modi in modified:
                    tmp = modi.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #CC
            cc = response.xpath('//*[@id="bz_show_bug_column_2"]/table/tr[3]/td/text()').extract()
            if len(cc) == 0:
                of.write('None')
            else:
                for c in cc:
                    tmp = c.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #description
            description = response.xpath('//*[@id="c0"]/pre/text()').extract()
            if len(description) == 0:
                of.write(' ')
            else:
                for des in description:
                    tmp = des.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #comments
            comments = response.xpath('//*[@class="bz_comment"]/pre/text()').extract()
            if len(comments) == 0:
                of.write(' ')
            else:
                for comm in comments:
                    tmp = comm.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\t')
            #num_comment
            num_comment = response.xpath('count(//*[@class="bz_comment"])').extract()
            if len(num_comment) == 0:
                of.write('0')
            else:
                for num in num_comment:
                    tmp = num.replace('\n','')
                    t = ' '.join(tmp.split())
                    of.write(t)
            of.write('\n')
