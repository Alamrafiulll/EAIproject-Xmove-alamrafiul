
# XMove Shoe Shop Web Application

A responsive, pixel-art-inspired web shoe shop built with **HTML, CSS, JS** and powered by a Flask REST API.

---

## Features

- Shop by gender and brand
- Add to cart, order now, view/cancel orders
- Retro game-style font and UI (uses Press Start 2P)
- Mobile-friendly

---

## Folder Structure

```
EAI_project/
├── backend/
│   ├── app.py           # Flask backend (run this first)
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── shop-single.js
│   └── fonts/
│       └── PressStart2P-Regular.ttf   # (Optional)
├── README_WEB.md
└── ...
```

---

## 1. **Prerequisites**

- Python 3.7+ (for backend)
- Flask backend running (`python backend/app.py`)

---

## 2. **Run the Web App**

1. **Start Flask backend:**
   ```bash
   cd backend
   python app.py
   ```
2. **Start local web server:**
   ```bash
   cd ../frontend
   python -m http.server 8000
   ```
3. Open your browser and go to:
   ```
   http://localhost:8000/
   ```

---

## 3. **Retro Pixel Font Setup (Optional, but recommended)**

1. In your `frontend/css/style.css`, these lines add the font:
    ```css
    @font-face {
      font-family: 'PressStart2P';
      src: url('../fonts/PressStart2P-Regular.ttf') format('truetype');
      font-weight: normal;
      font-style: normal;
    }
    body {
      font-family: 'PressStart2P', Arial, sans-serif;
    }
    ```
2. Make sure `fonts/PressStart2P-Regular.ttf` exists.
   - If not, download from [Google Fonts](https://fonts.google.com/specimen/Press+Start+2P) → Download Family → Unzip and copy TTF file.
3. Refresh your browser. All text should look pixelated and retro!

---

## 4. **How to Use**

- **Browse:** "Men", "Women" buttons and brand sidebar.
- **Add to Cart:** Click "Add to Cart".
- **Order Now:** Click "Order".
- **Cart:** Edit or remove items.
- **Orders:** View/cancel orders.

---

## 5. **Troubleshooting**

- **No products?** Make sure backend is running.
- **No pixel font?** Ensure font path is correct and browser cache is cleared (Ctrl+F5).
- **API errors?** Make sure API_URL in JS matches your Flask backend.

---

## 6. **Credits**

- Font: [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P)
- UI: HTML/CSS/JS

---

## 7. **Contact**

For help, open an issue or email the author.
some times you need to define folder example :to run backend 
python backend/app.py 
