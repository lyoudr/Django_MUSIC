def api_authenticate(allowed_roles):
    def real_decorator(func):
        def check_role(*args, **kwargs):
            for role in args[1].user.userrole_set.all():
                print('allowed_roles is =>', allowed_roles)
                print('role is =>', role)
                if role.role not in allowed_roles:
                    raise Exception('02', '0002', '403', args[1].user.username)
            return func(*args, **kwargs)
        return check_role
    return real_decorator

    
    