def is_admin(user)->bool:
    if user.role == 'Admin':
        return True
    else:
        return False