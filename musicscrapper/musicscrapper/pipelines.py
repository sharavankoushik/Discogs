# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import json
import re

class MusicscrapperPipeline(object):
    def process_item(self, item, spider):
        #item['address'] = self.cleanup_address(item['address'])
        #item.save()
        return item

    #def cleanup_address(self, address):
        #m = re.search('(?P<numb>(\d+))\s(?P=numb)', address)
     #   if m:
      #      return address[0:m.end(1)]
      #  return address

    def append_to_json(filepath, data):
        """
        Append data in JSON format to the end of a JSON file.
        NOTE: Assumes file contains a JSON object (like a Python
        dict) ending in '}'.
        :param filepath: path to file
        :param data: dict to append
        """

        # construct JSON fragment as new file ending
        new_ending = ", " + json.dumps(data)[1:-1] + "}\n"

        # edit the file in situ - first open it in read/write mode
        with open(filepath, 'r+') as f:

            f.seek(0, 2)  # move to end of file
            index = f.tell()  # find index of last byte

            # walking back from the end of file, find the index
            # of the original JSON's closing '}'
            while not f.read().startswith('}'):
                index -= 1
                if index == 0:
                    raise ValueError("can't find JSON object in {!r}".format(filepath))
                f.seek(index)

            # starting at the original ending } position, write out
            # the new ending
            f.seek(index)
            f.write(new_ending)

            # let 'er rip