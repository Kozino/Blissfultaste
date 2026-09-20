#!/usr/bin/env python3
"""Blissful Tastes Restaurant — elegant PDF menu generator (reportlab)."""
import os
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(BASE, 'assets', 'fonts')
OUT = os.path.join(BASE, 'assets', 'blissful-tastes-menu.pdf')
LOGO = os.path.join(BASE, 'assets', 'logo-trans.png')

INTERLUDES = [
    "Every plate leaves our pass the way it would leave a family kitchen - unhurried, generous and made from scratch.",
    "From Lagos to Nairobi, Beirut to Bangkok - every recipe on this table carries a homeland with it.",
    "Breakfast at midnight, jollof at dawn - our table never closes, and neither does the welcome.",
    "Come taste the bliss.",
]

for tag, f in [('CG', 'cormorantgaramond-400.ttf'), ('CGB', 'cormorantgaramond-600.ttf'),
               ('CGI', 'cormorantgaramond-400i.ttf'), ('JS', 'jost-400.ttf'), ('JSM', 'jost-500.ttf')]:
    pdfmetrics.registerFont(TTFont(tag, os.path.join(FONTS, f)))

# ---- palette (from the logo) ----
NAVY = (0.078, 0.149, 0.247)
NAVY_DEEP = (0.039, 0.078, 0.141)
GOLD = (0.706, 0.576, 0.282)
GOLD_DEEP = (0.592, 0.471, 0.184)
GOLD_PALE = (0.906, 0.851, 0.706)
CREAM = (0.969, 0.949, 0.906)
MUTED = (0.431, 0.463, 0.514)

W, H = 595.28, 841.89          # A4
LM, RM = 66, W - 66            # content margins
CONTENT_W = RM - LM

MENU = [
    ("I", "African Specialties", "THE SOUL OF WEST & EAST AFRICA", [
        ("Classic Jollof Rice", "Smoky party jollof, char-grilled chicken, fried plantain & pepper sauce", "35", True),
        ("Suya Beef Skewers", "Hausa-style beef, yaji peanut spice, charred onions & fresh tomato", "38", False),
        ("Egusi & Pounded Yam", "Rich melon-seed stew with assorted meat, spinach & hand-pounded yam", "40", False),
        ("Nyama Choma", "Slow-charred East-African goat, kachumbari salad & ugali", "45", True),
        ("East-African Beef Pilau", "Fragrant spiced pilau rice, tender beef, kachumbari & lime", "32", False),
        ("Light Soup & Fufu", "Tender goat in aromatic light soup with hand-pounded fufu", "36", False),
    ]),
    ("II", "Arabic & Asian Favourites", "PERFUMED GRILLS OF THE LEVANT, WOK-FIRE OF ASIA", [
        ("Blissful Mixed Grill", "Shish tawook, lamb kofta & beef kebab, grilled vegetables, hummus & saj bread", "55", True),
        ("Chicken Shawarma Plate", "Garlic toum, pickles & crispy fries", "28", False),
        ("Lamb Kabsa", "Slow-roasted lamb on fragrant rice, daqous & toasted nuts", "42", False),
        ("Mezze Selection", "Hummus, mutabbal, fattoush, falafel & warm bread", "30", False),
        ("Chicken Biryani", "Layered basmati, saffron & mint raita", "30", False),
        ("Beef Chow Mein", "Wok-tossed noodles, garden vegetables & toasted sesame", "28", False),
        ("Sweet & Sour Chicken", "Crispy chicken, pineapple & peppers with jasmine rice", "30", False),
    ]),
    ("III", "International Grills & Pasta", "TIMELESS COMFORT, BEAUTIFULLY PLATED", [
        ("Char-Grilled Ribeye (250 g)", "Herb butter, sweet-potato fries & market greens", "65", True),
        ("Pan-Seared Salmon", "Lemon beurre blanc, saffron mash & asparagus", "58", False),
        ("Blissful Beef Burger", "Aged cheddar, house sauce & brioche bun, sweet-potato fries", "38", False),
        ("Creamy Chicken Penne", "Sun-dried tomato & parmesan cream", "32", False),
        ("Spaghetti Bolognese", "Slow-simmered beef ragu, basil & parmesan", "34", False),
        ("Sweet-Potato Fries / Garden Salad", "Our famous sides - crisp, golden & fresh", "15 / 12", False),
    ]),
    ("IV", "All-Day Breakfast", "BECAUSE WE NEVER CLOSE - MORNING CLASSICS AT ANY HOUR", [
        ("Full Blissful Platter", "Eggs any style, sausage, baked beans, grilled tomato, toast & fruit", "38", True),
        ("Shakshuka", "Baked eggs in spiced tomato, feta & saj bread", "25", False),
        ("Banana Pancake Stack", "Maple syrup, berries & whipped cream", "22", False),
        ("Masala Omelette & Chapati", "East-African style spiced omelette with buttered chapati", "20", False),
        ("Ful Medames & Falafel", "Slow-cooked fava beans, falafel, pickles & bread", "18", False),
    ]),
    ("V", "Beverages & Desserts", "FRESH-PRESSED, SLOW-BREWED & SWEETLY FINISHED", [
        ("Fresh-Pressed Juices", "Mango, orange, watermelon or pineapple - pressed to order", "15", False),
        ("Chapman Royale", "The classic Lagos cooler - grenadine, citrus & cucumber", "16", False),
        ("Berry Bliss Smoothie", "Mixed berries, banana & honey yoghurt", "18", False),
        ("Specialty Coffee", "Flat white, cappuccino or V60 - single-origin beans", "14", False),
        ("Karak Chai", "Slow-brewed with cardamom & a whisper of saffron", "10", False),
        ("Puff-Puff & Chocolate", "Warm Nigerian doughnuts with chocolate & caramel dips", "18", False),
        ("Kunafa Cheesecake", "Crispy kunafa, molten cheese & orange-blossom syrup", "22", True),
    ]),
]


