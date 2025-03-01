# Dum Dum Social - Character Dumb Charades Platform

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

A social platform for movie and TV show fans to play character dumb charades and connect with other enthusiasts.

<p align="center">
  <img src="/demo/QuizSocial.gif" alt="GIF">
</p>

## Key Features
🎭 **Core Functionality**
- Google OAuth2 authentication
- Real-time chat interface with AI assistant (Sia)
- Video room creation and management
- Event scheduling with Google Calendar integration
- Subscription management with Stripe

🤖 **AI Features**
- GPT-4 powered conversation flow
- Dynamic response generation
- Conversation history management
- Text embedding and similarity matching

📊 **Background Services**
- Automated ranking system
- Subscription auto-renewal
- Room supervision and cleanup
- Event creation and matching
- Referral program management

## Installation

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/quiz-social.git
cd quiz-social
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Variables**
Create `.env` file with:
```ini
SECRET_KEY=your_django_secret_key
DATABASE_URL=postgres://user:password@host:port/dbname
OPENAI_API_KEY=your_openai_key
STRIPE_SECRET_KEY=your_stripe_key
TELEGRAM_API_TOKEN=your_telegram_bot_token
# Add other required keys from the code
```

5. **Database Setup**
```bash
python manage.py migrate
```

6. **Run Development Server**
```bash
python manage.py runserver
```

## Environment Variables
| Key | Description |
|-----|-------------|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | PostgreSQL connection URL |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 |
| `STRIPE_*` | Stripe payment integration keys |
| `TELEGRAM_*` | Telegram bot credentials |
| `AWS_*` | AWS S3 storage credentials |
| `PINECONE_*` | Vector database credentials |

## Project Structure
```
quiz-social/
├── QuizSocial-app/
│   ├── dumdumsocialbot/       # AI chat bot implementation
│   ├── home/                  # Core application logic
│   ├── jobs/                  # Background tasks and cron jobs
│   ├── templates/             # HTML templates
│   ├── static/               # CSS/JS/assets
│   └── settings.py           # Django configuration
├── requirements.txt
└── manage.py
```

## Background Jobs
The system uses APScheduler for:
- 🕒 Daily event creation
- 💳 Subscription management
- 🏆 Ranking calculations
- 🧹 Resource cleanup
- 🤖 AI model updates

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

---

**Note:** Update the repository URLs and environment variables according to your specific configuration. Add screenshots and detailed API documentation as needed for your deployment.

## Screenshots
<p align="center">
  <img src="/demo/QuizSocial-1.png" alt="Image 1" width="100%">
</p>
<p align="center">
  <img src="/demo/QuizSocial-2.png" alt="Image 3" width="47%">
  <img src="/demo/QuizSocial-3.png" alt="Image 4" width="47%">
</p>
<p align="center">
  <img src="/demo/QuizSocial-4.png" alt="Image 4" width="47%">
  <img src="/demo/QuizSocial-5.png" alt="Image 5" width="47%">
</p>
