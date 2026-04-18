
import json
def get_data(username):
    if username:
        try:
            with open("app/db/sampledata.json","r") as file:
                data = json.load(file)
            return data['users'][username]
        except Exception as e:
            return {"error found ": e}
    else:
        return {"message":"username not found"}