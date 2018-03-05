from .views import app
from .models import graph

graph.run("CREATE CONSTRAINT ON (n:User) ASSERT n.username IS UNIQUE")
graph.run("CREATE CONSTRAINT ON (n:Skill) ASSERT n.name IS UNIQUE")
