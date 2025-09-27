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
import time
from .multitasker import Multitasker
import json
import re

class Email(BaseModel):
    subject: str
    greeting: str
    paragraph1: str
    paragraph2: str
    paragraph3: str
    closing: str

def worker(person, name, university, program, batch, client):
    crawler = ScientificWebCrawler()
    fullname = person['fullname']
    print(f"Processing: {fullname}")

    try:
        researchdata = crawler.process(f"{fullname} Research Paper")

        url = researchdata['url']
        data = researchdata['data']

        if (not (url and data)):
            raise ValueError(f"Missing required research information: url={url} data={data}")
        
    except Exception as e:
        print(f"Error processing {fullname}: {e}")
        url = "n/a"
        data = "Could not find research paper."

    # Call Gemini API

    # print(conclusionparagraph)
    if len(data) == 0:
        data = "No research results found, please research the scientist's recent work online."

    # if len(prompt) < 10:

        # with open("prompt.txt", "r", encoding="utf-8") as file:
        # prompt = file.read()
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"""
    You are a professional email writer. Your highest priority is to write an email that is **exactly 256 words long**. After writing, count all words and adjust phrasing to meet exactly 300 words. Word count **takes priority** over style, paragraph length, or other considerations. Do not write more or less than 300 words.  

    Using the information below, write a **polite, professional email** addressed to the scientist/doctor. The email must strictly follow the structure below and return valid JSON with the exact keys: subject, greeting, paragraph1, paragraph2, paragraph3, closing. Do **not** include placeholders — all fields must be filled using the information provided.

    Information:
    - Scientist's Full Name: {fullname}
    - Scientist Research Results: {data}
    - My Name: {name}
    - My University: {university}
    - My Program of Study: {program}

    Requirements:
    1. Subject: Creative, professional, and summarizing the purpose of the email.
    2. Greeting: Use a professional and slightly creative greeting in this format:
    "Greetings Dr./Mr./Mrs./Ms. [Last Name],"
    3. Paragraph 1: Introduce yourself clearly using this style:
    "My name is {name}, and I am an undergraduate student studying {program} at {university}. I am reaching out to express my interest in exploring potential research opportunities within your lab."
    4. Paragraph 2: Discuss a specific result from the scientist’s research. Explain how this research aligns with your interests and connects to a real-world problem. Write in **first person**, making it authentic and engaging.
    5. Paragraph 3: Close politely, mention attachments, and express gratitude. Follow this style:
    "Please find my attached resume and transcript for your review. I appreciate you taking the time out of your busy schedule to consider my application. I welcome any chance to meet with you to discuss your research and explore potential opportunities for engaging with your work."
    6. Closing: Use a professional sign-off appropriate for academic emails (e.g., "Sincerely,", "Best regards,", "Kind regards,") **without adding your name after it**.
    7. JSON format: The output must be valid JSON with keys exactly as: subject, greeting, paragraph1, paragraph2, paragraph3, closing.

    Do not include any instructions, notes, or placeholders in the output. Fill in all text using the provided variables and research data. Ensure the **final email is exactly 300 words**.
    """,
        config={
            "response_mime_type": "application/json",
            "response_schema": Email,
        },
    )



    try:
        # Try to extract the JSON using a regex
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in response")
        
        json_text = match.group(0).strip()

        # Validate with Pydantic
        email_data = Email.model_validate_json(json_text)

        # Handle case where data wasn't found
        if data == "Could not find research paper.":
            email_data.paragraph2 = "Could not find research paper."

        print(email_data)

        draft = Draft.objects.create(
            name=fullname,
            url=url,
            content=email_data.model_dump(),
            email=person["gmail"],
            subject=email_data.subject,
        )
        batch.drafts.add(draft)

    except Exception as e:
        print("Error validating email:", e)
        print("Problematic response text:", repr(response.text))

    return email_data



