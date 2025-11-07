{
    "name": "Custom POS",
    "description": "Case study JavaScript",
    "summary": "Case study JavaScript",
    "depends": [
        "base",
        "point_of_sale",
    ],
    "data": [
        "views/pos_config_view.xml"
    ],
    "assets": {
        'point_of_sale._assets_pos': [
            "custom_pos/static/src/**/*",
        ]
    },
    "installable": True
}