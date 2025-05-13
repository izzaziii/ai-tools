{
    "week": 23,
    "year": 2024,
    "conversion_rates": {
        "traffic_to_view_item": 0.0412,
        "view_item_to_type_addr": 0.198,
        "type_addr_to_add_contact": 0.572,
        "add_contact_to_add_addr": 0.785,
        "add_addr_to_add_date": 0.601,
        "add_date_to_checkout": 0.883,
        "checkout_to_purchase": 0.729,
        "traffic_to_purchase": 0.00287
    },
    "percentiles_vs_previous_weeks": {
        "traffic_to_view_item": 55,
        "view_item_to_type_addr": 18,
        "type_addr_to_add_contact": 40,
        "add_contact_to_add_addr": 50,
        "add_addr_to_add_date": 30,
        "add_date_to_checkout": 65,
        "checkout_to_purchase": 45,
        "traffic_to_purchase": 50
    },
    "flags": {
        "below_25th_percentile": [
            "view_item_to_type_addr"
        ]
    },
    "significant_changes": [
        "View_item to type_addr conversion rate has dropped significantly, falling into the 18th percentile and flagged as below the 25th percentile.",
        "Add_addr to add_date conversion rate is near the lower quartile but not flagged as below 25th percentile.",
        "Traffic to view_item and other downstream conversion rates remain stable compared to previous weeks."
    ],
    "insights": [
        "The key issue in the funnel is the notably low conversion rate from viewing an item to typing an address, indicating a potential UX or motivation barrier at this stage.",
        "Despite healthy overall traffic and purchase rates, this early funnel drop threatens scalability and limits overall conversion growth.",
        "Downstream conversion steps appear steady, so initiatives focused on improving the transition from item viewing to address input would yield the greatest lift.",
        "Recommended actions include revisiting the item detail page design, clarifying next steps, and reducing friction around starting the address entry process."
    ]
}