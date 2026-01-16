import json
import os
import uuid
import xml.etree.ElementTree as ET

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Brand
from django.db import IntegrityError
from django.views.decorators.http import require_GET
from django.db.models import Q
from .forms import BrandForm


DATA_DIR = os.path.join(settings.BASE_DIR, "data", "exports")

def save_brand(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            save_to = data.pop("save_to")

            # ===== Сохранение в БД =====
            if save_to == "db":
                try:
                    Brand.objects.create(**data)
                    messages.success(request, "Данные сохранены в базе данных.")
                except IntegrityError:
                    messages.error(request, "Такая запись уже существует в базе данных!")

            # ===== Сохранение в JSON =====
            elif save_to == "file_json":
                filename = f"{uuid.uuid4()}.json"
                filepath = os.path.join(DATA_DIR, filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                messages.success(request, "Данные сохранены в JSON-файл.")

            # ===== Сохранение в XML =====
            elif save_to == "file_xml":
                filename = f"{uuid.uuid4()}.xml"
                filepath = os.path.join(DATA_DIR, filename)

                root = ET.Element("brand")
                for key, value in data.items():
                    el = ET.SubElement(root, key)
                    el.text = str(value)

                tree = ET.ElementTree(root)
                tree.write(filepath, encoding="utf-8", xml_declaration=True)

                messages.success(request, "Данные сохранены в XML-файл.")

        else:
            messages.error(request, "Ошибка валидации формы.")

    return redirect("brands:index")


def index(request):
    form = BrandForm()

    source = request.GET.get("source", "files")  # files | db

    files = []
    parsed = []
    db_items = []

    if source == "files":
        files = get_all_files()
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
                        item["data"] = {child.tag: child.text for child in root}

                    else:
                        item["valid"] = False
                        item["error"] = "Неизвестный формат"

                except Exception as e:
                    item["valid"] = False
                    item["error"] = str(e)

                parsed.append(item)

    else:
        # source == "db"
        db_items = Brand.objects.order_by("-created_at")

    context = {
        "form": form,
        "source": source,
        "files": files,
        "parsed": parsed,
        "db_items": db_items,
    }
    return render(request, "brands/index.html", context)

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

@require_GET
def search_db(request):
    q = (request.GET.get("q") or "").strip()

    qs = Brand.objects.all().order_by("-created_at")
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(country__icontains=q) |
            Q(description__icontains=q)
        )

    data = [
        {
            "id": b.id,
            "name": b.name,
            "country": b.country,
            "founded": b.founded,
            "description": b.description,
        }
        for b in qs[:50]
    ]
    return JsonResponse({"results": data})

