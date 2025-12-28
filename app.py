from flask import Flask, jsonify
import requests

app = Flask(__name__)

# 🔑 API KEY
API_KEY = "BZji6kBCqIXB2Lnq6jPYexP6A7w236mI"

API_URL = "https://BrsApi.ir/Api/Market/Gold_Currency.php"

# ✅ User-Agent معتبر (خیلی مهم)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# ===============================
# API: قیمت طلا و ارز
# ===============================
@app.route("/api/market")
def market():
    try:
        r = requests.get(
            API_URL,
            params={"key": API_KEY},
            headers=HEADERS,
            timeout=10
        )
        data = r.json()

        return jsonify({
            "Ok": True,
            "Source": "BrsApi.ir",
            "Data": data
        })

    except Exception as e:
        return jsonify({
            "Ok": False,
            "error": str(e)
        })


# ===============================
# سایت (UI)
# ===============================
@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<title>قیمت طلا و ارز</title>
<style>
body {
    background: #0f172a;
    color: #fff;
    font-family: Tahoma;
    text-align: center;
    padding-top: 50px;
}
.card {
    display: inline-block;
    background: #020617;
    padding: 30px 40px;
    border-radius: 20px;
    box-shadow: 0 0 30px rgba(255,215,0,0.25);
}
h1 { color: gold; }
.price {
    font-size: 28px;
    margin: 15px 0;
}
.info {
    font-size: 14px;
    color: #94a3b8;
}
.error {
    color: #ff4d4d;
}
</style>
</head>
<body>

<div class="card">
    <h1>قیمت بازار</h1>
    <div class="price" id="gold">در حال دریافت...</div>
    <div class="price" id="usd"></div>
    <div class="info" id="src"></div>
</div>

<script>
fetch("/api/market")
  .then(r => r.json())
  .then(res => {
    if (!res.Ok) {
      document.getElementById("gold").innerHTML =
        '<span class="error">خطا ❌</span>';
      return;
    }

    const data = res.Data;

    // 🔸 طلای ۱۸ عیار
    if (data.geram18) {
      document.getElementById("gold").innerText =
        "طلای ۱۸ عیار: " + data.geram18.price + " تومان";
    }

    // 🔸 دلار
    if (data.usd) {
      document.getElementById("usd").innerText =
        "دلار: " + data.usd.price + " تومان";
    }

    document.getElementById("src").innerText =
      "منبع: " + res.Source;
  })
  .catch(() => {
    document.getElementById("gold").innerHTML =
      '<span class="error">خطا ❌</span>';
  });
</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
