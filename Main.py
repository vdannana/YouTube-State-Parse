import os

import Common_Function as cf
import Configuration as conf

if not os.path.exists(conf.Input_Folder + '/' + conf.File_Name):
    cf.Parse_Log(conf.Input_Folder + '/' + conf.File_Name)
else:
    print("No input file")