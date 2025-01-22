from owlready2 import *

onto = get_ontology("./Reto/ontology.owl")

#if onto is not None:
#    onto.destroy()

with onto:
    class Agent(Thing):
        pass
    
    class Box(Thing):
        pass

    class Position(Thing):
        pass

    class has_position(FunctionalProperty, ObjectProperty):
        domain = [Agent]
        range = [Position]

    class has_position_x(FunctionalProperty, DataProperty):
        domain = [Position]
        range = [int]

    class has_position_z(FunctionalProperty, DataProperty):
        domain = [Position]
        range = [int]

    class has_id(FunctionalProperty, DataProperty):
        domain = [Agent]
        range=[int]

onto.save("./Reto/ontology.owl")