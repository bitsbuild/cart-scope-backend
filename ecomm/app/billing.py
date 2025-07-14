import weasyprint
def billing(product_name_list,product_quantity_list,product_price_list,discount_percentage):
    amnt = sum(product_price_list)
    disc = (discount_percentage*amnt)/100
    final_amnt = amnt - disc
    return {
        'amount':amnt,
        'discount':disc,
        'final_amount':final_amnt,
        'invoice':0
    }