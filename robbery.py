enemies_2 = [('охранник', 100, 10, '', 'Ах ты, нажмите тревожную кнопку!', ('кровотечение', 20)),
             ('автоматчик', 150, 20, '', 'Противник на 12 часов!', ('кровотечение', 10)),
             ('снайпер', 50, 50, '', 'Вижу противника, отслеживаю', ('страх', 10)),
             ('пулеметчик', 200, 30, '', 'Гони, гони, гони!', ('вялость', 1)),
             ('офицер', 80, 70, '', 'Вот и пришел твой конец, щенок!', ('страх', 10)),
             ('Джон', 40, 200, '', 'Глупец, это просто бизнес', ('страх', 10))]
# [<имя>, <здоровье>, <урон>, <заклинание(пока пустая строчка)>, <фраза перед боем>, <один из трех эффектов, сколько отнимает от показателя>]
dungeon_2 = ['Я и Джон давно планировали это ограбление\nМы составили план и тщательно подготовились\nКогда все было готово, мы заехали в оружейную лавку,,,',
             enemies_2,
             {'большая аптечка': ['med', 30, 'Лучшее лекарство на рынке', 150],
              'аптечка': ['med', 20, 'Второе лекарство на рынке', 100],
              'пулемет томпсона': ['gun', 60, 'Скорострельный и мощный "томми"', 30],
              'мачете': ['gun', 50, 'Надежное холодное оружие', 80],
              'дезерт игл': ['gun', 80, 'Блюститель пустнынного закона', 60]}, # type('gun', 'med', 'luck', 'def'), price, description, points added to skill
             ['Купив оружие, мы поехали в банк.\nВзяв в руки оружие, я выбил дверь ногой и потребовал сложить все деньги в сумку\nНо старый охранник был против этого...',
              'Расправившись с охранником, я собрал деньги в сумку.\nОказалось, что этот гад нажал тревожную кнопку\nУслышав сирену, я двинулся к черному входу, где меня поджидал первй коп',
              'Опустошив магазин, мне наконец удалось продырявить голову этому придурку\nЯ неспешно решил пробраться к фургону обходным путем\nЯ был почти у цели, но неожиданно рядом с моей головой просвистела пуля...',
              'Каким-то образом мне удалось ранить проклятого снайпера и сбежать\nЯ залез в фургон.Джон похлопал меня по плечу и завел мотор\nМы спокойно ехали по шоссе, но впереди стояла бронированная машина с огромным пулеметом на крыше\nВОТ ТАК СЮРПРИЗ',
              'Последняя пуля была пущена в лоб водителю, а не пулеметчику\nПолицейская машина резко вильнула и врезалась нам в бок\nЯ лишь помню, как весь мир крутился у меня перед галазми.Туда и обратно, туда и обратно\nОчнувшись, я увидел полуживого Джона и оставшегося в живых офицера',
              'Да, опытный боец\nЯ проверил тело и уже хотел пойти к Джону, но..\nОн был сзади меня и держал в руках здоровенную ракетницу\nЗачем, Джон? Все это время я задавался этим вопросом\nЯ приготовился к финальной схватке',
              'Я в последний раз посмотрел на Джона и ушел с огромной кучей денег.\nМожно было бы закончить с такой жизнью, но...\nРазве это интересно?'],
              300 # максимальная денежная награда за противника
             ]