from flask import Flask, render_template, request, url_for, jsonify
import os
import requests


app = Flask(__name__, static_folder='static/')
API_TOKEN = os.getenv('MAILSEND_KEY')
FROM_EMAIL = 'noreply@test-eqvygm009p5l0p7w.mlsender.net'  
TO_EMAIL = 'ukovictor8@gmail.com' 

services = {
    "api-backend": {
        "title": "API & Backend Development",
        "intro": "Fast, scalable backends with FastAPI, Celery, and Redis.",
        "image": "assets/img/backend-development.jpg",
        "heading": "Powerful FastAPI Backend Services",
        "description_intro": "FastAPI is a modern web framework for building APIs with Python. It’s designed to be fast and easy to use...",
        "features": [
            "High performance with async support",
            "Easy integration with databases & third-party services",
            "Automatic OpenAPI & JSON Schema docs",
            "Secure auth & authorization",
            "Real-time with WebSockets & background tasks"
        ],
        "paragraphs": [
            "With FastAPI, we ensure that the backend services we create are efficient, scalable, and ready for modern use cases such as Web3 integrations, complex data handling, and real-time notifications.",
            "Our FastAPI backend supports Ethereum, Arbitrum, Sui, TON and more. Optimized for mobile & web apps to deliver secure, high-speed experiences.",
            "Whether you need real-time airdrop tracking, secure wallet functionality, or payment gateway integration, our tailored FastAPI solutions have you covered."
        ]
    },
    "mobile-app": {
        "title": "Mobile App Development",
        "intro": "Cross-platform mobile apps built with Flet, focusing on clean UI and rapid iteration.",
        "image": "assets/img/flet-prototype.jpg",
        "heading": "Interactive Flet Prototypes & MVPs",
        "description_intro": "Flet lets us build real native mobile experiences in Python. Perfect for rapid prototyping to validate ideas...",
        "features": [
            "Single codebase for iOS & Android",
            "Customizable UI with live reload",
            "Seamless API integration",
            "Push notifications via FCM",
            "Lightweight APKs optimized for size"
        ],
        "paragraphs": [
            "Our Flet prototypes give you working mobile apps in days, not weeks—ideal for market testing and investor demos.",
            "After validation, we can transition your MVP to React Native or Flutter for broader reach without losing momentum."
        ]
    },
    "community-management": {
        "title": "Community Management",
        "intro": "Building and growing engaged Web3 communities.",
        "image": "assets/img/community-management.jpg",
        "heading": "Scalable Community Growth",
        "description_intro": "A loyal, engaged community is critical in Web3 — and we know how to build it from scratch...",
        "features": [
            "Organic growth strategies",
            "Event & campaign management",
            "Moderation & feedback loops",
            "Community analytics",
            "Telegram & Discord support"
        ],
        "paragraphs": [
            "With experience managing communities of 500+ members, we help you create spaces that people want to return to.",
            "We leverage tools like Guild.xyz, Zealy, and Collab.Land to drive deeper user engagement and retention."
        ]
    },
    "technical-writing": {
        "title": "Technical Writing & Content",
        "intro": "Translating complex tech into clear, engaging content.",
        "image": "assets/img/technical-writing.jpg",
        "heading": "Content That Connects",
        "description_intro": "Good writing bridges the gap between builders and users. Whether for docs, threads, or landing pages — clarity wins.",
        "features": [
            "Twitter/X growth threads",
            "Product documentation",
            "Pitch decks & whitepapers",
            "Community guides & FAQs",
            "SEO-ready content for devs"
        ],
        "paragraphs": [
            "We’ve created award-winning Twitter threads and dev-focused content that informs, inspires, and converts.",
            "From onboarding guides to protocol deep-dives, we make sure your message resonates with both devs and users."
        ]
    },
    "product-strategy": {
        "title": "Product Strategy & Roadmapping",
        "intro": "Vision, planning, and execution for long-term success.",
        "image": "assets/img/product-strategy.jpg",
        "heading": "Clear Roadmaps for Impact",
        "description_intro": "Launching is just the beginning. We help you shape your product roadmap to hit KPIs, manage teams, and win users...",
        "features": [
            "Vision-to-MVP planning",
            "Vesting & equity structure setup",
            "Launch & go-to-market playbooks",
            "Team hiring & delegation",
            "Product analytics & feedback loops"
        ],
        "paragraphs": [
            "We help early-stage founders structure their product from day one — from defining core features to shaping investor decks and launch timelines.",
            "We’ll work with you to prioritize growth, retention, and monetization strategies tailored to your user base and industry."
        ]
    }
}




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services/<service_slug>')
def view_service(service_slug):
    service = services.get(service_slug)
    if not service:
        return "Service not found", 404
    return render_template(
        'service-details.html',
        services=services,
        service=service,
        service_slug=service_slug
    )


@app.route('/contact', methods=['POST'])
def contact():
    try:
        # Get form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Prepare the email data for MailerSend API
        data = {
            "from": {
                "email": FROM_EMAIL,
                "name": "Notifications"
            },
            "to": [
                {
                    "email": TO_EMAIL,
                    "name": "test"
                }
            ],
            "subject": f"New Message: {subject}",
            "text": f"Name: {name}\nEmail: {email}\nMessage: {message}"
        }
        print(data)
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }

        # Send email using MailerSend API
        response = requests.post(
            "https://api.mailersend.com/v1/email",
            json=data,
            headers=headers
        )

        # Check the response status
        print(response)
        if response.status_code in [200, 202]:
            print('Mail Sent')
            return jsonify({"message": "Your message has been sent. Thank you!"}), 200
        else:
            return jsonify({"error": f"MailerSend error: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route ('/start')
def start():
    return render_template('portfolio-details.html')

if __name__=='__main__':
    app.run(debug=True)