<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img src="assets/hero-light.svg" width="100%" alt="Sham. AI/ML Architect | Consultant | Applied AI. LLM and agentic systems, healthcare AI, Azure, AWS and GCP. Microsoft Certified AI-102. Open to applied AI, AI research and applied science. Artwork: a rotating point-cloud globe of an embedding space with three colour-coded clusters for the three focus areas.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/typing-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/typing-light.svg">
  <img src="assets/typing-light.svg" width="760" alt="Inference ticker: AI/ML Architect, Consultant, Applied AI. LLM and agentic systems, RAG, LangGraph, vLLM. Healthcare AI, HIPAA, HL7 FHIR R4, ambient scribe. Azure, AWS, GCP, Microsoft Certified AI-102.">
</picture>

<br>

<a href="https://www.linkedin.com/in/shamuddin-n-b90018160/"><img alt="LinkedIn: Sham" src="https://img.shields.io/badge/LinkedIn-Sham-0A66C2?style=for-the-badge"></a>
<a href="mailto:shamuddin1011@gmail.com"><img alt="Email: shamuddin1011@gmail.com" src="https://img.shields.io/badge/Email-shamuddin1011%40gmail.com-D14836?style=for-the-badge&amp;logo=gmail&amp;logoColor=white"></a>
<a href="#open-to"><img alt="Open to: Applied AI, AI Research, Applied Science" src="https://img.shields.io/badge/Open%20to-Applied%20AI%20%C2%B7%20AI%20Research%20%C2%B7%20Applied%20Science-2EA44F?style=for-the-badge"></a>

</div>

## whoami

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/whoami-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/whoami-light.svg">
  <img src="assets/whoami-light.svg" width="100%" alt="Model card for Sham in an editor window: AI/ML Architect and Consultant with 6+ years in production AI, cloud and healthcare SaaS. Core: C#, .NET, ASP.NET Core, Python, TypeScript. AI: Azure OpenAI, Azure AI Speech, LangGraph, vLLM, RAG, AI agents. Cloud: Azure, AWS, GCP. Domains: healthcare SaaS, HIPAA, HL7 FHIR R4, payments, finance. Certifications: AI-102 (Dec 2025), AI-900 (Aug 2025). Education: MCA 2024, BCA 2020. Intended use: applied AI, AI research, applied science with AI. Languages: English (C1, fluent). Status: online.">
</picture>

AI/ML Architect & Consultant with **6+ years** building production AI and cloud platforms, mostly in **healthcare SaaS** (HIPAA, HL7 FHIR). I design secure .NET and Python services on **Azure, AWS and GCP** and ship LLM, speech and agentic features on top — one ambient clinical scribe cut manual documentation time by **80%**.

I guide teams of 2–4 engineers and turn rough ideas into working proofs of concept fast.

<details>
<summary>Text version</summary>

```yaml
model: shamuddin-n
role: AI/ML Architect & Consultant
experience: 6+ years            # production AI, cloud, healthcare SaaS
architecture:
  core:   [C#, .NET, ASP.NET Core, Python, TypeScript]
  ai:     [Azure OpenAI, Azure AI Speech, LangGraph, vLLM, RAG, AI agents]
  cloud:  [Azure, AWS, GCP]
training_data:
  domains: [Healthcare SaaS, HIPAA, HL7 FHIR R4, Payments, Finance]
eval:
  certifications: [AI-102 (Dec 2025), AI-900 (Aug 2025)]
  education:      [MCA 2024, BCA 2020]
intended_use: [Applied AI, AI Research, Applied Science with AI]
languages: [English (C1, fluent)]
status: online
```

</details>

## Impact & strengths

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/impact-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/impact-light.svg">
  <img src="assets/impact-light.svg" width="100%" alt="Strengths: multi-cloud (Azure, AWS, GCP); applied AI and LLM systems (RAG, agents, speech, vision-language); healthcare compliance (HIPAA, HL7 FHIR R4, PHI encryption); certified and experienced (6+ years, AI-102, AI-900).">
</picture>

## Capabilities

What I build, end to end. Healthcare AI is one of five capabilities.

