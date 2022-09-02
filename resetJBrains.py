import os
import shutil


def main():
    home_path = os.getenv('HOME')
    print('''
##################################################################################
#####  Program for reset JBrains IDE test periods version 2020.3 in Manjaro  #####
##################################################################################
''')

    answer = input('Before start you must close all instances of JetBrains IDEs, press Y to continue or any other key '
                   'to cancel: ')
    if answer == 'Y' or answer == 'y':
        # Detect IDE folders
        print()  # And end line
        print('Step (1/4) Detecting IDE folders')
        ide_list = []
        jetbrains_configuration_path = os.path.join(home_path, '.config/JetBrains')
        for file in os.listdir(jetbrains_configuration_path):
            if os.path.isdir(os.path.join(jetbrains_configuration_path, file)):
                ide_list.append(file)
        print('\t-> {} ide(s) detected:'.format(len(ide_list)))
        for ide in ide_list:
            print('\t\t=> {}'.format(ide))

        # Delete file in eval folder
        print('Step (2/4) Deleting eval files [*.evaluation.key]')
        delete_files_counter = 0
        for ide in ide_list:
            ide_path = os.path.join(jetbrains_configuration_path, ide)
            eval_path = os.path.join(ide_path, 'eval')
            if os.path.exists(eval_path):
                if len(os.listdir(eval_path)):
                    for file in os.listdir(eval_path):
                        if file.endswith('.evaluation.key'):
                            print("\t{}".format(os.path.join(eval_path, file)))
                            os.remove(os.path.join(eval_path, file))
                            delete_files_counter += 1
                else:
                    print("\t-> [v] {} - File hasn't been created".format(ide))
            else:
                print("\t-> [x] {} - It doesn't have an eval folder".format(ide))
        if delete_files_counter > 0:
            print("\t{} {} deleted successfully."
                  .format(delete_files_counter, 'file' if delete_files_counter == 1 else 'files'))

        # Edit other.xml in options folder
        print('Step (3/4) Editing other.xml files in option folder')
        edited_files_counter = 0
        for ide in ide_list:
            ide_path = os.path.join(jetbrains_configuration_path, ide)
            option_path = os.path.join(ide_path, 'options')
            other_xml_path = os.path.join(option_path, 'other.xml')
            if os.path.exists(other_xml_path):
                result = ''
                edited = False
                with open(other_xml_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if 'evlsprt' not in line:
                            result += line
                        else:
                            edited = True
                if edited:
                    print("\t{}".format(other_xml_path))
                    with open(other_xml_path, 'w') as f:
                        f.write(result)
                    edited_files_counter += 1
            else:
                print("\t-> [x] {} - It doesn't have an other.xml file".format(ide))
        if edited_files_counter > 0:
            print("\t{} {} edited successfully."
                  .format(edited_files_counter, 'file' if edited_files_counter == 1 else 'files'))

        # Delete java preferences
        print('Step (4/4) Deleting java JetBrains preferences folder')
        jetbrains_java_preferences_path = os.path.join(home_path, '.java/.userPrefs/jetbrains')
        if os.path.exists(jetbrains_java_preferences_path):
            shutil.rmtree(jetbrains_java_preferences_path)
            print("\tFolder deleted successfully.")

        print('\nDone. You\'ve already reset the trial period on JetBrains IDEs.')

    else:
        print('Process canceled by user')


if __name__ == '__main__':
    main()
