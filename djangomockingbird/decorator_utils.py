
def resolve_input_path(path):
    parts = path.split('.')
    model_name = parts[len(parts)-1]
    parts.remove(model_name)
    module = '.'.join(parts)
    return module, model_name

def build_file_path(module):
    new_path = module.replace('.', '/')
    final_path = new_path + '.py'
    return final_path
