from owlready2 import *

onto = get_ontology("ontology.owl").load()

#if onto is not None:
#    onto.destroy()

with onto: 
    class Agent(Thing):
        pass

    class AgentMover(Agent):
        pass

    class Box(Agent):
        pass

    class Position(Agent):
        pass

    class has_position(FunctionalProperty, ObjectProperty):
        domain = [AgentMover]
        range = [Position]

    class has_position_x(FunctionalProperty, DataProperty):
        domain = [Position]
        range = [int]

    class has_position_z(FunctionalProperty, DataProperty):
        domain = [Position]
        range = [int]

    class has_id(FunctionalProperty, DataProperty):
        domain = [AgentMover]
        range = [int]

onto.save("./Act Integradora/ontology.owl")