import vk_api
print("VK отписатор v 1.0 by feelatkeen")
userdata = open("userdata.vkotp", "r+")
userdatar = userdata.read()
userdata.close()

if userdatar == "":
    login = input("Логин: ")
    password = input("Пароль: ")
    userdata = open("userdata.vkotp", "w")
    userdata.write(login + ":" + password)
    userdata.close()
else:
    userdatar = userdatar.split(":")
    login = userdatar[0]
    password = userdatar[1]
    deletuser = input("Забыть логин и пароль? (y/n): ")
    if deletuser.lower() == "y":
        userdata = open("userdata.vkotp", "w")
        userdata.write("")
        userdata.close()
        raise  SystemExit

confirmremove = input("Вы точно уверены что хотите очистить ВСЕ подписки? (y/n): ")

if confirmremove.lower() == "n":
    raise SystemExit

def auth_handler():
    userkey = input("Код: ")
    remember_device = True
    return userkey, remember_device

def main():
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    vk = vk_session.get_api()    
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    print("Выберите тип фильтра:")
    print("0 - без фильтра\n1 - только группы\n2 - только паблики\n3 - группы/паблики где вы администрируете\n4 - группы/паблики где вы модерируете\n5 - группы/паблики где вы редактор\n6 - события")
    filtertype = int(input())
    filtertypes = [None, "groups", "publics", "admin", "moder", "editor", "events"]
    if isinstance(filtertype, int):
        if filtertype < 6:
            filtertype = filtertypes[filtertype]
    else:
        print("Ошибка!")
        raise SystemExit
    groups = vk.groups.get(filter=filtertype, count="2")
    publicwrite = open("publics.txt", "a")
    while len(groups['items']) != 1:    
        grouptype = ""
        groups = vk.groups.get(filter=filtertype, count="2")
        if vk.groups.getById(group_id=groups['items'][0])[0]['type'] == "page":
            grouptype = "public"
        if vk.groups.getById(group_id=groups['items'][0])[0]['type'] == "group":
            grouptype = "club"
        if vk.groups.getById(group_id=groups['items'][0])[0]['type'] == "event":
            grouptype = "event"
        publicwrite.write(vk.groups.getById(group_id=groups['items'][0])[0]['name'] + ": " + "https://vk.com/" + grouptype + str(groups['items'][0]) + "\n")
        print(vk.groups.getById(group_id=groups['items'][0])[0]['name'] + ": " + "https://vk.com/" + grouptype + str(groups['items'][0]))
        vk.groups.leave(group_id=groups['items'][0])
    if len(groups['items']) != 0:
        publicwrite.write(vk.groups.getById(group_id=groups['items'][0])[0]['name'] + ": " + "https://vk.com/" + grouptype + str(groups['items'][0]) + "\n")
        print(vk.groups.getById(group_id=groups['items'][0])[0]['name'] + ": " + "https://vk.com/" + grouptype + str(groups['items'][0]))
        vk.groups.leave(group_id=groups['items'][0])
    print("Моя работа закончена. Все паблики сохранены в publics.txt")

if __name__ == "__main__":
    main()
            