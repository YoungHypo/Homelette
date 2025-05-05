# Homelette

A mobile app designed to connect subletters with subtenants in Isla Vista

## Installation Instructions

To get started with the Homelette App, follow these steps:

### Prerequisites
* Ensure you have Node.js installed.
* Ensure you have Python 3.9+ installed for the backend services.
* Ensure you have Docker and Docker Compose installed for containerized deployment.

### Frontend Setup

* Install Expo CLI globally by running:
```
npm install -g expo-cli
```

* Clone the repository and navigate to the project directory:
```
git clone https://github.com/YoungHypo/Homelette.git
cd Homelette
```

* Install frontend dependencies:
```
cd react-native
npm install
```

### Backend Setup

* Install backend dependencies:
```
cd flask/backend-api
pip install -r requirements.txt

cd ../backend-socket
pip install -r requirements.txt
```

### Running Locally

```
cd react-native
expo start
```

To run the entire application stack:

```
docker-compose up -d
```

This will start:
- Flask API backend on port 5001
- Flask WebSocket backend on port 5002

### Installation of the APK (v1.1.0-project-demo)

* To install the APK directly on your Android device, download it using this link: [Homelette APK](https://expo.dev/artifacts/eas/rTAiYZMqd6jLN9P91UXCPu.apk)

* Once downloaded, ensure that your device allows installations from unknown sources. Navigate to the downloaded APK file and tap to install.

### Functionality

* You can navigate the app using the navigation bar at the bottom of the screen
* Leases can be posted on the Post page
* Leases can be viewed on the Rent page
* Real-time chat between users
* The user can sign out via the button on the Home page
* Profile details can be viewed on the Profile page

### Known Problems

# Tech Stack

## Frontend
- Development framework: React Native (Expo)
- UI Components: React Native Paper
- Maps: React Native Maps
- Image Handling: Expo Image Picker
- Storage: Async Storage

## Backend
- API Server: Flask (Python)
- Real-time Communication: Flask-SocketIO with Eventlet
- Authentication: JWT (JSON Web Tokens)
- Database: MariaBD
- ORM: SQLAlchemy

## Infrastructure
- Containerization: Docker & Docker Compose
- CI/CD: GitHub Actions

## Cloud Services (Previous Version)
- Database: Firestore
- Cloud Storage: Firebase Storage

# App Planning

# User Stories

## As a subtenant
- I want to be able to view more details/pictures about a property by tapping on it's card on the Rent page (more details: date posted, etc.).
- I want to be able to filter by price, roommate count, amenities include (water, electricity, Wi-Fi), distance from school.
- I want to be able to view a Zillow-like map of clickable posted properties.
- I want to chat with potential subletters.
- I want to receive real-time notifications when I get new messages.
- I want to see when someone is typing a message to me.
- I want to see when my messages have been delivered and read.
- I want to be able to share images and location pins in chat.
- I want to favorite/unfavorite listings on the RentPage and view my favorited listings in a favorited listings page.

## As a subletter
- I want to be able to post listings quickly, upload pictures and fill in the necessary details.
- I want to be able to view the status of posted listings (e.g. number of times viewed, number of people interested).
- I want to be able to edit or delete my listing information (e.g. change the rent or add a description).
- I want to receive instant notifications when someone is interested in my listings so that I can respond quickly to potential subleasers.
- I want to manage multiple conversations with different interested subtenants simultaneously.
- I want to see my chat history with potential subtenants when I come back to the app.

## As a user
- I want manuals or tutorials of how to use the app.
- I want to be able to edit various details about my profile, such as my password, profile picture, and class info.
- I want to set my online/offline status to control my visibility to other users.
- I want to see which users are currently online.
- I want to search through my message history with a specific user.

# Project Team

This project was originally developed by a team of students at UCSB. It is now maintained by:

- Haibo Yang ([@YoungHypo](https://github.com/YoungHypo)) - Full Stack Developer

## Original Contributors

### Frontend
- Jonathan Herring - @jonathan-herring
- Collin Qian - @CollinQ
- Haibo Yang - @YoungHypo

### Backend
- Allen Qiu - @aqiu04
- Amy Wang - @awaang
- Jason Vu - @Firoc

# Deployment

[APK for our app here](https://expo.dev/artifacts/eas/rTAiYZMqd6jLN9P91UXCPu.apk)
