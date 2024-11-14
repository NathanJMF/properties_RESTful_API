from flask_restful import reqparse


def get_property_request_parser():
    property_argument_parser = reqparse.RequestParser()

    # Define expected arguments
    property_argument_parser.add_argument(
        "address", type=str, required=True, help="Address cannot be blank!"
    )
    property_argument_parser.add_argument(
        "postcode", type=str, required=True, help="Postcode cannot be blank!"
    )
    property_argument_parser.add_argument(
        "city", type=str, required=True, help="City cannot be blank!"
    )
    property_argument_parser.add_argument(
        "num_rooms", type=int, required=True, help="Number of rooms must be a positive integer."
    )
    property_argument_parser.add_argument(
        "created_by", type=int, required=True, help="Created_by user ID is required and must be an integer."
    )

    return property_argument_parser
