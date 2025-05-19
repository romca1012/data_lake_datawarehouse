# data_lake_datawarehouse
Projet académique

📘 API Documentation – TP3
L’API expose différents endpoints pour accéder aux métriques, à l’audit du Data Lake et à la recherche textuelle. Elle est construite avec Django REST Framework.

🌐 Base URL
bash
Copier
Modifier
http://localhost:8000/api/
📊 Endpoints de Metrics
GET /api/metrics/top-products/?x=5
Description : Retourne les X produits les plus achetés.

Paramètres :

x (int, optionnel) : nombre de produits à retourner (par défaut : 5)

Réponse :

json
Copier
Modifier
[
  {"product": "Laptop", "quantity": 154},
  {"product": "Headphones", "quantity": 132}
]
GET /api/metrics/total-by-user/
Description : Donne le total dépensé par utilisateur, classé par type de produit.

Réponse :

json
Copier
Modifier
[
  {
    "user_id": "user_001",
    "total": 345.20,
    "by_category": {
      "electronics": 200.0,
      "books": 145.2
    }
  }
]
GET /api/metrics/last-5min/
Description : Affiche le montant total des achats réalisés dans les 5 dernières minutes.

Réponse :

json
Copier
Modifier
{
  "total_transactions": 24,
  "total_amount": 1580.75
}
🔍 Endpoints d’Audit du Data Lake
GET /api/audit/resources/
Description : Liste tous les fichiers bruts disponibles dans le Data Lake (JSON).

Réponse :

json
Copier
Modifier
[
  "2025-05-18.json",
  "2025-05-19.json"
]
GET /api/audit/version/?date=YYYY-MM-DD
Description : Retourne le contenu brut du fichier JSON du jour spécifié.

Paramètre :

date (str, requis) : format YYYY-MM-DD

Réponse :

json
Copier
Modifier
[
  {"user_id": "user_002", "product": "Mouse", "amount": 25.0}
]
GET /api/audit/access-log/
Description : Simule des logs d'accès aux ressources du Data Lake (à des fins de gouvernance/démo).

Réponse :

json
Copier
Modifier
[
  {
    "user": "admin",
    "action": "read",
    "resource": "2025-05-19.json",
    "timestamp": "2025-05-19T14:55:00Z"
  }
]
🧠 Recherche textuelle
GET /api/fulltext_search/<text>
Description : Effectue une recherche textuelle brute dans le contenu des fichiers JSON du Data Lake.

Paramètre :

text (dans l’URL) : chaîne de caractères à rechercher

Exemple :

bash
Copier
Modifier
/api/fulltext_search/headphones