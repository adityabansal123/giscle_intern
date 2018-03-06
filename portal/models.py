from py2neo import Graph, Node, Relationship
import uuid


graph = Graph()

class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def register(self, Name, Email, Contact, Password, Linkedin, CV):
        if not self.find():
            user = Node("User",
                         name = Name,
                         username = self.username,
                         email = Email,
                         contact = Contact,
                         password = Password,
                         linkedin = Linkedin,
                         cv = CV)
            graph.create(user)
            return True
        return False

    def verify_password(self, password):
        user = self.find()

        if not user:
            return False
        
        return password == user["password"]
    
    def apply(self, title, skills, ques):
        user = self.find()
        details = Node("Details",
                        id = str(uuid.uuid4()),
                        title = title,
                        ques = ques)
        rel = Relationship(user, "SENT", details)
        graph.create(rel)
        skills = [x.strip() for x in skills.lower().split(",")]
        skills = set(skills)
        for skill in skills:
            s = Node("Skill", name = skill)
            graph.merge(s)
            rel = Relationship(s, "TAGGED", details)
            graph.create(rel)
            #graph.merge(details)
            #details["name"] = skill
            #details.push()

def entries():
    query = """
            MATCH (user:User)-[:SENT]->(details:Details)
            RETURN user.name AS Name, user.username AS UserName, user.email AS Email, user.contact AS Contact, user.linkedin AS Linkedin, details.title AS Position, details.ques AS Answer
            """
    r = list(graph.run(query))
    return r
    


