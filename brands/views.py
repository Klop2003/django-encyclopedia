import json
import os
import uuid
import xml.etree.ElementTree as ET

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import BrandForm


DATA_DIR = os.path.join(settings.BASE_DIR, "data", "exports")


def index(request):
    form = BrandForm()
    files = get_all_files()
    parsed = []

    if files:
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            path = os.path.join(DATA_DIR, fname)
            item = {
                "filename": fname,
                "ext": ext,
                "valid": True,
                "data": None,
                "error": None,
            }

            try:
                if ext == ".json":
                    with open(path, "r", encoding="utf-8") as f:
                        item["data"] = json.load(f)

                elif ext == ".xml":
                    tree = ET.parse(path)
                    root = tree.getroot()
                    # превращаем <brand><name>..</name>...</brand> в dict
                    item["data"] = {child.tag: child.text for child in root}

                else:
                    item["valid"] = False
                    item["error"] = "Неизвестный формат"

            except Exception as e:
                item["valid"] = False
                item["error"] = str(e)

            parsed.append(item)

    context = {
        "form": form,
        "files": files,
        "parsed": parsed,
    }
    return render(request, "brands/index.html", context)



def save_json(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            filename = f"{uuid.uuid4()}.json"
            filepath = os.path.join(DATA_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            messages.success(request, "Данные успешно сохранены в JSON.")
        else:
            messages.error(request, "Ошибка валидации данных формы.")

    return redirect("brands:index")


def save_xml(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            filename = f"{uuid.uuid4()}.xml"
            filepath = os.path.join(DATA_DIR, filename)

            root = ET.Element("brand")

            for key, value in data.items():
                el = ET.SubElement(root, key)
                el.text = str(value)

            tree = ET.ElementTree(root)
            tree.write(filepath, encoding="utf-8", xml_declaration=True)

            messages.success(request, "Данные успешно сохранены в XML.")
        else:
            messages.error(request, "Ошибка валидации данных формы.")

    return redirect("brands:index")


def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        ext = os.path.splitext(file.name)[1].lower()

        if ext not in [".json", ".xml"]:
            messages.error(request, "Можно загружать только JSON или XML файлы.")
            return redirect("brands:index")

        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(DATA_DIR, filename)

        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Проверка валидности
        if not validate_file(filepath, ext):
            os.remove(filepath)
            messages.error(request, "Файл невалиден и был удалён.")
        else:
            messages.success(request, "Файл успешно загружен.")

    return redirect("brands:index")


def get_all_files():
    if not os.path.exists(DATA_DIR):
        return []

    files = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".json") or fname.endswith(".xml"):
            files.append(fname)

    return files


def validate_file(filepath, ext):
    try:
        if ext == ".json":
            with open(filepath, "r", encoding="utf-8") as f:
                json.load(f)

        if ext == ".xml":
            ET.parse(filepath)

        return True
    except Exception:
        return False
