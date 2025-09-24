from rest_framework.views import APIView
from rest_framework.response import Response
import csv
import io
from .serializers import RequestSerializer
from .scientificwebcrawler import ScientificWebCrawler
from google import genai
import os
from DraftGenerator.models import Draft, Batch
from User.models import User
from .serializers import DraftSerializer, BatchSerializer
from rest_framework import status
from pydantic import BaseModel, TypeAdapter
import json

class Email(BaseModel):
    subject: str
    greeting: str
    paragraph1: str
    paragraph2: str
    paragraph3: str
    closing: str

class DraftGeneratorAPIView(APIView):
    client = genai.Client(api_key=os.environ.get("GEMINI_KEY"))

    def post(self, request):
        serializer = RequestSerializer(data=request.data)

        print(serializer)
        print(serializer.is_valid())
        if serializer.is_valid():
            
            unique_id = serializer.validated_data.get('unique_id', None)
            name = serializer.validated_data.get('name', None)
            university = serializer.validated_data.get('university', None)
            program = serializer.validated_data.get('program', None)
            file = serializer.validated_data.get('file', None)
            prompt = serializer.validated_data.get('prompt', None)
            

            user = User.objects.get(unique_id=unique_id)
            batch = Batch.objects.create(user=user)

            # Read CSV in memory
            people = parseCSV(file)

            for person in people:
                
                crawler = ScientificWebCrawler()
                fullname = f"{person['first_name']} {person['last_name']}"
                print(f"Processing: {fullname}")


                # scientisturl = crawler.getSignificantWebsites(fullname + " Lab")[0]

                try:
                    # researchPaperURL, conclusionparagraph = crawler.getResearchInfo(scientisturl)

                    researchPaperURL, conclusionparagraph = crawler.getResearchInfo(f"{fullname} Research Paper")

                    if (researchPaperURL == None or conclusionparagraph == None):
                        raise ValueError(f"Missing required research information: "
                     f"researchPaperURL={researchPaperURL}, "
                     f"conclusionparagraph={conclusionparagraph}")
                except Exception as e:
                    print(f"Error processing {fullname}: {e}")
                    researchPaperURL = "n/a"
                    conclusionparagraph = "Could not find research paper."

                # Call Gemini API

                # print(conclusionparagraph)
                if len(conclusionparagraph) == 0:
                    conclusionparagraph = "No research results found, please research the scientist's recent work online."

                if len(prompt) < 10:
                    print("No prompt provided, using default.")
                    response = self.client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents=f"""
                    You are a professional email writer. Using the information below, write a **polite, professional email** addressed to the scientist/doctor **with a WORD COUNT of approximately 250**. The email should be **structured in exactly 3 paragraphs** and have a **professional and straight forward subject line** suitable for academic/research correspondence.

                    Information:
                    - Scientist First Name: {person['first_name']}
                    - Scientist Last Name: {person['last_name']}
                    - Scientist Research Results: {conclusionparagraph}
                    - My Name: {name}
                    - My University: {university}
                    - My Program of Study: {program}

                    Requirements:
                    - Subject: Creative and professional, summarizing the purpose of the email.
                    - Greeting: Use a professional and slightly creative greeting in this format: 
                    "Greetings Dr./Mr./Mrs./Ms./etc. [Last Name],"
                    - Paragraph 1: Introduce yourself and express interest in research opportunities. Here is an example:
                    "My name is [Your Name], and I am a undergraduate student studying
                    [Your Program] at [Your University]. I am reaching out to express my
                    interest in exploring potential research opportunities within your lab."
                    - Paragraph 2: Given the scientist's research results, comment on a specific result and make a connection to a specific real world problem the specific research results hope to investigate or solve. Make sure to write a statement in first person addressing how the research aligns with own personal interest, make it genuine, authentic and capitative. This should ideally be integrated with the real world connection if possible."
                    - Paragraph 3: Close politely, mention attachments, and express gratitude professionally while feeling geniune. Here is an example: "Please find my attached resume and transcript for your review. I
                    appreciate you taking the time out of your busy schedule to consider my
                    application. I welcome any chance to meet with you to discuss your
                    research andexplorepotential opportunities for engagingwith yourwork."
                    - Closing: Use a professional sign-off appropriate for academic emails (e.g., "Sincerely,", "Best regards,", "Kind regards,") **without** adding your name after it.

                    Return the output as JSON with these keys: subject, paragraph1, paragraph2, paragraph3. 
                    Do NOT include placeholders or instructions; the JSON should be ready to use.
                    """,
                        config={
                            "response_mime_type": "application/json",
                            "response_schema": Email,
                        },
                    )


                email_data = Email.model_validate_json(response.text)
                if conclusionparagraph == "Could not find research paper.":
                    email_data.paragraph2 = "Could not find research paper."



                print(email_data)
                draft = Draft.objects.create(
                    name=fullname,
                    url=researchPaperURL,
                    content=email_data.model_dump(),
                    email=person["gmail"],
                    subject=email_data.subject,
                    # website=scientisturl
                )
                batch.drafts.add(draft)


                    
                batch_id_str = str(batch.id)


            return Response({'message': 'Emails have been generated!', 'id': batch_id_str}, status=200)

        return Response({'errors': serializer.errors}, status=400)


def parseCSV(file):
    decoded_file = file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    csv_reader = csv.reader(io_string, delimiter=',')

    data = []

    for row in csv_reader:
        if (len(row) < 3):
            continue

        first_name, last_name, gmail = row
        data.append({
            "first_name": first_name,
            "last_name": last_name,
            "gmail": gmail
        })

    return data


class DraftListAPIView(APIView):
    def get(self, request):
        drafts = Draft.objects.all()
        serializer = DraftSerializer(drafts, many=True)
        return Response(serializer.data, status=200)


class BatchListAPIView(APIView):
    def get(self, request):
        batch_id = request.query_params.get('id')
        unique_id = request.query_params.get('uid')

        # If both id and uid are provided, return specific batch
        if batch_id and unique_id:
            try:
                batch = Batch.objects.get(id=batch_id)
                if batch.user.unique_id != unique_id:
                    return Response(
                    {'error': 'Invalid Authorization'},
                    status=status.HTTP_403_FORBIDDEN
                )
                serializer = BatchSerializer(batch)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Batch.DoesNotExist:
                return Response(
                    {'error': 'Batch not found with the given id and uid'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If neither id nor uid provided, return all batches
        elif not batch_id and not unique_id:
            batches = Batch.objects.all()
            serializer = BatchSerializer(batches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If one is missing
        else:
            return Response(
                {'error': 'Both id and uid must be provided to fetch a specific batch'},
                status=status.HTTP_400_BAD_REQUEST
            )