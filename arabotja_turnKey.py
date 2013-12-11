#!/usr/bin/python
#-*- coding: UTF-8 -*-

import os
from arabotja import BabyBird

arabotja = BabyBird('ilbe', '정보')
arabotja.wakeBird()

# If you use 'crontab', you have to find the 3 log files in /home/yourName/ after arabotja_turnKey.py or just change the source