<table>
<tr>
<td width="34%"><b>LLM & agentic systems, RAG</b></td>
<td>Azure OpenAI and Microsoft Foundry deployments, LangGraph multi-agent pipelines, vLLM serving, retrieval-augmented generation, prompt orchestration, deterministic guardrails for agents. Proof: <a href="https://github.com/sham-2510/ClinSight">ClinSight</a>, <a href="https://github.com/sham-2510/playbook">PLAYBOOK</a>.</td>
</tr>
<tr>
<td width="34%"><b>Healthcare AI & interoperability</b></td>
<td>Ambient clinical scribe (Azure AI Speech + Azure OpenAI), sentiment-driven patient-feedback escalation (Azure AI Language), clinical audio transcription with speaker diarization in Python, HIPAA-compliant multi-tenant HL7 FHIR R4 data hub (Azure Functions, Service Bus, Logic Apps).</td>
</tr>
<tr>
<td width="34%"><b>Cloud & platform engineering (Azure · AWS · GCP)</b></td>
<td>Secure multi-tenant ASP.NET Core and Python services; edge security with Front Door WAF, API Management and origin locking; Key Vault, Entra ID, AD B2C; CI/CD with Azure DevOps and GitHub Actions; on-prem Oracle/SQL Server → Azure SQL migration with Data Factory.</td>
</tr>
<tr>
<td width="34%"><b>Secure payments & integrations</b></td>
<td>Multi-tenant payment gateway (100+ TPS peaks), PCI-conscious client-side tokenization, X.509-encrypted results over Service Bus, retry/dead-letter recovery, lab-partner integration APIs with OAuth 2.0/OIDC.</td>
</tr>
<tr>
<td width="34%"><b>AI research & proofs of concept</b></td>
<td>NeRF 3D reconstruction from 2D radiographs (NVIDIA GPUs), AI-assisted CAD engine on Azure AI + Python. Details below.</td>
</tr>
</table>

### Inside the AI clinical scribe

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/arch-scribe-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/arch-scribe-light.svg">
  <img src="assets/arch-scribe-light.svg" width="100%" alt="Architecture of the AI clinical scribe in seven steps: 1, the Blazor WebAssembly app inside the fertility EMR calls Azure API Management over HTTPS; 2, API Management forwards to the speech token service on ASP.NET Core 8 in Azure App Service; 3, the service returns a short-lived token so no keys reach the browser; 4, the app streams audio to Azure AI Speech for live transcription; 5, the transcript goes to the note orchestrator; 6, the orchestrator and Azure OpenAI draft a structured note; 7, the draft is encrypted with X.509 certificates, reviewed by the clinician and saved to the chart. Azure Key Vault holds the secrets and certificates.">
</picture>

<sub>Simplified. Service keys never reach the browser; PHI is encrypted with certificates held in Azure Key Vault; a clinician reviews every note.</sub>

<details>
<summary><b>R&D and proofs of concept</b></summary>

- **NeRF from radiographs (NVIDIA)** — reconstructed 3D models of the hand and leg from 2D radiographic images with Neural Radiance Fields; benchmarked GPU configurations for rendering speed vs. anatomical detail.
- **AI-assisted CAD engine (Azure AI + Python)** — quantity takeoff from vector CAD PDFs: 72 object types and 480 instances recognised on a production A0 drawing, 87 rooms measured, 890 automated tests; Azure AI Document Intelligence OCR at 97% text coverage, Azure OpenAI optional and off by default.

</details>

## Tech stack

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=cs%2Cdotnet%2Cpy%2Cfastapi%2Cts%2Cjs%2Creact%2Cnextjs%2Cpostgres&amp;perline=14&amp;theme=dark">
  <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=cs%2Cdotnet%2Cpy%2Cfastapi%2Cts%2Cjs%2Creact%2Cnextjs%2Cpostgres&amp;perline=14&amp;theme=light">
  <img src="https://skillicons.dev/icons?i=cs%2Cdotnet%2Cpy%2Cfastapi%2Cts%2Cjs%2Creact%2Cnextjs%2Cpostgres&amp;perline=14&amp;theme=light" alt="Skill icons: C#, .NET, Python, FastAPI, TypeScript, JavaScript, React, Next.js, PostgreSQL">
