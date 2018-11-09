class Card(object):
    identifier = None
    name = None
    card_type = None # Hero, Special.. 

    def __init__(self, name, card_type):
        self.identifier = uuid.uuid4()
        self.name = name 
        self.card_type
    
    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.card_type

# weather effects etc..
class SpecialCard(Card):
    ability = None 
    description = None 

    def __init__(self, ability, description):
        super(SpecialCard, self).__init__()
        self.ability = ability
        self.description = description
    
    def get_ability(self):
        return self.ability
    
    def get_description(self):
        return self.description

# Units.. but some units act like special cards.. such as Dandelion
class UnitCard(SpecialCard):
    row = None
    strength = None
    faction = None

    def __init__(self, row, strength, faction):
        super(UnitCard, self).__init__()
        self.row = row
        self.strength = strength
        self.faction = faction

        def get_row(self):
            return self.row;
        
        def get_strength(self):
            return self.strength
        
        def get_faction(self):
            return self.faction