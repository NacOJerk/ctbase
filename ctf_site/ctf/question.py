from . import models

# Setup for holder functions
questions = {}
categories = []

DEBUG = False
INIT = False

try:
    str(models.Category.objects.all())
    INIT = True
except:
    pass


def question(file_name, name, score, category_name):
    if not INIT:
        def inner(func):
            return func
        return inner
    category = models.Category.objects.get_or_create(title_field=category_name)[0]
    category.save()
    try:
        category.challenge_set.get(title_field=name, file_field=file_name, score_field=score)
    except models.Challenge.DoesNotExist as e:
        print("Creating")
        category.challenge_set.filter(title_field=name).delete()
        challenge = category.challenge_set.create(title_field=name, file_field=file_name, score_field=score)
        challenge.save()
    categories.append(category_name)
    if DEBUG:
        print("[*] Created Name: %s File: %s Score: %d Category: %s" % (name, file_name, score, category_name))

    def inner(func):
        questions["%s-%s" % (category_name, name)] = func
        return func
    return inner


def final():
    if not INIT:
        return None
    if DEBUG:
        print(questions)
        print(categories)
    for category in models.Category.objects.all():
        if category.title_field not in categories:
            category.delete()
            print("[*] Deleted %s category" % category.title_field)
        else:
            for challange in category.challenge_set.all():
                if "%s-%s" % (category.title_field, challange.title_field) not in questions:
                    challange.delete()
                    print("[*] Deleted %s.%s challenge" % (category.title_field, challange.title_field))