</picture>
<br>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=azure%2Caws%2Cgcp%2Cgithubactions%2Cpowershell&amp;perline=14&amp;theme=dark">
  <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=azure%2Caws%2Cgcp%2Cgithubactions%2Cpowershell&amp;perline=14&amp;theme=light">
  <img src="https://skillicons.dev/icons?i=azure%2Caws%2Cgcp%2Cgithubactions%2Cpowershell&amp;perline=14&amp;theme=light" alt="Skill icons: Azure, AWS, GCP, GitHub Actions, PowerShell">
</picture>
</p>

<table>
<tr>
<td width="170"><b>AI · LLM · Agents</b></td>
<td>
<img alt="Azure OpenAI" src="https://img.shields.io/badge/Azure%20OpenAI-0078D4?style=flat-square"> <img alt="Microsoft Foundry" src="https://img.shields.io/badge/Microsoft%20Foundry-0078D4?style=flat-square"> <img alt="Azure AI Speech" src="https://img.shields.io/badge/Azure%20AI%20Speech-0078D4?style=flat-square"> <img alt="Azure AI Language" src="https://img.shields.io/badge/Azure%20AI%20Language-0078D4?style=flat-square"> <img alt="Azure AI Document Intelligence" src="https://img.shields.io/badge/Azure%20AI%20Document%20Intelligence-0078D4?style=flat-square"> <img alt="Azure AI Search" src="https://img.shields.io/badge/Azure%20AI%20Search-0078D4?style=flat-square"> <img alt="Azure Machine Learning" src="https://img.shields.io/badge/Azure%20Machine%20Learning-0078D4?style=flat-square"> <img alt="LangGraph" src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&amp;logo=langgraph&amp;logoColor=white"> <img alt="vLLM" src="https://img.shields.io/badge/vLLM-30A2FF?style=flat-square&amp;logo=vllm&amp;logoColor=white"> <img alt="RAG" src="https://img.shields.io/badge/RAG-6E40C9?style=flat-square"> <img alt="AI Agents" src="https://img.shields.io/badge/AI%20Agents-6E40C9?style=flat-square"> <img alt="Prompt Orchestration" src="https://img.shields.io/badge/Prompt%20Orchestration-6E40C9?style=flat-square"> <img alt="Vision-Language Models" src="https://img.shields.io/badge/Vision--Language%20Models-6E40C9?style=flat-square"> <img alt="Speaker Diarization" src="https://img.shields.io/badge/Speaker%20Diarization-6E40C9?style=flat-square"> <img alt="NVIDIA" src="https://img.shields.io/badge/NVIDIA-76B900?style=flat-square&amp;logo=nvidia&amp;logoColor=white">
</td>
</tr>
<tr>
<td width="170"><b>Azure</b></td>
<td>
<img alt="App Service" src="https://img.shields.io/badge/App%20Service-0078D4?style=flat-square"> <img alt="Functions" src="https://img.shields.io/badge/Functions-0078D4?style=flat-square"> <img alt="Container Apps" src="https://img.shields.io/badge/Container%20Apps-0078D4?style=flat-square"> <img alt="AKS" src="https://img.shields.io/badge/AKS-0078D4?style=flat-square"> <img alt="Container Registry" src="https://img.shields.io/badge/Container%20Registry-0078D4?style=flat-square"> <img alt="Service Bus" src="https://img.shields.io/badge/Service%20Bus-0078D4?style=flat-square"> <img alt="Event Grid" src="https://img.shields.io/badge/Event%20Grid-0078D4?style=flat-square"> <img alt="Event Hubs" src="https://img.shields.io/badge/Event%20Hubs-0078D4?style=flat-square"> <img alt="API Management" src="https://img.shields.io/badge/API%20Management-0078D4?style=flat-square"> <img alt="Front Door WAF" src="https://img.shields.io/badge/Front%20Door%20WAF-0078D4?style=flat-square"> <img alt="Static Web Apps" src="https://img.shields.io/badge/Static%20Web%20Apps-0078D4?style=flat-square"> <img alt="Logic Apps" src="https://img.shields.io/badge/Logic%20Apps-0078D4?style=flat-square"> <img alt="Health Data Services (FHIR)" src="https://img.shields.io/badge/Health%20Data%20Services%20%28FHIR%29-0078D4?style=flat-square"> <img alt="Cosmos DB" src="https://img.shields.io/badge/Cosmos%20DB-0078D4?style=flat-square"> <img alt="Azure SQL" src="https://img.shields.io/badge/Azure%20SQL-0078D4?style=flat-square"> <img alt="Blob · Queue · Table Storage" src="https://img.shields.io/badge/Blob%20%C2%B7%20Queue%20%C2%B7%20Table%20Storage-0078D4?style=flat-square"> <img alt="Redis Cache" src="https://img.shields.io/badge/Redis%20Cache-0078D4?style=flat-square"> <img alt="SignalR" src="https://img.shields.io/badge/SignalR-0078D4?style=flat-square"> <img alt="Notification Hubs" src="https://img.shields.io/badge/Notification%20Hubs-0078D4?style=flat-square"> <img alt="Synapse · Fabric" src="https://img.shields.io/badge/Synapse%20%C2%B7%20Fabric-0078D4?style=flat-square"> <img alt="Data Factory" src="https://img.shields.io/badge/Data%20Factory-0078D4?style=flat-square"> <img alt="Key Vault" src="https://img.shields.io/badge/Key%20Vault-0078D4?style=flat-square"> <img alt="Entra ID" src="https://img.shields.io/badge/Entra%20ID-0078D4?style=flat-square"> <img alt="AD B2C" src="https://img.shields.io/badge/AD%20B2C-0078D4?style=flat-square"> <img alt="Managed Identities" src="https://img.shields.io/badge/Managed%20Identities-0078D4?style=flat-square"> <img alt="Virtual Network" src="https://img.shields.io/badge/Virtual%20Network-0078D4?style=flat-square"> <img alt="Monitor" src="https://img.shields.io/badge/Monitor-0078D4?style=flat-square"> <img alt="Application Insights" src="https://img.shields.io/badge/Application%20Insights-0078D4?style=flat-square"> <img alt="Log Analytics" src="https://img.shields.io/badge/Log%20Analytics-0078D4?style=flat-square"> <img alt="Defender for Cloud" src="https://img.shields.io/badge/Defender%20for%20Cloud-0078D4?style=flat-square"> <img alt="Azure Policy" src="https://img.shields.io/badge/Azure%20Policy-0078D4?style=flat-square"> <img alt="Bicep · ARM" src="https://img.shields.io/badge/Bicep%20%C2%B7%20ARM-0078D4?style=flat-square"> <img alt="Resource Manager APIs" src="https://img.shields.io/badge/Resource%20Manager%20APIs-0078D4?style=flat-square">
</td>
</tr>
<tr>
<td width="170"><b>AWS</b></td>
<td>
<img alt="Bedrock" src="https://img.shields.io/badge/Bedrock-232F3E?style=flat-square"> <img alt="SageMaker" src="https://img.shields.io/badge/SageMaker-232F3E?style=flat-square"> <img alt="Lambda" src="https://img.shields.io/badge/Lambda-232F3E?style=flat-square"> <img alt="S3" src="https://img.shields.io/badge/S3-232F3E?style=flat-square"> <img alt="EC2" src="https://img.shields.io/badge/EC2-232F3E?style=flat-square"> <img alt="ECS" src="https://img.shields.io/badge/ECS-232F3E?style=flat-square"> <img alt="EKS" src="https://img.shields.io/badge/EKS-232F3E?style=flat-square"> <img alt="API Gateway" src="https://img.shields.io/badge/API%20Gateway-232F3E?style=flat-square"> <img alt="DynamoDB" src="https://img.shields.io/badge/DynamoDB-232F3E?style=flat-square"> <img alt="RDS" src="https://img.shields.io/badge/RDS-232F3E?style=flat-square"> <img alt="CloudWatch" src="https://img.shields.io/badge/CloudWatch-232F3E?style=flat-square"> <img alt="IAM" src="https://img.shields.io/badge/IAM-232F3E?style=flat-square">
</td>
</tr>
<tr>
<td width="170"><b>Google Cloud</b></td>
<td>
<img alt="Vertex AI" src="https://img.shields.io/badge/Vertex%20AI-4285F4?style=flat-square&amp;logo=googlecloud&amp;logoColor=white"> <img alt="Gemini API" src="https://img.shields.io/badge/Gemini%20API-4285F4?style=flat-square&amp;logo=googlegemini&amp;logoColor=white"> <img alt="Cloud Run" src="https://img.shields.io/badge/Cloud%20Run-4285F4?style=flat-square&amp;logo=googlecloud&amp;logoColor=white"> <img alt="Cloud Functions" src="https://img.shields.io/badge/Cloud%20Functions-4285F4?style=flat-square&amp;logo=googlecloud&amp;logoColor=white"> <img alt="GKE" src="https://img.shields.io/badge/GKE-4285F4?style=flat-square&amp;logo=googlecloud&amp;logoColor=white"> <img alt="BigQuery" src="https://img.shields.io/badge/BigQuery-4285F4?style=flat-square&amp;logo=googlebigquery&amp;logoColor=white"> <img alt="Cloud Storage" src="https://img.shields.io/badge/Cloud%20Storage-4285F4?style=flat-square&amp;logo=googlecloudstorage&amp;logoColor=white"> <img alt="Pub/Sub" src="https://img.shields.io/badge/Pub%2FSub-4285F4?style=flat-square&amp;logo=googlepubsub&amp;logoColor=white">
</td>
</tr>
<tr>
<td width="170"><b>.NET & Backend</b></td>
<td>
<img alt="C#" src="https://img.shields.io/badge/C%23-512BD4?style=flat-square"> <img alt=".NET 6/8/10" src="https://img.shields.io/badge/.NET%206%2F8%2F10-512BD4?style=flat-square&amp;logo=dotnet&amp;logoColor=white"> <img alt="ASP.NET Core" src="https://img.shields.io/badge/ASP.NET%20Core-512BD4?style=flat-square&amp;logo=dotnet&amp;logoColor=white"> <img alt="Blazor WebAssembly" src="https://img.shields.io/badge/Blazor%20WebAssembly-512BD4?style=flat-square&amp;logo=blazor&amp;logoColor=white"> <img alt="Dapper" src="https://img.shields.io/badge/Dapper-512BD4?style=flat-square"> <img alt="REST APIs" src="https://img.shields.io/badge/REST%20APIs-555555?style=flat-square"> <img alt="Event-driven Microservices" src="https://img.shields.io/badge/Event--driven%20Microservices-555555?style=flat-square"> <img alt="Swagger / OpenAPI" src="https://img.shields.io/badge/Swagger%20%2F%20OpenAPI-85EA2D?style=flat-square&amp;logo=swagger&amp;logoColor=black"> <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white"> <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&amp;logo=fastapi&amp;logoColor=white">
</td>
</tr>
<tr>
<td width="170"><b>Data</b></td>
<td>
<img alt="SQL Server / T-SQL" src="https://img.shields.io/badge/SQL%20Server%20%2F%20T--SQL-CC2927?style=flat-square"> <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&amp;logo=postgresql&amp;logoColor=white"> <img alt="ETL & Data Migration" src="https://img.shields.io/badge/ETL%20%26%20Data%20Migration-555555?style=flat-square">
</td>
</tr>
<tr>
<td width="170"><b>Frontend</b></td>
<td>
<img alt="React" src="https://img.shields.io/badge/React-20232A?style=flat-square&amp;logo=react&amp;logoColor=61DAFB"> <img alt="Next.js" src="https://img.shields.io/badge/Next.js-000000?style=flat-square&amp;logo=nextdotjs&amp;logoColor=white"> <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&amp;logo=typescript&amp;logoColor=white"> <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&amp;logo=javascript&amp;logoColor=black"> <img alt="Bootstrap" src="https://img.shields.io/badge/Bootstrap-7952B3?style=flat-square&amp;logo=bootstrap&amp;logoColor=white"> <img alt="jQuery" src="https://img.shields.io/badge/jQuery-0769AD?style=flat-square&amp;logo=jquery&amp;logoColor=white">
</td>
</tr>
<tr>
<td width="170"><b>DevOps & Quality</b></td>
<td>
<img alt="Azure DevOps Pipelines" src="https://img.shields.io/badge/Azure%20DevOps%20Pipelines-0078D4?style=flat-square"> <img alt="GitHub Actions" src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&amp;logo=githubactions&amp;logoColor=white"> <img alt="CI/CD" src="https://img.shields.io/badge/CI%2FCD-555555?style=flat-square"> <img alt="PowerShell" src="https://img.shields.io/badge/PowerShell-5391FE?style=flat-square"> <img alt="Azure CLI" src="https://img.shields.io/badge/Azure%20CLI-0078D4?style=flat-square"> <img alt="xUnit" src="https://img.shields.io/badge/xUnit-512BD4?style=flat-square"> <img alt="NUnit" src="https://img.shields.io/badge/NUnit-512BD4?style=flat-square"> <img alt="Moq" src="https://img.shields.io/badge/Moq-512BD4?style=flat-square"> <img alt="BenchmarkDotNet" src="https://img.shields.io/badge/BenchmarkDotNet-512BD4?style=flat-square"> <img alt="TDD" src="https://img.shields.io/badge/TDD-2EA44F?style=flat-square">
</td>
</tr>
<tr>
<td width="170"><b>Security & Compliance</b></td>
<td>
<img alt="HIPAA" src="https://img.shields.io/badge/HIPAA-2EA44F?style=flat-square"> <img alt="HL7 FHIR R4" src="https://img.shields.io/badge/HL7%20FHIR%20R4-E34F26?style=flat-square"> <img alt="OAuth 2.0 / OIDC" src="https://img.shields.io/badge/OAuth%202.0%20%2F%20OIDC-EB5424?style=flat-square"> <img alt="JWT" src="https://img.shields.io/badge/JWT-000000?style=flat-square&amp;logo=jsonwebtokens&amp;logoColor=white"> <img alt="X.509 Encryption" src="https://img.shields.io/badge/X.509%20Encryption-555555?style=flat-square"> <img alt="RBAC" src="https://img.shields.io/badge/RBAC-555555?style=flat-square"> <img alt="PCI-conscious Tokenization" src="https://img.shields.io/badge/PCI--conscious%20Tokenization-555555?style=flat-square"> <img alt="DevSecOps" src="https://img.shields.io/badge/DevSecOps-2EA44F?style=flat-square">
</td>
</tr>
</table>

