import datetime
from django.http import HttpResponse


def page(title, content):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>{title}</title>

            <style>
                * {{
                    box-sizing: border-box;
                }}

                body {{
                    margin: 0;
                    min-height: 100vh;
                    background: linear-gradient(135deg, #fce7f3, #ede9fe);
                    font-family: Arial, sans-serif;
                    color: #352747;
                }}

                nav {{
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    gap: 12px;
                    padding: 25px 15px;
                }}

                nav a {{
                    padding: 12px 22px;
                    background: white;
                    color: #7c3aed;
                    text-decoration: none;
                    border-radius: 12px;
                    transition: 0.3s;
                }}

                nav a:hover {{
                    background: #7c3aed;
                    color: white;
                    transform: translateY(-3px);
                }}

                main {{
                    display: flex;
                    justify-content: center;
                    padding: 60px 20px;
                }}

                .card {{
                    width: 600px;
                    max-width: 100%;
                    padding: 45px 25px;
                    text-align: center;
                    background: white;
                    border-radius: 24px;
                    box-shadow: 0 15px 40px rgba(80, 40, 100, 0.15);
                    overflow-wrap: anywhere;
                }}

                h1 {{
                    margin: 0 0 20px;
                    font-size: clamp(28px, 5vw, 40px);
                }}

                p {{
                    color: #756782;
                    font-size: 18px;
                    line-height: 1.6;
                }}

                .label {{
                    color: #8b5cf6;
                    font-size: 14px;
                    font-weight: bold;
                    letter-spacing: 3px;
                }}
            </style>
        </head>

        <body>
            <nav>
                <a href="/">Main</a>
                <a href="/datetime/">Datetime</a>
                <a href="/my-name/">My name</a>
            </nav>

            <main>
                <div class="card">
                    {content}
                </div>
            </main>
        </body>
        </html>
    """


def index(request):
    return HttpResponse(page("Main", """
        <p class="label">MY FIRST DJANGO WEBSITE</p>
        <h1>Hello World!</h1>
        <p>Welcome! Choose a page from the menu above.</p>
    """))


def current_datetime(request):
    now = datetime.datetime.now()

    return HttpResponse(page("Datetime", f"""
        <p class="label">DATE AND TIME</p>
        <h1>Current datetime</h1>
        <p>{now}</p>
    """))


def my_name(request):
    return HttpResponse(page("My name", """
        <p class="label">NICE TO MEET YOU</p>
        <h1>My name is Radmila</h1>
        <p>I am learning Python and Django!</p>
    """))