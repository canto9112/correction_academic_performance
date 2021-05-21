import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson
import random
import argparse


def get_schoolkid(name, last_name):
    schoolkid_name = Schoolkid.objects.get(full_name__contains=f'{name} {last_name}')
    return schoolkid_name


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = random.randint(4, 5)
        bad_mark.save()


def remove_chastisements(schoolkid):
    bad_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in bad_chastisements:
        chastisement.delete()


def get_random_commendation():
    commendation = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
                    'Ты меня приятно удивил!', 'Прекрасно!', 'Великолепно!',
                    'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                    'Сказано здорого - просто и ясно', 'Ты как всегда точен',
                    'Очень хороший ответ', 'Талантливо!', 'Ты сегодня прыгнул выше головы',
                    'Я поражен!', 'Уже существенно лучше', 'Потрясающе!', 'Замечательно!',
                    'Прекрасное начало!', 'Здорово!']
    return random.choice(commendation)


def create_commendation(schoolkid, subject):
    year_of_study = schoolkid.year_of_study
    group_letter = schoolkid.group_letter
    lessons = Lesson.objects.all()
    kid_lessons = lessons.filter(year_of_study=year_of_study, group_letter=group_letter)
    lesson = kid_lessons.filter(subject__title=subject).get()

    random_commendation = get_random_commendation()

    Commendation.objects.create(text=random_commendation,
                                created=lesson.date,
                                schoolkid=schoolkid,
                                subject=lesson.subject,
                                teacher=lesson.teacher)


def get_arguments():
    parser = argparse.ArgumentParser(description='Скрипт исправляет плохие оценкки и замечания учителей')

    parser.add_argument('name', help='Имя ученика')
    parser.add_argument('last_name', help='Фамилия ученика')
    parser.add_argument('subject', help='Предмет для написания похвалы от учителя')

    args = parser.parse_args()
    return {'name': args.name,
            'last_name': args.last_name,
            'subject': args.subject}


def main():
    arguments = get_arguments()

    name = arguments['name'].capitalize()
    last_name = arguments['last_name'].capitalize()
    subject = arguments['subject'].capitalize()

    try:
        schoolkid = get_schoolkid(name, last_name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject)
    except Schoolkid.MultipleObjectsReturned:
        print(f'Учеников с именем {name} {last_name} найдено больше одного!')
    except Schoolkid.DoesNotExist:
        print(f'Учеников с именем {name} {last_name} не найдено!')
    except Lesson.DoesNotExist:
        print('Вы допустили опечатку в названии предмета!')


if __name__ == '__main__':
    main()