## Featured work

Two solo hackathon builds that are public. Most of my production and client work lives in private repositories — the telemetry below counts it.

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/sham-2510/ClinSight">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/clinsight-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cards/clinsight-light.svg">
  <img src="assets/cards/clinsight-light.svg" width="100%" alt="ClinSight, solo hackathon build: hierarchical multimodal clinical decision support. Chest X-rays, labs, vitals and triage notes reasoned through a compiled LangGraph pipeline of 5 parent agents, 7 subagents and 12 reasoning nodes; Qwen2.5-VL and Qwen3.5 MoE served with vLLM on AMD MI300X at FP16; 50 of 50 cases on a live benchmark, mean latency 23.02 seconds.">
</picture>
</a>
</td>
<td width="50%" valign="top">
<a href="https://github.com/sham-2510/playbook">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/playbook-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cards/playbook-light.svg">
  <img src="assets/cards/playbook-light.svg" width="100%" alt="PLAYBOOK, solo hackathon build: a deterministic SOAR layer that intercepts, judges and contains rogue AI agents. Detect under 2 ms, judge under 5 ms, enforce under 1 ms with allow, deny, quarantine or escalate verdicts, forensics async; end-to-end p95 under 40 ms with zero LLM calls in the judge path; NIST SP 800-53 policy builder; EU AI Act, NIST AI RMF, SOC 2, HIPAA and GDPR mapping; tamper-evident forensics signed with SHA-256 manifests and HMAC.">
