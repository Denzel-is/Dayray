from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
from models import Category, Product

class ProductAdminView(ModelView):
    form_overrides = {
        'category_id': SelectField
    }

    def on_form_load(self, form):
        print("on_form_load called")  # Логируем вызов метода
        categories = Category.query.all()
        form.category_id.choices = [(category.category_id, category.name) for category in categories]
        return super().on_form_load(form)


