import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import sys
sys.path.insert(0, '/home/fadhil/Desktop/Mental system/Mental-health-and-well-being-support-system')

django.setup()
print('Django setup OK')

