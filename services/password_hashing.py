import bcrypt

def hash_password(input_string):
    # Gerando um salt aleatório
    salt = bcrypt.gensalt()
    
    # Hasheando a string com o salt
    hashed = bcrypt.hashpw(input_string.encode('utf-8'), salt)
    
    return hashed

def check_hashed_password(input_string, hashed_string):
    # Verificando se a senha fornecida corresponde ao hash
    return bcrypt.checkpw(input_string.encode('utf-8'), hashed_string)
