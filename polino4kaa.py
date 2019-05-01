from Server import Server, list_of_users
from config import vk_api_token
import random
from robbery import dungeon_2
import os
server1 = Server(vk_api_token, 181682083, 'server1')


class Hero:
    def __init__(self, id):
        self.health = 100
        self.defence = 50
        self.weapons = {'fist': 5, 'stick': 10}
        self.luck = 0
        self.medicine = []
        self.book = [('страх', 'снимает очки защиты'), ('вялость', 'шанс успешно уклониться ниже'), ('коровотечение', 'снимает очки здоровья')]
        self.current_weapon = 'fist'
        self.beaten = {'крыса': 10}
        self.money = 100
        self.id = id

    def fight_normal(self, opp):
        action = str(server1.send_msg_keyboard(self.id, f'\nпротивник: {opp.name}\nмаксимальный урон: {opp.damage}\n'
              f'статус противника: {opp.health}\nстатус вашего героя: {self.health}\nстатус защиты: {self.defence}\n', process))
        while action not in ['Атака', 'Уклонение', 'Защита']:
            if action == 'Аптечка':
                self.get_health()
            elif action == 'Сменить оружие':
                self.change_weapon()
            elif action == 'Достать глоссарий':
                self.get_spells()
            action = str(server1.send_msg_keyboard(self.id, f'\nпротивник: {opp.name}\nмаксимальный урон: {opp.damage}\n'
              f'статус противника: {opp.health}\nстатус вашего героя: {self.health}\nстатус защиты: {self.defence}\n', process))
        if action == 'Атака':
            opp.health -= self.weapons[self.current_weapon]
            server1.send_msg(self.id, f'Вы наносите врагу сокрушительный удар, отнимающий {self.weapons[self.current_weapon]} очков здоровья' + '\n')
            damage = random.randint(1, opp.damage)
            self.health -= damage
            server1.send_msg(self.id, f'Но враг тут же наносит вам ответный удар, отнимая {damage} очков здоровья' + '\n')
        elif action == 'Уклонение':
            if random.randint(self.luck, 20) > 15:
                server1.send_msg(self.id, f'Вы уворачиваетесь и наносите противнику двойной урон.' + '\n')
                opp.health -= self.weapons[self.current_weapon] * 2
            else:
                server1.send_msg(self.id, 'Вы подскользнулись и упали, дав противнику шанс нанести вам двойной урон' + '\n')
                self.health -= random.randint(1, opp.damage) * 2
        else:
            if self.defence <= 0:
                server1.send_msg(self.id, 'Да вы дурак, батюшка, щит-то дырявый\nВы получаете тройной урон' + '\n')
                self.health -= random.randint(1, opp.damage) * 3
                return
            attack = random.randint(1, opp.damage)
            if self.defence - attack < 0:
                server1.send_msg(self.id, f'Вы защитились, но щит подвел в последний момент\n'
                      f'Вы получаеете {(attack - self.defence) // 2} очков урона' + '\n')
                self.defence = 0
                self.health -= (attack - self.defence) // 2
            else:
                self.defence -= attack
                server1.send_msg(self.id, 'Вы успешно защитились' + '\n' + f'Защитившись, вы проводите неожиданную атаку, которая отняа у'
                  f' противника {self.weapons[self.current_weapon]} очков здоровья')
            opp.health -= self.weapons[self.current_weapon]

    def get_health(self):
        if self.medicine:
            plus = self.medicine.pop(0)
            self.health += plus
            server1.send_msg(self.id, f'Использовав волшебный пузырек, вы восстанавливаете {plus} очков здоровья' + '\n')
        else:
            server1.send_msg(self.id, 'Пусто' + '\n')

    def change_weapon(self):
        server1.send_msg(self.id, '\n'.join(f'{el[0]} - {el[1]} очков урона' for el in self.weapons.items()))
        answer = server1.vk_mes(self.id, 'Введите название оружия\n', process).lower().rstrip()
        if answer in self.weapons:
            self.current_weapon = answer
        else:
            self.current_weapon = 'fist'
        server1.send_msg(self.id, f'Теперь вы пользуетесь {self.current_weapon}' + '\n')

    def beaten_func(self, opp):
        self.beaten[opp.name] = self.beaten.get(opp.name, 0) + 1
        if self.beaten[opp.name] > 10:
            server1.send_msg(self.id, 'У вас новое заклинание!\nВы можете открыть книгу во время битвы\n' + '\n')
            self.book.append((opp.name, opp.spell))

    def get_spells(self):
        server1.send_msg(self.id, 'Вы открыли книгу заклинаний\n' + '\n'.join(f'{el[0]} - {el[1]}' for el in self.book))

    def effect(self, name_of_effect, impact, back=1):
        impact = back * impact
        if name_of_effect == 'кровотечение':
            self.health = max(30, self.health - impact)
        elif name_of_effect == 'вялость':
            self.luck = max(0, self.luck - impact)
        elif name_of_effect == 'страх':
            self.defence = max(10, self.defence - impact)


