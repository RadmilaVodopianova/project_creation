
from django.http import HttpResponse
from datetime import datetime


def page_template(title, content):
    return f"""
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{title}</title>

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: #f8fafc;
            }}

            nav {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 22px 8%;
                background: #1e293b;
                border-bottom: 1px solid #334155;
            }}

            .logo {{
                color: #38bdf8;
                font-size: 24px;
                font-weight: bold;
            }}

            nav a {{
                color: #cbd5e1;
                text-decoration: none;
                margin-left: 25px;
                transition: color 0.2s;
            }}

            nav a:hover {{
                color: #38bdf8;
            }}

            main {{
                max-width: 1050px;
                margin: 80px auto;
                padding: 0 25px;
                text-align: center;
            }}

            h1 {{
                font-size: 42px;
                margin-bottom: 15px;
            }}

            .subtitle {{
                color: #94a3b8;
                font-size: 18px;
                line-height: 1.7;
            }}

            .cards {{
                display: flex;
                gap: 20px;
                margin-top: 45px;
                flex-wrap: wrap;
            }}

            .card {{
                flex: 1 1 220px;
                background: #1e293b;
                padding: 30px;
                border-radius: 16px;
                border: 1px solid #334155;
                transition: transform 0.2s;
            }}

            .card:hover {{
                transform: translateY(-5px);
            }}

            .card h2 {{
                color: #38bdf8;
            }}

            .card p {{
                color: #94a3b8;
            }}

            .button {{
                display: inline-block;
                background: #0284c7;
                color: white;
                padding: 14px 25px;
                margin-top: 25px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
            }}

            .button:hover {{
                background: #0369a1;
            }}

            .clock {{
                font-size: 42px;
                color: #38bdf8;
                font-weight: bold;
                margin: 30px 0;
            }}

            footer {{
                text-align: center;
                padding: 25px;
                color: #64748b;
            }}

            @media (max-width: 600px) {{
                nav {{
                    flex-direction: column;
                    gap: 18px;
                }}

                nav a {{
                    margin: 0 10px;
                }}

                h1 {{
                    font-size: 30px;
                }}

                main {{
                    margin: 45px auto;
                }}
            }}
        </style>
    </head>

    <body>
        <nav>
            <div class="logo">DjangoLab</div>

            <div>
                <a href="/">Головна</a>
                <a href="/datetime/">Дата і час</a>
            </div>
        </nav>

        <main>
            {content}
        </main>

        <footer>
            DjangoLab • Навчальний проєкт на Python
        </footer>
    </body>
    </html>
    """


def index(request):
    content = """
        <h1>Вітаємо у DjangoLab!</h1>

        <p class="subtitle">
            Мій перший вебзастосунок на Django.
            Тут ми вивчаємо Python, маршрутизацію
            та створення динамічних вебсторінок.
        </p>

        <div class="cards">
            <div class="card">
                <h2>Python</h2>
                <p>Мова програмування для серверної логіки.</p>
            </div>

            <div class="card">
                <h2>Django</h2>
                <p>Потужний фреймворк для веброзробки.</p>
            </div>

            <div class="card">
                <h2>Routing</h2>
                <p>Керування URL-адресами нашого сайту.</p>
            </div>
        </div>

        <a class="button" href="/datetime/">
            Переглянути поточний час →
        </a>
    """

    return HttpResponse(page_template("Головна | DjangoLab", content))


def current_datetime(request):
    now = datetime.now()

    content = f"""
        <h1>Поточна дата та час</h1>

        <p class="subtitle">
            Ця інформація генерується Python на сервері Django.
        </p>

        <div class="card">
            <h2>Сьогодні</h2>
            <p>{now.strftime('%d.%m.%Y')}</p>

            <div class="clock">
                {now.strftime('%H:%M:%S')}
            </div>

            <p>Час оновлюється після перезавантаження сторінки.</p>
        </div>

        <a class="button" href="/">
            ← Повернутися на головну
        </a>
    """

    return HttpResponse(page_template("Дата і час | DjangoLab", content))

