NutriSync AI: Context-Aware Wellness Engine
1. Chosen Vertical
Food and Health Platform
Targeting: Working Professionals, Women's Health, and Families.

2. Approach and Logic
The core philosophy of NutriSync AI is to bridge the gap between "generic advice" and "safe action." Most health apps fail because they don't account for the user's physical constraints or lifestyle stressors.

The "Smart" Logic Engine:
BMI-Safe Exercise Override: The application evaluates the user's BMI input. If the BMI is over 25 (Overweight/Obese), the system applies a safety filter that forces the AI to suggest only low-impact, joint-safe movements (e.g., swimming, seated resistance) to prevent injury.

Persona-Based Nutrition: * Working Professionals: Logic prioritizes low-glycemic foods to prevent energy crashes during work.

Women's Health: Logic prioritizes critical micronutrients like Iron, Calcium, and Folate.

Family Caretakers: Logic focuses on batch-cooking and nutrient-dense, time-efficient meals.

3. How the Solution Works
NutriSync AI is built as a lightweight, full-stack microservice.

Frontend: A responsive, accessible UI built with Tailwind CSS allows users to input their persona and BMI.

Reasoning Engine (Google Gemini): The backend (FastAPI) sends the user data to Google Gemini 1.5 Flash. The prompt engineering ensures the AI acts as a certified coach, cross-referencing the BMI safety logic with persona needs.

Dynamic Generation: Instead of static lists, Gemini generates a real-time, unique meal and exercise plan tailored to that specific moment.

Deployment: The app is containerized via Docker and hosted on Google Cloud Run, ensuring it is fast, scalable, and follows modern cloud-native standards.

4. Google Services Integrated
Google Gemini 1.5 Flash: Used for real-time health reasoning and personalized content generation.

Google Cloud Run: Used for serverless deployment of the application.

Google Antigravity: The primary development environment used for building and pushing the solution.

Artifact Registry: Used to manage and store the containerized images.

5. Assumptions Made
User Accuracy: It is assumed the user provides an accurate BMI for the safety logic to function correctly.

Equipment: The AI assumes basic kitchen tools and household items (like chairs or water bottles) are available for "at-home" routines.

Consultation: While the logic is safety-first, it is assumed users will consult a physician before starting new intense regimens.