class Enemy:
    def __init__(self, name, health, damage, spell, pharse, effect):
        self.phrase = pharse
        self.spell = spell
        self.name = name
        self.health = health
        self.damage = damage
        self.effect = effect

    def spell(self):
        self.health //= 2
        print(f'Вы применили магическое заклинание')


class Dungeon:
    def __init__(self, description, enemies, for_sell, story, reward, id):
        self.description = description
        self.enemies = enemies.copy()
        self.for_sell = for_sell.copy()
        self.story = story
        self.reward = reward
        self.id = id

    def in_dungeon(self, hero):
        self.shop(hero)
        for i in range(len(self.enemies)):
            server1.send_msg(self.id, ('#' * 10) + '\n' + self.story[i] + '\n' + ('#' * 10) + '\n')
            chosen = self.enemies.pop(0)
            opp = Enemy(chosen[0], chosen[1], chosen[2], chosen[3], chosen[4], chosen[5])
            server1.send_msg(self.id, opp.phrase)
            server1.send_msg(self.id, f'{opp.name} накладывает на вас эффект {opp.effect[0]}')
            hero.effect(opp.effect[0], opp.effect[1])
            while opp.health > 0 and hero.health > 0:
                hero.fight_normal(opp)
            if hero.health <= 0:
                server1.send_msg(self.id, 'Похоже, вы проиграли\n')
                return
            else:
                hero.effect(opp.effect[0], opp.effect[1], -1)
                hero.beaten_func(opp)
                server1.send_msg(self.id, 'Славная победа\nПосле битвы силы вернулись, отрицательные эффекты снимаются\n')
                reward = random.randint(10, self.reward)
                hero.money += reward
                server1.send_msg(self.id, f'Вы получаете {reward} монет в награду')
        server1.send_msg(self.id, ('#' * 10) + '\n' + self.story[-1] + '\n' + ('#' * 10) + '\n')

    def shop(self, hero):
        server1.send_msg(self.id, f'{"#" * 10}\n{self.description}\n{"#" * 10}\n')
        server1.send_msg(self.id, 'Вы встречаете какого-то непонятного торговца...')
        if server1.vk_mes(self.id, 'Не хотите ли что-нибудь купить?(введите "выход", чтобы пропустить)\n', process).lower().rstrip() != 'выход':
            server1.send_msg(self.id, 'Выбирайте\nНаберите "выход", чтобы продолжить приключение\n')
            while hero.money > 0 and self.for_sell:
                server1.send_msg(self.id, f'Ваши деньги - {hero.money}')
                answer = server1.vk_mes(self.id, '\n'.join([f'{el[0]} - {el[1][1]}\n{el[1][2]}' for el in self.for_sell.items()]) + '\n', process).lower().rstrip()
                if answer.lower() not in self.for_sell:
                    break
                else:
                    if self.for_sell[answer][1] <= hero.money:
                        server1.send_msg(self.id, f'Вы приобрели {answer}')
                        hero.money -= self.for_sell[answer][1]
                        if self.for_sell[answer][0] == 'med':
                            hero.medicine.append(self.for_sell[answer][3])
                        else:
                            hero.weapons[answer] = self.for_sell[answer][3]
                        del self.for_sell[answer]
                    else:
                        server1.send_msg(self.id, 'Ах ты обаманщик!!')
                        break
        server1.send_msg(self.id, 'Вы покинули торговца\n')


def process(current_user):
    port = os.getenv('PORT', default=8000)
    updater.start_webhook(port=port)
    hero = Hero(current_user)
    dungeon = Dungeon(dungeons[0][0], dungeons[0][1], dungeons[0][2], dungeons[0][3], dungeons[0][4], current_user)
    dungeon.in_dungeon(hero)
    hero.__init__(current_user)
    server1.send_msg(current_user, 'спасибо за игру')
    list_of_users.remove(current_user)
                         
dungeons = list()
dungeons.append(dungeon_2)
while True:
    current_user = server1.start()
    process(current_user)





