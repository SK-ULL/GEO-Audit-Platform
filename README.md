# 🚀 MLABS GEO Audit Platform

**Live Frontend (Streamlit):** [https://mlabsgeoauditplatform.streamlit.app]  
**Live Backend API (Render):** [https://geo-audit-platform.onrender.com]

---

## 📌 Project Overview
An automated pipeline that generates "Generative Engine Optimization" (GEO) audits for companies. The platform takes a company URL, scrapes it, uses AI to analyze their AI-search readiness, and delivers a professional PDF report via email while evaluating it based on 5 major metrics. I have focused on this domain as GEO is a new-age growing industry and all companies require this to improve their online presence in the new world of AI and search engines like Chatgpt and Gemini accumulating more search ratio compared to the traditional search engines everyday. I have used Render for Backend deployment, Streamlit for the frontend, Resend for emailling, JinaAI for scraping through the sites and Groq API for the LLM model. This pipeline focuses on all the fallbacks in cases of invalid urls or email domains to errors in scraping or preventing prior knowledge use by the AI model to generate the pdf.

### 🔄 The Workflow
1. **Scraping:** Uses Jina Reader API to bypass bot detection.
2. **AI Analysis:** Leverages LLMs to evaluate digital presence.
3. **PDF Generation:** Creates a custom-branded audit report.
4. **Email Delivery:** Bypasses cloud firewalls using the Resend API.
5. **CRM Logging:** Automatically updates a Google Sheet with lead info.

---

## 🛠️ Detailed Setup & Deployment

### 1. Prerequisites (API Keys Needed)
To run this project, you need to collect the following:
* **Jina AI:** Get a key from [r.jina.ai](https://r.jina.ai/) (for scraping).
* **Resend:** Get a key from [resend.com](https://resend.com/) (for emails).
* **Google Cloud:** A `service_account.json` file with access to Google Sheets.
* **OpenAI/Anthropic:** (Whichever AI model you are using for analysis).

### 2. Render Deployment
This project is optimized for Render's infrastructure. To avoid **502 Gateway Timeouts**, we use **Synchronous Background Tasks**.

**Environment Variables to add in Render Dashboard:**
| `JINA_API_KEY` | Your Jina Reader Key |
| `RESEND_API_KEY` | Your Resend API Key |
| `GOOGLE_SHEETS_ID` | The ID of your tracking spreadsheet |
| `GOOGLE_CREDENTIALS_JSON` | The entire content of your JSON service account file |

### 3. Email Configuration (Sandbox Mode)
Because we are using the **Resend API** to bypass Render's SMTP block:
* **Testing:** While in "Sandbox mode," you can only send emails to the address you signed up with for Resend.
* **Production:** To send to any recipient (e.g. @gmail.com), you must verify a domain in the Resend dashboard.
* When you try to run it without deployment it uses the private IP and that allows emailling to any domain without errors but the use of Render blocks it as it is considered as one of the major targets for mass bot spamming and it denies email requests disrupting the pipeline requiring the use of RESEND.

### 4. Local Development
1. Clone the repo.
2. Create a `.env` file with the keys listed above.
3. Install dependencies: `pip install -r requirements.txt`.
4. Start Backend: `uvicorn main:app --reload`.
5. Start Frontend: `streamlit run app.py`.
This deployment is the most effective form of the prototype which executes the pipeline and allows emailling it to any domain.

---

## Important decisions:

**Q: Why use Resend instead of standard SMTP?** **A:** Render and most cloud providers block Port 465/587 to prevent spam. Using a Web API (Resend) sends mail over Port 443, which is never blocked. Render blocks use of smtp as it can lead to malicious use for mail spamming.

**Q: Google Drive error: "Service Accounts do not have storage quota"?** **A:** Service accounts start with 0GB. You must create a folder in your personal drive and "Share" it with the service account email (found in your JSON) as an Editor. To prevent this I have not actively initiated the google drive script but you can execute it by simply adding the access to a personal google drive folder and it will keep an archive of all the generated pdfs.
The pipeline in progress:
<img width="1800" height="1169" alt="Screenshot 2026-05-19 at 3 01 07 PM" src="https://github.com/user-attachments/assets/b499653d-08ce-41b1-b47f-1fd2f583ae7d" />

The result:
<img width="1800" height="1169" alt="Screenshot 2026-05-19 at 3 01 47 PM" src="https://github.com/user-attachments/assets/4e2c6a11-821b-4444-a730-8352085b7a8d" />

The updated google sheet leads:
<img width="1205" height="646" alt="Screenshot 2026-05-19 at 3 03 34 PM" src="https://github.com/user-attachments/assets/1f8642c9-3a2d-4d9f-bf58-cc64d6a58d3a" />

Sample report:

<img width="811" height="1122" alt="Screenshot 2026-05-19 at 3 07 30 PM" src="https://github.com/user-attachments/assets/4f2766d0-62b8-4479-b3bc-7137735f1594" />
