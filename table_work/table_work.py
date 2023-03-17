from main.models import OwnerModel, TextModel


def add_data_tb(list_tuple: list[tuple[str, str, str]]):
    data = [OwnerModel(lexemm=lexemm, morph=morph, role=role)
            for lexemm, morph, role in list_tuple]
    OwnerModel.objects.bulk_create(data)


def clear_tb():
    OwnerModel.objects.all().delete()
