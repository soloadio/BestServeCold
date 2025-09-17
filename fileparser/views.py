from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import csv
import io
from .serializers import FileSerializer
from rest_framework.renderers import TemplateHTMLRenderer

from google import genai
import os


class CSVUploadView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'fileparser_index.html'
    parser_classes = [MultiPartParser, FormParser]
    client = genai.Client(api_key=os.environ.get("GEMINI_KEY"))

    def get(self, request):
        return Response({})

    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']

            # Read CSV in memory
            decoded_file = uploaded_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            csv_reader = csv.reader(io_string, delimiter=',')

            generated_emails = []

            for row in csv_reader:
                if (len(row) < 2):
                    continue
                first_name, last_name, lab_description = row

                # Call Gemini API
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"""
                        You are a professional email writer.

                        Using the following information:
                        - Scientist First Name: {first_name}
                        - Scientist Last Name: {last_name}
                        - Lab Description: {lab_description}
                        - My First Name: Jeffrey
                        - My Last Name: Han

                        Write a polite and professional email addressed to the scientist.
                        Do NOT include placeholders, instructions, or extra notes.
                        Return ONLY the final email content, ready to send, as plain text.
                        """
                )

                generated_emails.append({
                    "scientist_first_name": first_name,
                    "scientist_last_name": last_name,
                })
                print(response.text)

            return Response({"emails": generated_emails}, status=200)

        return Response({'errors': serializer.errors}, status=400)