class DraftGeneratorAPIView(APIView):
    client = genai.Client(api_key=os.environ.get("GEMINI_KEY"))

    def valid_data(self, result):
        return True

    def post(self, request):
        start = time.perf_counter()
        serializer = RequestSerializer(data=request.data)

        # print(serializer)
        # print(serializer.is_valid())
        if serializer.is_valid():
            
            unique_id = serializer.validated_data.get('unique_id', None)
            name = serializer.validated_data.get('name', None)
            university = serializer.validated_data.get('university', None)
            program = serializer.validated_data.get('program', None)
            file = serializer.validated_data.get('file', None)
            # prompt = serializer.validated_data.get('prompt', None)
            

            user = User.objects.get(unique_id=unique_id)
            batch = Batch.objects.create(user=user)

            # Read CSV in memory
            # people = parseCSV(file)

            # multitasker = Multitasker()
            # multitasker.run(worker, people, (prompt, name, university, program, batch, self.client), self.valid_data, stop_on_first_valid=False)
            people = parseCSV(file)

            multitasker = Multitasker()

            # Process in chunks of 10
            chunk_size = 10
            for i in range(0, len(people), chunk_size):
                batch_people = people[i:i + chunk_size]
                multitasker.run(
                    worker,
                    batch_people,
                    (name, university, program, batch, self.client),
                    self.valid_data,
                    stop_on_first_valid=False
                )


            batch_id_str = str(batch.id)
            
            end = time.perf_counter()
            print(f"This request took: {round((end - start), 2)} seconds")
            return Response({'message': 'Emails have been generated!', 'id': batch_id_str}, status=200)

        return Response({'errors': serializer.errors}, status=400)

    # def post(self, request):
    #     start = time.perf_counter()
    #     serializer = RequestSerializer(data=request.data)

    #     print(serializer)
    #     print(serializer.is_valid())
    #     if serializer.is_valid():
            
    #         unique_id = serializer.validated_data.get('unique_id', None)
    #         name = serializer.validated_data.get('name', None)
    #         university = serializer.validated_data.get('university', None)
    #         program = serializer.validated_data.get('program', None)
    #         file = serializer.validated_data.get('file', None)
    #         prompt = serializer.validated_data.get('prompt', None)
            

    #         user = User.objects.get(unique_id=unique_id)
    #         batch = Batch.objects.create(user=user)

    #         # Read CSV in memory
    #         people = parseCSV(file)

    #         for person in people:
                
    #             crawler = ScientificWebCrawler()
    #             fullname = person['fullname']
    #             print(f"Processing: {fullname}")

    #             try:
    #                 researchdata = crawler.process(f"{fullname} Research Paper")
    #                 url = researchdata['url']
    #                 data = researchdata['data']

    #                 if (not (url and data)):
    #                     raise ValueError(f"Missing required research information: url={url} data={data}")
                    
    #             except Exception as e:
    #                 print(f"Error processing {fullname}: {e}")
    #                 url = "n/a"
    #                 data = "Could not find research paper."

    #             # Call Gemini API

    #             # print(conclusionparagraph)
    #             if len(data) == 0:
    #                 data = "No research results found, please research the scientist's recent work online."

    #             if len(prompt) < 10:

    #                 # with open("prompt.txt", "r", encoding="utf-8") as file:
    #                 # prompt = file.read()
    #                 print("No prompt provided, using default.")
    #                 response = self.client.models.generate_content(
    #                     model="gemini-2.5-flash-lite",
    #                     contents=f"""
    #                 You are a professional email writer. Your highest priority is to write an email that is **exactly 256 words long**. After writing, count all words and adjust phrasing to meet exactly 300 words. Word count **takes priority** over style, paragraph length, or other considerations. Do not write more or less than 300 words.  

    #                 Using the information below, write a **polite, professional email** addressed to the scientist/doctor. The email must strictly follow the structure below and return valid JSON with the exact keys: subject, greeting, paragraph1, paragraph2, paragraph3, closing. Do **not** include placeholders — all fields must be filled using the information provided.

    #                 Information:
    #                 - Scientist's Full Name: {fullname}
    #                 - Scientist Research Results: {data}
    #                 - My Name: {name}
    #                 - My University: {university}
    #                 - My Program of Study: {program}

    #                 Requirements:
    #                 1. Subject: Creative, professional, and summarizing the purpose of the email.
    #                 2. Greeting: Use a professional and slightly creative greeting in this format:
    #                 "Greetings Dr./Mr./Mrs./Ms. [Last Name],"
    #                 3. Paragraph 1: Introduce yourself clearly using this style:
    #                 "My name is {name}, and I am an undergraduate student studying {program} at {university}. I am reaching out to express my interest in exploring potential research opportunities within your lab."
    #                 4. Paragraph 2: Discuss a specific result from the scientist’s research. Explain how this research aligns with your interests and connects to a real-world problem. Write in **first person**, making it authentic and engaging.
    #                 5. Paragraph 3: Close politely, mention attachments, and express gratitude. Follow this style:
    #                 "Please find my attached resume and transcript for your review. I appreciate you taking the time out of your busy schedule to consider my application. I welcome any chance to meet with you to discuss your research and explore potential opportunities for engaging with your work."
    #                 6. Closing: Use a professional sign-off appropriate for academic emails (e.g., "Sincerely,", "Best regards,", "Kind regards,") **without adding your name after it**.
    #                 7. JSON format: The output must be valid JSON with keys exactly as: subject, greeting, paragraph1, paragraph2, paragraph3, closing.

    #                 Do not include any instructions, notes, or placeholders in the output. Fill in all text using the provided variables and research data. Ensure the **final email is exactly 300 words**.
    #                 """,
    #                     config={
    #                         "response_mime_type": "application/json",
    #                         "response_schema": Email,
    #                     },
    #                 )


    #             try:
    #                 # Try to extract the JSON using a regex
    #                 match = re.search(r'\{.*\}', response.text, re.DOTALL)
    #                 if not match:
    #                     raise ValueError("No JSON object found in response")
                    
    #                 json_text = match.group(0).strip()

    #                 # Validate with Pydantic
    #                 email_data = Email.model_validate_json(json_text)

    #                 # Handle case where data wasn't found
    #                 if data == "Could not find research paper.":
    #                     email_data.paragraph2 = "Could not find research paper."

    #                 print(email_data)

    #                 draft = Draft.objects.create(
    #                     name=fullname,
    #                     url=url,
    #                     content=email_data.model_dump(),
    #                     email=person["gmail"],
    #                     subject=email_data.subject,
    #                 )
    #                 batch.drafts.add(draft)

    #             except Exception as e:
    #                 print("Error validating email:", e)
    #                 print("Problematic response text:", repr(response.text))
                    
                    
    #         batch_id_str = str(batch.id)


    #         end = time.perf_counter()
    #         print(f"This request took: {round((end - start), 2)} seconds")
    #         return Response({'message': 'Emails have been generated!', 'id': batch_id_str}, status=200)

    #     return Response({'errors': serializer.errors}, status=400)

def parseCSV(file):
    decoded_file = file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    csv_reader = csv.reader(io_string, delimiter=',')

    data = []

    for row in csv_reader:
        if (len(row) < 2):
            continue

        fullname, gmail = row
        data.append({
            "fullname": fullname,
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

        # Case 1: Both id and uid are provided -> return specific batch
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

        # Case 2: Only unique_id is provided -> return all batches for that user
        elif unique_id and not batch_id:
            try:
                user = User.objects.get(unique_id=unique_id)
                batches = Batch.objects.filter(user=user).order_by('-created_at')[:10]  # 10 most recent
                serializer = BatchSerializer(batches, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found with the given unique_id'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # Case 3: Neither id nor uid provided -> return all batches
        elif not batch_id and not unique_id:
            batches = Batch.objects.all()
            serializer = BatchSerializer(batches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Case 4: Only batch_id provided -> error
        else:
            return Response(
                {'error': 'Both id and uid must be provided to fetch a specific batch'},
                status=status.HTTP_400_BAD_REQUEST
            )
