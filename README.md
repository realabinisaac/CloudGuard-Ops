# CloudGuard-Ops 🛰️
### Event-Driven Image Ingestion & Cost-Optimized Security Pipeline

I built a backend infrastructure in the AWS Mumbai (ap-south-1) region that processes incoming camera feeds for threat detection. The goal was to build a system that can handle sudden spikes of image uploads without crashing the backend, while scaling down to exactly 0 INR when no traffic is coming in.

## How it Works
* **Storage Separation:** Images land in an Amazon S3 bucket. S3 does not call our code directly; it sends a decoupled notification payload forward.
* **The SQS Buffer:** Messages sit in an Amazon SQS queue backed by a Dead Letter Queue (DLQ). If a camera malfunctions and drops thousands of images at once, the queue holds them in line to stop our backend from getting throttled or crashing. Bad files drop into the DLQ so they don't block the pipeline.
* **Cheap Compute:** AWS Lambda handles the processing. It runs on ARM64-based Graviton2 processors (which are 20% cheaper than standard nodes). I set up 20-second Long Polling so Lambda sits quietly and waits for batches of files instead of constantly checking an empty queue and running up a bill.
* **Auto-Cleanup:** An S3 Lifecycle rule automatically deletes files after 48 hours. This stops our cloud storage bill from growing continuously over time.
* **Access Rules:** No hardcoded API keys. Lambda uses an IAM role with restricted trust policies to securely query Amazon Rekognition AI and shoot alerts out via Amazon SNS.

## Proof of Success
Here is the automated security alert that hits my personal inbox within seconds when a threat image passes through the queue:

![Infrastructure Success Proof](INSERT_YOUR_EMAIL_SCREENSHOT_LINK_HERE)

## Tech Stack
* **Cloud:** AWS (S3, SQS, DLQ, Lambda, Rekognition, SNS, IAM)
* **Code Engine:** Python 3.12 (Boto3 SDK)
