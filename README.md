# 🛶 Majorka Roztocze – Backend

**Backend aplikacji internetowej dla organizatora spływów kajakowych, wynajmu domków letniskowych oraz miejsc na polu namiotowym.**  
Odpowiada za system rezerwacji, zarządzanie cenami, blogiem oraz administrację treścią strony.

🌐 **Frontend Demo:** [https://majorkaroztocze.pl](https://majorkaroztocze.pl)

---

## ⚙️ Technologie

- **Django** – szybki i bezpieczny framework backendowy
- **Django REST Framework** – budowa API do komunikacji z frontendem
- **PostgreSQL** – relacyjna baza danych hostowana w chmurze
- **Cloudinary** – przechowywanie i obsługa obrazów
- **CKEditor** – rozbudowany edytor treści używany w blogu
- **Railway** – hosting aplikacji backendowej (Django)

---

## 🧩 Funkcjonalności

- **System rezerwacji** domków, miejsc biwakowych i spływów
- **Zarządzanie ofertą** (ceny, opisy, zdjęcia) z poziomu panelu administracyjnego
- **Blog** z obsługą obrazów i edycją przez CKEditor
- **REST API** używane przez frontend React
- **Panel administracyjny** (`/admin`) do pełnej kontroli treści
- **Obsługa przesyłania plików** i przechowywania ich w Cloudinary

---

## 🌐 Hosting i zasoby

- **Railway** – deployment i hosting backendu
- **PostgreSQL** – baza danych w Railway
- **Cloudinary** – zdalna obsługa zdjęć i plików multimedialnych

---

## 📌 Uwagi

- Wszystkie dane (ceny, oferty, rezerwacje) są obsługiwane przez API i synchronizowane z frontendem
- Panel administratora pozwala na pełne zarządzanie treścią
- Obsługa zdjęć i plików działa dzięki Cloudinary
- Blog z CKEditorem pozwala na wygodne formatowanie treści

## ✨ Autor

- Projekt przygotowany dla właściciela oferty Majorka Roztocze.
- Backend: Django + PostgreSQL + Cloudinary