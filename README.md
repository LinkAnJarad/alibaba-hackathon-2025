# AI-Powered Document Processing System

## Overview
Barangay residents and LGU officials spend countless hours manually filling out repetitive forms and managing paper-based documentation. This process is error-prone, time-consuming, and creates administrative bottlenecks that delay essential community services. SmartBarangay Forms is an intelligent document automation platform that revolutionizes how barangay residents interact with local government services. By leveraging advanced OCR and Natural Language Processing powered by Alibaba Cloud's Qwen model family, the system eliminates manual data entry, reduces processing time, and minimizes errors in barangay form submissions. 

# SmartBarangay Forms - Technical Specification (MVP)

## System Architecture

**Three-Tier Architecture**
- **Frontend**: React SPA (Progressive Web App)
- **Backend**: FastAPI REST API
- **Storage**: Alibaba OSS (documents) + PolarDB MySQL (structured data)

## Technology Stack

### Frontend
- **Framework**: React
- **UI Library**: Tailwind CSS
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Authentication**: JWT tokens
- **File Handling**: Python Pillow for image preprocessing
- **ORM**: SQLAlchemy with async support
- **API Documentation**: Auto-generated via FastAPI/Swagger

### AI/ML Services (Alibaba Cloud, specific models may vary)
- **Qwen-OCR**: Document text extraction
- **QwenVL**: Document layout understanding and field detection
- **Qwen2.5**: Data validation and entity extraction
- Model access via Alibaba Cloud PAI or direct API calls

### Infrastructure (Alibaba Cloud)
- **Compute**: ECS instances (2-4 vCPU for MVP)
- **Storage**: OSS for document images
- **Database**: PolarDB MySQL (single instance)

## Resident User Flow

### Initial Setup (One-time)
1. **Register Account**
   - User opens web app, clicks "Register"
   - Enters email, password, basic info (name, contact)
   - Alibaba eKYC (ID scan, liveliness detection, facial recog)

2. **Identity Verification**
   - User visits barangay hall in person with valid IDs
   - Admin verifies identity and updates account to `verified`
   - User receives confirmation (email/SMS)
   - Can now access form submission features


## Resident Flow

1. **One-Time Setup**
   - Register account → Visit barangay hall for in-person verification → Account activated

2. **Submit a Form**
   - Login → Select form type (e.g., "Barangay Clearance")
   - Take photo of Valid ID → AI extracts data (3-5 seconds)
   - Review auto-filled form → Edit if needed → Submit
   - Track status in "My Submissions"

---

## Admin Flow

1. **Review Submissions**
   - Login → View pending submissions list
   - Click submission → See uploaded documents + auto-filled data side-by-side
   - Verify accuracy → **Approve** / **Request Correction** / **Reject**
   - Resident receives notification
