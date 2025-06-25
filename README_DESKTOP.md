
# XMove Shoe Shop Desktop Application

A retro-inspired desktop shoe shop client built with **Tkinter** (Python) and powered by a Flask backend REST API.

---

## Features

- Browse, filter, and search men's and women's shoes by brand.
- Add shoes to cart, place orders, view and cancel orders.
- Stylish **90s pixel-game look** (optional Press Start 2P font).
- Desktop experience, smooth and simple.

---

## Folder Structure

```
EAI_project/
├── backend/
│   ├── app.py           # Flask backend (run this first)
│   └── static/          # Product images
├── frontend/
│   ├── index.html
│   └── ...              # Web app code (see separate README)
├── fonts/
│   └── PressStart2P-Regular.ttf  # Pixel font (see below)
├── desktop_app.py       # Main desktop app (Tkinter)
├── README_DESKTOP.md
├── README_WEB.md
└── ...
```

---

## 1. **Prerequisites**

- Python 3.7+
- `pip install flask pillow requests`
- (Optional for pixel font:) Ability to install fonts on your OS

---

## 2. **Setup & Run**

### **A. Start the Backend**

Open a terminal in `backend/` and run:
```bash
python app.py
```
- By default runs on `http://127.0.0.1:5000/`

---

### **B. Install the Retro Pixel Font (Optional, for 90s look)**

1. Go to `fonts/PressStart2P-Regular.ttf`  
   - If you don’t have it, download:  
     https://fonts.google.com/specimen/Press+Start+2P (Download Family → unzip)
2. **Double-click the font file and click 'Install'** on Windows or macOS.
3. Restart your Python app to apply the font.

If you skip this, the app will fall back to Arial.

---

### **C. Run the Desktop App**

From the root project folder (where `desktop_app.py` is), run:
```bash
python desktop_app.py
```

**Tip:**  
If you see `Font file not found. Using default font.`, double-check the `fonts/PressStart2P-Regular.ttf` file **and** that it is installed on your OS.

---

## 3. **How to Use**

- **Browse:** Use "Men"/"Women" buttons and brand sidebar.
- **Add to Cart:** Click "Add to Cart" on a shoe.
- **Order Now:** Click "Order" to buy directly.
- **Cart:** See, update, or remove items.
- **Orders:** View or cancel your previous orders.

---

## 4. **Troubleshooting**

- **No products?** Make sure Flask backend is running.
- **Font not pixel-style?** Make sure the Press Start 2P font is *installed* on your OS.
- **API errors?** Double-check API_URL in your code.

---

## 5. **Credits**

- Font: [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P)
- UI: Tkinter + Pillow

---

## 6. **Contact**

For help, open an issue or email the author.
some times you need to define folder example :to run backend 
python backend/app.py 
---
