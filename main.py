import core.main as m
instance = m.login()

# instance.load_categories()[0].write_category_contents()
# print(instance.load_categories())
instance.load_categories()[0].load_category_contents()
