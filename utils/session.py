usuario_logado = None

def set_usuario(usuario_row):
    global usuario_logado
    usuario_logado = usuario_row

def get_usuario():
    return usuario_logado
