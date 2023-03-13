# importing sys
import sys, os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(ROOT_DIR, './models'))
sys.path.insert(0,os.path.join(ROOT_DIR, './settings'))


if __name__ == '__main__':  #python manage.py --migrate True
   from init import initdb
   #import argparse 
   #parser = argparse.ArgumentParser()
   #parser.add_argument('-migrate', '--migrate', nargs='+', required=False,dest = 'migrate', default = False,help = 'init DB')
   #args = parser.parse_args()
   #if args.migrate:
   initdb()
   print("migrate | Done..")