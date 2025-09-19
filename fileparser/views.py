from rest_framework.views import APIView
from rest_framework.response import Response
import csv
import io
from .serializers import RequestSerializer
from .scientificwebcrawler import ScientificWebCrawler

from google import genai
import os


class FileParserAPIView(APIView):
    client = genai.Client(api_key=os.environ.get("GEMINI_KEY"))
    crawler = ScientificWebCrawler()

    def get(self, request):
        example_data = {
            "name": "Your Name",
            "file": None,
            "prompt": "Optional prompt text"
        }
        serializer = RequestSerializer(data=example_data)
        serializer.is_valid()  # optional for demonstration
        return Response(serializer.initial_data)

    def post(self, request):
        serializer = RequestSerializer(data=request.data)


        if serializer.is_valid():
            
            file = serializer.validated_data['file']
            name = serializer.validated_data['name']
            prompt = serializer.validated_data['prompt']


            # Read CSV in memory
            people = parseCSV(file)

            for person in people:
                print(f"Processing: {person['first_name']} {person['last_name']}")
                scientisturl = self.crawler.getSignificantWebsite(person["first_name"] + " " + person["last_name"] + " Lab")
                researchPaperURL, conclusionparagraph = self.crawler.getResearchInfo(scientisturl)

                # Call Gemini API

                # print(conclusionparagraph)
                if len(conclusionparagraph) == 0:
                    conclusionparagraph = "No research results found, please research the scientist's recent work online."

                if len(prompt) < 10:
                    print("No prompt provided, using default.")
                    response = self.client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=f"""
                            You are a professional email writer.

                            Using the following information:
                            - Scientist First Name: {person["first_name"]}
                            - Scientist Last Name: {person["last_name"]}
                            - Scientist Research Results: {conclusionparagraph}
                            - My Name: {name}
                            Write a polite and professional email addressed to the scientist.
                            Do NOT include placeholders, instructions, or extra notes.
                            Return ONLY the final email content, ready to send, as plain text.
                            """
                    )
                print(response.text)

            return Response({'status': 'verygood!'}, status=200)

        return Response({'errors': serializer.errors}, status=400)


def parseCSV(file):
    decoded_file = file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    csv_reader = csv.reader(io_string, delimiter=',')

    data = []

    for row in csv_reader:
        if (len(row) < 2):
            continue

        first_name, last_name = row
        data.append({
            "first_name": first_name,
            "last_name": last_name,
        })

    return data