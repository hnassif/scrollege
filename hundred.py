import os
os.environ['DJANGO_SETTINGS_MODULE']='post.settings'
from website.models import Item
from django.contrib.auth.models import User

me =User.objects.all()[1]

import random

words = [line.strip() for line in open('/etc/dictionaries-common/words')]
print random.choice(words)

for x in xrange(100):
	Item(
		name =random.choice(words),
		category ='Item',
		price = random.randint(5,2000),
		negotiable = random.choice([True, False]),
		active = True,
		looking_for =random.choice([True,False]),
		owner =me,
		description =random.choice(words),
		image_first =None,
		image_second =None,
		image_third =None,
		isActive =random.choice([True,False])
	).save()


