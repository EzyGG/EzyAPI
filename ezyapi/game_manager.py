import sys
import sessions
import mysql_connection as connect


__user: sessions.User = None
__committed: bool = False


class UserParameterExpected(Exception):
    def __init__(self):
        super().__init__("Must be run with parameters: (--uuid <uuid> or --username <username>) and --password <pwd>")


class AlreadyCommitted(Exception):
    def __init__(self):
        super().__init__("This set is already committed.")


def client_initialization():
    global __user
    args = list(sys.argv[1:])
    if len(args) >= 4 and "--password" in args and args.index("--password") != len(args) - 1:
        password = args[args.index("--password") + 1]
        args.pop(args.index("--password"))
        args.pop(args.index("--password") + 1)

        if "--uuid" in args and args.index("--uuid") != len(args) - 1:
            id = args[args.index("--uuid") + 1]
            args.pop(args.index("--uuid"))
            args.pop(args.index("--uuid") + 1)
        elif "--username" in args and args.index("--username") != len(args) - 1:
            id = args[args.index("--username") + 1]
            args.pop(args.index("--username"))
            args.pop(args.index("--username") + 1)
        else:
            raise UserParameterExpected()

        __user = sessions.User(id, password)
        if not __user.connected():
            raise sessions.UserNotFoundException()
    else:
        raise UserParameterExpected()


def linked():
    return __user and isinstance(__user, sessions.User)


def get_user():
    return __user


def set_user(user: sessions.User):
    global __user
    if not user.connected():
        raise sessions.UserNotFoundException()
    __user = user


def is_committed():
    return bool(__committed)


def register_new_set(game_id: int, won: bool, exp_earned: int = 0, gp_earned: int = 0, other: str = None, query: str = None):
    global __user, __committed
    if __committed:
        raise AlreadyCommitted()
    connect.execute(f"""INSERT sets(player, game, won, exp, gp, other) VALUES ("{__user.get_uuid()}", "{game_id}",
                        {1 if won else 0}, {exp_earned}, {gp_earned}, "{"null" if other is None else other}")""")
    connect.commit()
    connect.execute(f"""UPDATE `users` SET `exp`=(SELECT `exp` WHERE `uuid`="{__user.get_uuid()}") + {exp_earned}
                        WHERE `uuid`="{__user.get_uuid()}\"""")
    connect.commit()
    connect.execute(f"""UPDATE `users` SET `gp`=(SELECT `gp` WHERE `uuid`="{__user.get_uuid()}") + {gp_earned}
                        WHERE `uuid`="{__user.get_uuid()}\"""")
    connect.commit()
    if query:
        connect.execute(str(query))
        connect.commit()
    __committed = True
