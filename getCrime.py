from police_api import PoliceAPI
from police_api.forces import Force
from police_api.neighbourhoods import Neighbourhood

api = PoliceAPI()

force = Force(api,id="Metropolitan Police Service") #London police force
