from django.core.exceptions import ValidationError
from .models import Review, Visit, Place
from django.db.models import Avg


def update_place_rating(place):                         #Среднее значение
    res = Review.objects.filter(place=place)            #Выбераем все отзывы из заведения
    avg = res.aggregate(Avg('rating'))['rating__avg']   #среднее значение рейтинга
    if avg is None:                                     # Если отзывов нет, агрегация вернет None
        place.rating = 0.0
    else:                                               # Округляет средний рейтинг до одного знака после запятой
        place.rating =round(avg, 1)
    place.save()


def create_place_visit(place, user, secret_key, visit_date):                            #Создание записи о заведения
    if place.secret_key != str(secret_key):                                             #Сравнение секретного кода с заведение
        raise ValidationError('Неверный 8-значный код заведения.')
    if Visit.objects.filter(user=user, place=place, visit_date__isnull=False).exists():
        raise ValidationError('Вы уже были в данном заведение.')

    visit = Visit(user=user, place=place, visit_date=visit_date)                        #Создание нового объекта посещения
    visit.save()                                                                        #Запись этого заведения
    return visit


def create_review(user, place, rating, text=''):                                        #принимает уже готового пользователя
    if not Visit.objects.filter(user=user, place=place).exists():                       #Проверка посещения
        raise ValidationError('Сначала подтвердите посещение заведения.')
    if place.objects.filter(user=user, place=place).exists():
        raise ValidationError('Вы уже оставляли отзыв об этом заведении.')

    review = Review(user=user, place=place, rating=rating, text=text)                   #Создание нового объекта отзывов
    review.full_clean()                                                                 #Принудительно запускает все валидаторы модели
    review.save()                                                                       #Сохраняет отзыв в БД
    update_place_rating(place)                                                          #Пересчитывает и обновляет общий рейтинг заведения
    return review                                                                       #Возвращает созданный объект отзыва