class Doc:
    def __init__(self):
        self.c = canvas.Canvas(OUT, pagesize=(W, H))
        self.c.setTitle("Blissful Tastes Restaurant - Menu")
        self.c.setAuthor("Blissful Tastes Restaurant, Doha")
        self.y = 0

    # ---------- primitives ----------
    def ls_width(self, s, font, size, cs):
        return pdfmetrics.stringWidth(s, font, size) + cs * max(len(s) - 1, 0)

    def text(self, s, x, y, font, size, color, cs=0, align='left'):
        c = self.c
        w = self.ls_width(s, font, size, cs)
        if align == 'center':
            x = W / 2 - w / 2
        elif align == 'right':
            x = x - w
        c.setFillColor(color)
        t = c.beginText(x, y)
        t.setFont(font, size)
        t.setCharSpace(cs)
        t.textLine(s)
        c.drawText(t)
        return w

    def diamond(self, x, y, s, color):
        c = self.c
        p = c.beginPath()
        p.moveTo(x, y + s)
        p.lineTo(x + s, y)
        p.lineTo(x, y - s)
        p.lineTo(x - s, y)
        p.close()
        c.setFillColor(color)
        c.drawPath(p, fill=1, stroke=0)

    def ornament(self, y, half=64, color=GOLD):
        c = self.c
        c.setStrokeColor(color)
        c.setLineWidth(0.7)
        c.line(W / 2 - 8 - half, y, W / 2 - 12, y)
        c.line(W / 2 + 12, y, W / 2 + 8 + half, y)
        self.diamond(W / 2, y, 3, color)

    def wrap(self, s, font, size, width):
        words, lines, cur = s.split(), [], ''
        for w in words:
            trial = (cur + ' ' + w).strip()
            if pdfmetrics.stringWidth(trial, font, size) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    # ---------- pages ----------
    def cover(self):
        c = self.c
        c.setFillColor(CREAM)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        # frames
        c.setStrokeColor(NAVY)
        c.setLineWidth(2)
        c.rect(28, 28, W - 56, H - 56, fill=0, stroke=1)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.rect(38, 38, W - 76, H - 76, fill=0, stroke=1)
        for x, y in [(38, 38), (W - 38, 38), (38, H - 38), (W - 38, H - 38)]:
            self.diamond(x, y, 4.5, GOLD)

        self.text("ABRAJ INN ROYAL HOTEL  ·  OLD AIRPORT ROAD  ·  DOHA, QATAR",
                  0, H - 84, 'JS', 7.5, GOLD_DEEP, 2.2, 'center')

        # logo
        img = ImageReader(LOGO)
        lw = 205
        c.drawImage(img, (W - lw) / 2, H - 84 - 18 - lw, width=lw, height=lw,
                    preserveAspectRatio=True, mask='auto')

        y = H - 84 - 18 - lw - 34
        self.ornament(y)
        y -= 34
        self.text("A WORLD OF FLAVOURS", 0, y, 'JSM', 9.5, GOLD_DEEP, 4.5, 'center')
        y -= 46
        self.text("MENU", 0, y, 'CGB', 46, NAVY, 18, 'center')
        y -= 30
        self.text("East & West African specialties  ·  Arabic & Asian favourites", 0, y, 'CGI', 12, MUTED, 0.4, 'center')
        y -= 18
        self.text("International grills & pasta  ·  All-day breakfast  ·  Fresh beverages", 0, y, 'CGI', 12, MUTED, 0.4, 'center')
        y -= 34
        self.diamond(W / 2 - 9, y, 3.4, GOLD)
        self.diamond(W / 2 + 9, y, 3.4, GOLD)

        # bottom info
        y = 118
        self.text("OPEN 24 HOURS  ·  MONDAY - SUNDAY", 0, y, 'JSM', 8, NAVY, 2.4, 'center')
        y -= 16
        self.text("ABRAJ INN ROYAL HOTEL, GROUND FLOOR, OQBA BIN NAFIE STREET (OLD AIRPORT ROAD), DOHA", 0, y, 'JS', 7.2, MUTED, 1.1, 'center')
        y -= 14
        self.text("+974 3113 0483   ·   @BTRESTAURANT ON INSTAGRAM, FACEBOOK & TIKTOK", 0, y, 'JS', 7.2, MUTED, 1.1, 'center')
        y -= 20
        self.ornament(y, 46)
        y -= 16
        self.text("ALL PRICES IN QATARI RIYAL (QR)", 0, y, 'JS', 6.8, GOLD_DEEP, 1.8, 'center')
        c.showPage()

    def page_chrome(self, page_no):
        c = self.c
        c.setFillColor(CREAM)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(38, H - 66, W - 38, H - 66)
        c.line(38, 66, W - 38, 66)
        self.diamond(W / 2, H - 66, 3, GOLD)
        self.diamond(W / 2, 66, 3, GOLD)
        self.text("BLISSFUL TASTES", 46, H - 56, 'CGB', 11, NAVY, 1.6)
        self.text("RESTAURANT - DOHA", W - 46, H - 55, 'JS', 7, GOLD_DEEP, 2, 'right')
        self.text("ABRAJ INN ROYAL HOTEL, OLD AIRPORT ROAD, DOHA  ·  +974 3113 0483  ·  OPEN 24 HOURS",
                  0, 48, 'JS', 6.8, MUTED, 1, 'center')
        self.text("- %d -" % page_no, W - 46, 48, 'CGI', 9, GOLD_DEEP, 1, 'right')
        self.y = H - 108

    def section_head(self, num, title, sub):
        c = self.c
        self.y -= 8
        self.text("-  %s  -" % num, 0, self.y, 'CGI', 10, GOLD, 2, 'center')
        self.y -= 24
        self.text(title, 0, self.y, 'CGB', 20, NAVY, 1, 'center')
        self.y -= 15
        self.text(sub, 0, self.y, 'JS', 6.8, MUTED, 2, 'center')
        self.y -= 14
        self.ornament(self.y, 40)
        self.y -= 30

    def item_height(self, name, desc, price, pick):
        lines = self.wrap(desc, 'CGI', 9.5, CONTENT_W - 6)
        return 17 + len(lines) * 12 + 13

    def draw_item(self, name, desc, price, pick):
        c = self.c
        x = LM
        if pick:
            self.diamond(LM + 3, self.y + 4, 2.6, GOLD)
            x = LM + 12
        # name
        c.setFillColor(NAVY)
        t = c.beginText(x, self.y)
        t.setFont('CGB', 12.5)
        t.textLine(name)
        c.drawText(t)
        nw = pdfmetrics.stringWidth(name, 'CGB', 12.5)
        # price
        self.text("QR " + price, RM, self.y, 'CGB', 11.5, GOLD_DEEP, 0.5, 'right')
        pw = pdfmetrics.stringWidth("QR " + price, 'CGB', 11.5)
        # leader
        c.setStrokeColor(GOLD_PALE)
        c.setLineWidth(1)
        c.setDash([0.8, 3])
        c.line(x + nw + 8, self.y + 3, RM - pw - 8, self.y + 3)
        c.setDash([])
        self.y -= 16
        # description
        for ln in self.wrap(desc, 'CGI', 9.5, CONTENT_W - 6):
            c.setFillColor(MUTED)
            t = c.beginText(x, self.y)
            t.setFont('CGI', 9.5)
            t.textLine(ln)
            c.drawText(t)
            self.y -= 12
        self.y -= 13

    def interlude(self, i):
        q = INTERLUDES[i % len(INTERLUDES)]
        lines = self.wrap(q, 'CGI', 12, CONTENT_W - 120)
        block_h = 34 + 30 + len(lines) * 18 + 8
        bottom = 100
        rem = self.y - bottom
        if rem > block_h:
            self.y = bottom + (rem + block_h) / 2
        self.y -= 34
        self.ornament(self.y, 46)
        self.y -= 30
        for ln in lines:
            self.text(ln, 0, self.y, 'CGI', 12, NAVY, 0.3, 'center')
            self.y -= 18
        self.y -= 8

    def build(self):
        self.cover()
        page = 1
        self.page_chrome(2)
        page = 2
        inter = 0
        for num, title, sub, items in MENU:
            # measure whole section
            head_h = 8 + 24 + 15 + 14 + 30
            total = head_h + sum(self.item_height(*it) for it in items)
            if self.y - total < 92:
                if self.y > 330:
                    self.interlude(inter)
                    inter += 1
                self.c.showPage()
                page += 1
                self.page_chrome(page)
            self.section_head(num, title, sub)
            for it in items:
                h = self.item_height(*it)
                if self.y - h < 92:
                    self.c.showPage()
                    page += 1
                    self.page_chrome(page)
                self.draw_item(*it)
        # closing footnote on last page
        if self.y < 150:
            self.c.showPage()
            page += 1
            self.page_chrome(page)
        self.y -= 6
        self.ornament(self.y, 40)
        self.y -= 22
        self.diamond(W / 2 - 60, self.y + 3, 2.4, GOLD)
        self.text("denotes a chef's recommendation", W / 2 - 50, self.y, 'CGI', 9, MUTED, 0.4)
        self.y -= 16
        self.text("Please inform our team of any allergies - our kitchen is happy to adapt any dish for you.",
                  0, self.y, 'CGI', 9, MUTED, 0.3, 'center')
        self.y -= 20
        self.text("ORDER DELIVERY ON KEETA & TALABAT  ·  COME TASTE THE BLISS", 0, self.y, 'JSM', 7.5, GOLD_DEEP, 2, 'center')
        self.c.showPage()
        self.c.save()
        print("PDF written:", OUT, "pages:", page)


if __name__ == '__main__':
    Doc().build()
