import re
import time
import os.path
from scrapy.exceptions import DropItem
from scrapy.utils.response import body_or_str

class CraigslistSamplePipeline(object):
    def process_item(self, item, spider):
        return item

class EmptyDrop(object):
    def process_item(self, item, spider):
    	if not(all(item.values())):
            raise DropItem()
        else:
	        return item

class SaveFiles(object):
    def process_item(self, item, spider):
        name1 = item["title"]
        name = "".join(re.findall("[a-zA-Z0-9 ]+", name1))
        save_path = os.path.join('data', item["date"], name+".txt")
        if not os.path.exists(os.path.dirname(save_path)):
            try:
                os.makedirs(os.path.dirname(save_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(save_path, 'a+') as f:
            f.write('name: {0} \nlink: {1}\n\n {2}'.format(name, item['link'], item["article"]))
        return item