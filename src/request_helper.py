class helper(object):
    @staticmethod
    def parse_request(parser):
        parser.add_argument('name', required=True)
        parser.add_argument('card_type', required=True)
        parser.add_argument('ability', required=True)
        parser.add_argument('description', required=True)
        parser.add_argument('row', required=True)
        parser.add_argument('strength', required=True)
        parser.add_argument('faction', required=True)
        parser.add_argument('quantity', required=True)

        return parser.parse_args()

    @staticmethod
    def validate_card_name(shelf, name):
        if not (name in shelf):
            return False
        
        return True

