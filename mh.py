# Generar armas aleatorias para nosotros 4
# Establecer la estructura de los usuarios
# Guardarnos como usuarios
# Generar armas aleatorias con los ajustes anteriores
import argparse
import random
import json


class MHData:
    all_weapons = ['Gran Espada', 'Espada Larga', 'Espada Escudo', 'Doble Espada', 'Martillo', 'Cornamusa',
                   'Lanza', 'Lanza Pistola', 'Hacha Espada', 'Hacha Cargada', 'Glaive Insecto',
                   'Ballesta Ligera', 'Ballesta Pesada', 'Arco', 'Gatador']

    all_styles = ['Gremio', 'Ariete', 'Aereo', 'Sombra', 'Audaz', 'Alquimia']
    data = {}

    def __init__(self):
        self.load_data()

    def load_data(self):
        with open('mh-data.json', 'r') as file:
            self.data = json.load(file)

    def save_data(self):
        json_object = json.dumps(self.data, indent=4)
        with open('mh-data.json', 'w') as outfile:
            outfile.write(json_object)

    def show_user_list(self):
        if 'users' in self.data:
            users = self.data['users']
            if len(users) == 0:
                print('There are not registered users. Use the command \'user add Username\' to add users.')
            else:
                for i in range(0, len(users)):
                    if users[i]['name']:
                        print('({}) {}'.format(i + 1, users[i]['name']))
                    else:
                        print('({}) User {}'.format(i + 1, i + 1))
        else:
            self.data['users'] = []
            print('There are not registered users. Use the command \'user add Username\' to add users.')

    def add_user(self, name):
        if 'users' in self.data:
            self.data['users'].append({'name': name, "active": True, 'weapons': [], 'monsters': []})
        else:
            self.data['users'] = {'name': name, "active": True, 'weapons': [], 'monsters': []}
        print('User {} added successfully.'.format(name))
        self.save_data()

    def edit_user(self, user_id, name):
        if 'users' in self.data:
            users = self.data['users']
            if len(users) < user_id:
                print('Inserted user id is invalid. Use the command \'user ls\' to see the users id.')
            else:
                users[user_id - 1]['name'] = name
                self.save_data()
                print('User {} edited successfully.'.format(name))
        else:
            print('Something went wrong.')

    def remove_user(self, user_id):
        if 'users' in self.data:
            users = self.data['users']
            if len(users) < user_id:
                print('Inserted user id is invalid. Use the command \'user ls\' to see the users id.')
            else:
                users.pop(user_id - 1)
                self.save_data()
                print('User removed successfully.')
        else:
            print('Something went wrong.')

    def get_users_id(self):
        if 'users' in self.data:
            return range(1, len(self.data['users']) + 1)
        else:
            return []

    def show_user_profile(self, user_id):
        if 'users' in self.data:
            if 0 < user_id <= len(self.data['users']):
                user = self.data['users'][user_id - 1]
                if 'name' in user:
                    name = user['name']
                else:
                    name = 'User {}'.format(user_id)
                print(name)

                if 'weapons' in user and len(user['weapons']) > 0:
                    print('-> Armas')
                    for weapon in user['weapons']:
                        if 'name' in weapon and weapon['name'] in self.all_weapons:
                            weapon_message = '  => {}'.format(weapon['name'])
                            available_styles = []
                            if 'styles' in weapon and len(weapon['styles']) > 0:
                                for style in weapon['styles']:
                                    if 'name' in style and 'skill' in style:
                                        available_styles.append(style)
                            if len(available_styles) > 0:
                                weapon_message += ' [{}({})'.format(available_styles[0]['name'], available_styles[0]['skill'])
                                for i in range(1, len(weapon['styles'])):
                                    weapon_message += ', {}({})'.format(available_styles[0]['name'], available_styles[0]['skill'])
                                weapon_message += ']'
                            print(weapon_message)

                print('{}'.format(self.data['users'][user_id - 1]))
        else:
            print('Something went wrong.')

    def show_weapon_list(self):
        for i in range(0, len(self.all_weapons)):
            print('({}) {}'.format(i + 1, self.all_weapons[i]))

    def show_style_list(self):
        for i in range(0, len(self.all_styles)):
            print('({}) {}'.format(i + 1, self.all_styles[i]))

    def random(self, min_skill, max_skill):
        if 'users' in self.data:
            users = self.data['users']
            for i in range(0, len(users)):
                if 'active' in users[i] and users[i]['active']:
                    if users[i]['name']:
                        name = users[i]['name']
                    else:
                        name = 'User {}'.format(i + 1)

                    if 'weapons' in users[i] and len(users[i]['weapons']) > 0:
                        selectable_weapons = []

                        for weapon in users[i]['weapons']:
                            if 'name' in weapon and weapon['name'] in self.all_weapons:
                                if 'styles' in weapon and len(weapon['styles']) > 0:
                                    for style in weapon['styles']:
                                        if 'name' in style and 'skill' in style:
                                            if min_skill <= style['skill'] <= max_skill:
                                                selectable_weapons.append('{} [{}]'
                                                                          .format(weapon['name'], style['name']))
                                else:
                                    selectable_weapons.append('{}'.format(weapon['name']))

                        if len(selectable_weapons) > 0:
                            weapon = random.choice(selectable_weapons)
                        else:
                            weapon = random.choice(self.all_weapons)
                    else:
                        weapon = random.choice(self.all_weapons)

                    print('{}: {}'.format(name, weapon))


def main():
    mh = MHData()

    parser = argparse.ArgumentParser(description='Program for randomize the monster hunter games')
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_user = subparsers.add_parser('user', help='Manage program users')
    parser_user_option = parser_user.add_subparsers(dest='option', required=True)
    parser_user_option_add = parser_user_option.add_parser('add')
    parser_user_option_add.add_argument('name')
    parser_user_option_rm = parser_user_option.add_parser('rm')
    parser_user_option_rm.add_argument('id', type=int)
    parser_user_option_edit = parser_user_option.add_parser('edit')
    parser_user_option_edit.add_argument('id', type=int)
    parser_user_option_edit.add_argument('name')
    parser_user_option.add_parser('ls')

    parser_user_option_profile = parser_user_option.add_parser('user_id', aliases=(str(x) for x in mh.get_users_id()))

    parser_random = subparsers.add_parser('random', help='Manage program randomization')
    parser_random.add_argument('--min', type=int, default=0)
    parser_random.add_argument('--max', type=int, default=3)

    parser_weapon = subparsers.add_parser('weapon', help='Manage program weapons')
    parser_weapon_option = parser_weapon.add_subparsers(dest='option', required=True)
    parser_weapon_option.add_parser('ls')

    parser_styles = subparsers.add_parser('style', help='Manage program weapon styles')
    parser_styles_option = parser_styles.add_subparsers(dest='option', required=True)
    parser_styles_option.add_parser('ls')

    args = parser.parse_args()

    if args.command == 'user':
        if args.option == 'ls':
            mh.show_user_list()
        elif args.option == 'add':
            mh.add_user(args.name)
        elif args.option == 'edit':
            mh.edit_user(args.id, args.name)
        elif args.option == 'rm':
            mh.remove_user(args.id)
        elif args.option.isnumeric():
            mh.show_user_profile(int(args.option))
    elif args.command == 'random':
        mh.random(args.min, args.max)
    elif args.command == 'weapon':
        if args.option == 'ls':
            mh.show_weapon_list()
    elif args.command == 'style':
        if args.option == 'ls':
            mh.show_style_list()


if __name__ == '__main__':
    main()
