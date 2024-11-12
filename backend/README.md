# Course Recommendation System API

A Django-based REST API for course recommendations with web crawling capabilities and user management.

## Project Structure

### Core Components

1. User Management (`/usermanagement/`)
- Custom user model with email authentication
- Registration and authentication endpoints
- User serializers and views

2. Web Course Management (`/webcourse/`)
- Course models and relationships
- Course enrollment functionality
- JSON export capabilities

3. Crawling System (`/crawl/`)
- Supported platforms:
  - Udemy
  - Coursera
  - ed2go
  - LinkedIn Learning
  - Udacity
  - Skillshare
- NER (Named Entity Recognition) integration
- Custom spiders for each platform

### Key Features

- Email-based authentication
- Course enrollment system
- Web crawling for course data
- NER-based skill extraction
- REST API endpoints

## Setup and Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Tech Stack

### Backend Framework
- Django - Core web framework
- Django REST Framework - API development

### Database
- Neo4j - Graph database
- neomodel - Object Graph Mapper for Neo4j

### Web Crawling
- Scrapy - Main web scraping framework 
- Splash - JavaScript rendering for dynamic content
- BeautifulSoup - HTML parsing
- requests - HTTP requests handling

### User Management
- Custom User model with email authentication
- JWT for token-based authentication

## Data Flow

### 1. Data Collection
- Web crawlers fetch course data from multiple platforms:
  - Udemy
  - Coursera 
  - ed2go
  - LinkedIn Learning
  - Udacity
  - Skillshare
- Scraped data is processed and normalized
- Data stored in Neo4j graph database using defined relationships

### 2. User Journey
- User registration/login via email
- Course exploration and discovery 
- Course enrollment system
- Progress tracking (complete/in-progress courses)

### 3. Course Management
Courses are connected with related entities:
- Tools
- Programming Languages  
- Knowledge Areas
- Frameworks
- Organizations
- Instructors

### 4. Recommendation Flow
- Based on graph relationships
- User skills and completed courses influence recommendations
- Career path based course suggestions

The system leverages Neo4j's graph structure to create complex relationships between courses, skills, and users, enabling sophisticated recommendation patterns.

