def individual_serial(todo)->dict:
    return{
        "id":str(todo["_id"]),
        "name": str(todo["name"]),
        "description": str(todo["description"]),
        "complete": str(todo["complete"]),
    }
# deserialize and return all todos if needed
def list_serial(todos)->list:
    return[individual_serial(todo) for todo in todos]