"""
  ******************************************************************************
  * @project AMDS
  * @file    Controller.py
  * @author  THM Gesundheit Team
  * @brief   Init of core Controlelr
  * @date    24.05.2023
  ******************************************************************************
"""
import json


class Controller:
    def __init__(self):
        pass

    def returnJSON(self, obj):
        # Convert the given object to JSON format
        return json.dumps(obj)