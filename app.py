from flask import Flask, jsonify
import requests

app = Flask(__name__)

# 🟡 تنظیم API Key خودت اینجا
API_KEY = "BZji6kBCqIXB2Lnq6jPYexP6A7w236mI"

# URL پایه BrsApi
BASE_URL = "https://BrsApi.ir/Api/Market/Gold_Currency.php"

@app.route("/api/gold18")
def gold18():
    try:
        # ساخت URL کامل
        url = f"{BASE_URL}?key={API_KEY}"
        r = requests.get(url, timeout=10)
        data = r.json()

        # چک خروجی اگه خطا داشت
        if not isinstance(data, dict) or "price" not in data:
            return jsonify({"ok": False, "error": "invalid response from BRS API", "raw": data})

        # پاسخ استاندارد
        return jsonify({
            "Currency": data.get("symbol", "gold18"),
            "Price": data.get("price"),
            "ChangePercent": data.get("change_percent"),
            "Ok": True,
            "Source": "BrsApi.ir"
        })

    except Exception as e:
        return jsonify({"Ok": False, "error": str(e)})

@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<title>قیمت طلای ۱۸ عیار</title>
<style>
body { background: #0f172a; color:#fff; font-family:Tahoma; text-align:center; padding-top:50px; }
.price { font-size:36px; margin:20px; color: gold; }
.info { font-size:18px; }
.error { color: #ff4d4d; }
</style>
</head>
<body>
<h1>طلای ۱۸ عیار</h1>
<div class="price" id="price">در حال دریافت...</div>
<div class="info" id="change"></div>
<div class="info" id="src"></div>

<script>
fetch("/api/gold18")
  .then(r => r.json())
  .then(d => {
    if (!d.Ok) {
      document.getElementById("price").innerHTML =
        '<span class="error">خطا ❌</span>';
      return;
    }
    document.getElementById("price").innerText = d.Price + " تومان";
    document.getElementById("change").innerText = "تغییر: " + (d.ChangePercent ?? "-");
    document.getElementById("src").innerText = "منبع: " + d.Source;
  })
  .catch(e => {
    document.getElementById("price").innerHTML = '<span class="error">خطا ❌</span>';
  });
</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
