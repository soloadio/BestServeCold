import { Injectable } from '@angular/core';
import { GoogleGenAI } from "@google/genai";
import { environment } from '../../environments/environment';
import { Type } from '@google/genai';


@Injectable({
  providedIn: 'root'
})
export class Geminiservice {

  ai = new GoogleGenAI({apiKey: environment.GEMINI_API_KEY});

  private getHeader(content: string) {
    return {
      model: "gemini-2.0-flash-lite",
      contents: content,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.ARRAY,
          items: {
            type: Type.OBJECT,
            properties: {
              recipeName: {
                type: Type.STRING,
              },
              ingredients: {
                type: Type.ARRAY,
                items: {
                  type: Type.STRING,
                },
              },
            },
            propertyOrdering: ["recipeName", "ingredients"],
          },
        },
      },
    }
  }

  async generateResponse(content: string){
    const response = await this.ai.models.generateContent(this.getHeader(content));
    console.log(response.text);
  }
}
