import unittest
import random
from HelperFunctions import allowed_file, clear_temp, splitter
import os
import cv2
import shutil

class TestStringMethods(unittest.TestCase):

    """ ------------------------------ 
    ------- application.py -------
    -------------------------------"""
    

    """ ------------------------------ 
    ------- HelperFunctions.py -------
    -------------------------------"""
    # TEST SPLITTER
    def test_splitter(self):
        """
        Copies testing video to the TEMPVID folder, runs the splitter function,
        and checks that frames are extracted to the TEMPPICS FOLDER.
        """
        source = "2020-05-14_14-55-47.mp4"
        destination = "TEMPVID/2020-05-14_14-55-47.mp4"
        shutil.copyfile(source, destination)

        splitter("2020-05-14_14-55-47.mp4", frameskip=50)

        self.assertTrue(len(os.listdir('TEMPPICS')) >= 1)
        clear_temp()
        self.assertTrue(len(os.listdir('TEMPPICS')) == 0)

    # TEST ALLOWED FILE
    def test_allowed_file(self):
        self.assertTrue(allowed_file('fake_file_name.mp4'))
        self.assertFalse(allowed_file('fake_file_name.png'))
 
    # TEST CLEAR TEMP
    def test_clear_temp(self):
        clear_temp()
        self.assertTrue(len(os.listdir('TEMPPICS')) == 0)
        self.assertTrue(len(os.listdir('TEMPVID')) == 0)

    """ ------------------------------ 
    ------- ModelFunctions.py -------
    -------------------------------"""




if __name__ == '__main__':
    unittest.main()