</picture>
</a>
</td>
</tr>
</table>

## Experience

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/timeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/timeline-light.svg">
  <img src="assets/timeline-light.svg" width="100%" alt="Career timeline drawn as a training run. Epoch 1, 2020 to 2022: Full Stack Azure Developer; Oracle and SQL Server to Azure SQL migration, load time from about 2 minutes to about 2 seconds, 70% less manual deployment. Epoch 2, 2023 to present: Senior AI Engineer; AI clinical scribe with 80% less documentation time, HL7 FHIR R4 data hub, 100+ TPS payment gateway, leads teams of 2 to 4. Checkpoints: BCA 2020, MCA 2024, AI-900 August 2025, AI-102 December 2025.">
</picture>

<details>
<summary><b>Text version</b></summary>

**Senior AI Engineer** · 2023 – Present

- Lead and mentor teams of 2–4 engineers through Agile/DevSecOps delivery, partnering with stakeholders to turn client needs into shipped software.
- Built an AI clinical scribe inside a fertility EMR (Azure AI Speech + Azure OpenAI) that cut manual documentation time by 80%.
- Designed a multi-tenant payment gateway handling peaks of 100+ transactions per second; Pub/Sub retry and dead-letter workflows cut payment failures by 40%.
- Architected a HIPAA-compliant, multi-tenant HL7 FHIR R4 data hub with Azure Functions, Service Bus and Logic Apps.
- Secured a public patient-onboarding chatbot with Azure Front Door WAF, API Management and origin locking.

