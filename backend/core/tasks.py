import re

from backend.celery import app
from .models import File


@app.task(serializer='json')
def interest_calculation(id):
    f = File.objects.get(id=id)
    file_link = 'media/' + str(f.file)
    count = 0
    len_file = 0
    with open(file_link, 'r') as file:

        for line in file:
            new_s = re.sub(r'[^\w\s]', '', line).lower().split()
            for word in new_s:
                count += word[:-1].count('е')
                len_file += len(word)

    res = round(count / len_file * 100, 3)
    File.objects.filter(id=id).update(percentage=res)
    return res
