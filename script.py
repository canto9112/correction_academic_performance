import os

import django
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson
import random
import argparse


def get_name(name, lastname):
    schoolkid_name = Schoolkid.objects.get(full_name__contains=f'{name} {lastname}')
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


def create_commendation(schookid_name, subject):
    year_of_study = schookid_name.year_of_study
    group_letter = schookid_name.group_letter
    lessons = Lesson.objects.all()
    kid_lessons = lessons.filter(year_of_study=year_of_study, group_letter=group_letter)
    lesson = kid_lessons.filter(subject__title=subject).first()

    random_commendation = get_random_commendation()
    Commendation.objects.create(text=random_commendation,
                                created=lesson.date,
                                schoolkid=schookid_name,
                                subject=lesson.subject,
                                teacher=lesson.teacher)


def get_arguments():
    parser = argparse.ArgumentParser(description='Скрипт исправляет плохие оценкки и замечания учителей')

    parser.add_argument('name', help='Имя ученика')
    parser.add_argument('lastname', help='Фамилия ученика')
    parser.add_argument('subject', help='Предмет для написания похвалы от учителя')

    args = parser.parse_args()
    return {'name': args.name,
            'lastname': args.lastname,
            'subject': args.subject}


def main():
    arguments = get_arguments()

    name = arguments['name'].capitalize()
    lastname = arguments['lastname'].capitalize()
    subject = arguments['subject'].capitalize()

    try:
        schookid_name = get_name(name, lastname)
        fix_marks(schookid_name)
        remove_chastisements(schookid_name)
        create_commendation(schookid_name, subject)
    except MultipleObjectsReturned:
        print(f'Учеников с именем {name} найдено больше одного!')
    except ObjectDoesNotExist:
        print(f'Учеников с именем {name} не найдено!')
    except AttributeError:
        print('Вы допустили опечатку в названии предмета!')


if __name__ == '__main__':
    main()