**Full Stack Azure Developer** · 2020 – 2022

- Migrated on-premises Oracle and SQL Server financial systems to Azure SQL with Azure Data Factory ETL pipelines.
- Reduced application load time from ~2 minutes to ~2 seconds.
- Cut manual deployment effort by 70% with PowerShell, Azure CLI and Azure DevOps CI/CD.

**Education** · MCA, 2024 · BCA, 2020

</details>

## Certifications

<table>
<tr>
<td align="center" width="140"><a href="https://learn.microsoft.com/api/credentials/share/en-us/Shamuddin-2510/38E1EAFD8E68B47F?sharingId=78AC01E7BE1C0E0"><img src="assets/badges/microsoft-certified-associate-badge.svg" width="110" alt="Microsoft Certified Associate badge for Azure AI Engineer Associate (AI-102)"></a></td>
<td><b>Microsoft Certified: Azure AI Engineer Associate</b> (AI-102)<br>Issued Dec 29, 2025 · <a href="https://learn.microsoft.com/api/credentials/share/en-us/Shamuddin-2510/38E1EAFD8E68B47F?sharingId=78AC01E7BE1C0E0">Verify credential</a></td>
</tr>
<tr>
<td align="center" width="140"><a href="https://learn.microsoft.com/api/credentials/share/en-us/Shamuddin-2510/CC3350857AE51DD1?sharingId=78AC01E7BE1C0E0"><img src="assets/badges/microsoft-certified-fundamentals-badge.svg" width="110" alt="Microsoft Certified Fundamentals badge for Azure AI Fundamentals (AI-900)"></a></td>
<td><b>Microsoft Certified: Azure AI Fundamentals</b> (AI-900)<br>Issued Aug 16, 2025 · <a href="https://learn.microsoft.com/api/credentials/share/en-us/Shamuddin-2510/CC3350857AE51DD1?sharingId=78AC01E7BE1C0E0">Verify credential</a></td>
</tr>
</table>

## GitHub telemetry

Public **and** private work, self-rendered daily by a GitHub Action from GitHub data. Private repositories show up as counts only, never names or code.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/generated/telemetry-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/generated/telemetry-light.svg">
  <img src="assets/generated/telemetry-light.svg" width="100%" alt="GitHub telemetry for sham-2510 over the last 12 months: total, public and private contributions, current and longest streak, active days, public and private repository counts and language mix; numbers are in the image.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/generated/neural-activity-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/generated/neural-activity-light.svg">
  <img src="assets/generated/neural-activity-light.svg" width="100%" alt="Animated contribution transformer: the last 12 months of public and private GitHub contributions for sham-2510 shown as token cells, attention arcs and a neural network; numbers are in the caption.">
</picture>

## Open to

**Applied AI · AI Research · Applied Science with AI** — building, researching and shipping AI that works in the real world. Reach me on [LinkedIn](https://www.linkedin.com/in/shamuddin-n-b90018160/) or by [email](mailto:shamuddin1011@gmail.com).

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/footer-light.svg">
  <img src="assets/footer-light.svg" width="100%" alt="Decorative divider">
</picture>

**Building secure, useful AI. Let's talk.**

[LinkedIn](https://www.linkedin.com/in/shamuddin-n-b90018160/) · [Email](mailto:shamuddin1011@gmail.com) · [GitHub](https://github.com/sham-2510)

</div>
